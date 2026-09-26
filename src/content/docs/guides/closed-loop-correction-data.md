---
title: 闭环纠错与失败经验数据
description: 把阶段检查、失败证据、局部修正和再次执行组织为可学习的轨迹。
---

一段成功或失败的末尾标签，无法解释机器人在哪一步偏离目标。[VLA-Corrector](https://arxiv.org/abs/2609.06508)按任务阶段核验可观测状态并恢复固定 VLA 策略；[CommitFlow](https://arxiv.org/abs/2609.21908)把每阶段必须建立的物理条件称为语义承诺。数据集应记录“原本预期什么、实际观察到什么、依据什么纠错”，这样失败才可复查与再利用。

![机器人执行过程中从阶段承诺、状态观测、偏差判断到修正和经验回写的闭环](/images/docs/closed-loop-correction-data-flow.svg)

## 概念与数据问题

闭环纠错是利用执行后的新证据更新动作。局部修正只调整当前步骤，重规划则可能改变后续策略；两者都要与原计划关联。[Body-Grounded Replanning](https://arxiv.org/abs/2609.30024)把机器人自身关节负载和活动能力用于高层重规划，[残差故障适应](https://arxiv.org/abs/2609.17404)处理运行中关节指令通道故障。单靠物体视觉状态无法覆盖所有失败类型。

## 采集、处理与对齐

**采集**：保存原始指令、阶段目标、每次动作前后观测、实际动作、故障信号、人类接管和最终结果。[GRAFT](https://arxiv.org/abs/2608.27079)在有限真机交互中做在线适应，[REVOLVE](https://arxiv.org/abs/2609.14633)把失败评估、纠正和环境重置组成自动化循环；这些研究都说明失败轨迹是有效数据，而不是应删除的“脏样本”。

**标注与处理**：先标失败出现的阶段和可观察证据，再标修正策略及其影响。[TraceFlow](https://arxiv.org/abs/2609.20646)用成功和失败轨迹引导冻结的 flow-matching 策略；[Self-Adaptive VLA](https://arxiv.org/abs/2609.30092)关注部署时硬件磨损或标定偏差。对硬件变化要记录型号、标定和故障时间；对任务变化要记录指令和目标版本，避免误把环境改变标成策略错误。

![闭环纠错样本绑定预期状态、实际偏差、修正动作和复验结果](/images/docs/closed-loop-correction-data-contract.svg)

## 最小字段契约

字段名是建议的数据接口，不表示所引论文使用完全相同的文件格式。

| 字段 | 记录内容 | 检查重点 |
| --- | --- | --- |
| episode_id / stage_id | 任务和当前阶段 | 每次修正关联原任务 |
| expected_condition | 阶段应满足的物理条件 | 可由观测或传感器验证 |
| observed_state / evidence_uri | 图像、状态和故障证据 | 证据时间先于修正 |
| deviation_type / confidence | 目标错位、滑移、关节故障等 | 不确定原因可保留多标签 |
| original_action / applied_action | 计划动作与实际执行 | 区分控制器覆盖 |
| correction_type / parameters | 残差、提示、重规划或接管 | 修正版本和幅度可追溯 |
| recheck_condition / outcome | 复验结果与最终结果 | 局部恢复不等于任务成功 |
| robot_health / calibration_id | 负载、故障和标定状态 | 硬件偏移可归因 |

## 质控与评估

失败检测应按阶段类型、扰动强度和可观测性评估漏报与误报；恢复则统计修正后的成功、额外动作、时间和安全事件。[CommitFlow](https://arxiv.org/abs/2609.21908)强调每步物理承诺需要复验，[VLA-Corrector](https://arxiv.org/abs/2609.06508)强调阶段感知，[TraceFlow](https://arxiv.org/abs/2609.20646)强调失败经验回用。比较策略时保留相同初始条件和扰动协议，不要只挑容易恢复的案例。

![闭环系统的失败发现、恢复和跨场景经验复用三层评估](/images/docs/closed-loop-correction-data-evaluation.svg)

## 数据集使用边界

训练数据里可能同时有自然失败和人为注入扰动，二者分布不同，应单独标记。修正策略在新硬件或新场景上可能放大错误；应设独立安全停止条件。失败原因若不可直接观测，标签应写成“怀疑的机制”并附证据，而非伪造确定诊断。

## 本主题论文

以下论文按清单中的主主题归档。跨主题使用时，应重新核对任务、传感器和评测口径。

- [GRAFT: Grounded and Efficient Online Reinforcement Adaptation for Fine-Grained Robot Manipulation](https://arxiv.org/abs/2608.27079)（2608.27079）
- [VLA-Corrector: Stage-Aware Observable State Understanding for Prompt-Based Closed-Loop Recovery of Vision-Language-Action Policies](https://arxiv.org/abs/2609.06508)（2609.06508）
- [Residual Fault Adaptation for Dexterous In-Hand Manipulation Under Runtime Joint Faults](https://arxiv.org/abs/2609.17404)（2609.17404）
- [REVOLVE: An Automated Closed-Loop Framework for Evolving Robot Manipulation with Minimal Human Intervention](https://arxiv.org/abs/2609.14633)（2609.14633）
- [TraceFlow: Guiding Frozen Flow-Matching Robot Policies with Success and Failure Traces](https://arxiv.org/abs/2609.20646)（2609.20646）
- [CommitFlow: Semantic Commitment Verification and Local Correction for Long-Horizon Robot Manipulation VLA Execution](https://arxiv.org/abs/2609.21908)（2609.21908）
- [Self-Adaptive VLA for Robust Robot Deployment](https://arxiv.org/abs/2609.30092)（2609.30092）
- [Body-Grounded Replanning for Physically Adaptive Manipulation](https://arxiv.org/abs/2609.30024)（2609.30024）
