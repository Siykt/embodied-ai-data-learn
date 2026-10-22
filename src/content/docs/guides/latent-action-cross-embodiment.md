---
title: 潜在动作与跨本体对齐
description: 从无动作标签视频提取几何运动表征，并将异构人手与机器人动作连接到可执行监督。
---

潜在动作是从相邻观测或视频片段中学习到的变化表征，不直接等同于机器人关节命令。跨本体对齐要让不同手、夹爪或机器人在共享任务效果上可比较，同时保留各自的动作限制和几何细节。

[GeoLAM](https://arxiv.org/abs/2609.17099)从无动作标签的人类视频中用几何教师保留三维位移与表面方向变化；[GALA](https://arxiv.org/abs/2609.21948)结合视觉和末端几何运动以改进跨本体预训练；[SkelWAM](https://arxiv.org/abs/2609.21983)使用显式骨架与工具中心点状态连接不同本体，再由本体专属解码器输出控制。

![异构人类机器人视频经几何运动估计形成共享潜在动作，再由目标本体解码并执行验证。](/images/docs/latent-action-cross-embodiment-flow.svg)

## 输入、输出与处理链

输入是人体与不同机器人本体的视频片段，以及少量带真实动作的机器人轨迹；输出包括可比较的几何潜在动作、目标本体解码结果和闭环效果。无动作标签视频可以提供状态变化监督，但目标机器人的控制命令仍需独立学习和验证。

1. 采集人类与机器人视频，保留本体型号、相机、任务及动作标签可用性。
2. 估计几何运动、可见性与置信度，从无标签视频学习连续潜在动作。
3. 用工具位姿、末端几何或任务效果对齐不同本体，保存映射与解码版本。
4. 在目标机器人上验证动作可执行与任务效果，而非只看表征相似。

### 时间与空间对齐

视频窗口需要固定 `t_start/t_end`，并明确潜在动作描述的是该窗口的状态变化还是下一步动作。跨本体数据至少统一任务、工具中心点坐标、单位与动作方向；手指级几何应保留，不能全部压成一个夹爪开合量。无标签视频中的相机运动、遮挡和非操作物体变化要作为潜在混杂因素。

![跨本体数据契约包含视频窗口与本体来源、几何潜在编码及其版本、目标控制和结果。](/images/docs/latent-action-cross-embodiment-contract.svg)

## 最小数据字段

| 字段组 | 建议字段 | 用途 |
| --- | --- | --- |
| 样本来源 | `clip_id、task_id、embodiment_id、label_available` | 区分人类/机器人与监督形式 |
| 窗口 | `t_start、t_end、camera_motion、visibility` | 限定状态变化区间 |
| 几何变化 | `point_motion、tcp_pose、finger_geometry、confidence` | 保留动作相关物理变化 |
| 潜在动作 | `latent_code、encoder_version、normalization` | 可重算共享表征 |
| 目标控制 | `decoder_version、joint_action、constraint_status` | 连接真实机器人执行 |
| 结果 | `effect_label、success、domain_split、qc_flags` | 评估迁移而非仅重建 |

潜在编码、工具位姿和关节控制是三个层次；要保留各层转换版本，避免共享表征被误当成直接可执行动作。

![潜在动作评估分别检查跨本体检索、手指工具运动保真度与目标机器人的闭环成功。](/images/docs/latent-action-cross-embodiment-evaluation.svg)

## 质量控制与评估

核验潜在动作时，应先排除相机运动与遮挡造成的伪变化，再检验细粒度末端几何是否保留，最后测试目标本体解码与执行：

- 使用静态背景或相机运动估计区分相机平移与真实操作运动；低可见性片段降权。
- 检查共享表示是否保留抓取姿态、工具方向与手指接触等任务细节。
- 对未见本体、未见物体分别报告检索、动作解码和闭环成功率。
- 保留训练时几何教师与部署时输入的区别，避免评估阶段引入未来帧或训练专用真值。

| 评估层 | 指标或证据 | 判读要点 |
| --- | --- | --- |
| 表征 | 运动探针/跨本体检索 | 任务和本体分桶 |
| 解码 | 目标动作可执行率 | 限位与坐标核验 |
| 迁移 | 目标机器人闭环成功 | 无目标示教单列 |

## 数据集使用边界

潜在动作可将大量人类视频纳入预训练，但不能由视频变化唯一恢复真实施力或关节控制。跨本体相似只说明共享表示可能有用；最终监督仍需目标本体解码和闭环验证。源/目标本体、原视频及其派生窗口应按血缘隔离，防止评估泄漏。

## 本页术语

本页使用的关键术语：

- **潜在动作**：从状态变化学习的动作相关编码，而非直接可执行命令。
- **跨本体对齐**：把不同机器人或人体动作映射到可比较的共享表示。
- **工具中心点**：机器人末端工具上用于定义位姿与动作的参考点。

## 2026 年 10 月进展：区分视觉变化、共享动作语义与目标本体执行

### 人类视频中的运动不全部来自操作

[WING](https://arxiv.org/abs/2610.03607)把观察者自运动和手—物交互分开，再利用变化较慢的时间结构对齐人类视频与机器人行为。数据侧应保留相机运动估计、交互区域、原始帧间隔及频域处理版本。频域动作对齐指比较运动信号在不同变化速度上的组成；它帮助处理节奏差异，但低频相似不意味着接触瞬间也相同，因此仍需单独检查抓取、滑移和释放附近的证据。

[LAPT-Scale](https://arxiv.org/abs/2610.13732)使用连续潜在动作，并结合感知、语义和光流约束帧间变化。连续编码避免先把所有变化压成有限符号，但依然是学到的表征。建议保存 `latent_encoder_version`、`source_frame_pair`、`flow_quality`、`occlusion_mask` 和各监督来源，区分“视频变化被解释”与“机器人可以执行”。

![跨本体动作链先去除视角与节奏干扰，再区分学习的潜在编码和统一解剖坐标，最后在目标控制器上验证](/images/docs/latent-action-cross-embodiment-october-interfaces.svg)

### 共享潜在动作与统一关节坐标是不同接口

[VioLA](https://arxiv.org/abs/2610.12435)把人体和机器人动作映射到身体、手部的共享潜在空间，再由预训练控制器执行；[GreenWAM](https://arxiv.org/abs/2610.18774)采用跨机器人家族的共享解剖动作空间。共享解剖动作空间是按身体部位对应整理的共同关节坐标表达，它仍需原本体的关节名称、自由度、限位和转换映射。两条路线不能统一写成一列没有语义说明的 `action_vector`。

建议增加 `representation_kind` 来区分视觉潜在编码、控制器潜在命令和显式关节坐标，同时保存源/目标本体、身体与手部通道、归一化方式、映射及解码器版本。转换失败应标记原因，不应用零值补齐不存在的自由度，导致下游误以为机器人实际保持该角度。

### 用三层对照检查迁移收益

先检查源视频：相机运动被分离后，手物相对运动和接触事件是否保留。再检查共享表示：相同任务在不同本体上能否对应、不同物理效果是否仍可区分。最后检查目标机器人：在相同适配数据预算下，动作是否满足限位、接触是否正确、任务是否完成。人类数据规模、目标本体标签数量和控制器预训练来源要同时报告，才能判断收益来自共享表征还是额外机器人监督。

以上论文说明人类视频可以提供丰富的运动监督；涉及力、摩擦和遮挡内状态时，仍需额外传感器、物理假设或实机交互来补足。没有动作标签的视频不会因为经过潜在编码，就自动成为无歧义的机器人命令。

### 10 月来源与逐篇数据启示

以下为截至 2026 年 10 月 22 日、按论文 `published` 时间筛选的本主题主归类来源。字段与质检要求为本站结合论文设计的数据建议，不表示论文采用同名 schema；复现定量结果时，应回到论文全文核对数据划分和实验协议。

| 论文 | 数据启示与使用边界 |
| --- | --- |
| [WING](https://arxiv.org/abs/2610.03607)（2610.03607） | 去除自运动的人类视频潜在动作 |
| [VioLA](https://arxiv.org/abs/2610.12435)（2610.12435） | 人机共享身体和手部潜在动作 |
| [LAPT-Scale](https://arxiv.org/abs/2610.13732)（2610.13732） | 连续潜在动作与转移多信号监督 |
| [GreenWAM](https://arxiv.org/abs/2610.18774)（2610.18774） | 跨本体数据需要共享解剖动作空间，同时保留机器人家族与原始关节映射；共同动作格式应接受轨迹、深度、三维预测与真实控制的交叉验证。 |

## 2026 年 9 月整理来源

以下为该主题在 2026-08-27 至 2026-09-27 采集批次中的全部主归类论文；每条均链接原始 arXiv 页面。

- [Latent Cluster Analysis for Vision-Language-Action Models](https://arxiv.org/abs/2609.02634)（2609.02634）
- [Breaking the Vision-Action Shortcut: Latent Interface Training for Generalizable Robotics Foundation Models](https://arxiv.org/abs/2609.12641)（2609.12641）
- [Schema-Adaptive Action-Conditioned JEPA for Cross-Machine CNC Transfer under Partial Sensor Overlap](https://arxiv.org/abs/2609.16071)（2609.16071）
- [SAVLA: Symmetry-Aware Vision-Language-Action Models for Robotic Manipulation](https://arxiv.org/abs/2609.16641)（2609.16641）
- [Rethinking Visual Embodiment Dependence in Visuomotor Policies](https://arxiv.org/abs/2609.16815)（2609.16815）
- [GeoLAM: Learning Geometry-Grounded Latent Actions from Unlabeled Human Videos](https://arxiv.org/abs/2609.17099)（2609.17099）
- [GALA: Geometry-Aware Latent Action Modeling for Vision-Language-Action Model Pretraining across Embodiments](https://arxiv.org/abs/2609.21948)（2609.21948）
- [SkelWAM: A Skeleton-Guided World-Action Model for Zero-Shot Cross-Embodiment Manipulation](https://arxiv.org/abs/2609.21983)（2609.21983）
