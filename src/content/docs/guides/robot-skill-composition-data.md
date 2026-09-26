---
title: 机器人技能组合与任务过程数据
description: 设计子任务、前置条件、几何契约与技能结果的可复用数据表示。
---

长任务不是把多个短动作串起来就能成功。机器人必须知道每步的前置条件、对象关系、结束信号，以及失败后应返回哪个阶段。[神经符号过程推理](https://arxiv.org/abs/2609.05369)把任务图和程序记忆用于长程操作，[SUN](https://arxiv.org/abs/2608.31167)用带类型的程序保存控制和学习之间的任务语义，[动作前置条件研究](https://arxiv.org/abs/2609.16056)分析符号知识放在控制链不同位置的影响。数据应保存任务结构与物理结果，而不只存动作序列。

![机器人从语言任务到任务图、技能接口、执行核验的组合流程](/images/docs/robot-skill-composition-data-flow.svg)

## 概念与数据问题

技能是可复用的短程行为单元；任务图描述技能的依赖、分支和完成条件；几何契约定义技能必须获得哪些点、法向、接触面或目标位姿。[ManiSkillFormer](https://arxiv.org/abs/2609.16331)明确用任务条件几何契约连接感知与动作，[Show-Harness](https://arxiv.org/abs/2609.10522)使用离散语义动作接口与本体解释器，[KINO](https://arxiv.org/abs/2609.18869)以关键帧连接 VLM 规划和全身控制。接口字段不能只写技能名称，还应能由传感器核验。

## 采集、处理与对齐

**采集与标注**：记录原始任务指令、场景关系、每步技能 ID、输入参数、前置条件、实际动作和后置状态。[场景重排](https://arxiv.org/abs/2608.27371)在第一视角观测与俯视目标布局之间建立目标关系；[CAD 关系学习与装配规划](https://arxiv.org/abs/2609.17263)从 CAD 提取装配关系；[场景图充分性研究](https://arxiv.org/abs/2609.15587)提醒只保留当前任务所需关系，也需记录被裁剪信息的依据。

**处理与执行**：将动作轨迹切为技能段，保留关键帧与分支条件；按对象与关系重新组合训练/测试任务。[多机器人任务与运动规划](https://arxiv.org/abs/2609.18813)涉及不同机器人子集参与的转换，故执行者和共享资源也是任务接口的一部分。[本地编程代理](https://arxiv.org/abs/2609.26499)探索由语言模型生成、执行与调试操控程序，新生成技能应记录代码版本、调用参数和真实执行结果。

![任务图、前置条件、技能参数和实际结果之间的数据契约](/images/docs/robot-skill-composition-data-contract.svg)

## 最小字段契约

字段名是建议的数据接口，不表示所引论文使用完全相同的文件格式。

| 字段 | 记录内容 | 检查重点 |
| --- | --- | --- |
| task_id / task_graph_version | 任务图及版本 | 节点和边可复现 |
| step_id / skill_id | 技能调用与顺序 | 切段边界明确 |
| preconditions / evidence | 对象、关系、资源等前置条件 | 每项可由观测核验 |
| object_ids / geometry | 关键点、法向、位姿与关系 | 坐标系、单位和可见性记录 |
| actor_robot_ids | 执行机器人及共享资源 | 多机器人冲突可追踪 |
| action_trace / keyframes | 控制轨迹及关键帧 | 计划与实测区分 |
| postconditions / branch | 结束条件与后继分支 | 失败可回退 |
| program_version / outcome | 生成程序或技能版本及结果 | 成功和异常同时保留 |

## 质控与评估

首先校验任务图无不可达节点和相互矛盾的条件；其次检查前置条件是否真的可从感知数据判断；最后让组合任务在新物体、新顺序与新机器人上闭环执行。[ManiSkillFormer](https://arxiv.org/abs/2609.16331)的几何接口、[KINO](https://arxiv.org/abs/2609.18869)的关键帧接口和[过程记忆](https://arxiv.org/abs/2609.05369)提供不同中间表示，但均需要阶段级错误归因。报告每步通过率、条件误判、分支选择和最终任务成功，避免仅用整段成功掩盖某个接口长期失效。

![技能组合评估按接口有效性、组合泛化和长程执行成功分层](/images/docs/robot-skill-composition-data-evaluation.svg)

## 数据集使用边界

人工规划的任务图可能含未观察到的隐含状态；模型生成的程序可能调用不存在或不安全的动作。数据使用者应保留前置条件的证据链接，并在执行端重新检查。仿真可用于覆盖大量组合，但接触、遮挡和资源竞争须在真实环境另测。不同本体的同名技能只有在动作目标和结束条件一致时才可合并。

## 本主题论文

以下论文按清单中的主主题归档。跨主题使用时，应重新核对任务、传感器和评测口径。

- [Embodied Scene Rearrangement Planning](https://arxiv.org/abs/2608.27371)（2608.27371）
- [SUN: Persistent Programs For Language-Grounded Control-to-Learning-to-Real Policies](https://arxiv.org/abs/2608.31167)（2608.31167）
- [Towards Neuro-Symbolic Procedural Reasoning for Long-Horizon Vision-Language-Action Manipulation](https://arxiv.org/abs/2609.05369)（2609.05369）
- [Show-Harness: Just a VLM Agent Can Play Robots](https://arxiv.org/abs/2609.10522)（2609.10522）
- [CAD-Based Relation Learning and Geometric-Symbolic Planning for Robotic Assembly](https://arxiv.org/abs/2609.17263)（2609.17263）
- [ManiSkillFormer: Demonstration-Free Compositional Manipulation via Task-Conditioned Geometric Contracts](https://arxiv.org/abs/2609.16331)（2609.16331）
- [An Information-Space Perspective to Scene Graph Sufficiency for Robotic Task Planning](https://arxiv.org/abs/2609.15587)（2609.15587）
- [Managing Action Preconditions in Neuro-Symbolic RL: Three Placement Strategies for Embodied Agents](https://arxiv.org/abs/2609.16056)（2609.16056）
- [KINO: A Keyframe Interface for VLM Planning and Whole-Body Control in Humanoid Loco-Manipulation](https://arxiv.org/abs/2609.18869)（2609.18869）
- [Asymptotically Optimal Multi-Robot Task and Motion Planning](https://arxiv.org/abs/2609.18813)（2609.18813）
- [Generalizing Manipulation Skills with a Local Coding Agent](https://arxiv.org/abs/2609.26499)（2609.26499）
