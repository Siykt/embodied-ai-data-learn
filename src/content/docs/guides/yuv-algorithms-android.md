---
title: YUV 算法实现与 Android 端使用注意事项
description: 从具身智能数据采集、处理和端侧推理角度整理 YUV 格式、常见转换算法、Android Camera2 与 CameraX 使用要点。
---

YUV 经常出现在 Android 相机、视频编解码、端侧视觉模型和机器人数据采集里。对具身智能数据来说，它不是一个孤立的图像格式问题，而是会影响**采集带宽、时间戳、图像颜色、模型输入一致性、标注预览和质检复现**的一段关键链路。

这篇按工程实现来整理：先说明 YUV 4:2:0 怎么存，再整理常见算法，最后给 Android 端处理 `YUV_420_888` 的注意事项。

![YUV 4:2:0 中 Y 平面与 U/V 色度平面的采样关系](/images/docs/yuv-420-layout.svg)

## YUV 在数据管线里的位置

Android 相机通常先给到 YUV 或私有格式，再由应用决定是否转成 RGB、JPEG、Bitmap、Tensor 或视频编码输入。YUV 的优势是带宽低、接近相机和视频编码链路；代价是应用不能把它当成普通连续 RGB 数组直接读。

在具身智能数据采集中，建议把一次帧处理拆成两类产物：

- 原始或近原始记录：YUV 平面、宽高、`rowStride`、`pixelStride`、时间戳、旋转、相机 ID 和曝光相关元数据。
- 派生记录：RGB 预览图、模型输入 tensor、标注工具截图、压缩视频或质检报告。

这样做的价值是：如果后续发现颜色偏绿、左右镜像、模型训练不稳定，可以回到同一帧的 YUV 元数据复现处理过程，而不是只剩一张已经转换过的 RGB 图。

## 格式与内存布局

工程里说的 “YUV” 在 Android 文档里更准确地常指 YCbCr。可以先按三个通道理解：

- `Y`：亮度信息，决定图像明暗和大部分边缘细节。
- `U` / `Cb`：蓝色色差信息。
- `V` / `Cr`：红色色差信息。

常见采样格式的差别在于色度通道有多密：

| 格式 | 含义 | 8-bit 每像素近似大小 | 常见用途 |
| --- | --- | --- | --- |
| `YUV444` | 每个像素都有 Y、U、V | 24 bit | 高质量中间结果、少见于移动相机输出 |
| `YUV422` | 横向两个像素共享一组 U/V | 16 bit | 部分视频和采集设备 |
| `YUV420` | 2x2 四个像素共享一组 U/V | 12 bit | Android 相机、视频编码、端侧视觉 |

`YUV420` 还会分不同内存布局：

| 布局 | 平面顺序 | 说明 |
| --- | --- | --- |
| `I420` / `YUV420p` | Y + U + V | 三个平面顺序存储，很多算法库喜欢用它作中间格式 |
| `YV12` | Y + V + U | 和 I420 类似，但 U/V 顺序相反 |
| `NV12` | Y + UVUV... | 半平面格式，U/V 交错 |
| `NV21` | Y + VUVU... | Android 旧 Camera API 预览常见格式 |
| `YUV_420_888` | Y、U、V 三个 plane + stride 元数据 | Android 的通用描述格式，可能覆盖 planar 或 semiplanar 存储 |

关键点：`YUV_420_888` 不是承诺“内存一定是 I420”或“一定是 NV21”。它承诺的是应用能通过三个 plane 和每个 plane 的 stride 信息正确访问数据。

## 常见算法实现

![YUV 帧从采集、stride 安全读取、布局转换、颜色转换到模型或质检使用的处理管线](/images/docs/yuv-processing-pipeline.svg)

### 1. RGB 与 YUV 互转

颜色转换需要先明确标准和范围。常见标准包括 BT.601、BT.709、BT.2020；常见范围包括 full range 和 video/limited range。相同 YUV 数值如果用错矩阵，颜色会偏灰、偏绿或偏红。

工程上常见 8-bit BT.601 limited range 的 YUV 到 RGB 近似写法如下：

```text
C = Y - 16
D = U - 128
E = V - 128

R = clip((298 * C + 409 * E + 128) >> 8)
G = clip((298 * C - 100 * D - 208 * E + 128) >> 8)
B = clip((298 * C + 516 * D + 128) >> 8)
```

如果数据来自相机分析流，很多模型只关心结构和亮度，可以直接使用 Y 平面作为灰度输入，省掉 RGB 转换。但如果模型训练时用的是 RGB，就必须保持训练和推理阶段的矩阵、范围、旋转和归一化一致。

### 2. 色度上采样

`YUV420` 的 U/V 分辨率是 Y 的一半宽、一半高。转 RGB 时，每个输出像素都需要找到对应的色度值：

```text
yIndex = y * yRowStride + x * yPixelStride
uvIndex = (y / 2) * uvRowStride + (x / 2) * uvPixelStride
```

