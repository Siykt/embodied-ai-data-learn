---
title: Ego 数据、世界模式与 UMI 视频采集逻辑
description: 从具身智能数据角度整理 Ego 视角、世界模式、操作模式，以及 UMI 如何把手持拍摄视频转换成可训练数据。
---

这篇把“Ego”相关资料放在数据管线里理解：它不是单纯讨论第一人称视频，也不是泛泛讲世界模型，而是关注**人或夹爪在真实场景中看到什么、移动到哪里、如何操作物体，以及这些记录怎样变成机器人可学习的数据**。

这里的 Ego 主要指 egocentric view，也就是第一人称或本体视角。对具身智能数据来说，它有一个直接好处：画面天然接近执行者当时能看到的信息。人拿着工具、戴着眼镜，或手持 UMI 夹爪操作物体时，摄像头记录的是“我正在面向哪里、手边有什么、接下来怎样接触物体”。

![Ego 数据从第一人称观测进入世界模式，再转换成可训练操作数据的流程](/images/docs/ego-world-operation-overview.webp)

## 相关资料脉络

可以先把 Ego 数据分成三类来看：

- 普通第一人称视频：重点是人眼或头戴设备看到的画面，适合学习任务步骤、物体状态和接触时机，但动作不一定能直接给机器人执行。
- 带身体状态的 Ego 数据：除视频外，还记录手部轨迹、头部姿态、IMU 或眼动。EgoMimic 就属于这一类，它把人类第一人称视频和三维手部跟踪作为可扩展的模仿学习数据来源。
- 带可执行操作接口的 Ego 数据：采集工具本身尽量像机器人末端执行器，视频和动作可以转换成机器人末端轨迹。UMI 属于这一类，它用手持夹爪和 GoPro 采集真实世界演示，再生成可训练的视觉运动策略数据。

这三类数据的差别不在“有没有视频”，而在后处理后能不能回答下面几个问题：

- 观测：每一帧看到的环境和物体状态是什么？
- 位姿：执行者、相机或夹爪在统一坐标系里在哪里？
- 操作：末端执行器下一步应该到哪里、朝向哪里、夹爪开多大？
- 对齐：视频、轨迹、夹爪状态和 episode 边界是否在同一条时间线上？
- 评估：哪些片段定位失败、遮挡严重、标定不可靠，应该被丢弃？

## 世界模式是什么

“世界模式”可以理解成把 Ego 采集数据放进一个较稳定的环境坐标系里。它关心的是外部世界如何被记录和重建，而不是只看相机自己的画面。

在数据字段上，世界模式通常会包含：

- 环境参考坐标系，例如桌面标记板、房间地图、SLAM 地图原点。
- 相机或末端执行器的世界位姿，也就是每个时间点的位置和朝向。
- 地图、关键帧、点云、物体标记或语义信息。
- 相机内参、鱼眼畸变参数、相机到夹爪 TCP 的外参。
- 质量信息，例如 SLAM 是否丢失、漂移是否过大、标记板是否稳定可见。

用一个日常类比：Ego 视频像是“头上戴的运动相机”；世界模式像是事后把这段运动相机画面放回房间平面图里，知道每一秒拍摄者站在哪里、手伸向哪里、物体在桌面的哪个区域。

对具身智能数据来说，世界模式的价值是让不同演示、不同相机、不同机器人之间可以比较和对齐。否则同样一个“把杯子放到碟子上”的动作，在画面里可能方向完全不同，模型很难知道哪些变化来自相机运动，哪些变化来自任务本身。

## 操作模式是什么

“操作模式”关注的是数据怎样表达可执行动作。它不只问“世界是什么样”，而是问“机器人下一步应该怎么动”。

常见操作模式包括：

- 绝对动作：直接预测世界坐标系下的末端位置、朝向和夹爪宽度。
- 相对动作：预测相对于当前末端位姿的未来轨迹，例如往前 3 厘米、旋转一点、夹爪闭合。
- 增量动作：每个控制周期只预测一个小变化量，适合低层闭环控制。
- 轨迹动作：一次预测未来多个时间步，让控制器按轨迹执行。

UMI 论文强调的关键设计之一就是相对轨迹动作表示。这样做的直觉是：人手持夹爪在不同房间、不同桌面、不同机器人上演示时，绝对位置会变，但“相对当前手的位置怎样靠近杯子、怎样夹住、怎样移动到碟子上”更容易复用。

在训练数据里，操作模式通常会落成这些字段：

- `robot0_eef_pos`：末端位置。
- `robot0_eef_rot_axis_angle`：末端朝向。
- `robot0_gripper_width`：夹爪开合宽度。
- `action`：未来一段时间的末端位姿和夹爪宽度。
- `demo_start_pose` / `demo_end_pose`：episode 起止位姿，用于相对表示或额外条件。

## UMI 采集视频到底记录了什么

