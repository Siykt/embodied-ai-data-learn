---
title: MuJoCo 与具身数据
description: 按场景建模、数据采集、导出、质检与评估任务整理 MuJoCo 官方资料及具身数据实践。
---

MuJoCo（Multi-Joint dynamics with Contact）是 Google DeepMind 维护的开源物理引擎，以接触动力学、模型格式和程序接口为核心。它定义了 MJCF 场景格式，也被 dm_control、robosuite 和许多控制任务用作底层引擎；MJX 提供基于 JAX 的批量仿真路径。MuJoCo 是引擎，数据集格式和任务定义通常由上层项目决定。

从具身数据角度看，MuJoCo 最重要的角色是**轻量、高频、可复现的轨迹数据生产层**：它特别适合生成状态-动作轨迹、接触力和 RL 回放数据，也适合在数据管线的早期快速验证动作表示、episode 边界和数据集 schema。

## 先看结论：它在具身数据里做什么

- **上游**是 MJCF 场景与资产：机器人模型、物体、传感器、执行器、相机和任务定义。
- **中间**是引擎循环：观测 → 动作 → 物理推进 → 传感器读数 → 可选渲染。
- **下游**是轨迹、episode、观测、动作、状态、接触力、奖励、终止标记和质量报告。
- **闭环**是用少量真实数据检查接触参数、控制频率和观测噪声，再回写 MJCF 与采样配置。

它的价值是让模型、控制和数据采样可以分别检查。MJCF 是数据契约的重要部分，但还要保存采集脚本、控制频率、随机化、渲染和导出配置，才能复现一条轨迹。

![MuJoCo 从 MJCF 场景到可复用轨迹数据的链路](/images/docs/mujoco-data-flow.svg)

## MuJoCo 在完整仿真链路中的位置

| 技术环节 | MuJoCo 中的对应实现 | 数据工作重点 |
| --- | --- | --- |
| 场景资产与机器人 | MJCF、网格/纹理依赖、Menagerie 模型 | 固定模型和资产哈希，核对导入后的关节与碰撞体 |
| 物理与执行器 | 引擎步进、接触求解、actuator、solver 设置 | 保存控制映射、物理步长与接触参数并做回归 |
| 传感器与渲染 | MJCF sensor、`sensordata`、`Renderer` | 记录布局、相机配置、时间戳和标签来源 |
| 任务与采样 | 项目环境或 dm_control 等上层任务库；MJX 可做批量 rollout | 明确 reset/step、奖励、终止、随机化和动作语义 |
| 记录与评估 | 项目记录器、D4RL 或 robomimic 等格式 | 组装独立 episode，保存模型版本并用真实样本对照 |

这些环节的通用方法分别见[场景与物理配置](/guides/simulation-scene-physics/)、[传感器与时间对齐](/guides/simulation-sensors-timing/)、[任务与数据生成](/guides/simulation-task-generation/)及[验证与真实迁移](/guides/simulation-validation-sim2real/)。MuJoCo 负责其中的物理与传感器计算，任务规则、记录器和数据集准入还需由上层管线明确实现。

## MJCF：场景即数据契约

MJCF 是 MuJoCo 的原生 XML 场景格式。一个 MJCF 文件同时定义了：

```text
mujoco
  asset     网格、材质、纹理（几何与外观）
  worldbody  机器人、物体、场地与全局布局
  joint     关节：hinge / slide / free / ball
  tendon    肌腱与约束（软组织、驱动耦合）
  actuator  执行器：motor / position / velocity / cylinder
  sensor    传感器：关节、力、陀螺、加速度、磁力、深度、IMU 等
  camera    相机：固定或跟随视角
  option / size / default  求解器、时间步与默认参数
```

对数据集来说，**MJCF 和所引用资产要作为数据契约的一部分保存**（文件或可解析的版本与哈希），因为关节类型、执行器模型、接触参数、默认阻尼和限位都会影响轨迹分布。只记录任务名称或机器人名称不足以复现数据。

MuJoCo 也支持从 URDF 导入模型，但 URDF 转 MJCF 会丢失或改写部分信息，转换配置必须随数据记录。

## 能生成哪些数据

### 状态与传感器

每个 step 的核心状态包括：

```text
time       仿真时间
qpos       广义坐标（关节位置）
qvel       广义速度
qacc       广义加速度
ctrl       执行器输入
act        执行器状态（有动态执行器时）
sensordata 所有 sensor 的读数（按 sensor 声明顺序）
qfrc_actuator / qfrc_constraint / qfrc_applied
           不同来源的广义力，不能合并为一个未经说明的 qfrc 字段
```

