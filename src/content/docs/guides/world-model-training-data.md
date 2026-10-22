---
title: 世界模型训练数据与物理表征
description: 从具身数据视角整理动作条件视频、潜在状态与物理一致性训练样本。
---

世界模型学习在给定当前观测与候选动作时，环境可能如何变化。训练样本因此要同时保存动作前状态、动作语义和真实后态；只保存好看的未来视频，无法判断模型是否支持控制。[具身世界模型综述](https://arxiv.org/abs/2609.16697)和[世界动作模型综述](https://arxiv.org/abs/2609.16074)都把预测与行动的联系放在核心位置；[Riemann-1.0](https://arxiv.org/abs/2608.27033)则给出多视角视觉、机器人状态与本体动作共用因果序列的实例。

![世界模型训练数据从多源观测、动作对齐到条件预测与物理质检的流程](/images/docs/world-model-training-data-flow.svg)

## 概念与数据问题

这里的世界状态可以是图像、潜在向量、三维点集或显式物体状态。[PointCast](https://arxiv.org/abs/2609.28393)用物体和末端执行器的三维点及点身份表示不同形变类型；[Programmable World Model](https://arxiv.org/abs/2609.10540)把状态演化与画面生成分开；[WorldCrafter](https://arxiv.org/abs/2609.24984)使用可由相机视角查询的三维感知记忆。表示不同，数据必须回答同一问题：同一起点在不同动作下，哪些变化由动作导致，哪些只是视角或渲染变化？[IMPLY](https://arxiv.org/abs/2609.12441)强调仅让预测彼此一致不足以证明符合物理；[Frozen Flows Forget](https://arxiv.org/abs/2609.28414)展示潜在预测可能丢失操作所需的运动。

## 采集、处理与对齐

**采集**时为每个 episode 记录相机、关节/末端状态、控制命令、物体与任务条件，并保存发令和实际执行时间。[CLAP](https://arxiv.org/abs/2608.27406)利用人和机器人等异构视频讨论跨本体学习；[XPACE](https://arxiv.org/abs/2609.17372)联合世界与动作建模；[Underwater C3-JEPA](https://arxiv.org/abs/2609.30214)说明水下多视角与控制信号需要同步。跨本体样本应保留原始动作接口和转换规则，不宜把不同机器人命令直接拼成同一数值列。

**处理**时区分背景、目标与接触对象，再生成可追踪的派生状态。[AcrossVAM1.0](https://arxiv.org/abs/2608.28491)将物体运动与外观分开，[DUET-DINO](https://arxiv.org/abs/2609.10506)联合侧视与腕视潜在预测，[AlayaVista](https://arxiv.org/abs/2609.14462)处理宽视场状态到局部画面的生成，[MoWAM](https://arxiv.org/abs/2609.20709)用显式未来运动减轻视频生成开销。这些路线提示：物体身份、相机位姿和运动轨迹应作为可复查中间产物。

**对齐**时明确预测跨度、动作生效时刻和观测间隔。[CST-WM](https://arxiv.org/abs/2609.06302)关注自运动与遮挡下的目标可观测性；[Semigroup-JEPA](https://arxiv.org/abs/2609.10464)检验不同时间步的动力学一致性；[Movement Trend Guidance](https://arxiv.org/abs/2609.20669)把未来运动趋势用于三维策略。[DIDO](https://arxiv.org/abs/2609.15570)说明互动区域与静态背景在生成过程中的收敛速度不同，故不能只靠全帧平均误差判定数据与模型质量。

![世界模型样本把观测、动作、预测未来和实测证据绑定的字段关系](/images/docs/world-model-training-data-contract.svg)

## 最小字段契约

字段名是建议的数据接口，不表示所引论文使用完全相同的文件格式。

| 字段 | 记录内容 | 检查重点 |
| --- | --- | --- |
| episode_id / step_id | 任务与时间链唯一键 | 拆分训练集时整条 episode 隔离 |
| camera_id / calibration_id | 相机来源、外参与标定版本 | 多视角重投影一致 |
| observed_at / acted_at | 观测、发令和生效时间 | 延迟与预测跨度可计算 |
| robot_id / action_schema | 本体、自由度、单位与控制模式 | 跨本体转换可回溯 |
| object_track_id / pose | 目标身份、位姿与遮挡状态 | 失跟踪不伪作静止 |
| future_target / horizon | 实测未来视频、点轨迹或潜在目标 | 目标来自动作后真实观测 |
| physics_context | 材质、接触或环境参数（若可得） | 未知值明确为空而非默认 |
| quality_flags | 模糊、遮挡、碰撞、漂移与同步质量 | 可按失败机制筛选 |

## 质控与评估

训练前应检查时间戳单调、控制命令与实测运动一致、跨视角物体身份连续，以及已知物理量的单位。[PhysBrain 1.5](https://arxiv.org/abs/2609.14973)把语言、末端运动和视觉目标统一编码；[Successive Capacity Growth](https://arxiv.org/abs/2608.27367)研究编码器容量与任务复杂度。这类模型比较只有在数据划分和输入粒度一致时才有意义。

评估至少分三层：一是事实后态预测；二是同一起点的多动作比较与跨时间物理一致性；三是把预测接入真实或仿真控制后看任务结果。[IMPLY](https://arxiv.org/abs/2609.12441)提供物理锚定的滚动预测检查，[PointCast](https://arxiv.org/abs/2609.28393)关注点轨迹，[Underwater C3-JEPA](https://arxiv.org/abs/2609.30214)关注跨视角控制条件。报告时保留运动区域与静态区域的分项指标，避免背景质量掩盖接触错误。

![世界模型按预测一致性、物理可辨性及下游决策可用性分层评估](/images/docs/world-model-training-data-evaluation.svg)

## 数据集使用边界

[The Past Frames the Future](https://arxiv.org/abs/2609.28466)讨论长视频生成在有限上下文中丢失历史信息的问题，它可为记忆设计提供参考，但通用视频质量不能直接代表机器人控制能力。世界模型在训练集外的本体、材质、光照或动作幅度上应单独验证；如果模型未见接触类型，就不应把生成画面当作安全执行证据。论文中不同表示与任务协议不能直接合并为一个排行榜。

## 2026 年 10 月进展：把动作后果与画面变化分开监督

### 多源数据进入同一模型，监督角色仍需保留

[UniWAM](https://arxiv.org/abs/2610.02054)把问答、人类第一视角视频和机器人示教分配给不同组件；[UniW(A)M](https://arxiv.org/abs/2610.18697)让多个预测和动作接口共享动力学；[P³-WAM](https://arxiv.org/abs/2610.22363)通过改变可见模态，把视频与三维动作轮流作为条件或目标。这些方法扩大了同一轨迹的用途，也使“模型看到了什么”成为必须记录的变量。条件可见性掩码标记哪些模态和时间片可作输入、哪些仅作预测目标。建议为派生窗口保存 `source_domain`、`conditioning_mask`、`target_modality`、`action_interface` 和标注版本，避免把训练时可见的未来动作或未来帧带到部署评测。

[XGenAct](https://arxiv.org/abs/2610.03516)把深度、法线和功能分割编码成视频，说明统一文件形态不等于统一物理含义：深度单位、法线坐标、分割类别和编解码版本仍应独立保存。[Ropedia W0](https://arxiv.org/abs/2610.26855)统一相机位姿与投影骨架时，仍依赖本体正运动学及人工关键点修订。跨本体样本不能因为都变成图像通道，就省略原始单位和修订记录。

![世界模型训练样本分别保留来源与可见条件、动作因果和场景物理条件，再通过状态、预测和控制三层验证](/images/docs/world-model-training-data-october-supervision.svg)

### 外观稳定不代表动作信息完整

[AVL-JEPA](https://arxiv.org/abs/2610.03587)研究表征保留了视觉信息、却丢失动作后果的情况；[SplitJEPA](https://arxiv.org/abs/2610.12349)进一步区分与观测变化共同保持的因素和随观测改变的因素。数据质检应准备两类对照：只改相机或光照、保持物理过程不变；以及固定起点、改变实际动作。前者检查干扰鲁棒性，后者检查是否真的区分因果后果。[ALPS](https://arxiv.org/abs/2610.30120)则同时检验物理状态可读性、语言对齐和像素重建，提醒我们不要用一种表征分数代替全部用途。

[World Embedding Benchmark](https://arxiv.org/abs/2610.03632)把物理属性回归与图文匹配分开；[WOVEN](https://arxiv.org/abs/2610.12417)按场景、动作和推理操作组织转移监督，其样本来自视频生成模型的 rollout。应保留生成器版本、种子及真实性检查，不能把这些转移当作真实物理执行真值。对应的数据集应记录 `physics_label_source`、`reasoning_operation` 和控制变量，分别报告物理量可恢复性与语义对齐。[30,000 小时第一视角视频研究](https://arxiv.org/abs/2610.12464)把主体运动和物体受作用结果分开评价；[RoboJEPA](https://arxiv.org/abs/2610.10515)研究潜在预测误差与规划效果的关系。两者都支持保留分项指标，而不是将视频时长或总体误差视为充分质量证据。

### 用探索片段识别环境，用失败样本扩展作用范围

[Considering Context](https://arxiv.org/abs/2610.06651)问的是当前历史是否已足以预测；[T2-z](https://arxiv.org/abs/2610.22364)利用测试交互优化环境潜变量；[PhysiCalWorld](https://arxiv.org/abs/2610.30125)则把探索片段压缩成可复用物理描述符。环境潜变量是供模型使用的环境编码，不是直接测得的质量或摩擦系数。建议保存 `physics_group_id`、`context_episode_id`、`prediction_episode_id`、`adaptation_budget`，将适配证据与正式评测分开。PhysiCalWorld 的提示和预测片段需来自相同物理配置；其四个仿真环境结果不能替代实机验证，物理条件改变后也不能默认复用旧描述符。

[Dexterity from Supervised Play](https://arxiv.org/abs/2610.22340)区分人工自由交互、克隆策略采集和模型内自博弈；[DreamTrue](https://arxiv.org/abs/2610.12468)针对动作标定误差及失败交互覆盖不足，加入几何校准、反事实轨迹和人工缺陷标签。对这些样本应分别保存动作来源、真实/生成后态、缺陷类别及质量权重。生成的失败后果可用于训练和比较，但不能冒充真实执行记录。

### 相机、压缩与持久状态成为数据条件

[4Director](https://arxiv.org/abs/2610.02160)以刚体网格和逐帧变换控制视频；[CausalAlign](https://arxiv.org/abs/2610.29915)关注相邻帧自运动变化；[Velox](https://arxiv.org/abs/2610.22311)根据相机视锥与深度覆盖选择历史；[CADRE](https://arxiv.org/abs/2610.30129)显示运动质量对空间、时间压缩和相机是否移动有不同敏感性。建议追加 `camera_motion_regime`、`spatial_compression`、`temporal_compression`、`context_coverage`，在相同控制频率下联合检查运动误差和动作生效等待时间。

[WorldCast](https://arxiv.org/abs/2610.12412)的共享玩家/场景状态与[State World Models](https://arxiv.org/abs/2610.26811)的隐藏状态反事实对，都说明当前画面可能无法决定下一状态。[SCO](https://arxiv.org/abs/2610.10400)提供无需额外训练的生成时状态保持约束；[Future Chunk Prediction](https://arxiv.org/abs/2610.29989)提供远期视频块的辅助训练监督。它们可用于设计视频或交互世界的质检，但游戏一致性、通用视频物理观感和机器人动作条件控制应分别标明证据范围。

### 10 月来源与逐篇数据启示

以下为截至 2026 年 10 月 22 日、按论文 `published` 时间筛选的本主题主归类来源。字段与质检要求为本站结合论文设计的数据建议，不表示论文采用同名 schema；复现定量结果时，应回到论文全文核对数据划分和实验协议。

| 论文 | 数据启示与使用边界 |
| --- | --- |
| [UniWAM](https://arxiv.org/abs/2610.02054)（2610.02054） | 人机混合世界动作监督 |
| [4Director](https://arxiv.org/abs/2610.02160)（2610.02160） | 刚体场景控制与视频标注 |
| [XGenAct](https://arxiv.org/abs/2610.03516)（2610.03516） | 深度、法线和功能分割的联合监督 |
| [AVL-JEPA](https://arxiv.org/abs/2610.03587)（2610.03587） | 动作因果信息与视觉扰动对照 |
| [World Embedding Benchmark](https://arxiv.org/abs/2610.03632)（2610.03632） | 物理属性标注与表征可恢复性 |
| [Considering Context](https://arxiv.org/abs/2610.06651)（2610.06651） | 历史与环境上下文的预测充分性 |
| [SCO](https://arxiv.org/abs/2610.10400)（2610.10400） | 交错生成中的事件与状态一致性 |
| [RoboJEPA](https://arxiv.org/abs/2610.10515)（2610.10515） | 多本体规模化预测与规划代理指标 |
| [SplitJEPA](https://arxiv.org/abs/2610.12349)（2610.12349） | 不变与可变潜在因子的配对监督 |
| [WorldCast](https://arxiv.org/abs/2610.12412)（2610.12412） | 分布式多视图共享实体状态 |
| [WOVEN](https://arxiv.org/abs/2610.12417)（2610.12417） | 按推理操作组织生成视频的转移监督；保留生成来源，不将其当成真实执行。 |
| [30,000 小时第一视角视频研究](https://arxiv.org/abs/2610.12464)（2610.12464） | 第一视角规模与物体交互保真度 |
| [DreamTrue](https://arxiv.org/abs/2610.12468)（2610.12468） | 动作几何校准、反事实与缺陷标签 |
| [UniW(A)M](https://arxiv.org/abs/2610.18697)（2610.18697） | 同一具身轨迹可供世界预测与动作生成使用，但需保存各条件接口、动作块及接口选择结果，以比较联合监督对预测质量和执行成功率的影响。 |
| [Velox](https://arxiv.org/abs/2610.22311)（2610.22311） | 历史视频上下文应记录相机视锥、深度覆盖和上下文选择来源；加速评估需同时检查长 rollout 延迟、未覆盖区域表现及导航视频一致性。 |
| [Dexterity from Supervised Play](https://arxiv.org/abs/2610.22340)（2610.22340） | 把人工 play、克隆后的自主探索和模型内自博弈分别保留来源；无特定任务示教的交互数据仍须覆盖接触状态，并以真实手内操作验证规划用途。 |
| [P³-WAM](https://arxiv.org/abs/2610.22363)（2610.22363） | 统一视频与三维动作样本可通过可见模态随机化用于感知、预测和规划；三种能力应分开验证，生成操作视频的评价不能自动视为真实机器人执行证明。 |
| [T2-z](https://arxiv.org/abs/2610.22364)（2610.22364） | 训练样本应保留环境身份与交互轨迹，测试时隔离用于适配的少量交互和正式评测；无物理参数标签的环境潜变量仍需预测误差和动作成功率双重验证。 |
| [State World Models](https://arxiv.org/abs/2610.26811)（2610.26811） | 为相同初始图像和动作构造隐藏状态不同的反事实配对，可检验预测是否依赖持久状态；规则执行、三维引导和视频渲染应分别记录与评估。 |
| [Ropedia W0](https://arxiv.org/abs/2610.26855)（2610.26855） | 把相机位姿表示的移动与投影骨架表示的操作统一，仍须保留本体正运动学、人工关键点修订及质量记录，并使用高质量遥操作留出集验证跨本体泛化。 |
| [CausalAlign](https://arxiv.org/abs/2610.29915)（2610.29915） | 监督相邻帧变化可针对相机运动而非静态外观；检验几何一致性和时间平滑时，还应保留移动操作成功率作为生成数据的具身用途证据。 |
| [Future Chunk Prediction](https://arxiv.org/abs/2610.29989)（2610.29989） | 以间隔未来视频块作为辅助监督可削弱局部视觉连续性捷径；归档时应注明其证据为视频物理合理性，尚不能推断动作条件控制收益。 |
| [ALPS](https://arxiv.org/abs/2610.30120)（2610.30120） | 视觉预训练可结合语言、像素重建和空间对应监督；统一数据切分下应分别测量物理状态可读性、语言对齐、未来像素重建和策略成功。 |
| [PhysiCalWorld](https://arxiv.org/abs/2610.30125)（2610.30125） | 探索片段和预测片段需按相同物理配置分组，隔离片段后检验描述符；证据来自四个仿真环境，不把潜变量当物理数值测量，条件改变后重新采集。 |
| [CADRE](https://arxiv.org/abs/2610.30129)（2610.30129） | 评估视频压缩时应按相机是否移动区分空间和时间压缩，联合报告延迟、动作生效时间与运动误差；图像清晰度不能代替动态一致性质检。 |

## 2026 年 9 月整理来源

以下论文按清单中的主主题归档。跨主题使用时，应重新核对任务、传感器和评测口径。

- [CLAP: Cross-Embodiment Video World Models are Zero-Shot Physical Simulators](https://arxiv.org/abs/2608.27406)（2608.27406）
- [Successive Capacity Growth: Task-Complexity-Driven Width and Depth Expansion for Vision Transformer Encoders in JEPA World Models](https://arxiv.org/abs/2608.27367)（2608.27367）
- [Riemann-1.0: An Embodied World Action Model for Physical AI](https://arxiv.org/abs/2608.27033)（2608.27033）
- [AcrossVAM1.0: Particle World Modeling for Text-Assisted Robot Video Prediction](https://arxiv.org/abs/2608.28491)（2608.28491）
- [CST-WM: A Causally Structured World Model for Embodied Visual Tracking](https://arxiv.org/abs/2609.06302)（2609.06302）
- [Programmable World Model](https://arxiv.org/abs/2609.10540)（2609.10540）
- [DUET-DINO: Simultaneous Cross-View World Modeling for Latent Planning in Robot Manipulation](https://arxiv.org/abs/2609.10506)（2609.10506）
- [Semigroup-JEPA: Latent Dynamics Consistency for Zero-Shot Physics Generalization](https://arxiv.org/abs/2609.10464)（2609.10464）
- [XPACE: Joint World and Action Modeling from Heterogeneous Experience](https://arxiv.org/abs/2609.17372)（2609.17372）
- [World Models for Embodied Intelligence: From Plausible to Controllable to Actionable](https://arxiv.org/abs/2609.16697)（2609.16697）
- [DIDO: Distilling Interaction-Centric Dynamics into One-Step Denoising for World Action Models](https://arxiv.org/abs/2609.15570)（2609.15570）
- [PhysBrain 1.5: From Vision-Language Models to Physical Foundation Models](https://arxiv.org/abs/2609.14973)（2609.14973）
- [World-Action Models for Robot Learning and Control: A Survey](https://arxiv.org/abs/2609.16074)（2609.16074）
- [AlayaVista: Streaming World Modeling from Panoramic States to Perspective Video](https://arxiv.org/abs/2609.14462)（2609.14462）
- [IMPLY: Physically Anchored Consistency for World-Model Rollouts](https://arxiv.org/abs/2609.12441)（2609.12441）
- [MoWAM: Explicit Future Motion Prediction for Efficient World Action Models](https://arxiv.org/abs/2609.20709)（2609.20709）
- [Learning Foresight without Explicit Trajectories for 3D Diffusion Policies](https://arxiv.org/abs/2609.20669)（2609.20669）
- [WorldCrafter: Consistent Video World Model with Implicit 3D-aware Memory](https://arxiv.org/abs/2609.24984)（2609.24984）
- [The Past Frames the Future: Memory for Autoregressive Video Generation](https://arxiv.org/abs/2609.28466)（2609.28466）
- [Frozen Flows Forget: Diagnosing and Restoring Lost Motion in a Latent-flow World Model](https://arxiv.org/abs/2609.28414)（2609.28414）
- [PointCast: One World Model for Rigid, Articulated, and Deformable Object Manipulation](https://arxiv.org/abs/2609.28393)（2609.28393）
- [Underwater C3-JEPA: An Object-Centric Cross-View World Model for ROV Salvage](https://arxiv.org/abs/2609.30214)（2609.30214）
