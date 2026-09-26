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

## 本主题论文

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
