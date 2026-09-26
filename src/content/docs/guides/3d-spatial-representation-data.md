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

## 本月相关论文

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
