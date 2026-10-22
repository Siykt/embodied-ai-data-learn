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

## 2026 年 10 月：分层动作接口与环境条件的联合记录

截至 **2026-10-22**。以下增量依据本月论文，字段设计和验收步骤是本站工程建议。

### 同一动作意图可以通过不同层级实现

[HuMBLE（2610.10489）](https://arxiv.org/abs/2610.10489)将人类步态参考蒸馏为由本体状态和速度命令驱动的先验；[结构化运动参考研究（2610.24779）](https://arxiv.org/abs/2610.24779)让学习策略调整机身运动、落足和步态时序，保留优化控制器负责高频执行；[SP-HLM（2610.30044）](https://arxiv.org/abs/2610.30044)结合关键身体位姿与隐式运动先验。它们说明数据接口必须标明记录的是高层意图、完整运动参考还是底层控制命令。

建议每次采样绑定 `command_time`、`reference_time`、`actuation_time` 与父子接口 ID，保存参考生成器和跟踪器版本。高层运行慢、低层运行快时，不要通过简单复制高层标签掩盖其实际生效区间。步态自然程度、命令覆盖和受扰稳定性分别评价，不能把“像人”当作满足所有速度命令的证明。

![分层动作接口与环境条件的联合记录的数据记录与评估关系](/images/docs/humanoid-locomotion-data-october-data.svg)

### 参考生成与执行成功保持可追溯

[KinoGen（2610.20552）](https://arxiv.org/abs/2610.20552)从目标机器人与物体的标定渲染出发，经双视角视频生成及模型拟合恢复参考；[DiPLO（2610.24847）](https://arxiv.org/abs/2610.24847)则利用人到机器人的重定向运动，并进一步使计划适合固定跟踪器。数据需分清生成来源，保存相机、身体模型、关键帧约束、穿透/滑脚检查和执行日志。参考满足目标姿态，并不代表接触过程一定可执行。

[RISE（2610.30061）](https://arxiv.org/abs/2610.30061)研究跌倒后的感知恢复，同一倒地姿势可以采用不同支撑过渡和起身朝向。应保留周围场景、倒地姿态、支撑接触序列、期望方向与实际路径。恢复任务不能只存终点“站起来”，否则无法学习避开障碍或沿指定路径恢复。

### 策略权重也可能成为数据对象

[人形策略权重扩散研究（2610.20606）](https://arxiv.org/abs/2610.20606)直接建模训练所得控制网络的权重分布。**策略权重数据集**以网络参数及其训练、执行元数据为样本。整理时需要固定网络结构、参数顺序、观测归一化、动作接口、机器人模型和训练种子。若这些契约不一致，权重向量的距离不能直接解释为行为相似度；生成的权重仍需执行验证。

### 将重力、地形和接触模型作为交叉因素

[地月迁移研究（2610.30080）](https://arxiv.org/abs/2610.30080)联合改变重力、地形及土壤接触，并说明迁移可能不对称。训练条件与测试条件应分别列出，保留原环境回归结果，避免只报告适配后的目标环境。月面结果是依赖土壤模型与刚度假设的仿真预测，不是真实月面机器人数据。对每个交叉条件同时统计存活、前进距离、跌倒与脚底接触；短参考轨迹可能使归一化比值不稳定，需检查分母。

### 2026 年 10 月来源与数据启示

以下说明以原始摘要为依据；具体性能数字与复现实验应继续核对论文正文。

| 论文 | 数据启示 |
| --- | --- |
| [2610.10489 · HuMBLE: Human Motion-Driven Behavior Learning for Embodied Locomotion](https://arxiv.org/abs/2610.10489) | 采集不同速度方向的人体动作，兼顾风格、控制指令和实机泛化。 |
| [2610.20552 · KinoGen: Customizable Humanoid Loco-Manipulation References via Kinematically Grounded Video Generation](https://arxiv.org/abs/2610.20552) | 从机器人条件视频生成全身操作参考，并部署到真实人形机器人。 |
| [2610.20606 · Modeling and Understanding Neural Weights of Humanoid Policies with Diffusion](https://arxiv.org/abs/2610.20606) | 研究人形控制策略权重的生成与结构，并展示真实硬件动作，属于机器人策略数据边界。 |
| [2610.24779 · Learning Structured Locomotion References for Optimization-Based Whole-Body Control](https://arxiv.org/abs/2610.24779) | 四足控制中的身体、接触、落脚和步态参考及扰动实验属于足式机器人数据。 |
| [2610.24847 · DiPLO: Self-distilled Diffusion Planning for Loco-manipulation](https://arxiv.org/abs/2610.24847) | 人体动作重定向参考用于人形全身规划训练，并进行真实部署。 |
| [2610.30044 · SP-HLM: Sparse-Pose-Driven Motion Generation and Whole-Body Control for Humanoid Loco-Manipulation](https://arxiv.org/abs/2610.30044) | 以稀疏身体目标和运动先验联接人形任务策略与全身控制，并真实验证。 |
| [2610.30061 · Test-Time Motion Steering for Perceptive Humanoid Fall Recovery](https://arxiv.org/abs/2610.30061) | 在人形跌倒恢复中学习参考动作与任务化路线选择，并有真实示例。 |
| [2610.30080 · Do Earth-Trained Humanoid Controllers Walk on the Moon? Gravity, Terrain, and Soil Transfer](https://arxiv.org/abs/2610.30080) | 月球重力与土壤迁移属于人形物理控制边界，摘要明确限定为接触模型条件下的仿真预测。 |

## 2026 年 9 月来源

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
