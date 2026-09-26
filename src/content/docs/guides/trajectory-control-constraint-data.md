---
title: 轨迹规划、控制与物理约束数据
description: 统一目标、候选轨迹、接触模式和执行反馈，支持规划复现与真实可行性检查。
---

规划数据的基本问题是：在给定初态和约束下，机器人为什么选择这条轨迹，执行后是否仍满足约束。**接触模式**表示哪些部位与环境接触以及接触何时切换。仅保存最终关节轨迹会丢失候选方案、接触模式、优化目标及不可行原因。[CoMET](https://arxiv.org/abs/2609.21803)并行评价接触模式，[接触隐式轨迹优化](https://arxiv.org/abs/2609.28299)把接触选择纳入优化并试图找到多个不同策略；两者都说明一个场景可以有多条合理解。

![规划数据从任务与场景状态、候选轨迹到控制执行和反馈的流程](/images/docs/trajectory-control-constraint-data-flow.svg)

## 输入、候选与执行应分层记录

- **任务与场景**：保存目标位姿、机器人形态、障碍/物体几何、坐标系、动力学参数和不确定性。对物体可移动或易碎场景，几何碰撞不是二值风险；[CaSCo](https://arxiv.org/abs/2609.18910)考虑接触后的次生物体碰撞，应记录场景物体的风险属性与预测后果。
- **候选轨迹**：保存采样种子、时间参数化、控制点、成本各项、约束违反量、求解状态、接触模式和筛选原因。[Primitive-Informed MPC](https://arxiv.org/abs/2609.14868)用低维手指运动基元引导采样并剔除不可行轨迹，训练数据不能只保留被选中样本。
- **执行反馈**：保存名义轨迹、实际状态、控制命令、估计误差、接触力和重新规划触发点。[软执行器任务空间控制](https://arxiv.org/abs/2608.27186)使用模型估计与反馈，[Gripper-Aware Packing](https://arxiv.org/abs/2609.22062)结合感知、放置优化和力引导执行；两者都需要把计划与实际轨迹一一对应。

![轨迹规划问题中目标、决策变量、约束、求解器和执行反馈的字段关系](/images/docs/trajectory-control-constraint-data-contract.svg)

## 最小数据契约

| 层级 | 建议字段 | 必须明确 |
| --- | --- | --- |
| 问题实例 | `scene_id`, `robot_model`, `initial_state`, `goal`, `geometry_version` | 坐标系、单位和几何误差 |
| 约束 | `constraint_set_id`, `collision_margin`, `contact_rules`, `kinematic_limits`, `dynamics_model` | 硬约束、软成本及优先级 |
| 候选方案 | `plan_id`, `seed`, `waypoints`, `contact_mode`, `objective_terms`, `feasibility_status` | 不可行与求解超时分开 |
| 执行结果 | `executed_states`, `control_commands`, `replan_events`, `contact_observations`, `outcome` | 计划偏差与最终任务结果分开 |

[Amplify](https://arxiv.org/abs/2609.28377)把动力学、轨迹和参考运动算法写成优化模型中的约束，以提高机器人非线性规划问题的复现性。发布数据时对应保存变量定义、目标项、约束表达、求解器及版本，而不只是轨迹输出。车辆语义推理到连续动作 [LaPla](https://arxiv.org/abs/2609.04070)也要求记录离散表达与物理可执行轨迹之间的映射。

## 质检、切分与评估

![规划评估按可行性、接触后果、执行偏差和计算预算分层](/images/docs/trajectory-control-constraint-data-evaluation.svg)

离线检查运动学极限、轨迹连续性、碰撞余量、接触模式一致性及成本项重算是否匹配；真实执行检查规划坐标与传感器时钟、力矩/速度限幅和环境变化。接触可以增加支撑又压缩末端可达性，[CTCS](https://arxiv.org/abs/2609.30140)据此评估接触候选，质检要区分“接触可建立”和“建立后仍能完成任务”。

报告规划成功率、求解时间、约束违反、路径/能耗、真实执行误差与任务完成率。按场景几何、物体实例、约束组合、机器人形态和接触模式切分；相同问题的不同随机种子不能跨训练与测试。施工机器人 [CAST](https://arxiv.org/abs/2609.24841)具有多机器人与缆线约束，弹簧足四旋翼 [能量高效跳跃](https://arxiv.org/abs/2609.15447)具有混合动力学，这些域的结果应保留各自物理条件，避免单一“轨迹长度”掩盖关键失败。

## 本月论文索引

本页索引收录 2026-08-27 至 2026-09-27 发表、归入本主题的论文。

- [Task-space model-based control of pneumatic soft actuators](https://arxiv.org/abs/2608.27186)（2608.27186）
- [Continuous Actions from Discrete Minds: Latent-Aligned Planning for End-to-End Autonomous Driving](https://arxiv.org/abs/2609.04070)（2609.04070）
- [Learning to Exploit Passive Dynamics for Energy-Efficient Target Hopping of a Spring-Legged Quadcopter](https://arxiv.org/abs/2609.15447)（2609.15447）
- [Dynamics-Informed Reinforcement Learning for Agile and Energy-Efficient Locomotion of a Monopedal Hopping Quadcopter](https://arxiv.org/abs/2609.15399)（2609.15399）
- [Primitive-Informed Sampling-Based MPC for Multi-Fingered Dexterous Manipulation](https://arxiv.org/abs/2609.14868)（2609.14868）
- [CaSCo: Cascade-Aware Soft-Collision Motion Planning](https://arxiv.org/abs/2609.18910)（2609.18910）
- [Gripper-Aware Automatic Dense Packing of Irregular Objects](https://arxiv.org/abs/2609.22062)（2609.22062）
- [Contact-Rich Motion Planning via GPU-Parallel Mode Evaluation](https://arxiv.org/abs/2609.21803)（2609.21803）
- [CAST: Collision-Aware Assembly with Construction Robots using Simultaneous Trajectory Estimation and Planning](https://arxiv.org/abs/2609.24841)（2609.24841）
- [Amplify: A Lightweight Library for Reproducible Nonlinear Programming Problems in Robotics](https://arxiv.org/abs/2609.28377)（2609.28377）
- [Contact-Implicit Stein Projected ADMM for Discovery of Diverse Contact-Rich Manipulation Strategies](https://arxiv.org/abs/2609.28299)（2609.28299）
- [ReVAMP: Vector-Accelerated Motion Planning for Kinematically-Constrained Systems via Reparameterization](https://arxiv.org/abs/2609.30213)（2609.30213）
- [Contact as a Decision Variable: Capability-Tradeoff Contact Selection for Legged Loco-Manipulation](https://arxiv.org/abs/2609.30140)（2609.30140）
