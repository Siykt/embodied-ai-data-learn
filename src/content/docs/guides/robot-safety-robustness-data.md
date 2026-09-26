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

## 本月论文索引

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
