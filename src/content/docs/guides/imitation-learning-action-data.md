---
title: 模仿学习动作数据与轨迹表示
description: 将示教动作编码成频率、几何和连续性明确的训练目标，并评估生成动作的可执行性。
---

模仿学习利用示教中的观测—动作配对训练策略。动作数据不仅是数值数组，还包含位置、姿态、关节和频率等结构；表示选错会使模型产生不连续、不可执行或与任务节奏不符的轨迹。

[FreqFM](https://arxiv.org/abs/2609.10405)显式处理动作轨迹不同频率成分；[LieSpline-DP](https://arxiv.org/abs/2609.15162)以 SE(3) 上的样条描述末端轨迹并关注相邻动作块的连续性；[Riemannian MeanFlow Policy](https://arxiv.org/abs/2609.30127)在动作流形上生成序列并研究采样成本。它们指向同一数据要求：训练样本需保留动作的时间、坐标和几何约束。

![原始示教经观测动作时序配对，再编码为频域样条或流形表示，训练后验证闭环连续性。](/images/docs/imitation-learning-action-data-flow.svg)

## 输入、输出与处理链

输入是带任务条件的观测、原始控制命令及实际执行轨迹；输出是时间配对的动作监督、可复算的频域或几何派生表示及闭环评估记录。不同动作空间必须保留单位、坐标与控制频率，才能比较生成轨迹和真实示教。

1. 定义动作空间：关节、末端位姿、夹爪、速度或力，并锁定单位和控制频率。
2. 把观测与实际执行动作配对，切分动作窗口且保留跨窗口上下文。
3. 按策略需要生成频域、样条或流形派生表示，但原始轨迹保持不可变。
4. 在离线重建、仿真闭环和真实闭环中分别检验平滑性、延迟与任务成功。

### 时间与空间对齐

训练样本必须区分 `t_obs`、`t_plan` 与 `t_apply`，不能把未来已执行动作误配到当前观测。旋转应标注表示方式、坐标系及单位，末端位姿转换到 `SE(3)` 时保留原始控制命令。动作块边界需要前后窗口的重叠与连续性记录；频域变换保存窗口长度和采样率，才能复现原轨迹。

![模仿学习动作契约记录动作空间坐标与频率、动作窗口及转换版本、实际执行和质量掩码。](/images/docs/imitation-learning-action-data-contract.svg)

## 最小数据字段

| 字段组 | 建议字段 | 用途 |
| --- | --- | --- |
| 序列身份 | `episode_id、step_id、task_id、policy_source` | 追踪示教及任务 |
| 观测时序 | `t_obs、sensor_stream、latency` | 绑定策略可见输入 |
| 动作 | `raw_action、applied_action、action_space、unit` | 区分命令与实际生效 |
| 几何 | `frame_id、rotation_repr、joint_limits` | 保障姿态与约束 |
| 窗口表示 | `chunk_start/end、overlap、sampling_rate、transform_version` | 复原频率/样条目标 |
| 结果 | `outcome、jerk、constraint_violation、quality_mask` | 训练筛选与评估 |

原始动作、应用动作和派生动作表示应并存；只有保存窗口、采样率和转换版本，才能复算频域或样条目标。

![动作数据评估分别检查重建误差、动作块边界平滑性以及目标控制频率下的真实成功。](/images/docs/imitation-learning-action-data-evaluation.svg)

## 质量控制与评估

动作数据先查观测与执行的因果配对，再查轨迹在块内、块间及机器人约束下的连续性。离线拟合、实时采样代价与真实任务表现分别评价：

- 查动作幅值、速度、加速度和关节限制；位姿表示转换后做往返误差检查。
- 在动作块接缝测位置、速度和加速度连续性，勿只看每块内部平滑。
- 用不同频段检查高频接触修正是否被过滤，也检查低频目标运动是否漂移。
- 按任务、物体和控制频率分层报告离线误差与真实成功，避免只凭单步预测误差宣布有效。

| 评估层 | 指标或证据 | 判读要点 |
| --- | --- | --- |
| 数据重建 | 轨迹重建与频段误差 | 保留采样率 |
| 执行质量 | jerk、限位、块边界 | 与控制器约束比对 |
| 任务闭环 | 成功率/时长/延迟 | 真实与仿真分开 |

## 数据集使用边界

频域、样条和流形表示是不同策略的训练目标，不能在数据集里混成同一个无元数据的 `action` 字段。低离线误差不保证闭环成功；特别是接触丰富任务，应保留原始高频修正并评估实际控制频率。模型推理成本也必须和采样方式一起报告。

## 本页术语

本页使用的关键术语：

- **动作块**：策略一次生成、随后逐步执行的一段动作序列。
- **SE(3)**：同时表示三维平移和旋转的刚体位姿空间。
- **轨迹连续性**：相邻时间或动作块在位置、速度等量上的衔接程度。

## 本月相关论文

以下为该主题在 2026-08-27 至 2026-09-27 采集批次中的全部主归类论文；每条均链接原始 arXiv 页面。

- [Frequency-Conditioned Flow Matching for Vision-Language-Action Models](https://arxiv.org/abs/2609.10405)（2609.10405）
- [LieSpline-DP: Lie-Group B-Spline Diffusion Policy for Smooth Robot Manipulation](https://arxiv.org/abs/2609.15162)（2609.15162）
- [Flow-Matched Motion Priors: Online Optimal-Transport Rewards for Imitation Learning](https://arxiv.org/abs/2609.15631)（2609.15631）
- [Faster Visuomotor Policy Learning on Action Manifolds via Riemannian MeanFlow](https://arxiv.org/abs/2609.30127)（2609.30127）
