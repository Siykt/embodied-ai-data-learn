---
title: Aria、Ego4D 与 Ego-Exo4D 数据格式整理
description: 从具身智能数据采集、同步、标定、标注和训练使用角度，对比 Project Aria、Ego4D 与 Ego-Exo4D 的数据组织方式。
---

这篇整理三个经常一起出现、但层级不同的数据格式：

- **Project Aria**：更接近“设备级多传感器记录格式”。核心是 Aria 眼镜采集的 VRS 原始文件，以及 MPS 后处理得到的轨迹、点云、眼动、手部等派生数据。
- **Ego4D**：更接近“大规模第一人称视频数据集格式”。核心是规范化视频、`ego4d.json` 元数据和面向不同 benchmark 的 JSON 标注。
- **Ego-Exo4D**：更接近“多视角具身活动数据集格式”。它用 Aria 作为 ego 视角，同时加入多个 GoPro exo 视角，并在 take 级别保存同步视频、标定、轨迹、点云、眼动和标注。

把它们放在具身智能数据管线里看，差别不只是文件后缀，而是**谁是主时间轴、谁负责空间对齐、标注依附在哪个单位、训练时该从哪里采样**。

## 快速结论

如果只想先建立判断，可以用下面这张表：

| 数据体系 | 主体单位 | 原始数据重点 | 派生数据重点 | 更适合解决的问题 |
| --- | --- | --- | --- | --- |
| Project Aria | 一段 Aria 设备 recording | VRS 多传感器流 | MPS 轨迹、点云、眼动、手部、在线标定 | 设备级 ego 传感器读取、空间定位、眼动和手部状态对齐 |
| Ego4D | `video_uid` / canonical video / clip | 第一人称视频和可选 IMU、gaze、3D 等子集 | benchmark JSON 标注、clip 切片、特征 | 长视频理解、自然语言查询、手物交互、活动预测 |
| Ego-Exo4D | `capture` / `take_uid` / take | Aria ego + 多个 GoPro exo 同步记录 | take 级轨迹、GoPro 标定、点云、眼动、多任务标注 | 多视角动作理解、跨视角对齐、3D 姿态和技能评估 |

在数据工程里可以这样选：

- 要读 Aria 传感器原始流，先学 VRS 和 Project Aria Tools。
- 要训练第一人称视频理解模型，先学 Ego4D 的 canonical video、clip 和 annotation schema。
- 要研究同一动作在第一人称和第三人称之间如何对齐，先学 Ego-Exo4D 的 take、frame aligned videos、trajectory 和 camera calibration。

## Project Aria：设备级多传感器格式

![Project Aria 数据格式中 VRS 原始数据和 MPS 派生数据的关系](/images/docs/aria-vrs-mps-format.svg)

Project Aria 的核心不是一个普通 MP4，而是 **VRS（Vision Replay Systems）**。VRS 可以理解成一个多传感器记录容器：同一段 recording 里包含 RGB 相机、SLAM 相机、IMU、音频、眼动相关数据、设备标定和时间戳等多路 stream。

对具身智能数据来说，VRS 的价值在于它保留了设备级同步信息。普通视频文件主要回答“画面是什么”；Aria VRS 还要回答：

- 这一帧来自哪个 stream。
- 这一帧在设备时间线上是什么时间。
- 同一时间附近的 IMU、音频或其他相机读数是什么。
- 当前设备的相机内参、外参和坐标约定是什么。

Aria 的另一层重要数据是 **MPS（Machine Perception Services）** 输出。MPS 不是原始采集，而是从 Aria 原始数据后处理得到的机器感知结果。常见输出包括：

- SLAM / VIO 相关的 6DoF 轨迹。
- 半稠密点云。
- 在线传感器标定。
- 眼动估计及深度。
- 手部跟踪，例如手部关键点、腕部位姿和法向量。

所以 Aria 数据通常分成两层读取：

```text
recording.vrs
  streams
    rgb camera
    slam left / slam right camera
    imu
    audio
    calibration and timestamps

mps/
  trajectory
  semi_dense_point_cloud
  online_calibration
  eye_gaze
  hand_tracking
```

