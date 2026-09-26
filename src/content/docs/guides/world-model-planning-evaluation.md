---
title: 世界模型规划与决策评估
description: 记录候选动作、反事实预测与执行结果，评估世界模型是否真正改进决策。
---

规划中的世界模型要比较“若执行 A”和“若执行 B”的后果。事实预测误差小，并不保证动作排序正确：[D-JEPA](https://arxiv.org/abs/2609.24749)提出决策局部预测差距，[AD-WM](https://arxiv.org/abs/2609.30264)强调保留动作间可区分的信息。由此，数据集需要记录同一起点下的候选集合、预测评分、最终选择和实际执行结果，而不只记录成功轨迹。

![世界模型规划从固定状态生成候选动作到实测结果比较的闭环流程](/images/docs/world-model-planning-evaluation-flow.svg)

## 概念与数据问题

反事实预测是对未执行候选动作的后果估计；其真值通常无法在同一真实时刻全部观察，所以应把“模型预测”和“实际执行”分开存储。[When Should a World Model Move?](https://arxiv.org/abs/2609.15801)指出信息量高的预测未必带来更低损失；[Aim Short to Reach Far](https://arxiv.org/abs/2609.30036)说明只以目标图像距离评价短期结果，可能压制必须先远离目标的动作。比较协议要明确目标函数、可行约束与候选生成方式。

## 采集、处理与对齐

**采集与处理**：固定初始状态、任务目标和候选动作库；保存动作是否几何可行、预测后态、模型分数与实际选中动作。[挖掘机动作选择](https://arxiv.org/abs/2609.15382)将候选挖掘动作、几何约束及后果预测接入真机闭环；[机器人插入](https://arxiv.org/abs/2609.28258)结合本体状态与世界模型处理不同装配任务。不同机器人的坐标系、动作幅度和接触约束应保留原值与转换版本。

**规划运行**：记录每轮重规划的起点和截止时间，而非仅保存最终动作序列。[LePlanner](https://arxiv.org/abs/2609.13845)关注潜在空间中搜索成本，[Sampling-Guided Policy Search](https://arxiv.org/abs/2609.20575)讨论采样式模型预测控制（MPC）辅助视觉策略学习；[DualWAM](https://arxiv.org/abs/2609.24868)用异步全局规划与局部细化兼顾远期和反应性，[LiMA](https://arxiv.org/abs/2609.28431)面向长时想象与快速灵巧控制的时间错配。[Rolling-WAM](https://arxiv.org/abs/2609.30247)把生成过程分摊到连续重规划周期，因而推理耗时和动作年龄（从所依据的观测到命令生效的时间差）也应成为数据字段。

**反事实质量**：[LPA-CWM](https://arxiv.org/abs/2609.14073)对不同干预预测的可靠性作区别，[AD-WM](https://arxiv.org/abs/2609.30264)直接优化动作区分；评估要同时保存不确定性与排序。

![规划评估样本将同一起点、候选动作、预测后果与实测结果绑定](/images/docs/world-model-planning-evaluation-contract.svg)

## 最小字段契约

字段名是建议的数据接口，不表示所引论文使用完全相同的文件格式。

| 字段 | 记录内容 | 检查重点 |
| --- | --- | --- |
| decision_id / episode_id | 一次规划决策与所属任务 | 候选共享同一决策起点 |
| state_at / goal_id | 可复现的观测状态和目标 | 起点、目标版本固定 |
| candidate_id / action | 每个候选的动作与单位 | 可行性和边界记录完整 |
| predicted_next / score | 预测后态、收益与不确定性 | 分数方向和归一化明确 |
| selected_candidate_id | 真正执行的候选 | 与控制日志一致 |
| execution_trace / outcome | 实际轨迹、碰撞、成功与失败 | 区分预测与观测 |
| planning_latency_ms | 生成、评分、通信耗时 | 统计动作生效时的状态年龄 |
| planner_version / seed | 模型与搜索设置 | 配对比较可重现 |

## 质控与评估

离线可先检查同一起点候选的排序、可行候选召回与真实执行动作的相对后悔值；但不能把未执行候选的模拟后果当成真机真值。闭环要报告任务成功、碰撞、重规划次数、决策延迟及失败恢复，并按接触阶段和初始状态分层。[D-JEPA](https://arxiv.org/abs/2609.24749)与[AD-WM](https://arxiv.org/abs/2609.30264)直接表明排序目标与普通预测目标不同；[Aim Short to Reach Far](https://arxiv.org/abs/2609.30036)提示还需测长期目标进展。

评价实时性时，应把推理耗时与动作更新后的任务结果配对，而非只报告每秒生成数量。异步方法如[DualWAM](https://arxiv.org/abs/2609.24868)、[Rolling-WAM](https://arxiv.org/abs/2609.30247)尤其需要记录“预测所依据的状态”到“动作真正生效”的间隔。

![世界模型规划分别评估候选排序、闭环成功和实时计算成本](/images/docs/world-model-planning-evaluation-evaluation.svg)

## 数据集使用边界

模型从未执行候选中推断出的收益只是一种估计。若无法重置到相同物理起点，就不要把两个 rollout 写成严格配对实验；应报告初始状态差异。跨任务或跨本体比较须统一目标、预算、候选数量和安全约束。世界模型可帮助筛选动作，最终安全仍取决于执行时的传感反馈与独立约束。

## 本主题论文

以下论文按清单中的主主题归档。跨主题使用时，应重新核对任务、传感器和评测口径。

- [When Should a World Model Move? Loss-Conditioned State Execution](https://arxiv.org/abs/2609.15801)（2609.15801）
- [From Prediction to Decision: World-Model-Guided Action Selection for Continuous Pile Excavation](https://arxiv.org/abs/2609.15382)（2609.15382）
- [LPA-CWM: A Learned Physical Adjudicator for Motion Reasoning with Counterfactual World Models](https://arxiv.org/abs/2609.14073)（2609.14073）
- [LePlanner: An Iterative Amortized Controller For World Models](https://arxiv.org/abs/2609.13845)（2609.13845）
- [Accelerating Visual Policy Learning with Sampling-Based Model Predictive Control](https://arxiv.org/abs/2609.20575)（2609.20575）
- [DualWAM: Dual-System World Action Models for Asynchronous Global Planning and Local Refinement](https://arxiv.org/abs/2609.24868)（2609.24868）
- [D-JEPA: A Decision-Aligned Latent World Model](https://arxiv.org/abs/2609.24749)（2609.24749）
- [LiMA: Bridging Long-term Imagination to Real-time Dexterous Manipulation via Asynchronous Diffusion](https://arxiv.org/abs/2609.28431)（2609.28431）
- [Generalizable Robotic Insertion with World Models](https://arxiv.org/abs/2609.28258)（2609.28258）
- [AD-WM: Action-Discriminative World Models for Counterfactual Model Predictive Control](https://arxiv.org/abs/2609.30264)（2609.30264）
- [Rolling-WAM: World Action Models with Rolling Imagination](https://arxiv.org/abs/2609.30247)（2609.30247）
- [Aim Short to Reach Far: Your Frozen World Model Can Plan Better Than You Think](https://arxiv.org/abs/2609.30036)（2609.30036）
