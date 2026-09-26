---
title: VLA 实时执行与动作分块数据
description: 记录推理延迟、动作分块、实际执行和闭环反馈之间的时间关系。
---

VLA 常一次预测一段动作，以减少模型调用，但动作块越长，机器人越晚利用新观测纠错。[FlashVLA](https://arxiv.org/abs/2608.27384)研究流式解码和异步推理，[GeoAAC](https://arxiv.org/abs/2609.20776)按任务阶段自适应动作块长度，[SmolVLA 部署比较](https://arxiv.org/abs/2609.14146)显示降低推理延迟也可能改变闭环任务行为。数据必须记录动作实际生效的时间，不能只记录模型输出时间。

![VLA 从状态采样到动作分块、异步调度和闭环反馈的实时链路](/images/docs/vla-realtime-execution-data-flow.svg)

## 概念与数据问题

动作分块是一段连续控制命令；动作年龄是所依赖观测与实际执行之间的时间差；重规划边界是旧动作块切换到新动作块的位置。[GROOVE](https://arxiv.org/abs/2609.13695)针对块内及边界的末端轨迹急动度，[稀疏细化](https://arxiv.org/abs/2609.15840)把注意力放在少数关键时间步，[SkipVLA](https://arxiv.org/abs/2609.20648)用经典规划减少不必要的 VLA 查询。这些优化各改动不同环节，比较时需要相同任务和硬件日志。

## 采集、处理与对齐

**采集**：将相机帧、本体状态、模型查询、每个动作块、队列事件和控制器实际命令放到统一时钟。[FluxVLA Engine](https://arxiv.org/abs/2609.17210)讨论数据格式、训练、评估、推理运行时与本体接口的贯通；字段应允许重放从观测到执行的整条路径。

**处理与对齐**：为动作块标记预测起点、长度、每步目标时间及被覆盖或取消的命令；对异步系统记录推理与执行重叠。[rMuscle](https://arxiv.org/abs/2609.19104)针对重复工作中的推理效率，[Dense-to-MoE](https://arxiv.org/abs/2609.16503)研究紧凑部署；[高效 VLA 对照](https://arxiv.org/abs/2609.13984)把动作头、模型规模和设备延迟配对。若缺设备、批量大小、控制周期和通信条件，吞吐数字不可比较。

**动作质量**：驾驶连续轨迹也属于执行链；[DiffAdapterVLA](https://arxiv.org/abs/2609.15322)在驾驶 VLM 中生成连续轨迹。不同任务应保留各自的安全边界与坐标系。

![VLA 执行日志绑定观测时刻、预测动作块、调度信息与实测轨迹](/images/docs/vla-realtime-execution-data-contract.svg)

## 最小字段契约

字段名是建议的数据接口，不表示所引论文使用完全相同的文件格式。

| 字段 | 记录内容 | 检查重点 |
| --- | --- | --- |
| episode_id / query_id | 任务与一次模型调用 | 控制回放可定位 |
| observation_at / observation_id | 输入帧和本体状态时间 | 推理所见不是未来状态 |
| model_version / runtime | 权重、推理引擎、设备 | 不同部署可配对 |
| chunk_id / action_steps | 动作序列、单位、坐标系 | 每步目标时刻明确 |
| queued_at / emitted_at / applied_at | 排队、输出与执行时间 | 端到端动作年龄可算 |
| override / cancel_reason | 重规划、跳步与安全覆盖 | 实际命令不被预测命令替代 |
| measured_motion / contact | 实测轨迹与接触事件 | 检测块边界急动 |
| outcome / failure_type | 任务成功、停机、碰撞等 | 按延迟区间分层 |

## 质控与评估

离线检查时间戳单调、动作顺序、单位、块重叠和取消命令是否被误当成已执行。线上同时报告模型推理、传输、排队与控制生效延迟，以及末端速度、加速度、急动度和任务成功。[部署比较](https://arxiv.org/abs/2609.14146)和[高效 VLA 对照](https://arxiv.org/abs/2609.13984)强调时间与任务结果必须联报；[GROOVE](https://arxiv.org/abs/2609.13695)提示运动质量可能在动作块边界恶化。

![VLA 实时执行分别检验端到端延迟、运动质量和任务结果](/images/docs/vla-realtime-execution-data-evaluation.svg)

## 数据集使用边界

同一个动作误差在自由空间和接触瞬间后果不同，不能用全轨迹平均误差替代阶段评估。加速方法可能改变控制频率、动作年龄或动作分布；发布数据时需保留原始策略输出与控制器实际执行的两条轨迹。跨设备结果应明确硬件、运行时与控制周期。

## 本主题论文

以下论文按清单中的主主题归档。跨主题使用时，应重新核对任务、传感器和评测口径。

- [FlashVLA: Streaming Action Decoding for Fast and Asynchronous VLA Inference](https://arxiv.org/abs/2608.27384)（2608.27384）
- [FluxVLA Engine: A One-Stop VLA Engineering Platform for Embodied Intelligence](https://arxiv.org/abs/2609.17210)（2609.17210）
- [Dense to MoE Adaptation for Compact Vision Language Action Policies](https://arxiv.org/abs/2609.16503)（2609.16503）
- [Uncertainty-Guided Sparse Refinement for Action Chunking Transformer Policies](https://arxiv.org/abs/2609.15840)（2609.15840）
- [Planning in the Backbone: DiffAdapterVLA for Native Continuous Trajectory Generation with Driving VLMs](https://arxiv.org/abs/2609.15322)（2609.15322）
- [When Faster VLA Deployment Changes Closed-Loop Behavior: Task Success-Latency Analysis of SmolVLA Across PyTorch and ONNX Variants](https://arxiv.org/abs/2609.14146)（2609.14146）
- [What Makes an Efficient VLA? Navigating Action-Head Design, Scaling, and Latency](https://arxiv.org/abs/2609.13984)（2609.13984）
- [GROOVE: Geometry-Guided Reduction of Operational-Space Jerk in VLA Execution](https://arxiv.org/abs/2609.13695)（2609.13695）
- [rMuscle: Robotic Muscle Memory for Efficient Vision-Language-Action Model Inference](https://arxiv.org/abs/2609.19104)（2609.19104）
- [GeoAAC: Geometry-Based Adaptive Action Chunking from Denoising Trajectories in VLA Policies](https://arxiv.org/abs/2609.20776)（2609.20776）
- [SkipVLA: Skipping VLA Steps with Classical Planning for Fast Robot Manipulation](https://arxiv.org/abs/2609.20648)（2609.20648）
