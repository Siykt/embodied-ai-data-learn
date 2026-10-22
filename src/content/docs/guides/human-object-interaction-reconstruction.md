---
title: 人体与人-物交互重建数据
description: 把第一视角与外部视角视频转成可验证的四维人体、手部和关节物体轨迹。
---

人-物交互重建从视频恢复随时间变化的人体、手、物体及接触关系。这里的“四维”指三维几何随时间演化；视频中的像素位移不天然具有真实米制尺度，也不等于机器人可执行动作。

[Ego-Exo4D Human Meshes](https://arxiv.org/abs/2609.30187)为同步第一视角和外部视角数据增加密集 4D 人体重建；[MEgoVista](https://arxiv.org/abs/2609.16684)强调经标定的双目尺度、佩戴者手部归属和独立参考评估；[Track, Articulate, Act](https://arxiv.org/abs/2609.19119)从单目日常视频的密集点轨迹恢复可动部件及关节，并把手-物交互放入仿真重放。

![第一视角和外部视角视频经身份跟踪、尺度姿态恢复与接触重建，得到可核验的人物交互轨迹。](/images/docs/human-object-interaction-reconstruction-flow.svg)

## 输入、输出与处理链

输入是第一视角和可用的外部视角视频、相机标定以及独立参考；输出是带尺度来源、可见性和置信度的人体、手部、物体部件四维轨迹。人体轨迹与物体关节状态要在同一时间和世界坐标下解释，才能成为后续机器人学习的候选监督。

1. 采集第一视角与可用的外部视角视频，保存相机内外参、同步脉冲和场景元数据。
2. 检测佩戴者与旁观者，追踪双手、人体、物体部件及可见性。
3. 融合多视角或几何先验，恢复世界坐标中的网格、关节状态与接触候选。
4. 把每帧估计与独立参考或物理重放核对，输出置信度及无解片段。

### 时间与空间对齐

为每个观测保留相机 `frame_id`、曝光时间和世界坐标变换；双目/多视角三角化需要相同时间基准。单目输出若未有尺度锚点，应标记 `scale_source=unknown`，不能以米为单位训练控制。物体可动部件要区分固定连杆、移动连杆和关节状态，不能用整物体一个位姿代替。

![四维重建契约记录视角标定、人体手部与物体关节动态，以及参考误差和原视频血缘。](/images/docs/human-object-interaction-reconstruction-contract.svg)

## 最小数据字段

| 字段组 | 建议字段 | 用途 |
| --- | --- | --- |
| 身份 | `sequence_id、actor_id、object_id、view_id` | 连接多视角同一交互 |
| 成像 | `timestamp、intrinsics、extrinsics、scale_source` | 约束尺度与投影 |
| 人体 | `body_mesh、hand_pose、head_pose、joint_confidence` | 提供时序运动标签 |
| 物体 | `part_id、joint_type、joint_axis、joint_state` | 表达铰链/滑轨等可动结构 |
| 关系 | `contact_candidate、visibility、occlusion_mask` | 标注交互与不可见区间 |
| 质量 | `reprojection_error、reference_error、failure_flag` | 明确能否用于下游监督 |

尤其要保留每段姿态的尺度依据和遮挡标记；无法观测的手部或物体背面不能以无置信度的确定标签发布。

![人体交互重建分别检查米制尺度、遮挡下的时间连续性与物体关节接触重放。](/images/docs/human-object-interaction-reconstruction-evaluation.svg)

## 质量控制与评估

复核时先查佩戴者手部身份与米制尺度，再查跨帧轨迹和可动部件是否连续。重投影一致性、独立参考误差和交互可重放性提供不同层次的证据：

- 按帧检查相机投影残差、左右手身份交换、旁观者误归属与遮挡区间。
- 有独立动捕或外部参考时报告米制位置误差；没有参考时只报告可验证的重投影与几何一致性。
- 检查关节轴、部件刚性和接触时刻在时间上的连续性，保留原视频供人工复核。
- 同一场景或相邻片段不可跨训练与测试集，避免背景和动作泄漏。

| 评估层 | 指标或证据 | 判读要点 |
| --- | --- | --- |
| 几何准确度 | 重投影、米制姿态误差 | 注明参考系统与单位 |
| 时序稳定性 | 身份交换、抖动、轨迹缺口 | 按遮挡程度分层 |
| 交互有效性 | 关节状态与接触重放 | 核对物理可实现性 |

## 数据集使用边界

重建标签适合做人手运动、人体姿态和可动对象预训练的弱监督，也可用于机器人重定向前的中间表示。图像重建正确不代表接触力、摩擦或控制意图正确；单目恢复的不可见背面和尺度都含推断成分。用于机器人数据集时，须附上重建来源、置信度及重定向验证。

## 本页术语

本页使用的关键术语：

- **四维重建**：恢复三维对象在连续时间中的几何和运动。
- **米制尺度**：坐标数值具有可核验的实际长度单位。
- **可动关节状态**：门铰链或滑轨等部件相对固定部分的角度或位移。

## 2026 年 10 月补充：联合运动重建与交互语境

### 相机和手共同运动时，误差需要共同解释

[V-JEPA Hand（2610.26780）](https://arxiv.org/abs/2610.26780)从视频联合输出双手姿态、手是否出现和相机运动，再把手轨迹放入共同世界坐标。其训练混合伪标签与高精度三维标注，相机焦距既可输入也可预测。因此派生记录应带 `label_source`、`focal_source`、`hand_present`，并把伪标签片段与独立标注参考分层评估；只在成功检测到手的帧上报误差会掩盖漏检。

[DewHand（2610.29936）](https://arxiv.org/abs/2610.29936)同样联合恢复世界坐标中的手和相机，进一步以米制监督约束尺度，并将遮挡和出画运动视为条件生成问题。一段不可见手轨迹可能存在多个合理解释。数据发布应保留可见掩码、采样/预测来源和尺度依据，不能把生成结果写成逐帧实测真值。评估时要分开未对齐的世界轨迹误差、刚体对齐后误差和尺度误差；刚体对齐只校正旋转和平移，若又允许尺度拟合，就改变了指标含义。

![相机与双手联合恢复进入共同世界坐标，尺度和可见性各自检查，再与场景表面和携物目的地标签连接。](/images/docs/human-object-interaction-reconstruction-october-world-context.svg)

### 交互还需要场景与目的地

[ECHO（2610.10438）](https://arxiv.org/abs/2610.10438)把重建室内场景、携物活动、语言和语境目的地结合。其合成 episode 含同步 RGB-D、相机/人体/物体轨迹、起点与目的地表面，以及暗示目的地但不直接报答案的生活语境。这使“物体往哪里移动”成为可评估目标。数据集应稳定连接 `floor_id、surface_id、carried_object_id`，将任务上下文与目的地真值分字段保存，并按居住场景和习惯语境留出，避免模型靠房间模板猜答案。合成活动与人工语境标注仍不能当作真实家庭行为频率。

[MAMHOI（2610.12416）](https://arxiv.org/abs/2610.12416)面对人-场景与人-物数据难以完整配对的问题，使用**运动可供性接口**：先描述某场景哪里、以什么方式允许交互，再生成对应人-物运动。这是连接两种监督的中间表示，并不意味着两个原始数据集已经有逐帧配对关系。合并时记录各自来源、中间接口版本及生成阶段，分别检查场景碰撞和人-物接触。

| 质控对象 | 建议记录 | 需要独立报告的结果 |
| --- | --- | --- |
| 手与相机联合恢复 | 坐标、焦距来源、尺度锚点、可见性 | 世界轨迹误差、尺度误差、有效帧覆盖 |
| 伪标签与生成补全 | 原始视频、标注来源、补全区间 | 可见/遮挡/出画切片误差 |
| 场景中的交互 | 表面 ID、场景版本、可供性来源 | 物体-场景穿透、人-物接触保持 |
| 语境目的地 | 语言上下文、目标表面、标注者 | 未见场景与缺失输入模态测试 |

以上字段是本站的数据组织建议。四篇论文分别研究运动恢复、语境数据和生成监督衔接，不能将其中一种评测分数当作整个重建流程的精度；本段依据原始摘要归纳，未把模型补全标签视为已核验物理测量。

## 2026 年 9 月整理来源

以下为该主题在 2026-08-27 至 2026-09-27 采集批次中的全部主归类论文；每条均链接原始 arXiv 页面。

- [Reconstructing Humans and Objects in Interaction using Large Reconstruction Models](https://arxiv.org/abs/2608.27407)（2608.27407）
- [Open-UniMo: Towards Unified Motion-Language Understanding and Generation in the Open World](https://arxiv.org/abs/2609.14615)（2609.14615）
- [Beyond Gestures: Estimating Full Hand Pose and Contact Forces from Wrist-Worn Pressure Sensor Array](https://arxiv.org/abs/2609.16518)（2609.16518）
- [MEgoVista: Multi-view Ego-aware Motion Estimation for Metric 4D Hands and Head in the Wild](https://arxiv.org/abs/2609.16684)（2609.16684）
- [Track, Articulate, Act: Generating Articulation from Casual Human Videos](https://arxiv.org/abs/2609.19119)（2609.19119）
- [Ego-Exo4D Human Meshes Dataset: 4D Human Motion Reconstruction for Ego-Exo Captures](https://arxiv.org/abs/2609.30187)（2609.30187）
