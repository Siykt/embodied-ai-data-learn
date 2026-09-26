---
title: 可变形物体与材质状态数据
description: 描述布料、线缆、土壤和软体机器人中的形状、材质与接触演化。
---

布料、线缆、土壤和软体机身没有一个足以描述全过程的刚体位姿。相同动作作用于不同材料或不同初始褶皱，结果可能完全不同。[在线材质估计与扩散策略](https://arxiv.org/abs/2609.12634)以材料标签条件化线状物体塑形，[土壤操作](https://arxiv.org/abs/2609.12677)关注可转移的材质状态，[部分观测下的完整形状估计](https://arxiv.org/abs/2609.10308)强调遮挡部分对控制的影响。数据必须同时保存形状、材料、接触和动作时间序列。

![可变形物体数据从形状采集、材质估计到动作对齐和真实迁移的流程](/images/docs/deformable-material-state-data-flow.svg)

## 概念与数据问题

可变形状态可表示为网格、点云、粒子、中心线或关键点；材质状态可包括刚度、弹性、摩擦与含水等任务相关量。某些值不可直接测量，应保存估计方法和置信度。[ChainSplat](https://arxiv.org/abs/2608.28570)从多视角 RGB 视频学习线状物体几何与动力学，[SWIM](https://arxiv.org/abs/2609.17035)将视觉、语言与软体本体感知用于全身交互；两者的状态表示不同，合并数据前要明确坐标、拓扑和可观测范围。

## 采集、处理与对齐

**采集**：保留多视角视频、深度或几何真值（若可得）、工具/机器人动作、接触位置和目标形状。[FoldNet++](https://arxiv.org/abs/2609.12433)提供跨机器人、衣物和环境资产的合成折叠数据；[FolDeX](https://arxiv.org/abs/2609.10243)强调长程真实可变形操作基准。合成与真实样本应分开标记，不能把仿真形状标签视作实物精确真值。

**处理与对齐**：对线缆保存中心线、端点及自遮挡；对布料保存角点、层叠和折线；对土壤保存表面/体积变化及工具路径。[完整形状估计](https://arxiv.org/abs/2609.10308)在局部观测下推断全形态；[在线材质估计](https://arxiv.org/abs/2609.12634)在执行中更新材料条件。每一步须记录形状估计基于哪几帧、动作何时发生，以及遮挡区间是否被模型补全。

![形状、材质、接触动作和结果形状构成可变形操作样本](/images/docs/deformable-material-state-data-contract.svg)

## 最小字段契约

字段名是建议的数据接口，不表示所引论文使用完全相同的文件格式。

| 字段 | 记录内容 | 检查重点 |
| --- | --- | --- |
| episode_id / object_id | 任务及可变形对象 | 同物体跨动作身份稳定 |
| material_class / properties | 材质类别与已知参数 | 测量和估计来源区分 |
| state_representation / topology | 网格、点、粒子或中心线 | 分辨率与拓扑版本明确 |
| visible_mask / confidence | 可见区域及状态置信度 | 补全区域不伪作观测 |
| tool_pose / contact_region | 工具位姿与接触区域 | 与形状同坐标系 |
| action_at / force_trace | 动作时刻和施力信息 | 与形变序列同步 |
| target_shape / actual_shape | 目标与真实结果 | 指标定义和时间点固定 |
| sim_real_tag / asset_id | 仿真或实物、衣物/环境资产 | 跨域拆分避免泄漏 |

## 质控与评估

质检检查遮挡标记、点身份连续性、尺度、材质来源和动作同步。离线报告可见与不可见区域的形状误差、物体长度或体积守恒等任务适用约束；闭环报告目标形状达成、步骤数、破损和新材料迁移。[FolDeX](https://arxiv.org/abs/2609.10243)表明真实长任务与仿真短任务难度不同，[FoldNet++](https://arxiv.org/abs/2609.12433)适合研究数据规模和资产多样性，[土壤操作](https://arxiv.org/abs/2609.12677)要求按材质状态切分效果。

![可变形数据按形状重建、状态预测及真实操作迁移评估](/images/docs/deformable-material-state-data-evaluation.svg)

## 数据集使用边界

不同材料和形状表示之间不能直接用单一像素误差比较。合成环境可能缺少真实褶皱、摩擦或接触不确定性，发布结果应写清训练与测试的材料、物体和环境拆分。任何由模型补全的隐藏形状都应带置信度；下游策略不应将其当作传感器直接观测到的安全依据。

## 本主题论文

以下论文按清单中的主主题归档。跨主题使用时，应重新核对任务、传感器和评测口径。

- [ChainSplat: A Physics-Inspired Screw-Theoretic Model for Learning Deformable Linear Object Dynamics from Multi-View RGB Videos](https://arxiv.org/abs/2608.28570)（2608.28570）
- [Deformable Object Manipulation under Partial Observability via Real-Time Full-Shape Estimation](https://arxiv.org/abs/2609.10308)（2609.10308）
- [FolDeX: A Physical-World Benchmark for Long-Horizon Robotic Manipulation of Deformable Objects](https://arxiv.org/abs/2609.10243)（2609.10243）
- [SWIM: Vision-Language-Grounded Soft Whole-Body Interactive Manipulation](https://arxiv.org/abs/2609.17035)（2609.17035）
- [Size Doesn't Matter: Material-State Reinforcement Learning for Excavator Transferable Soil Manipulation](https://arxiv.org/abs/2609.12677)（2609.12677）
- [Online Material Estimation for Conditioned Diffusion Policy in Shaping Deformable Linear Objects](https://arxiv.org/abs/2609.12634)（2609.12634）
- [FoldNet++: a Large-Scale Synthetic Dataset for Robotic T-Shirt Folding and Unfolding](https://arxiv.org/abs/2609.12433)（2609.12433）
