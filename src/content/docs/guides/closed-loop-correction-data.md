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

## 2026 年 10 月：纠错对象从动作扩展到执行系统

截至 **2026-10-22**。以下增量依据本月论文，字段设计和验收步骤是本站工程建议。

### 区分证据缺失、证据误用与动作质量

[RPG（2610.02204）](https://arxiv.org/abs/2610.02204)从离线示教重建练习任务，用执行反馈修订符号技能和系统提示；[EnactOpt（2610.14977）](https://arxiv.org/abs/2610.14977)进一步联合修改上下文构建代码与文本技能。这里的**执行框架（harness）**指组织观测、调用技能并回收反馈的模型外围程序。权重不变并不意味着系统版本没有变化。

诊断时应保存某次决策实际送入模型的输入，而不只是完整传感器日志。门把手在原始图像里，却被裁剪过程删掉，属于证据未进入输入；它已经出现在输入里但未被动作使用，是另一种失败。数据中将两者混在“抓取失败”下，会让后续修正无法归因。建议绑定 `input_snapshot_id`、`context_builder_version`、`skill_library_version`、`decision_id` 与动作后的状态证据。

![纠错对象从动作扩展到执行系统的数据记录与评估关系](/images/docs/closed-loop-correction-data-october-data.svg)

### 失败视频与失败动作采用不同准入规则

[LoopWAM（2610.18873）](https://arxiv.org/abs/2610.18873)保留不同质量 rollout 的视频监督，并通过质量引导及加权控制动作模仿。失败中物体如何滑落，仍是有价值的动作后果；直接模仿导致滑落的动作，则可能重复错误。可把一段记录拆成 `world_supervision_eligible` 与 `action_imitation_weight` 两项，而不是整段简单保留或删除。质量标注还要保存产生它的规则和审核版本。

这些字段是本站的落地建议，不是三篇论文的统一格式。质量可按阶段变化：一段最终失败的轨迹，前半段可能已经可靠完成开门。保留阶段边界、失败发生点和接管前后片段，能支持局部再利用。

### 修订必须经过留出任务复验

为每次候选修订保存父版本、修改范围、用于诊断的 episode、验证任务和保留/拒绝结论。先测单个改动，再测合并后的技能库，避免两个各自有效的修订互相冲突。训练数据与候选选择数据也应分开：已经反复用于筛选提示的任务不能再作为未见任务成绩。

本文区分三种产物：模型权重更新、技能/提示更新、数据重加权。比较时分别固定另两项，并报告新增交互量、恢复成功和原有任务回退情况。仿真中的特权状态可辅助诊断，但部署输入只能使用真机能够获得的信息。

### 2026 年 10 月来源与数据启示

以下说明以原始摘要为依据；具体性能数字与复现实验应继续核对论文正文。

| 论文 | 数据启示 |
| --- | --- |
| [2610.02204 · Reconstruct, Practice, Go Real: Guided Self-Improvement for Embodied Agents](https://arxiv.org/abs/2610.02204) | 从离线轨迹重建任务，使用执行反馈检验修订并迁移实机。 |
| [2610.14977 · EnactOpt: Diagnosis-Guided Harness Evolution for Embodied Agents](https://arxiv.org/abs/2610.14977) | 将实际模型输入、动作、反馈及验证保留记录用于具身执行改进。 |
| [2610.18873 · LoopWAM: Closed-Loop Generalist Policy Improvement from Deployment Rollouts](https://arxiv.org/abs/2610.18873) | 从自身和其他部署策略的成功、次优、失败 rollout 中闭环更新通用机器人策略。 |

## 2026 年 9 月来源

以下论文按清单中的主主题归档。跨主题使用时，应重新核对任务、传感器和评测口径。

- [GRAFT: Grounded and Efficient Online Reinforcement Adaptation for Fine-Grained Robot Manipulation](https://arxiv.org/abs/2608.27079)（2608.27079）
- [VLA-Corrector: Stage-Aware Observable State Understanding for Prompt-Based Closed-Loop Recovery of Vision-Language-Action Policies](https://arxiv.org/abs/2609.06508)（2609.06508）
- [Residual Fault Adaptation for Dexterous In-Hand Manipulation Under Runtime Joint Faults](https://arxiv.org/abs/2609.17404)（2609.17404）
- [REVOLVE: An Automated Closed-Loop Framework for Evolving Robot Manipulation with Minimal Human Intervention](https://arxiv.org/abs/2609.14633)（2609.14633）
- [TraceFlow: Guiding Frozen Flow-Matching Robot Policies with Success and Failure Traces](https://arxiv.org/abs/2609.20646)（2609.20646）
- [CommitFlow: Semantic Commitment Verification and Local Correction for Long-Horizon Robot Manipulation VLA Execution](https://arxiv.org/abs/2609.21908)（2609.21908）
- [Self-Adaptive VLA for Robust Robot Deployment](https://arxiv.org/abs/2609.30092)（2609.30092）
- [Body-Grounded Replanning for Physically Adaptive Manipulation](https://arxiv.org/abs/2609.30024)（2609.30024）