这类格式适合做空间和身体状态对齐。例如要把“人头部看到的画面”“眼睛看的位置”“头部在世界坐标中的轨迹”“手腕和手掌的大概位置”连在一起，Aria 的 VRS + MPS 比单纯 MP4 更接近具身智能需要的数据底座。

它的使用难点也很明确：

- 不能只按帧号对齐，必须尊重每个 stream 的时间戳。
- 坐标系要认真查清楚，例如设备坐标、相机坐标、世界坐标和眼动坐标。
- MPS 是派生结果，要记录版本、质量状态和是否可用于当前片段。
- 训练前通常要把 VRS 解码成模型可用的图像、数组、表格或分片文件。

## Ego4D：视频数据集与任务标注格式

![Ego4D 数据格式中 video components、canonical videos、clips 和 JSON 标注的关系](/images/docs/ego4d-video-json-format.svg)

Ego4D 的核心单位是第一人称视频。官方文档把视频数据分成几种形态：

- **Video Components**：采集机构提交的原始视频片段，设备、帧率、时基、音频属性可能不一致。
- **Canonical Videos**：从 video components 处理出来的标准化长视频，是主要推荐消费的形式。
- **Canonical Clips**：围绕 benchmark 标注切出的较短视频片段，便于训练和评估。

因此 Ego4D 的数据读取通常不是直接从原始组件开始，而是从 `ego4d.json` 和任务标注 JSON 里找到需要的视频或 clip，再加载对应文件。

典型结构可以理解成：

```text
ego4d_data/
  v*/ego4d.json
  v*/full_scale/
    manifest.csv
    *.mp4
  v*/clips/
    manifest.csv
    *.mp4
  v*/annotations/
    nlq*.json
    mq*.json
    vq*.json
    fho*.json
    av*.json
```

`ego4d.json` 是主元数据表，围绕 `video_uid` 管理：

- 视频时长、帧率、帧数、编码和分辨率。
- `video_start_sec`、`audio_start_sec` 等音视频流偏移。
- split 信息，例如不同 benchmark 的 train / val / test。
- 采集来源、场景、设备、参与者匿名 ID。
- 是否有 IMU、gaze、3D scan、redaction 等额外数据。
- video components 与 canonical video 之间的关系。

任务标注 JSON 则围绕 benchmark 组织。不同任务字段不完全一样，但常见逻辑是：

- 用 `video_uid` 或 `clip_uid` 连接回视频。
- 用 `clip_start_sec`、`clip_end_sec`、`video_start_sec`、`video_end_sec` 或 frame 字段定位时间范围。
- 用自然语言、动作类别、物体框、查询文本、未来动作标签等表示监督信息。

Ego4D 和 Aria 的最大不同是：Ego4D 的主轴是**视频理解任务**，不是设备级传感器复现。它会把复杂来源的视频整理成更容易训练的 canonical video / clip，同时把标注拆到不同任务文件里。对数据使用者来说，关键不是“怎样恢复每个传感器的原始状态”，而是“怎样正确把视频片段、任务标注和 split 对上”。

常见质检重点包括：

- 使用 `clip_*` 字段还是 `video_*` 字段，不能混用时间轴。
- clip 的 `[start_frame, end_frame)` 是否和视频解码方式一致。
- 是否下载了与标注匹配的分辨率版本，例如全尺寸或 540 短边版本。
- 空间标注是否随下采样版本同步缩放。
- 同一个原始长视频切出的多个 clip 是否被错误地跨 split 使用。

## Ego-Exo4D：take 级多视角同步格式

![Ego-Exo4D 数据格式中 capture、take、同步视频、轨迹和标注的关系](/images/docs/ego-exo4d-take-alignment.svg)

Ego-Exo4D 在 Ego4D 的第一人称视频基础上更进一步：它记录同一个人做 skilled activity 时的第一人称和第三人称视角。一个典型 recording 包含：

- 至少一个 Aria 眼镜视角，作为 egocentric view。
- 多个 GoPro 静态外部相机，作为 exocentric views。
- Aria 的 RGB、SLAM 相机、IMU、音频、眼动和 MPS 轨迹。
- GoPro 的视频、音频、外参和内参标定。
- take 级任务、参与者、场景、同步和标注信息。

