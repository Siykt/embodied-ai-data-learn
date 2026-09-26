---
title: 特定行业具身数据设计
description: 将工程机械、医疗、空中、水下、空间与微流控任务中的环境约束写进数据契约。
---

行业场景中的“动作”通常带着设备、材料与法规边界。轮式装载机铲料、手术器械切除组织、水下夹持湿滑物体和实验室液滴移动，都不能只用通用相机帧与末端位姿描述。数据集的首要问题是确定任务特有的可观测量、隐藏状态、危险条件和验收证据，再把它们接入统一的 episode 结构。

![行业具身数据从场景特有传感、物理事件到通用 episode 的映射流程](/images/docs/domain-specific-embodied-data-flow.svg)

## 按行业补充关键观测

- **工程机械**：保存前后相机、激光雷达（LiDAR，测量周围距离与形状）、车体姿态、液压执行状态、铲斗/机械臂载荷与作业区地形。[sensVLA](https://arxiv.org/abs/2609.17021)将前后 LiDAR 融合的鸟瞰几何送给动作分支，[IL-ACT](https://arxiv.org/abs/2609.16696)在大型挖掘机示教策略后加入自适应笛卡尔跟踪。两者均需要记录视觉语义、几何和执行延迟的对齐关系。
- **医疗与软组织**：保存图像、深度、组织几何版本、器械位置、力/力矩和切除阶段；标注变形、遮挡及边缘确认。[自主肾部分切除](https://arxiv.org/abs/2609.16186)通过部分点云推断术中三维结构；[颅内力传感平台](https://arxiv.org/abs/2609.14198)在离体牛脑模型中验证力测量。后者提供程序模拟环境中的力数据，不能等同临床患者数据。
- **流体与微流控**：[液滴自主导航](https://arxiv.org/abs/2609.16369)用顶视相机追踪液滴和双轴倾斜控制，在润滑膜厚度、接触角等状态不可观测时学习控制。样本应保存液滴轮廓、几何通道、倾角命令、帧间延迟与路径成功判据，并记录这些隐藏变量未被直接测量。
- **空中与水下**：记录飞行姿态、推拉载荷、风/水流、接触或抓取模式与安全停机。[DuctAM](https://arxiv.org/abs/2609.15861)研究持续水平推拉，[水下斜面抓取](https://arxiv.org/abs/2609.12927)研究湿滑条件下的被动自适应夹爪，物理介质应成为切分和评价维度。

![行业 episode 的共享字段与工程、医疗、微流控等扩展字段](/images/docs/domain-specific-embodied-data-contract.svg)

## 共享契约与领域扩展

| 层级 | 共享字段 | 领域扩展示例 |
| --- | --- | --- |
| 来源 | `domain`, `site_id`, `device_model`, `calibration_id`, `operator_id` | 液压机型、手术平台、流体介质 |
| 观测 | `timestamp`, `sensor_refs`, `pose`, `command`, `uncertainty` | 组织点云、倾角、推进器电流 |
| 物理事件 | `contact`, `force`, `material_state`, `mode_transition` | 切割、液滴钉扎、桨叶入水 |
| 结果 | `goal`, `success`, `failure_reason`, `safety_event`, `reviewer` | 切除边界、铲装量、液滴到达 |

领域扩展字段要带单位、采样率、校准方法与缺失值语义。空间机器人综述 [AI-Enabled Space Robot Operations](https://arxiv.org/abs/2609.16880)讨论任务数据稀缺、特殊动力学与机载资源约束；这类数据还应保存通信延迟、仿真假设和任务环境来源。

## 质量控制、评估与复用

![行业数据评估按域内有效性、跨设备迁移和真实物理风险展开](/images/docs/domain-specific-embodied-data-evaluation.svg)

先做传感器标定与物理量合理性检查，再核对事件标签是否由独立证据支持。跨域复用时保留原始单位和坐标系，另给标准化视图；不要把“没有力传感器”编码为零力。按站点、设备、材料、操作者和日期切分，避免同一批样本的近似轨迹泄漏。评估应同时报告任务完成、关键物理约束、失败类型和人工复核比例。[REEF](https://arxiv.org/abs/2609.14254)依赖真实流体结构交互平台，[MagBot](https://arxiv.org/abs/2609.12883)涉及磁悬浮搬运转抓取，[第一视角空中集群操控](https://arxiv.org/abs/2609.18881)涉及个体化体态标定；这些能力各需自己的环境与控制字段，不能被通用成功率替代。

## 本月论文索引

本页索引收录 2026-08-27 至 2026-09-27 发表、归入本主题的论文。

- [sensVLA: Spatially-Grounded Vision-Language-Action Model for Autonomous Wheel Loader](https://arxiv.org/abs/2609.17021)（2609.17021）
- [Artificial Intelligence-Enabled Space Robot Operations: Technologies, Challenges and Prospects](https://arxiv.org/abs/2609.16880)（2609.16880）
- [IL-ACT: Imitation Learning with Adaptive Cartesian Tracking Control for a 30-ton Excavator](https://arxiv.org/abs/2609.16696)（2609.16696）
- [Autonomous Droplet Navigation via Model-Based Reinforcement Learning](https://arxiv.org/abs/2609.16369)（2609.16369）
- [Occupancy Network-Guided Autonomous Robotic Partial Nephrectomy](https://arxiv.org/abs/2609.16186)（2609.16186）
- [DuctAM: A Duct-Assisted Quadrotor-Based Aerial Manipulator Enabling High-Force Push-and-Pull Interactions](https://arxiv.org/abs/2609.15861)（2609.15861）
- [Embracing Flow Unsteadiness: A High-Throughput Learning Platform Enables Vortex-Exploiting Bioinspired Propulsion](https://arxiv.org/abs/2609.14254)（2609.14254）
- [Novel Ex-vivo Calf Brain Model with Integrated Sub-Skull Force Sensors to Access Simulated Neurosurgical Procedures](https://arxiv.org/abs/2609.14198)（2609.14198）
- [Robust Underwater Grasping of Sloped Objects with a Waterproof Passive Adaptive Gripper](https://arxiv.org/abs/2609.12927)（2609.12927）
- [From Transportation to Manipulation: Enabling Grasping in Magnetic Robotics](https://arxiv.org/abs/2609.12883)（2609.12883）
- [Body-Motion Control of a Simulated Aerial Swarm from a First-Person View](https://arxiv.org/abs/2609.18881)（2609.18881）
- [A Switched Adaptive Control Framework for Aerial Manipulators Under Dynamic Transitions](https://arxiv.org/abs/2609.24761)（2609.24761）
