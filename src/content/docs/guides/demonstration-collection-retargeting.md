---
title: 示教采集与动作重定向
description: 从远程操作、人体示教到机器人动作监督，整理来源、时序、坐标与执行结果的可追溯数据契约。
---

示教采集把操作者或人体完成任务时的观测、控制意图、实际执行动作和结果记录为同一条经验。动作重定向是把原始人体或异构设备动作映射到目标机器人可执行空间；映射后的动作是派生标签，不能覆盖原始控制记录。

[Robot Data Factory](https://arxiv.org/abs/2609.16705)把机器人经验组织为可复现的任务、episode 与能力评测链；[MATE](https://arxiv.org/abs/2609.26520)展示了多操作者在共享物理环境中采集协作示教；[HIL-UMI](https://arxiv.org/abs/2609.20659)在手持 UMI 示教流上对照当前策略的预测，针对偏离状态采集数据。三者共同提示：采集时必须记录任务、操作者、控制来源与后续使用条件。

![任务规格经多源采集、时空对齐和动作重定向后，以回放验收形成可用示教。](/images/docs/demonstration-collection-retargeting-flow.svg)

## 输入、输出与处理链

输入包括任务协议、操作者或策略的原始控制流、同步视频与机器人状态；输出是保留源动作、重定向动作、实际执行动作及任务结果的 episode。采集与重定向要分阶段验收：映射后的轨迹必须能回到源观测和控制命令。

1. 确定任务与成功条件；记录机器人、工具、操作者和场景版本。
2. 同时采集原始视频、设备位姿、控制命令、机器人状态及接触/终止事件。
3. 校准人手或远程控制器到机器人基座与工具坐标系的变换，生成可执行动作。
4. 回放或实机核验映射结果，保留失败、人工接管和安全停止片段。

### 时间与空间对齐

至少区分观测采样 `t_obs`、操作者命令 `t_command` 与机器人实际生效 `t_apply`。控制端、相机和机器人时钟要有映射及误差；原动作、映射动作和控制器限幅后的动作各存一份。多人协作时还需共用任务时间轴、角色与交接事件，不能仅凭视频相邻帧推断因果。

![示教数据契约分为操作者与控制来源、原始及应用动作时间链、接管结果与血缘三组。](/images/docs/demonstration-collection-retargeting-contract.svg)

## 最小数据字段

| 字段组 | 建议字段 | 用途 |
| --- | --- | --- |
| 身份与任务 | `episode_id、task_id、success_spec、scene_version` | 重放、去重与任务分层 |
| 来源 | `operator_id、control_source、device_id、consent_scope` | 区分人类、AI 与混合控制及授权 |
| 观测 | `camera_stream、robot_state、object_state、clock_id` | 重建执行时所见状态 |
| 动作 | `raw_command、retargeted_action、applied_action、action_source` | 避免把派生动作误作原始示教 |
| 变换 | `frame_id、calibration_version、unit、retarget_map_version` | 跨设备和本体复算 |
| 结果 | `event_log、handover_interval、outcome、quality_flags` | 区分任务成败和采集质量 |

远程控制、手持 UMI 和多人协作的字段可能不同，但原始命令、目标机器人应用动作及两者的变换关系都必须可追溯。

![示教评估分别核验任务可复现性、目标本体动作可执行性和未见操作者场景的迁移表现。](/images/docs/demonstration-collection-retargeting-evaluation.svg)

## 质量控制与评估

示教质量首先看控制来源与时间链是否可复原，再看重定向动作能否在目标本体安全执行。任务成功、示教完整性和人类控制可信度应分别给出结论：

- 抽样复核视频、原命令与实际动作的时序一致性，报告端到端延迟和失帧。
- 检查重定向后的关节限位、碰撞、接触与目标物位姿；失败样本可保留为分析数据。
- 按操作者、任务、设备及场景分层检查覆盖，避免一位操作者或一种动作主导数据。
- 将控制来源作为显式标签；[Ghost-in-the-Loop](https://arxiv.org/abs/2609.06434)的初步在线研究涉及人类与 AI 控制下语音、表情、手势的来源判断，提示多通道时间协调也应单独评估。

| 评估层 | 指标或证据 | 判读要点 |
| --- | --- | --- |
| 采集完整性 | 观测/动作缺失率、时钟残差 | 缺失段与训练掩码对应 |
| 重定向可执行性 | 限位、碰撞、接触及重放结果 | 通过率按本体报告 |
| 数据迁移效果 | 目标任务成功率、未见操作者/设备表现 | 与原示教和目标部署分开 |

## 数据集使用边界

用于模仿学习时只把通过授权与质量门的实际可执行动作作为监督目标；把纯人类动作、AI 生成动作和机器人执行动作分开标注。模拟协作示教不能自动代表真实机器人协作分布，单次重定向成功也不证明跨物体、跨机器人泛化。同一原始 episode 的衍生片段应整体进入同一 split。

## 本页术语

本页使用的关键术语：

- **示教数据**：把任务观测、操作者动作、机器人执行和结果绑定的轨迹记录。
- **动作重定向**：把源本体的动作映射为目标机器人可执行动作的过程。
- **控制来源**：某时刻控制命令由人、AI 策略或安全控制器产生的标签。

## 本月相关论文

以下为该主题主归类论文，并补入与控制来源标注相关的边界论文；每条均链接原始 arXiv 页面。

- [Can People Distinguish Human and AI Agency in Humanoid Teleoperation? A Preliminary Study of Agency Perception](https://arxiv.org/abs/2609.06434)（2609.06434）
- [Understanding Whole-Body Robot Teleoperation Strategies Under Diverse Task Objectives and Constraints](https://arxiv.org/abs/2609.12384)（2609.12384）
- [Continuous Manifold-Decomposed Impedance Retargeting for Contact-Rich Imitation Learning](https://arxiv.org/abs/2609.15716)（2609.15716）
- [Bi-MoDe: Bilateral Control-based Imitation Learning via Modifier-Conditioned Decoding for Modulation of Execution Speed and Contact Intensity](https://arxiv.org/abs/2609.16040)（2609.16040）
- [MR-GLi: Mixed Reality-Based Gripper-Linked Overlays for Underwater Robot Arm Teleoperation via Bilateral Control](https://arxiv.org/abs/2609.16041)（2609.16041）
- [XRoboToolKit-T: Teleoperation with High Stability and Precision with Tactile Sensing for Contact-rich Manipulation](https://arxiv.org/abs/2609.16437)（2609.16437）
- [The Robot Data Factory](https://arxiv.org/abs/2609.16705)（2609.16705）
- [Gated Residual Body-Hand Coordination for Whole-Body Humanoid Teleoperation](https://arxiv.org/abs/2609.18763)（2609.18763）
- [HIL-UMI: Bringing Human-in-the-Loop Post-Training of Vision-Language-Action Models to Universal Manipulation Interface](https://arxiv.org/abs/2609.20659)（2609.20659）
- [MATE: Multi-Agent Virtual Teleoperation Platform for Humanoid Collaboration Data Collection](https://arxiv.org/abs/2609.26520)（2609.26520）
- [RAPID: Robot Agentic Programming from Demonstrations](https://arxiv.org/abs/2609.30249)（2609.30249）
