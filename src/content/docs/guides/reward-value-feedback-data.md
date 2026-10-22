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

## 2026 年 10 月：奖励程序、适配接口与信用归因

截至 **2026-10-22**。以下增量依据本月论文，字段设计和验收步骤是本站工程建议。

### 奖励规则本身也需要数据血缘

[InterEvolve（2610.02196）](https://arxiv.org/abs/2610.02196)将任务表示为带完成条件和可调参数的分阶段奖励程序，通过执行反馈修订程序并验证候选。**奖励程序**不仅是一个标量函数，还包含阶段切换及其触发条件。交付数据时保留程序版本、常量、阶段标签、候选验证场景和保留理由，否则同一轨迹在不同版本下的回报不可比较。

[AtomicRL（2610.30097）](https://arxiv.org/abs/2610.30097)以原子子任务结构控制失败的信用传播，并将探索集中到瓶颈阶段。**信用分配**指把最终结果归因于此前哪些动作或阶段。建议保存原子任务边界、完成/失败证据、跨阶段回报连接规则及采样权重。不能仅根据最终失败，把已经完成的前置技能全部标成负样本。

![奖励程序、适配接口与信用归因的数据记录与评估关系](/images/docs/reward-value-feedback-data-october-data.svg)

### 不同适配位置要求不同日志

[SQAM（2610.10437）](https://arxiv.org/abs/2610.10437)研究价值信号如何作用于流策略；[NSL（2610.13943）](https://arxiv.org/abs/2610.13943)固定预训练 VLA、学习条件噪声分布；[CFG-Policy（2610.14936）](https://arxiv.org/abs/2610.14936)组合两个生成分支以管理探索和利用；[InsQL（2610.14941）](https://arxiv.org/abs/2610.14941)关注单步动作生成及价值引导候选选择。这些方法都用到回报，但更新的部件、采样过程和计算成本不同。

建议显式记录 `adaptation_target`、基础策略/可训练分支版本、噪声种子、引导强度、候选数量和执行动作。对生成后未执行的候选，只能保留预测价值，不能复制已执行动作的回报。比较效率时固定交互预算，再分别报告训练计算和推理延迟；减少生成步数不自动保证数据利用效率更高。

### 人类反馈与在线价值缓存保持时间一致

[HiRe-MoMa（2610.20607）](https://arxiv.org/abs/2610.20607)把移动底盘与机械臂残差分层，并利用稀疏人工干预调整价值；[VaM（2610.22368）](https://arxiv.org/abs/2610.22368)将近期价值预测作为进度记忆，结合示教、干预和自主 rollout 在线更新。前者要求分别记录基础动作、底盘残差和机械臂残差，后者则需要保存价值缓存的产生时间及评估器版本。

在线训练时，新旧策略并行采集的数据可能混在同一缓冲区。每段样本绑定采集策略、入池时间和用于更新的轮次，才能检查反馈新鲜度。价值缓存是模型估计，不是任务进度真值；应以独立阶段标签核对。评估既报告任务成功，也检查原技能保持、失败覆盖及同预算下的改进，避免奖励上升却掩盖行为范围收缩。

### 2026 年 10 月来源与数据启示

以下说明以原始摘要为依据；具体性能数字与复现实验应继续核对论文正文。

| 论文 | 数据启示 |
| --- | --- |
| [2610.02196 · InterEvolve: Test-Time Evolution of Reward Programs for Humanoid Loco-Manipulation](https://arxiv.org/abs/2610.02196) | 真实人形机器人任务将奖励结构、完成条件、候选验证和执行反馈结合。 |
| [2610.10437 · Q-Learning with Scalar Adjoint Matching](https://arxiv.org/abs/2610.10437) | 包含真实双臂机器人后训练，涉及示教与价值监督的分布差异。 |
| [2610.13943 · Noise Space Learning for VLA Adaptation](https://arxiv.org/abs/2610.13943) | 真实机器人采用不同在线/离线RL方式，需记录交互预算、安全约束和回报证据。 |
| [2610.14936 · CFG-Policy: Unified Diffusion Policy Learning Framework via Classifier-free Guidance](https://arxiv.org/abs/2610.14936) | 包含机器人仿真操作，讨论后训练行为多样性与在线/离线经验使用。 |
| [2610.14941 · Compositional Average Velocity Modeling for Efficient Diffusion Offline Reinforcement Learning](https://arxiv.org/abs/2610.14941) | 包含真实机器人任务，涉及历史轨迹价值估计和单步策略的资源对照。 |
| [2610.20607 · Hierarchical Residual Policy Learning for Real-World Mobile Manipulation with Sparse Human Guidance](https://arxiv.org/abs/2610.20607) | 以稀疏人工干预指导真实移动操作的在线残差更新。 |
| [2610.22368 · Value as Memory: Online Value-Guided Post-training for General Robot Policies](https://arxiv.org/abs/2610.22368) | 结合离线示教、干预和在线 rollout，以价值缓存推动真实机器人持续学习。 |
| [2610.30097 · AtomicRL: Atomic Reinforcement Learning for Long-Horizon Robotic Manipulation](https://arxiv.org/abs/2610.30097) | 使用原子子任务边界与掌握程度改进机器人长任务奖励分配和采样。 |

## 2026 年 9 月来源

本页索引收录 2026-08-27 至 2026-09-27 发表、归入本主题的论文。

- [Autonomously Acquiring Robot Manipulation Skills with Language-Driven Quality-Diversity](https://arxiv.org/abs/2608.30983)（2608.30983）
- [Intrinsic Robot Rewarding: Reusing VLA Representations for Autonomous Evaluation and Policy Improvement](https://arxiv.org/abs/2609.17115)（2609.17115）
- [Steering Generative Robot Policies with Lexicographic Preferences](https://arxiv.org/abs/2609.15014)（2609.15014）
- [Real-World Reinforcement Learning with MPC Scaffolding for Dexterous Manipulation](https://arxiv.org/abs/2609.14878)（2609.14878）
- [VGFM: Expressive Robot Policies via Dense Value Guidance in Flow Matching](https://arxiv.org/abs/2609.14261)（2609.14261）
- [SCQ: Stabilizing Conservative Q-Learning with Sigmoid-Bounded Entropy](https://arxiv.org/abs/2609.12749)（2609.12749）
- [SeeQ: Training Generalist Value Functions for Long-Horizon Robotic Manipulation](https://arxiv.org/abs/2609.22085)（2609.22085）
- [Res-HIL: Human-Guided Residual Reinforcement Learning for Sample-Efficient Dexterous Manipulation](https://arxiv.org/abs/2609.30023)（2609.30023）