最简单做法是最近邻上采样：四个 Y 像素共用一个 U/V。质量更好的预览或离线处理可以用双线性上采样，但端侧实时模型输入通常优先考虑稳定和速度。

### 3. 布局转换

许多 Android 或 NDK 代码会先把 `YUV_420_888` 规整成 `I420` 或 `NV21`：

- 转 `I420`：先拷贝 Y，再按 U 平面、V 平面逐点拷贝到连续数组。
- 转 `NV21`：先拷贝 Y，再按 V、U 交错写入。
- 转 `NV12`：先拷贝 Y，再按 U、V 交错写入。

实现时不要按 `width * height` 直接整块复制所有 plane。只有当目标 plane 没有 padding、`pixelStride` 正好符合预期时，整块复制才成立。更稳的做法是逐行、逐像素按 stride 读。

下面是一个 stride 安全的 Kotlin 版本，把 `Image` 转为 I420 连续数组：

```kotlin
fun imageToI420(image: android.media.Image): ByteArray {
    require(image.format == android.graphics.ImageFormat.YUV_420_888)

    val width = image.width
    val height = image.height
    val out = ByteArray(width * height * 3 / 2)
    val planes = image.planes

    copyPlane(
        buffer = planes[0].buffer,
        width = width,
        height = height,
        rowStride = planes[0].rowStride,
        pixelStride = planes[0].pixelStride,
        out = out,
        offset = 0,
        outputStride = 1,
    )

    val chromaWidth = width / 2
    val chromaHeight = height / 2
    val uOffset = width * height
    val vOffset = uOffset + chromaWidth * chromaHeight

    copyPlane(planes[1].buffer, chromaWidth, chromaHeight, planes[1].rowStride, planes[1].pixelStride, out, uOffset, 1)
    copyPlane(planes[2].buffer, chromaWidth, chromaHeight, planes[2].rowStride, planes[2].pixelStride, out, vOffset, 1)

    return out
}

private fun copyPlane(
    buffer: java.nio.ByteBuffer,
    width: Int,
    height: Int,
    rowStride: Int,
    pixelStride: Int,
    out: ByteArray,
    offset: Int,
    outputStride: Int,
) {
    var outputOffset = offset
    for (row in 0 until height) {
        val rowStart = row * rowStride
        for (col in 0 until width) {
            out[outputOffset] = buffer.get(rowStart + col * pixelStride)
            outputOffset += outputStride
        }
    }
}
```

### 4. 裁剪、旋转和缩放

YUV 图像做裁剪时要注意色度采样：`YUV420` 的裁剪起点和宽高最好使用偶数，否则 U/V 对应关系会变复杂。旋转 90 度或 270 度会交换宽高，也要同步处理每个 plane 的坐标映射。

实时 Android 端常见优先级：

1. 如果模型支持灰度或 Y 通道，直接在 Y plane 上裁剪、缩放和归一化。
2. 如果必须 RGB，优先使用成熟库或平台能力做转换，避免在 Java/Kotlin 热循环里逐像素创建对象。
3. 如果要同时存训练数据和跑推理，先把原始帧和元数据写清楚，再保存派生预览，避免离线重建时缺少 stride 信息。

### 5. 质量检查算法

YUV 原始帧很适合做轻量质检，因为 Y 平面已经能反映大部分清晰度和曝光问题：

- 亮度统计：检查 Y 均值、直方图、过暗和过曝比例。
- 模糊检测：在 Y 平面上计算 Laplacian 方差或边缘强度。
- 缺帧/重复帧：比较相邻帧时间戳和 Y 平面差异。
- 色度异常：抽样检查 U/V 均值是否长期贴边，排查 U/V 顺序错误或转换矩阵错误。
- 数据对齐：把 YUV 帧时间戳和 IMU、动作、机器人状态时间戳放在同一时间线检查。

这些检查比“只看 RGB 预览图”更适合采集现场，因为它们更接近传感器输出，也更容易定位是相机、转换、编码还是模型输入出了问题。

## Android 端使用注意事项

![Android Camera2 或 CameraX 中 YUV 帧到转换、模型输入和数据记录的流转](/images/docs/android-yuv-flow.svg)

### Camera2 与 `ImageReader`

使用 Camera2 时，如果需要 CPU 访问图像，常见做法是创建 `ImageReader.newInstance(width, height, ImageFormat.YUV_420_888, maxImages)`。注意事项：

- 处理完每个 `Image` 必须调用 `image.close()`，否则 `ImageReader` 队列会被占满，后续帧不再到达。
- `maxImages` 不要盲目设很大。队列越大，延迟越容易累积；采集数据时还会让图像和动作时间错位。
- `Image#getTimestamp()` 是对齐其他传感器和动作数据的关键字段，不要只用回调到达时间。
- 多摄像头采集时，要记录 camera id、传感器方向、镜头内参、畸变参数和外参，后续才能做空间对齐。

### CameraX `ImageAnalysis`

CameraX 的 `ImageAnalysis` 默认输出 `YUV_420_888`，也支持通过 `setOutputImageFormat()` 选择其他分析输出格式。实践中可以按用途选择：