UMI 的拍摄不是“拿手机随便拍一段人手视频”。它有几个重要约束：

- 摄像头安装在手持夹爪上，形成接近机器人末端执行器的 Ego 视角。
- GoPro 视频里同时有图像和可提取的 IMU 元数据。
- 夹爪手指上有 ArUco 标记，用来估计夹爪开合宽度和区分不同夹爪硬件。
- 采集 session 里通常包含 mapping 视频、gripper calibration 视频和正式 demo 视频。
- 后处理会把多台相机或双手演示按时间重叠段切成 episode。

因此，一段 UMI 视频在数据管线里承担三件事：

- 作为视觉观测：给策略模型看的 `camera0_rgb`。
- 作为定位输入：图像和 IMU 送进 ORB-SLAM3，得到相机轨迹。
- 作为夹爪状态输入：检测 ArUco 标记，得到夹爪宽度和硬件身份。

## UMI 视频处理逻辑

UMI 官方仓库的 `run_slam_pipeline.py` 会顺序调用 `scripts_slam_pipeline` 下的处理脚本。可以把它理解成从原始 MP4 到 dataset plan 的七步。

![UMI 从整理视频、提取 IMU、运行 SLAM、检测标记到生成 replay buffer 的处理管线](/images/docs/umi-video-processing-pipeline.webp)

### 1. 整理原始视频

`00_process_videos.py` 先把 session 下的 MP4 归入 `raw_videos`，再输出到 `demos` 目录。

它会做几件工程化处理：

- 如果没有 `raw_videos` 目录，就创建目录并移动 MP4。
- 如果没有 `mapping.mp4`，默认把最大的 MP4 当成 mapping 视频。
- 如果没有 `gripper_calibration` 目录，就按 GoPro 相机序列号选择每台相机最早的一段视频作为夹爪标定视频。
- 用 ExifTool 读取 GoPro 序列号和开始时间，把视频目录命名为 `demo_<camera_serial>_<start_time>`。
- 每个视频目录里统一保存为 `raw_video.mp4`。

这一步的核心目的是建立稳定的数据目录结构，让后续脚本不再依赖原始文件名。

### 2. 提取 GoPro IMU

`01_extract_gopro_imu.py` 使用 Docker 镜像中的 OpenImuCameraCalibrator 脚本，从每个 `raw_video.mp4` 里提取 GoPro IMU 元数据，生成 `imu_data.json`。

这一步很重要，因为 UMI 后面的定位不是纯视觉，而是视觉惯性 SLAM。视频负责看环境，IMU 负责补足快速转动和加速度信息。

### 3. 建立 SLAM 地图

`02_create_map.py` 使用 mapping 视频和对应的 `imu_data.json` 运行 ORB-SLAM3，输出：

- `mapping_camera_trajectory.csv`
- `map_atlas.osa`
- `slam_stdout.txt`
- `slam_stderr.txt`

脚本还会生成 `slam_mask.png`，把夹爪、手指或镜面区域从 SLAM 特征提取里遮掉。原因很直接：夹爪和手指会跟着相机动，不属于稳定环境；如果 SLAM 把它们当成墙角、桌角这类固定线索，轨迹会变差。

### 4. 对 demo 批量跑 SLAM

`03_batch_slam.py` 对每个正式 demo 视频运行同一套 GoPro 单目惯性 SLAM，并加载前面建好的 `map_atlas.osa`。输出的关键文件是每段视频的 `camera_trajectory.csv`。

这里会检查视频时长、设置超时、限制最大丢失帧数，并继续使用 mask。后续 `dataset_plan` 会根据 `is_lost` 过滤跟踪失败太多的片段。

### 5. 检测 ArUco 标记

`04_detect_aruco.py` 对每个视频运行 `scripts/detect_aruco.py`，结合 GoPro 鱼眼内参和 ArUco 配置，输出 `tag_detection.pkl`。

这个文件会被用于两类估计：

- 在 mapping 视频里估计 SLAM 地图与桌面标记板之间的变换。
- 在 demo 视频里估计夹爪手指标记，从而计算夹爪宽度。

### 6. 运行标定

`05_run_calibrations.py` 做两件事：

- 用 `calibrate_slam_tag.py` 生成 `tx_slam_tag.json`，把 SLAM 地图坐标和桌面标记板坐标连起来。
- 用 `calibrate_gripper_range.py` 生成 `gripper_range.json`，把视觉检测到的手指间距转换成实际夹爪宽度范围。

这一步把世界模式和操作模式接上了：SLAM 给相机在地图里的位姿，桌面标记板给可解释的任务坐标系，夹爪标定给可执行的开合量。

### 7. 生成 dataset plan

`06_generate_dataset_plan.py` 是 UMI 数据逻辑里最关键的一步。它会把多个视频、多个夹爪和多个相机合成 episode 计划。

主要逻辑包括：

