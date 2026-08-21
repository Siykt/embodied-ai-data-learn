---
title: 仿真器与具身数据
description: 横向梳理 MuJoCo、Isaac、Genesis、PyBullet、Gazebo、SAPIEN、Habitat 等主流仿真器的定位、数据产物与选型思路。
---

仿真器是具身智能数据的重要生产层：它可以在可控、可复现的环境里批量生成轨迹、观测、动作、状态、仿真真值和任务标签。但它不是“自动可信的数据集”——不同的仿真器在物理精度、视觉保真、速度规模和生态上差异很大，选型和使用都应该围绕“要生产什么数据、这些数据怎么被消费”来展开。

这篇文档横向整理主流仿真器的定位与资料入口，并从数据角度给出对比、选型和通用数据契约。

## 一句话结论

**仿真器负责“可控地造数据”：提供规模、标签和复现能力；真实数据负责“校准分布”：提供传感器噪声、执行器延迟、失败模式和最终验证。两者互补，不能互相替代。**

![主流仿真器按速度规模与视觉保真度定位](/images/docs/simulators-landscape.svg)

## 全景地图

可以从两个维度理解主流仿真器的差异：

- **速度与并行规模**：同一台机器能同时跑多少个环境、每秒能产出多少步。GPU 并行（MuJoCo MJX、Isaac Lab、Genesis）比单机串行高几个数量级。
- **视觉与传感器保真度**：图像渲染、材质、光照、相机噪声和传感器模型贴近真实世界的程度。

定位是相对的：同一个引擎可以通过开关渲染、物理精度和传感器模型在不同保真度之间移动。下面的表格按数据视角整理了各自的要点。

## 主流仿真器逐个看

### MuJoCo（DeepMind 开源物理引擎）

MuJoCo 以接触建模稳定、速度快、模型格式简洁（MJCF）著称，是 DeepMind 控制套件（dm_control）、robosuite、D4RL 等大量数据集与 benchmark 的底层引擎。3.x 之后原生支持 MJX，可以用 JAX 在 GPU 上并行跑大规模环境。

