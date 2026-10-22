---
title: 机器人安全与鲁棒性数据
description: 将感知失误、物理风险、攻击、隐私与恢复过程整理为可审计的具身数据。
---

具身安全评价需要把“系统收到什么”“实际环境是什么”“采取了什么动作”和“产生了什么后果”分开记录。[Rethinking Safety for Generalist Robots](https://arxiv.org/abs/2609.06326)指出风险依任务情境、用户意图与物理后果而变化：同一动作在维修窗口和日常使用中可能有不同安全含义。因此数据标签不能只写一个笼统的 `safe`。

![机器人安全数据从正常任务、扰动与攻击采集到后果核验的流程](/images/docs/robot-safety-robustness-data-flow.svg)

## 风险样本如何形成

- **入口扰动**：保存用户原始语音、自动语音识别（ASR）转写、纠错结果及模型实际收到的文本。[When Robots Mishear Us](https://arxiv.org/abs/2608.28518)显示语音识别错误可能改变危险指令的接受与执行，必须把转写误差和决策错误分开归因。
- **物理与环境状态**：记录机器人、人员、物体和路径的几何位置、速度、接触及可见性；标注碰撞、近失事件、进入风险区域等事件。**近失事件**是尚未发生碰撞、但距离或预计碰撞时间已触及预设风险阈值的过程。[CorrRisk-WM](https://arxiv.org/abs/2609.16724)按候选轨迹的走廊预测侵入和近失风险，说明风险标签与具体候选动作相关，不能脱离轨迹复用。
- **攻击与供应链**：记录攻击面、触发条件、被修改的传感器流或模型版本、受害控制器以及真实执行结果。[When the World Lies](https://arxiv.org/abs/2609.15781)研究被篡改世界模型检查点如何影响下游控制；训练/评估拆分须按模型版本和触发器家族进行。
- **恢复与干预**：保存名义动作、安全滤波/残差修正、实际动作、触发阈值、人工停机及恢复状态。[ResSafe](https://arxiv.org/abs/2609.15988)以残差策略修正人形动作，[RobResilience](https://arxiv.org/abs/2609.17349)在运行时判断扰动、退化及缓解可行性；两者都要求记录介入前后，而不只看最后是否跌倒。

![安全 episode 中事实、候选动作、约束、干预和后果的字段关系](/images/docs/robot-safety-robustness-data-contract.svg)

## 最小数据契约

| 记录层 | 建议字段 | 核验问题 |
| --- | --- | --- |
| 情境 | `task_id`, `user_intent`, `scene_state`, `risk_policy_version` | 规则在何时、对谁生效 |
| 输入链 | `raw_sensor_ref`, `perceived_state`, `uncertainty`, `attack_or_noise_id` | 事实是实测还是模型推断 |
| 决策链 | `proposed_action`, `constraint_verdict`, `intervention`, `executed_action` | 谁阻止或更改了动作 |
| 后果 | `near_miss`, `collision`, `privacy_event`, `recovery`, `review_label` | 真实后果与反事实风险分离 |

[法律约束世界模型规划](https://arxiv.org/abs/2609.15113)在模拟机械臂上考察了感知错误对规范推理事实输入的影响，以及同一规范对应多种规划约束解释的差异。适用的数据做法是保留感知事实、规则版本与约束翻译，供审计复现；该研究的实验范围不应被当成通用机器人安全保证。

## 质检与评估

![安全评估按输入扰动、物理后果、模型版本和恢复能力进行分层](/images/docs/robot-safety-robustness-data-evaluation.svg)

核对时间顺序，避免把事故发生后的信息作为决策前输入；严重事件由人工复核，标明可观察证据与主观判断。分别报告危险请求拦截率、误拦截率、碰撞/近失率、干预延迟、恢复成功率，以及攻击成功率；对安全和任务完成两轴同时评估。[LIMBO](https://arxiv.org/abs/2609.22075)的障碍目标、[READ](https://arxiv.org/abs/2609.12371)的驾驶风险场都提示风险代理量应和实际事件分开保存。

测试集按场景、操作者、任务、扰动类型、攻击触发器与设备版本分组。声称鲁棒性时给出复合扰动条件；视觉编码器表征扰动 [Aether](https://arxiv.org/abs/2609.10292)、社会互动中的言语/非言语欺骗 [MineAmongUs](https://arxiv.org/abs/2608.30428)、操作代码代理的障碍约束 [Obstacle-Aware Harness](https://arxiv.org/abs/2609.20822)涉及不同风险面，不能汇成一个综合安全分数。轨迹隐私攻击 [Temporal Gradient Inversion](https://arxiv.org/abs/2609.30258)针对共享的逐步策略梯度重建私有观测与动作序列，因此共享梯度流时还应评估序列级泄露风险。

## 2026 年 10 月：硬件扰动、指令冲突与干预代价

截至 **2026-10-22**。以下增量依据本月论文，字段设计和验收步骤是本站工程建议。

### 对照实验必须保留正常运行条件

[Detect and Suppress（2610.03498）](https://arxiv.org/abs/2610.03498)研究检测到视觉攻击后才启用表征干预，并发现持续干预会损伤正常行为；[TAPDreamer（2610.06814）](https://arxiv.org/abs/2610.06814)显示共享视觉编码器的局部扰动可能影响多个下游动作模型。面向数据质量，应记录输入是否被改变、扰动位置/持续区间、检测结果、干预是否启用和最终物理后果。

建议评估四类匹配条件：干净输入且不干预、干净输入且触发干预、扰动输入且不干预、扰动输入且干预。这样能同时检查漏检、误触发和干预本身的损害。视觉上的差异大小并不能直接代表机器人动作风险；安全终点仍需来自执行日志与环境事件。

![硬件扰动、指令冲突与干预代价的数据记录与评估关系](/images/docs/robot-safety-robustness-data-october-data.svg)

### 硬件设置变化不能全归入视觉增强

[LIBERO-RIG（2610.18843）](https://arxiv.org/abs/2610.18843)保持任务固定，改变相机、标定、控制速率、本体噪声、底座与夹爪等硬件设置。某些变化不会明显改变画面，却会改变动作效果。数据需要完整的设备配置快照，而不是仅在图像上标一个“域偏移”。

对每个扰动保存原值、修改值、单位、严重度、随机种子和生效阶段；相机变换与控制频率不能压缩成一个混合分数。先逐轴配对测量，再测有实际意义的组合。数据增强覆盖相机变化，不等于覆盖控制器增益或夹爪磨损，采样计划应直接列出这些缺口。

### 无可行动作与不安全指令需要独立标签

[FAITH（2610.12432）](https://arxiv.org/abs/2610.12432)区分存在安全动作与不存在安全动作的状态。**安全可行性**指当前状态下是否存在满足给定安全条件的动作。保存策略原动作、过滤后的动作、可行性估计、预测伤害与真实后果；从不可行初态尽量减小伤害不能写成“保证零违规”。学习的安全估计也需要校准和误差审计。

[SafeDriveVLA（2610.20609）](https://arxiv.org/abs/2610.20609)将自由语言导航与场景冲突共同评估。应保存原始指令、当时道路状态、冲突类型、遵从模式和决策依据，分别判断是否正确执行合法指令、是否拒绝或调整危险指令。拒绝所有指令可能减少某些碰撞，却不能代表同时具备导航能力。

最终报告按任务成功、安全事件、误干预和恢复分别统计，注明仿真/真机、初始可行性与扰动范围。论文里的安全率仅适用于其条件，不能推广成整个数据集或系统的无条件安全证明。

### 2026 年 10 月来源与数据启示

以下说明以原始摘要为依据；具体性能数字与复现实验应继续核对论文正文。

| 论文 | 数据启示 |
| --- | --- |
| [2610.03498 · Detect and Suppress: A Mechanistic Defense against Adversarial Patches in VLA Models](https://arxiv.org/abs/2610.03498) | 机器人VLA在受污染观测下的闭环数据和正常/攻击分桶直接相关。 |
| [2610.06814 · TAPDreamer: Transferable Adversarial Patches for World Action Models](https://arxiv.org/abs/2610.06814) | 机器人世界动作模型的固定污染输入与闭环失败，适合鲁棒性数据分桶。 |
| [2610.12432 · FAITH: Feasibility-Aware Safety-Filtered RL for High-Dimensional Systems](https://arxiv.org/abs/2610.12432) | 真实人形控制的安全过滤器需要违规、回报、伤害和初始可行性标签。 |
| [2610.18843 · LIBERO-RIG: A Hardware-Setup Robustness Benchmark for Vision-Language-Action Models](https://arxiv.org/abs/2610.18843) | 系统扰动机器人硬件与安装设置，检验策略部署鲁棒性。 |
| [2610.20609 · SafeDriveVLA: Navigation-Conditioned World Model Dreaming for Conflict-Aware End-to-End Autonomous Driving](https://arxiv.org/abs/2610.20609) | 自动驾驶的语言指令与物理场景冲突属于真实行动系统安全边界。 |

## 2026 年 9 月来源

本页索引收录 2026-08-27 至 2026-09-27 发表、归入本主题的论文。

- [When Robots Mishear Us: Mapping the Safety Risks of Voice-Controlled Embodied AI](https://arxiv.org/abs/2608.28518)（2608.28518）
- [Lies We Can See: Joint Verbal and Non-Verbal Deception by VLM Agents in Embodied Social Interactions](https://arxiv.org/abs/2608.30428)（2608.30428）
- [Rethinking Safety for Generalist Robots](https://arxiv.org/abs/2609.06326)（2609.06326）
- [Isotropic Embedding Perturbations for Robust Vision Language Encoders](https://arxiv.org/abs/2609.10292)（2609.10292）
- [RobResilience: Implementing and Evaluating a Resilience Framework for Cyber-Physical Embodied Systems](https://arxiv.org/abs/2609.17349)（2609.17349）
- [CorrRisk-WM: Corridor-Conditioned Risk World Modeling for Safety-Critical Trajectory Planning](https://arxiv.org/abs/2609.16724)（2609.16724）
- [ResSafe: Learning Safety Filtering with Residual Reinforcement Learning for Humanoids](https://arxiv.org/abs/2609.15988)（2609.15988）
- [When the World Lies: Backdoor Attacks on Latent World Models for Downstream Control](https://arxiv.org/abs/2609.15781)（2609.15781）
- [Legislating World-Model-Based Planning with Legal Reasoning](https://arxiv.org/abs/2609.15113)（2609.15113）
- [READ: Learning Risk-Informed Fields for End-to-End Autonomous Driving](https://arxiv.org/abs/2609.12371)（2609.12371）
- [Coding Agents with an Obstacle-Aware Harness for Safe Robot Manipulation](https://arxiv.org/abs/2609.20822)（2609.20822）
- [LIMBO: Learning and Internalizing Model-Free Barrier Objectives for Agile and Safe Whole-Body Control](https://arxiv.org/abs/2609.22075)（2609.22075）
- [Temporal Gradient Inversion for Private Trajectory Reconstruction in Embodied Reinforcement Learning](https://arxiv.org/abs/2609.30258)（2609.30258）