要注意 `sensordata` 是按传感器地址和维度排列的数组，必须依据模型中的 sensor 定义解析，并写明单位与坐标系。只保存数组而不保存 sensor 布局，会让数据“能读却难用”。`qpos` 也不总是“一关节一数值”，例如自由关节包含平移和四元数；导出时应保存关节名称、类型和切片索引。

### 时间、控制与采样

一次训练样本通常写成 `(观测_t, 动作_t, 观测_t+1)`。记录器要声明观测是在 `mj_step` 前还是后读取，动作是请求值还是实际写入 `ctrl` 的值。物理步长与控制周期可能不同：例如控制器每发出一次动作，引擎推进多个物理步。相机还可能按另一采样率渲染，因此不能仅凭数组下标推断图像、传感器和动作同时发生。

建议每步保存仿真时间、控制步序号、观测采样时间、动作下发时间以及图像帧时间；采样频率或保持策略改变时，应增加配置版本。离线重放时先检查首末状态、动作生效顺序和 episode 长度，再比较奖励或成功率。

### 动作与奖励

控制输入通过 `ctrl` 下发，动作可以是关节位置、速度、力矩或末端增量，取决于执行器类型。强化学习回放通常还会保存：

- `reward`：各奖励项与总和；
- `terminated`：任务自然结束（成功或失败）；
- `truncated`：因时间上限或安全条件被截断。

`terminated` 和 `truncated` 必须分开记录，否则后续训练会把超时误判成失败。

### 渲染与仿真真值

MuJoCo 可通过 Python 的 `Renderer` 离屏生成 RGB、深度和分割图。它同时可以直接读取许多真实世界很难获得的“仿真真值”：物体位姿、接触点与接触力、质心位置、关节内力。这些真值适合做监督标签和自动检查，但要标记来源（引擎直接输出、渲染生成或由观测推断），并且不能假定真实感知也能提供同样干净的信号。

## 常见数据形态

MuJoCo 生态里已经存在一批成熟的数据形态，可以直接参考：

- **D4RL 风格**：历史离线 RL 基准常用 observations、actions、rewards、terminals 等字段；读取现成数据时还要核对具体版本对超时和终止的编码，不应把格式习惯当作统一标准。
- **robosuite / robomimic 风格**：hdf5 按 episode 组织，包含 obs（图像、关节、末端位姿）、actions、states、rewards、dones，并附带环境配置与模式说明；robomimic 可以直接消费这类数据。
- **dm_control**：提供相机渲染、奖励分解和 replay buffer 工具，适合控制与视觉任务的数据生产。

