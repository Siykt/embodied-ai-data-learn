---
title: 三维空间表征与部件数据
description: 从点轨迹、深度和目标部件到机器人可用的米制三维状态，整理标注与评估契约。
---

三维空间表征将像素观测转为物体、部件、表面或点的几何状态。对具身任务，表征应服务于抓取、避障和状态变化判断：语义上知道“把手”还不够，还需知道它在哪里、属于哪个对象、能否接触及其不确定性。

[UniPart](https://arxiv.org/abs/2609.12898)研究自由文本指定的三维部件分割，并构建大规模文本—部件配对数据；[PointZero](https://arxiv.org/abs/2609.19142)研究补全三维点轨迹以学习可迁移动态；[VLMs Can Describe, But Not Measure](https://arxiv.org/abs/2609.28184)强调操作决策需要物体中心的可量测场景理解。三类工作分别对应语义、运动和米制几何。

![多视角深度数据经对象部件标注、米制重建和三维点轨迹补全，最后用机器人动作核验。](/images/docs/3d-spatial-representation-data-flow.svg)

## 输入、输出与处理链

输入为 RGB-D、多视角或点云观测及语言指称；输出为对象和部件的稳定 ID、米制几何、三维点轨迹以及可见性或预测标记。部件语义、几何精度和机器人可达性需要逐层验证，不能只用单一分割分数代表操作价值。

1. 从 RGB、深度、多视角或点云生成三维观测，保存标定和尺度来源。
2. 标注对象与功能部件的 ID、文本指称、可见区域和层级关系。
3. 追踪部件/关键点随时间的三维变化，明确遮挡与外推位置。
4. 将表征用于具体机器人任务，检查定位误差是否影响抓取或运动规划。

### 时间与空间对齐

统一世界、相机、物体与机器人基座坐标系；每个几何标签保存单位、变换链和版本。开放词汇部件标签要与具体物体实例绑定，不能只存“把手”字符串。点轨迹跨遮挡补全应保留观测点与预测点的差别，以及置信度；同一三维资产在不同视角中使用稳定 ID。

![三维数据契约连接场景物体部件身份、点云位姿和轨迹可见性，以及尺度和参考误差。](/images/docs/3d-spatial-representation-data-contract.svg)

## 最小数据字段

| 字段组 | 建议字段 | 用途 |
| --- | --- | --- |
| 几何来源 | `scene_id、camera_pose、depth_source、scale_source` | 判断米制可信度 |
| 实例/部件 | `object_id、part_id、parent_id、text_query` | 稳定语义指称 |
| 三维状态 | `point_cloud、mesh/voxel、pose、extent` | 提供形状与位姿 |
| 动态 | `track_id、t、visibility、predicted_flag` | 区别观测与补全 |
| 接触 | `surface_normal、grasp_region、collision_geometry` | 连接几何与动作 |
| 质量 | `annotation_source、uncertainty、registration_error` | 控制训练权重与准入 |

部件名称、三维坐标和轨迹补全都有不同来源；原始观测与模型外推结果应在字段层明确区分。

![三维表征评估分别衡量部件语义定位、米制几何误差与抓取规划中的实际效果。](/images/docs/3d-spatial-representation-data-evaluation.svg)

## 质量控制与评估

几何标签的质量从实例身份、尺度来源和遮挡补全开始检查，再看误差是否超出目标操作容差。语义分割准确和抓取定位准确应单独报告：

- 检查跨视角对象/部件 ID 一致性、点云空洞、尺度错误和遮挡区域的伪精确标签。
- 用重投影及独立测量核对米制位置；开放词汇分割报告未见对象与未见部件。
- 把定位误差转成任务尺度：抓取窗口、插孔余量和碰撞间隙不同，所需精度也不同。
- 评估集按资产、场景和生成来源隔离，防止同一模型重建资产同时进入训练和测试。

| 评估层 | 指标或证据 | 判读要点 |
| --- | --- | --- |
| 语义定位 | 部件 IoU/指称命中 | 未见对象单列 |
| 几何测量 | 米制位置/尺度误差 | 注明参考源 |
| 动作相关 | 抓取或导航闭环结果 | 与像素基线比较 |

## 数据集使用边界

三维标签可以用于空间编码器、部件级动作条件和世界模型，但重建后的点云仍可能遗漏不可见背面、接触面和材料属性。文本指称正确也不保证操作可达；进入控制训练前应核验可达性、碰撞几何和目标机器人坐标变换。

## 本页术语

本页使用的关键术语：

- **部件级分割**：为物体中的可操作组成部分单独分配空间标签。
- **点轨迹**：同一三维点随时间的位置序列。
- **米制几何**：尺寸和位姿可用实际长度单位解释的三维表示。

## 2026 年 10 月补充：把场景状态与观察方式分开

### 坐标、稀疏结构与相机运动

[3D-Prog（2610.02021）](https://arxiv.org/abs/2610.02021)用规范坐标框架将输入和输出锚定在共享欧氏坐标中，并加入任务相关反馈。其数据启示是将轴向、原点、尺度和输出坐标约定做成可校验接口；模型画出了正确关系，不代表其数值已能交给机器人。[SkeleWAM（2610.02120）](https://arxiv.org/abs/2610.02120)从 RGB-D 与本体状态形成机器人关节、物体中心和交互点组成的稀疏三维骨架，并预测未来骨架。保存这种表示时，应有节点语义、稳定 ID、测量来源和缺失掩码；物体中心不能替代接触点，稀疏骨架也不能表达完整碰撞表面。

[GeoState（2610.22343）](https://arxiv.org/abs/2610.22343)把场景状态演化与相机相关观察拆开，用相机射线查询几何，且整个预测段保持同一上下文尺度。**视角解耦状态**是尽量让相机移动不被误记为场景运动的表示。数据应保存独立的相机轨迹与场景状态，并检查跨帧固定尺度的预测误差；逐帧重新对齐尺度会掩盖漂移。该文摘要的主要证据来自驾驶数据集，迁移到机械臂接触几何还需单独验证。

![同一场景经多个相机观察后形成共同尺度的状态，节点语义、相机轨迹和干预记录分别保存，跨视角查询与机器人操作分别验收。](/images/docs/3d-spatial-representation-data-october-view-state.svg)

### 训练监督的结构会改变可用几何

[SNAP（2610.03717）](https://arxiv.org/abs/2610.03717)研究新视角合成中的编码器与解码器分工，采用受位姿约束的局部解码和潜在空间重建。对于数据制备，关键是保留同场景多视角关系、相机位姿及训练/测试相机变化，不能只发布脱离视角的图像特征；评估应包含定位、对应和机器人任务，而非单看生成图像质量。

[Block Disentanglement in CRL（2610.06809）](https://arxiv.org/abs/2610.06809)讨论在可获得干预机制下哪些潜在物理量能被成组区分，并在受控具身视觉状态估计中验证。干预是主动改变某个系统因素，而非给任意两帧贴“不同”标签。建议保存干预目标、操作范围、场景重置与可观测变化；理论中的可辨识条件不能不经检查推广到自然视频。

[Relational Spatial Alignment（2610.24705）](https://arxiv.org/abs/2610.24705)将几何监督从逐点特征相等改为成对关系对齐，针对直接对齐导致的表征表达能力下降。整理教师特征时需要记录对象/点配对、有效关系掩码及教师版本；对应不可靠的点对不能作为确定监督。验收除几何误差外，还应观察原任务能力是否退化。

| 状态层 | 必须保留的关系 | 适合的验收 |
| --- | --- | --- |
| 坐标与骨架 | 轴向尺度、节点身份、机器人与对象变换 | 米制误差、缺失节点、任务容差 |
| 视角与时间 | 同场景多视角、相机轨迹、共同尺度 | 未见视角、长预测段漂移 |
| 监督来源 | 干预机制、教师版本、点对有效性 | 条件满足情况、跨任务能力保持 |

上述字段与检查是本站的工程归纳，论文事实依据本地原始摘要。六种方法的输出粒度和验证域不同，不应把“学到了三维特征”作为米制测量、动力学状态和操作可执行性都已通过的结论。

## 2026 年 9 月整理来源

以下为该主题在 2026-08-27 至 2026-09-27 采集批次中的全部主归类论文；每条均链接原始 arXiv 页面。

- [DINOcular: Self-Supervised Visuospatial Representations](https://arxiv.org/abs/2608.27226)（2608.27226）
- [SeqAlign3DVG: A Sequence-Aligned Benchmark and Voxel Reasoning Framework for 3D Visual Grounding](https://arxiv.org/abs/2608.30451)（2608.30451）
- [GIFT: Guided Intermediate Feature Training via Action-Oriented Structural Supervision for Robotic Manipulation](https://arxiv.org/abs/2609.04193)（2609.04193）
- [GloVLA: Let Geometry Move and Local VLA Interact for Robust Object-Centric Manipulation in Unstructured Environments](https://arxiv.org/abs/2609.06256)（2609.06256）
- [Improving Imitation Learning Efficiency for Manipulation through Geometric Prior Pretraining](https://arxiv.org/abs/2609.12721)（2609.12721）
- [VideoTok4D: A 4D-Aware Video Tokenizer for Compact World Representation](https://arxiv.org/abs/2609.12874)（2609.12874）
- [UniPart: Towards Zero-shot Language-Grounded 3D Part Segmentation for Embodied Interaction](https://arxiv.org/abs/2609.12898)（2609.12898）
- [GeomVLA: Unifying Scene, Motion, and Action in 3D](https://arxiv.org/abs/2609.13812)（2609.13812）
- [PointZero: 3D Point Track Completion for Learning Transferable 3D Dynamics](https://arxiv.org/abs/2609.19142)（2609.19142）
- [CoRef-GS: Cooperative Referring Gaussian Splatting for Multi-Agent Scene Understanding](https://arxiv.org/abs/2609.20586)（2609.20586）
- [VLMs Can Describe, But Not Measure: Object-Centric Scene Understanding for Robotic Manipulation](https://arxiv.org/abs/2609.28184)（2609.28184）