- 读取每段视频的 GoPro 序列号、开始时间、帧数、帧率和结束时间。
- 找到所有相机同时录制的时间段，把这些重叠段切成 demo episode。
- 用 ArUco 标记识别每个视频属于哪个夹爪硬件。
- 对双手或多夹爪数据，按空间关系判断右手为 `camera_idx=0`、左手为 `camera_idx=1`，其他非夹爪相机排在后面。
- 读取 `camera_trajectory.csv`，把 SLAM 相机位姿转换到桌面标记板坐标系。
- 用固定的 GoPro 到夹爪 TCP 偏移，把相机位姿转换成夹爪 TCP 位姿。
- 从 `tag_detection.pkl` 中计算夹爪宽度，并插值到每一帧时间戳。
- 丢弃 SLAM 丢失太多、有效帧太少、手动检查失败或标记检测不足的片段。
- 输出 `dataset_plan.pkl`，其中每个 episode 包含 `episode_timestamps`、`grippers` 和 `cameras`。

这一步产出的 `tcp_pose` 和 `gripper_width`，就是从“拍到的视频”变成“机器人可学习动作”的关键桥。

### 8. 生成 replay buffer

`07_generate_replay_buffer.py` 再把 `dataset_plan.pkl` 转成 `dataset.zarr.zip`。

低维数据会写入：

- `robot0_eef_pos`
- `robot0_eef_rot_axis_angle`
- `robot0_gripper_width`
- `robot0_demo_start_pose`
- `robot0_demo_end_pose`

图像数据会从原始视频中截取对应帧，处理后写入：

- `camera0_rgb`
- `camera1_rgb`
- 更多相机则继续按编号扩展。

图像处理里还有几个 UMI 特有细节：

- 对 ArUco 标记区域做 inpaint，避免策略模型过度依赖标记图案。
- 遮掉夹爪本体，减少“看见自己的工具”带来的过拟合。
- 把图像 resize 到训练分辨率，默认常见为 `224x224`。
- 可选地对鱼眼图像做视场转换。
- 可选地处理镜面视角。

最终 `UmiDataset` 或 `SequenceSampler` 在训练时会从 replay buffer 中采样观测窗口和未来动作窗口。如果 replay buffer 里没有显式 `action` 字段，采样器会把末端位置、末端朝向和夹爪宽度拼成 action，再根据配置把绝对位姿转换成相对表示。

## 数据质量检查重点

整理 UMI 或类似 Ego 采集数据时，可以重点检查这些问题：

![Ego 和 UMI 数据质量检查中视频、IMU、SLAM 轨迹和夹爪状态的时间对齐关系](/images/docs/umi-data-quality-check.webp)

- GoPro 时间是否正确，多个相机开始时间是否能形成稳定重叠段。
- 每段视频是否有 `imu_data.json`，IMU 提取失败会直接影响 SLAM。
- mapping 视频是否覆盖足够的环境纹理，是否有桌面标记板。
- `camera_trajectory.csv` 里 `is_lost` 是否过多。
- `tag_detection.pkl` 中夹爪手指标记检测率是否足够高。
- `tx_slam_tag.json` 是否稳定，标记板不能在 mapping 后被移动。
- `gripper_range.json` 是否来自同一套夹爪硬件。
- 图像遮罩是否遮住了动态夹爪区域，同时没有误遮任务关键物体。
- replay buffer 中图像帧数、低维轨迹长度和 episode 边界是否一致。

如果这些检查没做好，模型表面上仍然能训练，但会学到错位的动作：比如看到“杯子已经在指尖前方”，动作标签却来自晚了几帧或偏了几厘米的轨迹。

## 与视觉惯性 SLAM 的关系

UMI 的视频管线本质上是视觉惯性 SLAM 在具身智能操作数据里的一个具体应用。

视觉惯性 SLAM 负责回答“夹爪相机在世界里怎么动”；ArUco 和夹爪标定负责回答“夹爪开了多大、坐标系怎么对齐”；replay buffer 负责把这些结果整理成策略训练可以直接读取的样本。

如果需要补充 SLAM 背景，可以先看[视觉惯性 SLAM 数据整理](/guides/visual-inertial-slam/)。

## 资料来源

- [Universal Manipulation Interface 项目页](https://umi-gripper.github.io/)
- [Universal Manipulation Interface 论文](https://arxiv.org/abs/2402.10329)
- [Universal Manipulation Interface 官方代码库](https://github.com/real-stanford/universal_manipulation_interface)
- [UMI 使用的 ORB-SLAM3 分支](https://github.com/cheng-chi/ORB_SLAM3)
- [OpenImuCameraCalibrator](https://github.com/urbste/OpenImuCameraCalibrator/)
- [EgoMimic 项目页](https://egomimic.github.io/)
- [EgoMimic 论文](https://arxiv.org/abs/2410.24221)
- [FastUMI 论文](https://arxiv.org/abs/2409.19499)