Ego-Exo4D 里有两个非常重要的组织单位：

- **Capture**：一次录制会话，可以包含多个 take，也会保存 capture 级同步信息，例如 `timesync.csv`。
- **Take**：一次具体任务片段，是大多数训练、标注和评估会使用的逻辑单位，常用 `take_uid` 追踪。

典型结构可以理解成：

```text
egoexo4d/
  takes.json
  captures.json
  participants.json
  physical_setting.json
  takes/<take_name>/
    aria01.vrs
    frame_aligned_videos/
      aria01_214-1.mp4
      cam01.mp4
      cam02.mp4
      cam03.mp4
      cam04.mp4
    trajectory/
      closed_loop_trajectory.csv
      semi_dense_points.csv.gz
      gopro_calibs.csv
  captures/<capture_name>/
    timesync.csv
  annotations/
    ...
```

`takes.json` 是理解 Ego-Exo4D 的入口。它会列出每个 take 的 `take_uid`、`take_name`、`root_dir`、任务和场景信息、参与者信息、关联 capture，以及各相机的 frame-aligned 视频路径。训练时通常先通过 `take_uid` 找到 take，再加载这一 take 下的 ego / exo 视频、trajectory、camera calibration 和 annotation。

Ego-Exo4D 的关键不只是“多了几个外部相机”，而是多了一层严格的**多视角对齐**：

- Aria ego 视角要通过 VRS 和 MPS 读取设备标定、轨迹和传感器数据。
- GoPro exo 视角要通过 `gopro_calibs.csv` 读取静态相机内参和外参。
- `frame_aligned_videos` 让同一个 frame index 尽量对应同一时刻的多相机画面。
- 标注通常以 `take_uid` 分组，再按 frame、time 或任务事件定位。

这让 Ego-Exo4D 更适合做具身智能里的跨视角学习。例如：

- 从第三人称视频辅助理解第一人称被遮挡的手部或物体状态。
- 把 Aria 头部轨迹、GoPro 外部视角和三维姿态放到同一个世界坐标系。
- 用多视角监督训练更稳的手部、身体和活动理解模型。
- 做技能水平、动作阶段、专家讲解和跨视角翻译等任务。

它的质检重点也比 Ego4D 更偏向时空对齐：

- 同一个 `frame_idx` 在 ego 和 exo 视频中是否真的同步。
- Aria MPS 轨迹和 GoPro 静态相机外参是否在同一坐标约定下使用。
- 某个 GoPro 是否成功定位，低质量外参是否应从训练样本中排除。
- annotation 的 frame 编号、take 起止范围和 downscaled take 是否一致。
- take 级 split 是否避免同一 capture 或同一参与者造成泄漏。

## 主要相同点

三者都围绕第一人称或具身视角展开，不是普通互联网视频集合。它们的共同点包括：

- 都关心时间：视频帧、音频、IMU、眼动、轨迹或标注必须落在正确时间线上。
- 都有元数据索引：不能只靠文件名理解数据，必须读 JSON、CSV 或 VRS metadata。
- 都会区分原始数据和处理后数据：例如 Aria VRS 与 MPS、Ego4D components 与 canonical videos、Ego-Exo4D capture 与 take。
- 都需要处理隐私和数据裁剪：公开数据通常经过 redaction、trim、downscale 或任务切片。
- 都能服务具身智能评估：可以用于观测理解、动作阶段识别、空间定位、手物交互和多模态对齐。

## 主要差异

最重要的差异是“数据主轴”不同：

| 维度 | Project Aria | Ego4D | Ego-Exo4D |
| --- | --- | --- | --- |
| 主轴 | 设备 recording 和 sensor stream | `video_uid`、canonical video、clip | `take_uid` 和多相机同步片段 |
| 文件核心 | `.vrs` + MPS CSV / JSON / 点云 | MP4 / WebM + JSON annotations | Aria VRS + GoPro MP4 + take metadata + trajectory |
| 时间对齐 | 多传感器 stream timestamp | canonical video / clip time 和 frame | capture time sync + take frame alignment |
| 空间信息 | 设备坐标、相机坐标、MPS 世界轨迹 | 部分视频有 gaze、IMU、3D scan 等扩展 | Aria 轨迹 + GoPro 静态相机标定 + 点云 |
| 标注单位 | 通常依附 recording 或 MPS 输出 | 依附 video / clip / benchmark task | 依附 take / frame / multi-view camera |
| 训练前处理 | 解码 VRS，抽取图像、IMU、轨迹和 gaze | 选择 canonical video / clip，合并 JSON 标注 | 选择 take，读取 frame-aligned 多视角和标定 |
| 最大风险 | 坐标系和 stream 时间戳用错 | clip/video 时间字段混淆 | ego-exo 不同步或外参质量差 |