选用哪种形态取决于下游消费方，但无论哪种，都应补充统一的元数据与质量字段（见[仿真数据契约](/guides/simulators-embodied-data/#通用数据契约)）。

## 批量生成与 MJX 的使用边界

当目标是大批量低维状态轨迹，可先在原生 MuJoCo 中固定一个可解释的参考任务，再评估是否迁到 MJX。MJX 的批量运算适合并行 rollout，但它与原生引擎的支持范围、编译开销和数值结果不能直接假定一致；模型特性与性能应查阅 [MJX 官方说明](https://mujoco.readthedocs.io/en/stable/mjx.html)。

迁移时用同一模型、初态和动作序列做小批量对照，报告关键状态、接触事件、终止条件和成功率的差异。大规模生成后的吞吐量应写明是否包含图像渲染与落盘，否则不同实验的“每秒步数”不可比。

## 与真实数据的关系

![MuJoCo 仿真与真实设备之间的差异检查](/images/docs/mujoco-real-check.svg)

MuJoCo 的接触求解器非常稳定，但“稳定”不等于“真实”。常见差异包括：

- **接触参数**：默认的刚度、阻尼（solref/solimp）和摩擦系数可能与真实材质明显不同；
- **关节特性**：阻尼、摩擦、限位、回差和软限位在 MJCF 里是理想化参数；
- **执行器**：真实电机有延迟、饱和和响应特性，MJCF 的 motor 模型更理想；
- **控制频率**：仿真可以轻松跑 500 Hz，真实控制器常受通信和调度限制；
- **观测**：真实传感器有噪声、丢帧和延迟，仿真默认偏干净。

因此更稳妥的使用方式是：用 MuJoCo 快速生成覆盖不同初始条件的大规模轨迹和标签，用真实设备采集少量样本校准接触参数、执行器延迟和观测噪声，并测量仿真与真实的成功率差异。

## 数据落盘建议

建议每个 MuJoCo 数据集至少保存：

```text
dataset
  schema_version
  mujoco_version / mjx_version
  mjcf_model  （版本或哈希，以及导出/转换配置）
  asset_hashes（网格、纹理等外部资产）
  task_id / environment_id
  seed / worker_id
  physics_timestep / control_hz / render_hz
  solver_settings（迭代次数、容差、积分器）
  sensor_layout（顺序、单位、坐标系）
  episodes
    episode_id
    observations / actions / states / rewards
    observation_time / action_time / frame_time
    requested_action / applied_control
    terminated / truncated / end_reason
    success / quality_flags
```

如果输出图像，还要保存相机位姿、内参或可恢复内参的配置、分辨率、渲染设置和深度单位。保留 MJCF、资产、求解器、随机种子与采样配置，才能解释某批轨迹为何异常。

![仿真 episode 数据契约中的元数据、观测动作、真值和质量字段](/images/docs/simulator-data-contract.svg)

## 质量检查清单

- **时间**：观测、动作、状态是否同一时间轴；控制频率是否稳定；是否存在重复或倒退时间戳。
- **边界**：每条 episode 是否有明确开始、自然终止、超时或失败原因；窗口是否跨越 episode。
- **传感器**：`sensordata` 是否按 MJCF sensor 声明顺序解析；单位、坐标系和采样率是否记录。
- **物理**：是否出现穿透、非物理抖动、异常接触力；接触参数是否与目标材质相符。
- **动作**：动作语义是否与执行器类型一致（位置/速度/力矩）；是否记录了动作生效时间。
- **复现**：抽取固定种子的 episode 重跑，核对模型哈希、初态、前若干步状态和结束原因；跨原生 MuJoCo 与 MJX 时分别报告差异。
- **分布**：训练和评估是否按场景、物体、初始状态和任务变体隔离。
- **迁移**：是否有真实小样本用于比较接触、延迟、成功条件和失败原因。

## 按数据任务查资料

| 要解决的问题 | 优先资料 | 读完后应确定的内容 |
| --- | --- | --- |
| 场景、机器人与传感器如何定义 | [MJCF XML Reference](https://mujoco.readthedocs.io/en/stable/XMLreference.html)、[Modeling](https://mujoco.readthedocs.io/en/stable/modeling.html) | 关节、执行器、接触、sensor 布局及资产版本 |
| 每步状态和控制如何读取 | [Python API](https://mujoco.readthedocs.io/en/stable/python.html)、[Simulation](https://mujoco.readthedocs.io/en/stable/programming/simulation.html) | `MjModel`、`MjData`、步进与采样时序 |
| 物理字段与接触如何解释 | [API Types](https://mujoco.readthedocs.io/en/stable/APIreference/APItypes.html)、[Computation](https://mujoco.readthedocs.io/en/stable/computation/index.html) | 状态维度、接触和力的来源、求解设置 |
| 大规模生成是否选 MJX | [MJX 官方说明](https://mujoco.readthedocs.io/en/stable/mjx.html) | 支持范围、批量策略、性能与数值对照 |
| 从模型和现成任务起步 | [MuJoCo Menagerie](https://github.com/google-deepmind/mujoco_menagerie)、[dm_control](https://github.com/google-deepmind/dm_control) | 可复用资产、任务定义和许可条件 |
| 消费已有轨迹数据 | [D4RL](https://github.com/Farama-Foundation/D4RL)、[robosuite](https://robosuite.ai)、[robomimic](https://robomimic.github.io) | episode 结构、终止语义和导出格式 |

如果数据目标以多相机视觉、USD 资产和大规模渲染为主，可结合[Isaac Lab 与具身数据](/guides/isaac-lab-embodied-data/)比较；两者之间迁移数据时，先统一动作语义、坐标系、时间轴和成功条件。

## 一句话定位

**MuJoCo 在具身数据中的角色，是轻量、高速、可复现的轨迹与接触数据生产层；它为数据管线和训练提供规模与迭代速度，而真实数据负责校准接触、延迟与噪声并完成最终验证。**

## 资料来源

本文的模型、状态与步进说明以 [MuJoCo 官方文档](https://mujoco.readthedocs.io/en/stable/)为准；应用与数据格式示例见上方资料表。版本变化以 [MuJoCo GitHub 发布记录](https://github.com/google-deepmind/mujoco/releases)为准。
