---
title: 导航、语义地图与可通行性数据
description: 从时空观测、地图更新和目标语义出发，组织导航任务的数据契约与评估切分。
---

导航数据不等于一张静态占据栅格。机器人要把语言或目标物体与当前视野、历史路径和可行走空间连起来，还要在环境变化后更新判断。**地图版本**表示某次访问或更新时刻的地图状态及其观测证据。[OVMAN](https://arxiv.org/abs/2609.06424)用两次访问及物体移动关系提出导航目标；“回到花瓶原来的位置”要求记住一个已空出的地点，而不是在当前画面里重新检测花瓶。面向具身数据，这意味着地图必须携带时间、证据来源和对象变化。

![导航数据从传感器观测、定位建图到目标与路径标签的处理流程](/images/docs/navigation-traversability-data-flow.svg)

## 采集与时空对齐

- **原始观测**：保存 RGB、深度、激光雷达（LiDAR）或里程计的原始时间戳、外参和有效区域，记录轨迹估计及其置信度。**语义占据**是在空间单元中同时表示可通行/占据状态与物体类别；相关预测把二维图像特征投到三维体素，[室内语义占据比较](https://arxiv.org/abs/2609.17257)表明上游视觉编码器选择会改变结果；所以数据集应同时可追溯原始图像、深度和投影参数。
- **地图版本**：区分一次访问时的地图、二次访问更新后的地图、最终人工核验地图。每个语义对象保存类别、位置、时间范围、可见性、观测来源及不确定性。[农业语义 SLAM](https://arxiv.org/abs/2609.20604)在定位地图中结合植物类型、尺寸和健康属性，说明语义属性要跟具体地图实体及测量时刻绑定。
- **任务与动作**：记录原始指令、目标实体或位置、候选路点、规划路径、执行轨迹和终止理由。[O2C-Nav](https://arxiv.org/abs/2609.06476)先选择图像上的候选路点，再由低层规划转成可执行路径；候选与执行结果应分别保留，便于定位错误来自语义选择还是几何执行。

![导航 episode 中地图版本、目标、轨迹及证据来源的数据字段](/images/docs/navigation-traversability-data-contract.svg)

## 最小数据契约

| 单位 | 建议字段 | 语义要求 |
| --- | --- | --- |
| 场景访问 | `scene_id`, `visit_id`, `map_version`, `change_events` | 同一场景多次访问不得混为同一真值 |
| 观测帧 | `timestamp`, `sensor_pose`, `rgb_depth_lidar_refs`, `pose_uncertainty` | 标定、丢帧和定位回环修正可追溯 |
| 地图实体 | `entity_id`, `semantic_class`, `geometry`, `valid_from_to`, `confidence` | 物体离开后保留历史位置与状态 |
| 决策步 | `instruction`, `goal_id`, `candidate_waypoints`, `chosen_waypoint`, `executed_path` | 高层目标与底层控制命令分离 |
| 结果 | `goal_reached`, `collision`, `path_length`, `termination_reason` | 到达容差及不可达判据明确 |

## 质量控制、切分与下游使用

![导航评估按未见场景、地图变化、定位误差和语言目标分层](/images/docs/navigation-traversability-data-evaluation.svg)

质检先查地图与视频时间是否一致、闭环后位姿是否回写、语义对象是否重复编号、障碍边界是否与真实通行空间冲突。导航中“可通行”还依机器人形态、宽度和动作能力变化；[LightNav-0](https://arxiv.org/abs/2608.30935)把空间意图与本体特定轨迹连接，数据中应把目标点与机器人的可执行路径分开标注。[HarnessVLN](https://arxiv.org/abs/2609.15195)对规划建议做空间证据和几何可行性验证，失败反馈也应作为数据保留。

评估可同时报告目标到达、路径效率、碰撞、地图更新正确率、指令定位和失败恢复。按建筑/农田、视角、访问时间、目标措辞与变化关系切分；同一场景相邻路线不能同时进入训练与未见场景测试。对需要人体引导的任务，还要记录身体相对方向与抓取确认阶段，[Touvigation](https://arxiv.org/abs/2609.21828)把寻物过程分成定向、行走、伸手与触觉验证。部分可观测多智能体任务 [HORIZON](https://arxiv.org/abs/2609.12422)则应额外保存可见性掩码和信念状态，不把隐藏状态泄漏给策略输入。

## 2026 年 10 月：未来轨迹评分与无地图脱困证据

截至 **2026-10-22**。以下增量依据本月论文，字段设计和验收步骤是本站工程建议。

### 记录被比较的候选，而不只记录最终路线

[LiteNWM（2610.12368）](https://arxiv.org/abs/2610.12368)共享视觉编码，预测多个候选轨迹在不同时间跨度的未来表示，再用评分器选择轨迹。用于学习和诊断的数据需要保存 `candidate_set_id`、候选轨迹、预测跨度、评分器版本以及最终选择。只有被选路线的执行结果可直接观测；未执行候选的预测不是实际未来真值。

**候选轨迹评分**是在同一当前观测下，比较多条拟执行路线的预计后果。建议区分候选生成器的覆盖能力与评分器的选择能力：若正确绕行方案根本没有出现在候选集中，单纯提高评分精度无法解决问题。使用相同候选集合比较评分器，另用固定评分器比较候选生成器，能减少混淆。

![未来轨迹评分与无地图脱困证据的数据记录与评估关系](/images/docs/navigation-traversability-data-october-data.svg)

### 短窗运动线索与累计地图承担不同职责

[SAS（2610.13838）](https://arxiv.org/abs/2610.13838)针对带摆臂履带机器人，以 IMU、摆臂角度和短时间窗内“是否在运动”的线索进行稳定与脱困控制。运动线索不累计成里程计，因此避免了长期积分地图误差的直接传播；但这并不等于短窗线索没有噪声，也不代表系统具备全局定位。

数据可增加 `motion_cue_window`、`motion_detected`、机体横滚/俯仰、摆臂关节角、控制意图与卡住区间。若命令持续前进而机体位移很小，需区分真正卡住、低速执行和传感器失效；阈值、窗口长度和线索来源都应随数据交付。将隐藏障碍物、可见障碍物与地图陈旧分别标注，才能分析无地图局部反馈在哪些条件下有效。

### 导航质量与计算成本使用独立证据

LiteNWM 的离线轨迹误差、特定硬件计算速度与真实机器人成功率属于不同评测口径。记录设备、候选数量、编码是否复用、预测跨度和端到端耗时；不能将高性能显卡上的速度直接当作任意机载平台的延迟。

SAS 的越障能力也不等于目标导航能力：局部控制可能成功越过障碍，却走向错误目标。统一导航记录可在任务层保留目标到达和路径代价，在控制层保留姿态稳定、脱困时间、摆臂动作和接触事件。按同场景、同初态、同预算比较，才可判断性能来自规划还是局部执行。

### 2026 年 10 月来源与数据启示

以下说明以原始摘要为依据；具体性能数字与复现实验应继续核对论文正文。

| 论文 | 数据启示 |
| --- | --- |
| [2610.12368 · LiteNWM: Efficient Latent World Models for Onboard Visual Navigation in the Wild](https://arxiv.org/abs/2610.12368) | RECON/SCAND/SACSoN离线轨迹与未见真实室内外导航形成可比评测。 |
| [2610.13838 · Mapless, Stabilizing, and Anti-Stuck Flipper Control for Articulated Tracked Robots](https://arxiv.org/abs/2610.13838) | 真实履带机器人用IMU、关节角与是否移动记录防卡死，无需累计里程计。 |

## 2026 年 9 月来源

本页索引收录 2026-08-27 至 2026-09-27 发表、归入本主题的论文。

- [LightNav-0: Eliciting VLM Spatial Intelligence for Generalist Embodied Navigation](https://arxiv.org/abs/2608.30935)（2608.30935）
- [One MLLM, One Call: Efficient Zero-Shot Vision-and-Language Navigation via Spatial-Aware Waypoints](https://arxiv.org/abs/2609.06476)（2609.06476）
- [OVMAN: A Task and Benchmark for Open-Vocabulary Motion-Aware Navigation](https://arxiv.org/abs/2609.06424)（2609.06424）
- [MobileVLA-R1 2.0: RL-Enhanced Reasoning for Mobile Robot Control](https://arxiv.org/abs/2609.06251)（2609.06251）
- [Exploring 2D backbone effects for indoor semantic occupancy prediction](https://arxiv.org/abs/2609.17257)（2609.17257）
- [HarnessVLN: Unifying Training-Free Embodied Navigation through an Agent Harness](https://arxiv.org/abs/2609.15195)（2609.15195）
- [Hierarchical Belief Modeling for Zero-Shot Opponent Adaptation in Partially Observable Multi-Agent Navigation](https://arxiv.org/abs/2609.12422)（2609.12422）
- [AdaGeoVLN: Selective Geometry Across Representation Depth and Navigation Time for Vision-Language Navigation](https://arxiv.org/abs/2609.18789)（2609.18789）
- [Semantic SLAM in Precision Agriculture using Bayesian Inference](https://arxiv.org/abs/2609.20604)（2609.20604）
- [Touvigation: Embodied Adaptive Object Acquisition for Blind and Low-Vision Users in Unfamiliar Indoor Environments](https://arxiv.org/abs/2609.21828)（2609.21828）
