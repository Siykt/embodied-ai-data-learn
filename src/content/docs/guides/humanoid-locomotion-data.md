---
title: 人形与足式全身运动数据
description: 记录地形、接触、全身参考动作与控制结果，支持足式运动的训练、质检和跨场景评估。
---

足式运动数据的核心单位是“机器人—地形—接触”随时间共同变化的过程。相同的目标速度，在颗粒地面、坡屋面、障碍物或悬挂支撑上对应不同的稳定条件。[颗粒地形人形行走](https://arxiv.org/abs/2609.10286)关注足地作用，[SwingBot](https://arxiv.org/abs/2609.10283)则关注释放、摆荡和再抓取的接触序列。构建数据集时，不能只保存躯干轨迹和成功标签。

![足式运动从地形与本体采集、动作重定向到接触序列的处理流程](/images/docs/humanoid-locomotion-data-flow.svg)

## 采集、对齐与标注

- **外感与地形**：保存 RGB-D、激光雷达（LiDAR）、地面高程或深度图及视场覆盖；标注坡度、颗粒/硬地、落脚区域、可通行空隙与动态障碍。[JEPLO](https://arxiv.org/abs/2609.15770)利用原始 LiDAR 与本体感觉学习预测地形表征，说明原始观测及其采样时间不能被最终地图完全替代。
- **本体与控制**：记录基座姿态、关节位置/速度、估计接触力、执行命令、目标速度和控制周期。全身控制器还应记录参考动作、实际跟踪和安全修正；[RECAL](https://arxiv.org/abs/2609.16405)研究的正是参考目标有误时的避碰跟踪。
- **动作来源**：人体演示、运动捕捉、VR 稀疏命令和仿真生成动作分层存档，保留重定向算法和机器人形态版本。[Weave](https://arxiv.org/abs/2609.16683)把人—物交互转换为可执行参考，[X-WBC](https://arxiv.org/abs/2609.15213)则对齐人体运动、机器人参考和 VR 观测；转换后的动作不能覆盖原始示教。
- **事件标注**：逐足/逐手标注触地、离地、滑移、绊碰、摆荡抓持和失衡恢复；记录身体或持物与环境的碰撞。多技能序列要标注切换点，[足式技能组合](https://arxiv.org/abs/2609.14647)将过渡可靠性视为独立问题。

## 最小数据契约

![全身运动 episode 的地形、参考动作、接触和安全事件字段](/images/docs/humanoid-locomotion-data-contract.svg)

| 层级 | 建议字段 | 采集注意点 |
| --- | --- | --- |
| 场景与设备 | `terrain_id`, `surface_class`, `robot_model`, `sensor_calibration`, `sim_or_real` | 明确地形参数与机器人质量、驱动限制 |
| 时间序列 | `timestamp`, `base_pose`, `joint_state`, `raw_exteroception`, `command`, `reference_motion` | 各流保留设备时间与统一时间 |
| 接触 | `limb_id`, `contact_state`, `force_estimate`, `slip_flag`, `collision_flag` | 实测、动力学估计与仿真真值分开 |
| 结果 | `goal_progress`, `fall_event`, `tracking_error`, `energy_proxy`, `termination_reason` | 正常停止、超时、保护停机和跌倒分开 |

场景对齐要允许“未观测到”：遮挡或 LiDAR 空洞不能自动填成安全地面。对人形搬运与全身操作，还要保存持物位姿、手部接触和全身控制意图，[WholeBodyWAM](https://arxiv.org/abs/2609.16644)与[双足移动操作](https://arxiv.org/abs/2609.18930)涉及的输出就超出单纯步态标签。

## 质量控制与评估

![足式运动按地形、接触状态、形态和技能过渡开展评估](/images/docs/humanoid-locomotion-data-evaluation.svg)

检查传感器与控制时钟漂移、地形网格与相机坐标错位、接触力异常、标注的触地相位与足端速度不符；仿真数据另外核对摩擦、质量和延迟参数。报告完成率之外，还要分列跌倒/碰撞、目标速度误差、滑移、能源代理指标与恢复时间。**接触占空比**是一只脚在一个步态周期内保持触地的时间比例。[Duty Factor](https://arxiv.org/abs/2609.22073)研究步态占空比与约束地形鲁棒性的关系，评估时应保存此项而非只用平均速度。

切分时跨地形布局、材料、机器人形态、动作风格和控制技能组合，而非随机拆分相邻帧。场景对齐动作训练 [PASSAGE](https://arxiv.org/abs/2609.18732)与动态补全动作增强 [OmniMimic](https://arxiv.org/abs/2609.20566)都涉及派生运动：应以原始来源分组切分，避免增强版本泄漏。实际部署还需单列屋面坡度 [坡地全身运动](https://arxiv.org/abs/2609.20558)、机载执行延迟 [PredActor](https://arxiv.org/abs/2609.24840)和跨介质切换 [空地运动控制](https://arxiv.org/abs/2609.26564)等条件。

## 本月论文索引

本页索引收录 2026-08-27 至 2026-09-27 发表、归入本主题的论文。

- [MulDP: Multimodal Diffusion Policy for Autonomous Quadruped Parkour Navigation across Complex Terrains](https://arxiv.org/abs/2609.03984)（2609.03984）
- [Learning Terrain-Adaptive Humanoid Locomotion on Granular Terrain](https://arxiv.org/abs/2609.10286)（2609.10286）
- [SwingBot: Learning Whole-Body Brachiation for Humanoid Robots](https://arxiv.org/abs/2609.10283)（2609.10283）
- [Frame-Coded Legged Locomotion over Noisy Terrain](https://arxiv.org/abs/2609.10273)（2609.10273）
- [Weave: Learning Whole-Body Dexterous Loco-Manipulation from Human-Object Interactions](https://arxiv.org/abs/2609.16683)（2609.16683）
- [WholeBodyWAM: Generalizing Pre-trained World-Action Priors to Humanoid Loco-Manipulation via WBC-Grounded Coordination](https://arxiv.org/abs/2609.16644)（2609.16644）
- [Collision-Aware Humanoid Whole-Body Control under Imperfect Tracking Targets](https://arxiv.org/abs/2609.16405)（2609.16405）
- [JEPLO: Joint-Embedding Predictive Learning for LiDAR-Based Legged Locomotion](https://arxiv.org/abs/2609.15770)（2609.15770）
- [X-WBC: A Cross-Embodiment Foundation Model for Humanoid Whole-Body Control](https://arxiv.org/abs/2609.15213)（2609.15213）
- [Skill Composition for Legged Robot Reinforcement Learning](https://arxiv.org/abs/2609.14647)（2609.14647）
- [EMoG: Emotion-Modulated Gait Generation for Expressive Humanoid Locomotion](https://arxiv.org/abs/2609.14432)（2609.14432）
- [Decentralized Evolution of Hexapod Gaits with Independent Leg Controllers](https://arxiv.org/abs/2609.12400)（2609.12400）
- [DWMP: Leveraging Dual World Models for Humanoid Obstacle Traversal](https://arxiv.org/abs/2609.12347)（2609.12347）
- [Learning Holistic Whole-Body Loco-Manipulation with a Bipedal Mobile Manipulator](https://arxiv.org/abs/2609.18930)（2609.18930）
- [PASSAGE: Scaling Scene-Aligned Motion Learning for Perceptive Humanoid Traversal in Cluttered Environments](https://arxiv.org/abs/2609.18732)（2609.18732）
- [OmniMimic: Dynamics-completed Motion Augmentation for Multi-style Omnidirectional Quadruped Locomotion](https://arxiv.org/abs/2609.20566)（2609.20566）
- [Learning Slope-Adaptive Whole-Body Locomotion for Humanoid Robots in Roofing Construction](https://arxiv.org/abs/2609.20558)（2609.20558）
- [Duty Factor Predicts Robust Constrained Quadrupedal Locomotion Across Gait Types](https://arxiv.org/abs/2609.22073)（2609.22073）
- [PredActor: Predictive Action Diffusion for Steerable Onboard Humanoid Control](https://arxiv.org/abs/2609.24840)（2609.24840）
- [Learning Air-Ground Motion Control with Temporal Mode Switching and Cross-Terrain Tracking](https://arxiv.org/abs/2609.26564)（2609.26564）
- [ForgetMimic: Motion Unlearning for Reinforcement Learning Humanoid Control](https://arxiv.org/abs/2609.28378)（2609.28378）