- 只做模型推理或质量检查：优先保留 `YUV_420_888`，在 Y plane 或 NDK 中处理。
- 需要直接喂给 RGB 模型或 UI 预览：可以评估 `RGBA_8888` 输出，减少自己维护转换代码的负担。
- 需要兼容旧的 NV21 处理链：确认当前 CameraX 版本是否支持对应输出，并仍然按 `ImageProxy` 的 plane 和 stride 访问。

`Analyzer` 里同样必须在处理完成后关闭 `ImageProxy`。如果推理耗时高于帧间隔，应该选择合适的背压策略：实时控制通常更适合只保留最新帧，离线采集则要明确队列深度、丢帧策略和日志。

### `YUV_420_888` 的硬约束

Android 官方文档给出几个重要保证：

- `planes[0]` 是 Y，`planes[1]` 是 U/Cb，`planes[2]` 是 V/Cr。
- Y plane 不会和 U/V 交织；在 `YUV_420_888` 中 Y plane 的 `pixelStride` 为 1。
- U/V plane 的 `rowStride` 相同，`pixelStride` 也相同。
- 每个 plane 都要结合自己的 `rowStride` 和 `pixelStride` 访问，不能假设连续紧密排列。

这些保证足够我们写出通用读取算法，但不足以假设所有设备输出都是同一种底层布局。不同手机、不同 Camera HAL、不同分辨率下，U/V 可能表现得像 I420、NV12 或 NV21。

### 性能与内存

Android 端 YUV 处理最容易出问题的是每帧分配内存和逐像素 Kotlin 循环。建议：

- 复用 `ByteArray`、`ByteBuffer` 和模型输入 tensor 缓冲区。
- 对实时链路使用 NDK、GPU、平台转换能力或 libyuv 这类成熟库。
- 不在 analyzer 回调里做耗时 I/O；保存数据时把帧拷贝到受控队列，再由后台线程写盘。
- 统一处理旋转和镜像，不要让预览、保存、模型输入各自维护一套方向逻辑。
- 对数据集记录保留处理版本、转换矩阵、输出尺寸和归一化参数。

### 端侧模型输入

把 YUV 送到模型前，需要明确模型训练时看到的是什么：

- RGB 模型：确认通道顺序是 RGB 还是 BGR，像素范围是 `0..255`、`0..1` 还是标准化后的分布。
- 灰度模型：可以直接使用 Y plane，但要记录是否来自 full range 或 limited range。
- 多模态具身模型：要把图像帧、IMU、关节状态、末端位姿和动作标签按时间戳对齐，而不是按数组下标粗略配对。
- 视频模型：如果训练数据来自编码后视频，端侧推理却来自相机 YUV 原帧，要检查颜色、锐化、降噪和动态范围差异。

### 常见错误排查

| 现象 | 常见原因 | 检查方式 |
| --- | --- | --- |
| 图像偏绿或偏紫 | U/V 顺序反了，或矩阵/范围用错 | 交换 U/V 做 A/B 对比，检查 BT.601/709 与 full/limited range |
| 图像斜线、错行 | 忽略 `rowStride` padding | 用逐行拷贝验证，不按 `width` 推断一行字节数 |
| 图像马赛克或色块错位 | 忽略 `pixelStride` 或奇数裁剪 | 打印 U/V pixelStride，裁剪起点改为偶数 |
| 画面方向不对 | 未处理 sensor orientation、display rotation 或前摄镜像 | 把保存帧、预览帧、模型帧分别画坐标轴核对 |
| 推理延迟越来越大 | analyzer 没及时关闭帧或队列过深 | 记录队列长度、帧时间戳和处理耗时 |
| 训练集颜色与端侧不一致 | 离线和在线转换路径不同 | 固定转换库、矩阵、尺寸、归一化参数，并写入数据版本 |

## 面向具身智能数据的建议

在机器人或手机端采集具身智能数据时，YUV 处理最好写入数据规范，而不是散在应用代码里：

- 每帧保存 `frame_id`、`timestamp_ns`、`width`、`height`、`format`、`rowStride`、`pixelStride`、rotation 和 camera id。
- 记录从 YUV 到训练图像的完整路径：裁剪、旋转、缩放、颜色矩阵、归一化、是否只用 Y plane。
- 质检时同时看 Y 平面指标和 RGB 预览，避免颜色转换问题掩盖真实采集质量。
- 标注工具使用的预览图要能追溯到原始帧，否则人工框、分割 mask 和动作标签可能对不上。
- 对 SLAM、VIO、手眼标定和操作学习任务，要优先保证时间戳和相机标定正确；颜色好看不等于数据可用。

## 资料来源

- [Android Developers: ImageFormat](https://developer.android.com/reference/android/graphics/ImageFormat)
- [Android Developers: CameraX Image analysis](https://developer.android.com/media/camera/camerax/analyze)
- [libyuv formats documentation](https://chromium.googlesource.com/libyuv/libyuv/+/HEAD/docs/formats.md)
