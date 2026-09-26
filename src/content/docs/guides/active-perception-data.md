---
title: 主动感知与任务化测量数据
description: 将观测动作、可见性变化、测量证据和任务决策组织为可审计的主动感知数据。
---

主动感知指机器人通过移动视角、接触或施加受控动作来获取任务所需信息。数据记录不能只保存最终测量值，还需记录为何选择该观测动作、测量前后的不确定性，以及该证据是否满足任务要求。

[FRAME](https://arxiv.org/abs/2609.14219)把检验要求转成可追溯的计量证据，明确覆盖与准入检查；[MAAP](https://arxiv.org/abs/2609.21929)利用多机械臂腕部相机在协作操作时形成移动视角；[Before the Tipping Point](https://arxiv.org/abs/2609.12894)通过受控推拉和力—角度观测估计未知物体的质量与质心。这些案例分别以视觉或接触动作换取信息。

![检验要求驱动机器人选择视角或接触探测，再采集动作前后证据、审计覆盖并决定结论或补测。](/images/docs/active-perception-data-flow.svg)

## 输入、输出与处理链

输入是待测属性、当前证据缺口、传感器标定和允许的探测动作；输出是“探测动作—新增观测—属性估计—证据准入”链及补测决策。每次主动移动视角或接触物体都会改变后续采样条件，因此动作前后观测必须成对记录。

1. 定义待判定属性及允许的测量方式、参考标准和安全边界。
2. 记录当前不确定性，选择相机视角、机械臂位姿或接触探测动作。
3. 采集动作前后观测及执行状态，保留测量设备标定和原始证据。
4. 按覆盖和误差标准判断证据是否足够，再输出结论或请求补测。

### 时间与空间对齐

每条测量应连接 `query_id`、`probe_action_id` 与产生的 `observation_id`，并记录动作实际生效及测量采样时间。多视角需保留相机位姿，力控测量需保留接触点、力矩传感器坐标、推拉方向和安全阈值。主动改变场景后，前后状态不能当作同一个静态样本。

![主动感知契约记录属性规格、计划与实际探测动作、测量时钟标定和证据准入理由。](/images/docs/active-perception-data-contract.svg)

## 最小数据字段

| 字段组 | 建议字段 | 用途 |
| --- | --- | --- |
| 测量目标 | `task_id、property_id、spec_limit、evidence_rule` | 定义什么算充分证据 |
| 探测动作 | `probe_action、role、planned_view/contact` | 重建采样决策 |
| 实际执行 | `applied_action、t_apply、robot_pose、safety_event` | 区别计划与事实 |
| 原始证据 | `image/force/angle、t_sample、sensor_calib` | 复算属性估计 |
| 覆盖与估计 | `coverage_map、estimate、uncertainty` | 决定是否补测 |
| 准入 | `admissible_flag、reason、reviewer、split` | 支持审计与评估隔离 |

测量结论必须指向实际探测动作和原始传感器证据；仅有模型估计而无标定或覆盖记录时，不应写成已通过检验。

![主动感知评估分别观察视角覆盖增益、参考测量误差与证据不足时的决策结果。](/images/docs/active-perception-data-evaluation.svg)

## 质量控制与评估

主动感知的关键不是取得一个数值，而是判断证据是否覆盖了任务要求且测量过程安全。准入审核要区分未观测、证据不足和测得不合格：

- 先验证标定、观测范围和动作实际到位，再接受测量值。
- 报告视角覆盖、遮挡与重复测量一致性；接触测量检查是否越过安全阈值。
- 把“未能测到”“证据不足”“测得不合格”分成不同状态，不自动归为通过。
- 抽样人工复核测量证据与最终结论，尤其检查假接受与边界附近样本。

| 评估层 | 指标或证据 | 判读要点 |
| --- | --- | --- |
| 信息增益 | 不确定性下降/覆盖提升 | 与固定视角对照 |
| 测量质量 | 参考误差与重复性 | 标定和安全分桶 |
| 任务决策 | 误判/漏判及采样成本 | 不足证据不得通过 |

## 数据集使用边界

这类数据适合训练视角选择、操作中感知和测量策略。信息增益高不表示测量具有计量可追溯性；视觉估计也不能自动替代独立标定的仪器结果。安全阈值和允许探测动作必须随物体、场景及设备版本保存，不能从一个实验直接迁到所有对象。

## 本页术语

本页使用的关键术语：

- **主动感知**：通过改变视角或与环境交互，主动获取任务所需信息。
- **证据准入**：按预定规则决定观测能否支持某个任务结论。
- **信息增益**：一次观测使目标属性的不确定性减少的程度。

## 本月相关论文

以下为该主题在 2026-08-27 至 2026-09-27 采集批次中的全部主归类论文；每条均链接原始 arXiv 页面。

- [Active sensing to characterize the heterogeneity of plant stress](https://arxiv.org/abs/2608.27088)（2608.27088）
- [Before the Tipping Point: Force-Guided Active Perception for Shape-Agnostic Estimation of 3D Centers of Mass](https://arxiv.org/abs/2609.12894)（2609.12894）
- [Task-Specified Active Metrological Inspection with Measurement-Steered VLA Manipulation and Deterministic Evidence Gating](https://arxiv.org/abs/2609.14219)（2609.14219）
- [Optimal Excitation Trajectories for System Identification of Underwater Vehicles](https://arxiv.org/abs/2609.16786)（2609.16786）
- [MAAP: Multi-Agent Active Perception for Collaborative Manipulation](https://arxiv.org/abs/2609.21929)（2609.21929）