可以用一个类比理解：

- Aria 像“传感器黑匣子”，把设备看到、听到、感到的东西都按时间记录下来。
- Ego4D 像“第一人称视频图书馆”，每本书有目录、章节和任务标注。
- Ego-Exo4D 像“多机位动作采集棚”，同一个动作有头戴视角、外部机位、同步表和三维标定。

## 转成具身智能训练数据时怎么处理

如果要把这些数据转成统一 episode / trajectory 格式，可以按下面顺序设计：

1. 先确定主样本单位。
   - Aria：通常是一段 recording 或按任务后切出的 episode。
   - Ego4D：通常是 benchmark clip 或从 canonical video 裁出的片段。
   - Ego-Exo4D：通常是一个 take 或 take 内的任务阶段。

2. 明确主时间轴。
   - Aria：以设备 timestamp 或某个相机 stream timestamp 为基准。
   - Ego4D：以 canonical video time / frame 或 clip time / frame 为基准。
   - Ego-Exo4D：以 take 内 frame index 或 synchronized timestamp 为基准。

3. 建立路径索引。
   - 保存原始 VRS、MP4、MPS、annotation、calibration 的 source path。
   - 训练样本只存必要数据，但要能追溯回原始片段。

4. 统一坐标系说明。
   - 写清楚位姿是在 Aria device、camera、GoPro camera、world、scene 还是 robot base 坐标系。
   - 如果做机器人迁移，还要记录相机到 TCP、世界到机器人基座等外参。

5. 保存质量字段。
   - 时间同步状态、缺帧、轨迹丢失、标定质量、redaction、遮挡和人工审核结果都应进入 `quality_flags`。

6. 再做窗口采样。
   - 不要在还没校验 episode 边界和时间轴前直接切训练窗口。
   - 多视角数据要保证同一窗口里的 ego、exo、轨迹和标注引用的是同一段真实时间。

一个统一后的样本可以长这样：

```text
episode
  episode_id
  source_dataset: aria | ego4d | egoexo4d
  source_uid: recording_uid | video_uid | take_uid
  time_axis
    fps
    start_time
    end_time
    frame_offset
  observations
    ego_rgb
    exo_rgb(optional)
    imu(optional)
    gaze(optional)
    hand_pose(optional)
  trajectories
    camera_pose(optional)
    body_pose(optional)
    object_pose(optional)
  annotations
    language
    action_segment
    object_box
    proficiency
  calibration
    camera_intrinsics
    camera_extrinsics
    coordinate_frames
  quality_flags
```

## 资料来源

- [Project Aria Data Formats](https://facebookresearch.github.io/projectaria_tools/docs/data_formats)
- [Project Aria MPS Outputs](https://facebookresearch.github.io/projectaria_tools/docs/data_formats/mps/mps_summary)
- [Ego4D Start Here](https://ego4d-data.org/docs/start-here/)
- [Ego4D Metadata](https://ego4d-data.org/docs/data/metadata/)
- [Ego4D Videos](https://ego4d-data.org/docs/data/videos/)
- [Ego4D Annotation Schemas](https://ego4d-data.org/docs/data/annotations-schemas/)
- [Ego-Exo4D Overview](https://docs.ego-exo4d-data.org/overview/)
- [Ego-Exo4D Metadata](https://docs.ego-exo4d-data.org/data/metadata/)
- [Ego-Exo4D Data Format and Loader in Project Aria Tools](https://facebookresearch.github.io/projectaria_tools/docs/open_datasets/ego-exo4d/ego-exo4d_data_format)
