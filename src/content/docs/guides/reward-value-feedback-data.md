---
title: 奖励、价值函数与反馈数据
description: 组织示教、在线交互、奖励证据、子任务价值及人工干预，用于可追溯的策略改进。
---

奖励是对某个状态或转移的评价信号，价值函数估计未来可得到的回报；其中 **Q 值**估计从某个状态采取某个动作后可得到的累计回报。二者都依赖清楚的任务边界和数据来源。若只保存一个标量 `reward`，后续很难查明它来自传感器、视觉相似度、人工介入还是模型估计。[Intrinsic Robot Rewarding](https://arxiv.org/abs/2609.17115)提出复用 VLA 的视觉表征和成功演示终点来给新结果评分；这种分数应标注为“模型评估”，与实测成功判定分开。

![奖励数据从示教、控制器先验和在线交互汇入反馈与策略更新的流程](/images/docs/reward-value-feedback-data-flow.svg)

## 采集与对齐

- **离线起点**：保存成功、失败、次优示教及采集策略；给每个 episode 记录奖励规则版本、终止原因与任务阶段。[SeeQ](https://arxiv.org/abs/2609.22085)利用离线机器人数据中的子任务标注学习当前阶段的 Q 值，说明“打开抽屉”的中间步骤应在时间轴上有明确起止，而非仅在整段末尾给成功标签。
- **在线交互**：逐步记录行为策略版本、候选动作、实际动作、环境反馈和回放池来源。[真实机器人 MPC 辅助强化学习](https://arxiv.org/abs/2609.14878)先用模型预测控制（MPC）轨迹初始化，再把新的物理交互加入学习；应能区分 MPC 引导样本与纯策略样本。
- **人类反馈**：标注何时接管、纠正了哪个动作、接管前的失败线索和接管后的结果。[Res-HIL](https://arxiv.org/abs/2609.30023)把人工干预同时用于残差监督与先前行为的奖励塑形，因而一个干预事件需要明确作用的时间范围。

![奖励与价值样本中信号来源、奖励规则版本和人工反馈的字段契约](/images/docs/reward-value-feedback-data-contract.svg)

## 最小数据契约

| 单位 | 建议字段 | 解释 |
| --- | --- | --- |
| Episode | `task_id`, `subtask_spans`, `behavior_policy_id`, `dataset_origin` | 训练来源与阶段边界 |
| Transition | `observation`, `proposed_action`, `executed_action`, `next_observation`, `terminal`, `timeout` | 终止与截断分开 |
| 反馈 | `reward_value`, `reward_source`, `reward_model_version`, `human_intervention`, `feedback_scope` | 直接观测、推断和人工给分分开 |
| 价值估计 | `q_estimate`, `candidate_action_id`, `critic_version`, `uncertainty` | 估计值不是环境真值 |

## 质检与评估

![奖励数据按信号来源、分布变化、子任务与在线安全进行评估](/images/docs/reward-value-feedback-data-evaluation.svg)

重点检查奖励是否使用了未来信息、视觉奖励的参考图是否与测试场景泄漏、不同版本规则是否混用，以及干预样本是否存在选择偏差。**词典序偏好**是先满足高优先级目标，再在其可行范围内考虑低优先级目标。对[词典序偏好引导](https://arxiv.org/abs/2609.15014)，必须保存各级约束和候选轨迹的逐级筛选结果；不宜把多级目标直接压成一个未说明权重的总分。[VGFM](https://arxiv.org/abs/2609.14261)对生成动作的中间流步骤施加价值指导，记录每一步的候选动作和评分版本有助于重现策略改进。

评估按离线、离线转在线、纯在线分别报告成功率、学习曲线、物理交互量、失败/保护停机次数与跨任务泛化。对单示教设置必须说明其来源、是否包含额外回放数据、评估时是否继续交互；[SCQ](https://arxiv.org/abs/2609.12749)在单示教和常规数据集设置中研究离线转在线价值估计稳定性，这两种设置不应合并比较。语言驱动的质量多样性搜索 [Autonomously Acquiring Robot Manipulation Skills](https://arxiv.org/abs/2608.30983)还要保存行为描述符、质量指标及生成的技能库覆盖范围，不能只挑最高分轨迹。

## 本月论文索引

本页索引收录 2026-08-27 至 2026-09-27 发表、归入本主题的论文。

- [Autonomously Acquiring Robot Manipulation Skills with Language-Driven Quality-Diversity](https://arxiv.org/abs/2608.30983)（2608.30983）
- [Intrinsic Robot Rewarding: Reusing VLA Representations for Autonomous Evaluation and Policy Improvement](https://arxiv.org/abs/2609.17115)（2609.17115）
- [Steering Generative Robot Policies with Lexicographic Preferences](https://arxiv.org/abs/2609.15014)（2609.15014）
- [Real-World Reinforcement Learning with MPC Scaffolding for Dexterous Manipulation](https://arxiv.org/abs/2609.14878)（2609.14878）
- [VGFM: Expressive Robot Policies via Dense Value Guidance in Flow Matching](https://arxiv.org/abs/2609.14261)（2609.14261）
- [SCQ: Stabilizing Conservative Q-Learning with Sigmoid-Bounded Entropy](https://arxiv.org/abs/2609.12749)（2609.12749）
- [SeeQ: Training Generalist Value Functions for Long-Horizon Robotic Manipulation](https://arxiv.org/abs/2609.22085)（2609.22085）
- [Res-HIL: Human-Guided Residual Reinforcement Learning for Sample-Efficient Dexterous Manipulation](https://arxiv.org/abs/2609.30023)（2609.30023）
