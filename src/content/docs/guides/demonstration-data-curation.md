---
title: 示教数据筛选与再利用
description: 按任务相关性、动作精度和分布差异选择异质示教数据，并保留权重和训练用途。
---

示教数据整理决定哪些现有片段值得进入下一轮训练、以何种权重进入、应只作上下文还是可作动作监督。任务成功并不保证轨迹适合某个预训练模型；来源不完美也不等于没有价值。

[DATAFARM](https://arxiv.org/abs/2609.12316)显示规划生成轨迹即使能完成任务，也需要考虑与 VLA 预训练数据在关节配置、运动风格和时序上的分布差异；[ReWeight](https://arxiv.org/abs/2609.13851)以示教检索和样本权重筛选人类数据；[Imperfection for Precision](https://arxiv.org/abs/2609.26672)区分目标任务低精度与其他任务高精度数据的作用。这些结论支持保留多维质量标签，而非一个全局“好/坏”分数。

![人类机器人规划示教经任务动作特征统一、检索筛选、用途权重分配，最后做等预算训练验证。](/images/docs/demonstration-data-curation-flow.svg)

## 输入、输出与处理链

输入是人类、机器人和规划器等异质示教及目标策略的训练需求；输出是可重算的检索结果、样本权重、训练用途和排除原因。整理过程不改变原始示教，新的选择规则只形成一个版本化数据集视图。

1. 汇集人类、机器人、规划器或历史策略示教，记录来源和任务版本。
2. 按任务语义、对象、视角、本体、精度和运动风格建立可比较特征。
3. 去重并给片段分配用途、权重或排除原因，冻结筛选规则版本。
4. 用相同训练预算做消融，核验样本选择对目标任务和未见任务的影响。

### 时间与空间对齐

检索和重加权只在可比较的时间窗口、动作单位和任务条件上进行。人类视频若无机器人动作标签，应标记为表征预训练或弱监督来源；规划动作和真实遥操作动作要保留来源。精度评价必须对照目标任务容差，不能用“轨迹平滑”代替对位误差。

![示教整理契约连接原始来源、分布与精度特征、检索权重版本和训练用途。](/images/docs/demonstration-data-curation-contract.svg)

## 最小数据字段

| 字段组 | 建议字段 | 用途 |
| --- | --- | --- |
| 身份与血缘 | `sample_id、source_episode、source_type、license` | 回溯原始数据与授权 |
| 任务与本体 | `task_id、object_id、embodiment、frame_id` | 判断可迁移性 |
| 动作质量 | `precision_error、contact_event、outcome` | 区分精度与任务结果 |
| 分布属性 | `motion_style、timing、state_features、domain_tag` | 估计目标/预训练差异 |
| 筛选结果 | `retrieval_score、sample_weight、use_mask、reason` | 复现准入与权重 |
| 评估隔离 | `split、filter_version、training_run_id` | 防止测试反馈回流 |

来源、精度和运动风格应保留为分开的属性；单个“质量分”不足以重建筛选决策或解释迁移失败。

![数据整理评估检查筛选准入、等预算目标收益和未见任务中的性能退化。](/images/docs/demonstration-data-curation-evaluation.svg)

## 质量控制与评估

筛选质量要同时看样本是否完整、筛后覆盖是否偏斜以及等预算训练收益。目标任务提升也要和未见任务退化一起报告：

- 先用原始 ID 和感知哈希去重；同一 episode 的重采样窗口保持同一 split。
- 记录缺失标签、坐标错误和动作不可执行片段，明确 `trainable`、`context_only` 与 `excluded`。
- 按来源、任务、操作者、动作精度和场景报告筛后覆盖率；避免高权重样本过于集中。
- 用“全量混合、随机等量、筛选加权”同预算对照，监测目标外任务退化。

| 评估层 | 指标或证据 | 判读要点 |
| --- | --- | --- |
| 数据覆盖 | 来源/任务/精度分布 | 筛前筛后对照 |
| 选择有效性 | 同预算训练消融 | 对照随机混合 |
| 泛化代价 | 未见任务与本体结果 | 报告退化切片 |

## 数据集使用边界

数据权重依赖当前模型和目标任务，策略更新后可能需要重算，不能写成样本永久质量分。检索表征若使用未来动作或测试任务标签，评估必须隔离；高精度异任务数据不能无条件替代目标任务数据。筛选结论与原始文件分开保存，让后续使用者能按自身目标重建数据集。

## 本页术语

本页使用的关键术语：

- **数据再利用**：把原用途之外的数据经筛选、重标或加权用于新任务。
- **分布对齐**：使训练样本在关键状态、动作和时序属性上更接近目标用途。
- **样本权重**：训练时控制一条样本贡献大小的显式数值。

## 本月相关论文

以下为该主题在 2026-08-27 至 2026-09-27 采集批次中的全部主归类论文；每条均链接原始 arXiv 页面。

- [DATAFARM: Distribution-Aligned Task and Motion Planning for Fine-Tuning Vision-Language-Action Models](https://arxiv.org/abs/2609.12316)（2609.12316）
- [ReWeight: Leveraging Human Data for VLA Post-Training via Demonstration Retrieval and Sample Weighting](https://arxiv.org/abs/2609.13851)（2609.13851）
- [In-Context Robot Learning with VLM Agents](https://arxiv.org/abs/2609.19138)（2609.19138）
- [Learning Beyond What Humans Can Demonstrate](https://arxiv.org/abs/2609.24996)（2609.24996）
- [Imperfection for Precision: Upcycling Imperfect Data for High-Precision Robotic Manipulation](https://arxiv.org/abs/2609.26672)（2609.26672）
- [TANDEM: Task and Motion Planning with As-Needed Demonstrations for Efficient Vision-Language-Action Model Fine-tuning](https://arxiv.org/abs/2609.28314)（2609.28314）