- 数据视角：非常适合生产**轻量、高频率的状态-动作轨迹**（关节位置/速度、接触力、传感器读数），视觉渲染主要用于回放而非训练。
- 场景即契约：MJCF 场景文件同时是机器人模型、物体布局、传感器和执行器的完整定义，数据集必须记录它的版本或哈希。
- 资料入口：[MuJoCo 文档](https://mujoco.readthedocs.io)、[MuJoCo Menagerie 模型库](https://github.com/google-deepmind/mujoco_menagerie)、[dm_control](https://github.com/google-deepmind/dm_control)。

### Isaac Sim / Isaac Lab（NVIDIA）

Isaac Sim 基于 USD + PhysX + RTX 渲染，提供接近真实的图像、深度、分割和多种传感器仿真；Isaac Lab 在其上提供并行的机器人学习环境，支持强化学习、模仿学习以及 Mimic / DexMimicGen 这类示范扩增工具。适合需要**高保真视觉数据和合成数据集**的项目。NVIDIA 也在推动用 Cosmos 等模型把仿真数据生成规模化。

- 数据视角：数据产物丰富但环境重、版本耦合强（Isaac Lab 与 Isaac Sim 版本必须匹配）。
- 专项整理见[Isaac Lab 与具身数据](/guides/isaac-lab-embodied-data/)。

### Genesis（生成式物理引擎）

Genesis 是 2024 年底开源、由 CMU 等多家机构合作开发的生成式物理引擎。它把物理仿真、视觉渲染（光栅化与 RTX 光线追踪）和生成式能力放在一起：可以用自然语言生成场景、对象和机器人，支持 GPU 并行，还内置了从数据生成策略的“universal data engine”思路。

- 数据视角：适合探索**场景与任务的自动生成、扩增和自动化数据管线**，处于快速演进阶段，使用时要注意版本与 API 变化。
- 资料入口：[Genesis 文档](https://genesis-world.readthedocs.io)、[GitHub 仓库](https://github.com/Genesis-Embodied-AI/Genesis)。

### PyBullet / Bullet

Bullet 是历史悠久的开源物理引擎，PyBullet 是其 Python 绑定，直接支持 URDF 模型和简单的相机、射线传感器。上手快、依赖轻，常用于教学、快速原型和低规模实验。

- 数据视角：适合小规模验证和数据管线原型；物理与渲染精度有限，不适合作为高保真数据源。
- 资料入口：[PyBullet 文档](https://docs.google.com/document/d/10sXEhzFRSnvFcl3XxNGhnD4N2SedqwdhK7dsvKnfChA)、[Bullet 仓库](https://github.com/bulletphysics/bullet3)。

### Gazebo

Gazebo 是 ROS 生态中最常用的机器人仿真平台，支持 SDF/URDF 场景、多传感器（激光、相机、IMU、接触）和物理引擎插件（目前默认 ODE，也支持其他后端）。移动机器人、导航与传感器测试场景中非常常见。

- 数据视角：适合与 ROS 采集、标定和真机工具链打通；环境配置和传感器插件质量直接影响数据可信度。
- 资料入口：[Gazebo 文档](https://gazebosim.org/docs)、[ROS Integration 文档](https://docs.ros.org/en/ros2/Tutorials/Advanced/Simulators/Gazebo.html)。

### SAPIEN / ManiSkill

SAPIEN 是面向具身智能和机器人学习的交互式物理引擎，强调部件级关节体（如柜门、抽屉、阀门）的交互；ManiSkill 构建在其上，提供大规模操作 benchmark 和标准化评测数据。

- 数据视角：适合生产**带部件级交互标签的操作数据**和参与公开 benchmark 对比。
- 资料入口：[SAPIEN 文档](https://sapien.ucsd.edu)、[ManiSkill](https://maniskill.ai)。

### Habitat（Meta）

Habitat 系列（Habitat Sim / Habitat Lab / Habitat 3.0）主打**高保真视觉导航和家务机器人场景**，提供 photo-real 渲染、多智能体仿真和标准化评测。它也支持用模拟数据做具身任务评估与合成数据。

- 数据视角：适合导航、多智能体和视觉任务的数据生产与评测；物理操作不是它的强项。
- 资料入口：[Habitat 文档](https://aihabitat.org/docs/habitat-lab/)。

### 其他值得了解的

- **robosuite**：基于 MuJoCo 的操作仿真套件，产出与 [robomimic](https://robomimic.github.io) 数据集格式对接，适合模仿学习数据生产。
- **CoppeliaSim（V-REP）**：商业授权友好的通用机器人仿真平台，支持多种物理引擎和 Lua/Python 脚本。
- **AI2-THOR / ThreeDWorld**：室内场景与物理交互仿真，常用于具身视觉与导航研究。

## 从数据角度对比

| 仿真器 | 场景/模型格式 | 物理后端 | 渲染/传感器 | 典型数据产物 | 适合的数据任务 |
| --- | --- | --- | --- | --- | --- |
| MuJoCo / MJX | MJCF（URDF 可转） | 内置接触求解器 | 简单相机、深度、分割 | 高频状态-动作轨迹、接触力、RL 回放 | 操作、灵巧手、轨迹数据集（D4RL/robosuite 风格） |
| Isaac Sim / Lab | USD | PhysX 5 | RTX 光追、RGB/深度/分割、IMU 等 | 高保真合成数据、Mimic 扩增、评测数据 | 高保真视觉数据、合成数据集、策略评测 |
| Genesis | 程序化/生成式 | 内置 + 生成式场景 | 光栅化 + RTX | 自动生成的场景与轨迹 | 场景/任务自动扩增、数据引擎探索 |
| PyBullet | URDF | Bullet | 简单相机 | 小规模轨迹与原型 | 教学、原型、快速验证 |
| Gazebo | SDF/URDF | ODE 等插件 | 激光、相机、IMU、接触 | ROS 风格传感器记录 | 移动机器人、导航、传感器测试 |
| SAPIEN / ManiSkill | SDF/URDF + 部件关节 | 内置 | 光栅化 | 部件级操作轨迹、benchmark 数据 | 操作 benchmark、部件交互 |
| Habitat | 网格/语义场景 | 简化物理 | photo-real RGB/深度/语义 | 导航轨迹、多智能体数据 | 导航、多智能体、视觉评测 |

表格里的“适合的数据任务”是相对判断。实际选型请结合下面的决策流程和项目约束（GPU 预算、团队熟悉度、真实设备型号、训练框架）。

## 怎么选：从数据目标出发

![仿真器选型决策流程](/images/docs/simulator-choice-flow.svg)

1. **先定数据目标**：数据是给训练（RL / 模仿学习）、给评测（benchmark / 闭环评估），还是给下游模型做合成数据集？目标决定保真度和格式要求。
2. **再看任务类型**：导航和移动任务考虑 Habitat、Gazebo；桌面操作考虑 MuJoCo、Isaac；灵巧手考虑 MuJoCo、Isaac + Mimic/DexMimicGen。
3. **然后评估视觉需求**：训练需要真实相机图像时，优先 Isaac Sim / Habitat；只用关节状态和物理交互时，MuJoCo 更快更稳。
4. **最后看规模与生态**：需要万级并行 episode 选 MJX、Isaac、Genesis；需要 ROS 工具链选 Gazebo；需要和 robomimic/robosuite 格式对接选 MuJoCo。

## 通用数据契约

无论用哪个仿真器，产出都应整理成统一的、可追溯的数据对象：

![仿真数据契约：episode 由元数据、观测、动作状态、真值来源和边界质量字段构成](/images/docs/simulator-data-contract.svg)

- **元数据**：任务、场景、机器人、引擎与资产版本、随机种子、生成脚本提交版本。
- **观测**：RGB / 深度 / 分割、关节状态、IMU、接触，并写明单位、坐标系和控制频率。
- **动作与状态**：动作表示方式（关节位置/速度/力矩/末端位姿）、生效时间、奖励、terminated / truncated 的区分。
- **真值与来源**：物体位姿、接触、分割 ID 等“仿真真值”必须标注来源（引擎直接输出，还是由观测推断）。
- **边界与质量**：episode 起始、终止原因、成功标记、质检状态。

没有这些信息，仿真数据虽然可以读取，却无法复现、无法解释异常、也无法和真实数据做对照。

## 质量检查清单

- **时间**：观测、动作、状态是否同一时间轴；控制频率是否稳定；是否存在重复或倒退时间戳。
- **坐标**：世界、基座、末端、相机、物体坐标系是否声明；位姿方向和单位是否固定。
- **传感器**：相机分辨率、内参、深度单位、分割 ID、遮挡规则是否随数据保存。
- **物理**：接触、摩擦、关节限位和执行器模型是否与目标真实平台相符；是否出现穿透或非物理抖动。
- **分布**：训练与评估是否按场景、物体、初始状态和任务变体隔离，避免只记住固定布局。
- **迁移**：是否有真实小样本或硬件回放用于比较图像、动作延迟、成功条件和失败原因。

## 仿真数据常见坑

- **把仿真成功率当真实成功率**：仿真环境和真实机器人存在系统性差异，报指标时必须同时报告环境版本、任务定义和尝试次数。
- **过度依赖仿真真值**：仿真里的物体位姿、分割、接触标签很干净，但真实感知不一定能拿到同样的信号，标签分布会偏。
- **忽视版本与 seed**：同一份脚本在不同引擎版本、不同随机种子下可能产出分布完全不同的数据。
- **渲染好看但不物理**：视觉保真高不等于动力学准确；反之动力学准确也不等于图像贴近真实，两者要分开评估。

## 一句话定位

**仿真器是具身数据的“可控生产层”：MuJoCo 提供轻量高频的轨迹，Isaac 提供高保真合成数据，Genesis 探索自动生成，Gazebo/Habitat/SAPIEN 各自服务移动、导航与操作生态；选型围绕数据目标，落盘围绕统一契约，可信度围绕 sim-to-real 对照。**

## 资料来源

- [MuJoCo 官方文档](https://mujoco.readthedocs.io) / [GitHub](https://github.com/google-deepmind/mujoco)
- [MuJoCo Menagerie 模型库](https://github.com/google-deepmind/mujoco_menagerie)
- [Isaac Lab 官方文档](https://isaac-sim.github.io/IsaacLab) / [Isaac Sim 文档](https://docs.isaacsim.omniverse.nvidia.com/latest/index.html)
- [Genesis 文档](https://genesis-world.readthedocs.io) / [GitHub](https://github.com/Genesis-Embodied-AI/Genesis)
- [PyBullet 文档](https://docs.google.com/document/d/10sXEhzFRSnvFcl3XxNGhnD4N2SedqwdhK7dsvKnfChA)
- [Gazebo 文档](https://gazebosim.org/docs)
- [SAPIEN](https://sapien.ucsd.edu) / [ManiSkill](https://maniskill.ai)
- [Habitat 文档](https://aihabitat.org/docs/habitat-lab/)
