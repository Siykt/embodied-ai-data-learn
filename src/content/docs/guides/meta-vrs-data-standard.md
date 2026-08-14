---
title: Meta VRS 多传感器数据规范
description: 从记录模型、时间与坐标契约、质量控制和数据集转换角度整理 Meta 开源 VRS 格式及其与具身智能数据标准的关系。
---

VRS（Vision Replay Systems）是 Meta 开源的多传感器记录格式，也是 Project Aria 原始数据的重要底层容器。它适合保存相机、IMU、音频及其他离散传感器的带时间戳记录；但它**不是**把不同厂商设备自动变成同一种语义的跨厂商数据标准。

因此，使用 VRS 建设具身智能数据集时，应把问题分成两层：

- **记录层**：VRS 是否完整、可读、时间顺序正确，且能复现原始传感器输出？
- **数据集层**：不同设备、坐标系、标定版本和任务片段，是否被整理为可比较、可训练、可评估的 episode？

![VRS 文件中多路传感器流、记录类型和共同时间域的关系](/images/docs/vrs-record-model.svg)

## VRS 在“标准”里的位置

VRS 的核心是“多流的时间戳记录容器”。一个文件可保存多条 sensor stream；每条 stream 都有自身标签和记录序列，记录共享该文件的时间域。记录可承载元数据、图像、音频或自定义内容块，并可使用无损压缩、随机访问和分块文件。

这给它带来很好的采集复现能力：同一设备上的相机帧、IMU 样本和状态变化可以按原始时间保存。但以下语义并不会仅凭 `.vrs` 后缀自动成立：

| 需求 | VRS 本身提供 | 数据集仍须补充 |
| --- | --- | --- |
| 多传感器回放 | stream、记录、时间戳、数据载荷 | stream 的任务语义和选择规则 |
| 相机几何 | 可记录配置和标定相关内容 | 内外参版本、坐标轴、畸变模型与适用区间 |
| 多设备协作 | 各 recording 的本地记录 | 设备间时钟映射、同步误差和失效标记 |
| 训练样本 | 可解码为帧和传感器序列 | episode 边界、动作标签、窗口规则、split |
| 跨系统互用 | 开源 C++ / Python 读取工具 | 统一 schema、单位、坐标系、许可证与隐私处理 |

和相邻方案相比，VRS 更接近高保真**传感器记录层**：ROS bag 常与机器人消息生态结合；MCAP 重点是可扩展消息日志；HDF5 和 Zarr 常用于科学数组；Parquet 适合列式训练元数据。它们可以出现在同一条数据管线里，并不是互相排斥的“胜负关系”。例如原始 Aria 数据保留 VRS，解码后的低维状态存 Parquet，图像做分片视频或对象存储，episode 索引则由 JSON 或数据库管理。

## VRS 的记录模型

一个 VRS 文件可以把“谁产生了什么”和“何时产生”拆开理解：

- **文件与 stream 标签**：描述 recording 或具体 stream，例如设备、传感器和格式相关信息。
- **Configuration 记录**：描述怎样解释后续数据，例如图像尺寸、编码、单位或相机参数。不要把它当成永远不变的全局常量；配置可能随设备状态或记录段变化。
- **State 记录**：描述传感器或设备状态的变化。
- **Data 记录**：通常是数量最多的记录，例如图像帧、IMU 读数和音频包。
- **内容块**：一条记录由类型化内容块组成，常见为 metadata、image、audio 或自定义数据。

这里最容易出错的是把“第 `n` 个数据记录”误当成“第 `n` 个主相机帧”。不同 stream 的采样率、断流、配置变更和写入节奏都可能不同。跨 stream 对齐必须以时间戳和明确的容差规则完成，而不是以数组位置完成。

对于 Project Aria，VRS 还承载设备级记录；MPS（轨迹、点云、眼动、手部等）是对原始记录的后处理结果。MPS 可提高使用效率，却不能覆盖原始 VRS 的溯源价值。两者关系可先参考 [Aria、Ego4D 与 Ego-Exo4D 数据格式](/guides/aria-ego4d-egoexo4d-formats/)。

![从原始 VRS、标准化处理到可训练 episode 的数据契约](/images/docs/vrs-to-episode-contract.svg)

## 面向具身数据的最小转换契约

将 VRS 导出为模型数据时，建议把原始文件视为不可变证据，将派生数据视为带版本的产品。一个可复现转换至少应记录：

```text
source_vrs
  uri, sha256, recording_start, reader_version
streams
  stream_id, sensor_role, source_time_domain, unit, configuration_digest
time_alignment
  primary_stream, timestamp_mapping, max_skew_ms, interpolation_policy
coordinate_frames
  frame_id, parent_frame_id, axis_convention, transform, calibration_version
episode
  episode_id, start_timestamp, end_timestamp, task, split
quality_flags
  missing_frames, imu_gap, decode_error, calibration_warning, privacy_status
```

