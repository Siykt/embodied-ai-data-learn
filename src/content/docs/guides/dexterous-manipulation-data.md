---
title: 灵巧操作与双臂装配数据
description: 整理灵巧手、手内操作与双臂装配的采集、接触对齐、标注、质检和泛化评估。
---

灵巧操作数据记录的不只是“手指移动到哪里”，还包括物体在掌内如何运动、哪些接触正在承重或传力，以及双臂在装配中如何分工。**手内操作**指不释放原有抓持，通过手指协调改变物体相对手掌的位姿。手内六维位姿到达把目标定义为相对手掌的位置和朝向 [POISE](https://arxiv.org/abs/2609.13761)；手内装配则要求同一只手的手指同时稳定两个零件并完成配合 [Assembling Two Parts in One Hand](https://arxiv.org/abs/2609.10137)。这两类任务不能只用最终抓取成功标注代替过程数据。

![灵巧操作数据从多源采集到接触事件与训练窗口的流程](/images/docs/dexterous-manipulation-data-flow.svg)

## 采集与处理

- **观测输入**：同步保存手眼与外部相机、手指关节位置与速度、执行器命令、腕部和物体位姿；有条件时记录力、触觉或近距几何。手部遮挡会影响视觉接触判断，[ProxiDex](https://arxiv.org/abs/2609.16586) 因而用手物距离构造交互线索，但距离仍不能直接充当真实接触力。
- **机构参数**：逐次记录手型、关节轴、驱动耦合、腱绳路由和标定版本。腱驱动手的一个执行器可能影响多个关节，[Aero Hand Open](https://arxiv.org/abs/2608.28578) 与[形态和驱动分析](https://arxiv.org/abs/2609.05206)都说明了仅以“关节目标角”描述动作会丢失执行约束。
- **时间与坐标对齐**：相机曝光、状态采样和控制命令各保留原始时间戳；将物体位姿变换到掌心、腕部及世界坐标系时保存变换链和不确定性。重采样应标出插值点，不能把不同步造成的穿透误当成接触。
- **事件标注**：区分接近、初次接触、稳定抓持、手内重定位、滑移、释放和重新抓取。装配另外标注零件角色、支撑臂、插入阶段和卡滞/错位原因；[BrickCraft-Duo](https://arxiv.org/abs/2609.28281) 的双臂技能组合提示应保存步骤依赖与角色切换。

## 最小数据契约

![灵巧操作 episode 中机构、动作、接触和任务标签的字段关系](/images/docs/dexterous-manipulation-data-contract.svg)

| 层级 | 建议字段 | 必须说明的语义 |
| --- | --- | --- |
| Episode | `task_id`, `object_ids`, `hand_model`, `calibration_id`, `initial_grasp_id` | 物体实例、手型及初始抓持如何形成 |
| Step | `timestamp`, `camera_frames`, `joint_state`, `actuator_command`, `wrist_pose`, `object_pose` | 控制命令是位置、速度、力矩还是腱长 |
| 接触事件 | `finger_id`, `object_part_id`, `contact_region`, `slip_flag`, `confidence` | 由传感器实测、几何推断还是人工核验 |
| 任务结果 | `goal_pose`, `assembly_stage`, `success`, `failure_reason` | 位姿误差、配合容差与完成判据 |

目标约束也应成为数据字段，而不是散在文本指令里：接近方向、允许接触区域、腕部轨迹及功能手型可以组合，[ConGraspXL](https://arxiv.org/abs/2609.16319)针对这些条件生成抓取动作；[三点抓取接口](https://arxiv.org/abs/2609.24896)则把候选接触点与局部闭环控制连接起来。可动关节物体还需记录物体自身的关节状态和功能抓点，[ArtManip](https://arxiv.org/abs/2609.12498)强调其对跨实例泛化的重要性。

## 质检、评估与数据集使用

![灵巧操作按物体、手型、接触和任务阶段进行质量与泛化评估](/images/docs/dexterous-manipulation-data-evaluation.svg)

逐帧检查位姿跳变、运动学越界、手物几何穿透、接触状态与力信号矛盾；按 episode 检查目标是否真正达到，避免把“视觉看似插入”标成装配成功。测量接触或装配容差时应注明传感器精度和人工复核规则。

训练窗口应覆盖接触前、接触瞬间与稳定阶段，保留失败与恢复样本。评估分开报告物体位姿误差、抓持稳定性、接触违规、步骤成功率及完整任务成功率。按物体实例、材质、目标位姿、手型和装配结构切分，避免同一 CAD 模型的近似姿态流入训练与测试。跨本体双臂迁移可参考 [VLBiMan++](https://arxiv.org/abs/2609.14310) 对新物体、场景和执行条件的设置；手的自支撑运动 [Fingers as Legs](https://arxiv.org/abs/2609.17172)及可重构连续体机器人 [Tensegrity Continuum Robots](https://arxiv.org/abs/2608.27221)则提醒数据契约要写明形态和任务边界。

## 本月论文索引

本页索引收录 2026-08-27 至 2026-09-27 发表、归入本主题的论文。

- [Tensegrity Continuum Robots Enable Task-Adaptive Morphologies for Cooperative Behaviors](https://arxiv.org/abs/2608.27221)（2608.27221）
- [Aero Hand Open: A Simulation-Ready Tendon-Driven Hand for Dexterous Manipulation Learning](https://arxiv.org/abs/2608.28578)（2608.28578）
- [Morphology and actuation as inductive biases in robotic hand manipulation](https://arxiv.org/abs/2609.05206)（2609.05206）
- [Assembling Two Parts in One Hand](https://arxiv.org/abs/2609.10137)（2609.10137）
- [Fingers as Legs: Learning Self-Supported Locomotion and Manipulation with an Anthropomorphic Hand](https://arxiv.org/abs/2609.17172)（2609.17172）
- [ProxiDex: Learning Dynamics-Guided Proximity Policy for Dexterous Manipulation](https://arxiv.org/abs/2609.16586)（2609.16586）
- [ConGraspXL: Controllable Constraint-Conditioned Dexterous Grasping Motion Synthesis](https://arxiv.org/abs/2609.16319)（2609.16319）
- [VLBiMan++: Expanding the Generalization Boundary of Vision-Language Anchored One-Shot Bimanual Manipulation](https://arxiv.org/abs/2609.14310)（2609.14310）
- [Learning In-Hand Object Reaching to General 6D Poses](https://arxiv.org/abs/2609.13761)（2609.13761）
- [ArtManip: Category-Level Articulated In-Hand Manipulation](https://arxiv.org/abs/2609.12498)（2609.12498）
- [Steerable and Reactive Grasping Through Modular Design with a Three-Point Interface](https://arxiv.org/abs/2609.24896)（2609.24896）
- [BrickCraft-Duo: Efficient Dual-Arm Skill Learning and Refinement for Compositional Long-Horizon Assembly](https://arxiv.org/abs/2609.28281)（2609.28281）