其中 `sensor_role` 是刻意加入的一层语义。例如同为 image stream，也可能分别承担主观测、双目定位、眼动或第三人称参照的职责；训练加载器不应通过 stream 编号猜测它们。`timestamp_mapping` 则要说明时间戳是否原样使用、是否映射到全局时钟、是否重采样，以及允许的最大对齐误差。

坐标变换必须写成可追溯的帧关系，例如 `T_world_device`、`T_device_camera` 或 `T_robot_base_camera`，并记录轴约定、长度单位和标定版本。只存一个没有 frame id 的 4x4 矩阵，后续无法可靠判断轨迹、点云和机器人动作能否放在同一空间中。相关概念见[标定文件](/reference/terms/#标定文件)和[数据对齐](/reference/terms/#数据对齐)。

## 质量控制与评估

VRS 文件能打开不代表它适合训练。建议在 ingest 阶段形成每条 recording 的质量报告：

| 检查项 | 需要回答的问题 | 对下游的影响 |
| --- | --- | --- |
| 完整性 | 文件是否可读，分块文件是否齐全，校验和是否一致？ | 防止样本静默缺失或无法复现 |
| stream 清单 | 预期相机、IMU、音频和标定记录是否存在？ | 防止训练时错误填充缺失模态 |
| 时间连续性 | 相邻 timestamp 的间隔、倒退、长 gap 和跨 stream 偏差是否异常？ | 防止视觉、动作和惯性信号错配 |
| 配置一致性 | 分辨率、编码、单位、内参是否在预期段内变化？ | 防止一个 decoder 假设覆盖整段 recording |
| 空间关系 | 外参与坐标系版本是否完整且与派生轨迹匹配？ | 防止 SLAM、点云、手部和机器人姿态错位 |
| 派生结果 | MPS 或其他处理是否标注版本、置信度和失败片段？ | 防止把估计结果当作真值 |
| 隐私与授权 | 人脸、音频、位置等是否按数据使用条件处理？ | 决定能否发布、共享和用于训练 |

评估时不要只报告模型平均分。应按 `quality_flags` 分桶，至少比较“同步正常 / 存在 gap”“标定稳定 / 标定警告”“轨迹可用 / 轨迹失败”等子集。这样才能区分模型真的不擅长某类任务，还是数据时间或空间关系出了问题。

## 可发散的资料与实践方向

围绕 VRS 可以继续延伸到以下几条更具数据价值的路线：

- **跨设备采集基准**：把 Aria VRS、机器人状态、外部相机和环境传感器通过统一时钟和 frame graph 组织起来，专门测量跨设备时间偏差与空间残差。
- **数据 lineage**：为每个训练 episode 保存 VRS 校验和、读取工具版本、解码参数、标定版本和过滤规则，使模型结果可追溯到原始 recording。
- **自监督多模态对齐**：以 VRS 的相机-IMU 时间关系构造正负样本，评估表征能否识别时间偏移、镜头遮挡和传感器失真。
- **质量感知训练**：将 `imu_gap`、曝光异常、轨迹置信度和标定状态作为采样权重或辅助标签，而不是简单删除所有“非完美”数据。
- **从人类演示到机器人数据**：通过可审计的相机外参与世界坐标，把 Aria 的第一人称观测、手部估计与机器人 TCP、夹爪状态连接起来；转换不确定性也应成为样本字段。
- **隐私优先的数据产品**：把 redaction 版本、访问级别和可用模态写入数据契约，在生成训练分片前执行策略检查，避免在下游复制受限原始内容。

## 工具与资料

- [VRS Overview](https://facebookresearch.github.io/vrs/docs/Overview)：格式定位、记录和 stream 的基础说明。
- [VRS Organization](https://facebookresearch.github.io/vrs/docs/Organization)：文件、stream、record type 与内容块的组织方式。
- [VRS CLI](https://facebookresearch.github.io/vrs/docs/VrsCliTool)：检查、导出和生成修改后 VRS 文件的命令行工具。
- [VRS GitHub Repository](https://github.com/facebookresearch/vrs)：C++ 库、样例和 Python 绑定入口。
- [Project Aria Tools](https://github.com/facebookresearch/projectaria_tools)：Aria Gen1/Gen2 的 VRS 数据读取、标定、同步与 MPS 工具。
- [Project Aria Gen2 Tutorials](https://github.com/facebookresearch/projectaria_tools/tree/main/examples/Gen2/python_notebooks)：VRS、设备标定、多传感器顺序读取、时间同步和 MPS 的可运行教程。
- [ROS bag](https://docs.ros.org/en/rolling/Concepts/Intermediate/About-Bag-Files.html)、[MCAP](https://mcap.dev/) 和 [Apache Parquet](https://parquet.apache.org/)：制定自有数据产品分层时可对照的记录、消息和列式存储方案。
