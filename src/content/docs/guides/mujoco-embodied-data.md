---
title: MuJoCo 与具身数据
description: 整理 MuJoCo 的定位、MJCF 场景即数据契约、轨迹数据产物、质量控制与 sim-to-real 使用边界。
---

MuJoCo（Multi-Joint dynamics with Contact）是 DeepMind 开源维护的高性能物理引擎，以接触建模稳定、速度快、模型格式简洁著称。它直接定义了 MJCF 场景格式，并被 dm_control、robosuite、D4RL、Humanoid 等大量数据集和 benchmark 用作底层引擎；3.x 之后加入的 MJX 可以用 JAX 在 GPU 上大规模并行。

从具身数据角度看，MuJoCo 最重要的角色是**轻量、高频、可复现的轨迹数据生产层**：它特别适合生成状态-动作轨迹、接触力和 RL 回放数据，也适合在数据管线的早期快速验证动作表示、episode 边界和数据集 schema。

## 先看结论：它在具身数据里做什么

- **上游**是 MJCF 场景与资产：机器人模型、物体、传感器、执行器、相机和任务定义。
- **中间**是引擎循环：观测 → 动作 → 物理推进 → 传感器读数 → 可选渲染。
- **下游**是轨迹、episode、观测、动作、状态、接触力、奖励、终止标记和质量报告。
- **闭环**是用少量真实数据检查接触参数、控制频率和观测噪声，再回写 MJCF 与采样配置。

MuJoCo 不负责“好看”，也不负责“真实”。它的价值是快、稳、可控：一份 MJCF 就是完整的数据契约，容易版本化、容易复现。

![MuJoCo 从 MJCF 场景到可复用轨迹数据的链路](/images/docs/mujoco-data-flow.svg)

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

对数据集来说，**MJCF 本身要作为数据契约的一部分保存**（版本号或文件哈希），因为模型质量直接决定数据质量：关节类型、执行器模型、接触参数、默认阻尼和限位都会影响轨迹分布。改动 MJCF 的一行默认参数，就可能让同一批策略数据失效。

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
qfrc       广义力（接触、约束、驱动等）
```

要注意 `sensordata` 只是按顺序拼接的数组，必须用 MJCF 里的 sensor 声明顺序解析，并写明单位与坐标系。只保存数组而不保存 sensor 布局，是 MuJoCo 数据最常见的“能读但没法用”的原因。

### 动作与奖励

控制输入通过 `ctrl` 下发，动作可以是关节位置、速度、力矩或末端增量，取决于执行器类型。强化学习回放通常还会保存：

- `reward`：各奖励项与总和；
- `terminated`：任务自然结束（成功或失败）；
- `truncated`：因时间上限或安全条件被截断。

`terminated` 和 `truncated` 必须分开记录，否则后续训练会把超时误判成失败。

### 渲染与仿真真值

MuJoCo 提供离屏渲染（通过 render 回调或模型 viewer），可以得到 RGB、深度、分割。它同时可以直接读取许多真实世界很难获得的“仿真真值”：物体位姿、接触点与接触力、质心位置、关节内力。这些真值适合做监督标签和自动检查，但要标记来源（引擎直接输出 vs 由观测推断），并且不能假定真实感知也能提供同样干净的信号。

## 常见数据形态

MuJoCo 生态里已经存在一批成熟的数据形态，可以直接参考：

- **D4RL 风格**：以 dict（或 hdf5）保存 observations、actions、rewards、terminals/truncations，以及环境相关的额外字段，是离线 RL 事实上的常用格式之一。
- **robosuite / robomimic 风格**：hdf5 按 episode 组织，包含 obs（图像、关节、末端位姿）、actions、states、rewards、dones，并附带环境配置与模式说明；robomimic 可以直接消费这类数据。
- **dm_control**：提供相机渲染、奖励分解和 replay buffer 工具，适合控制与视觉任务的数据生产。

选用哪种形态取决于下游消费方，但无论哪种，都应补充统一的元数据与质量字段（见[仿真数据契约](/guides/simulators-embodied-data/#通用数据契约)）。

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
  task_id / environment_id
  seed / worker_id
  timestep / control_hz
  solver_settings（迭代次数、容差、积分器）
  sensor_layout（顺序、单位、坐标系）
  episodes
    episode_id
    observations / actions / states / rewards
    timestamps / control_hz
    terminated / truncated / end_reason
    success / quality_flags
```

保留 MJCF 版本、求解器设置和随机种子是最低要求。没有它们，轨迹无法复现，也无法解释为什么模型在某批数据上表现异常。

## 质量检查清单

- **时间**：观测、动作、状态是否同一时间轴；控制频率是否稳定；是否存在重复或倒退时间戳。
- **边界**：每条 episode 是否有明确开始、自然终止、超时或失败原因；窗口是否跨越 episode。
- **传感器**：`sensordata` 是否按 MJCF sensor 声明顺序解析；单位、坐标系和采样率是否记录。
- **物理**：是否出现穿透、非物理抖动、异常接触力；接触参数是否与目标材质相符。
- **动作**：动作语义是否与执行器类型一致（位置/速度/力矩）；是否记录了动作生效时间。
- **分布**：训练和评估是否按场景、物体、初始状态和任务变体隔离。
- **迁移**：是否有真实小样本用于比较接触、延迟、成功条件和失败原因。

## 资料地图

- [MuJoCo 官方文档](https://mujoco.readthedocs.io)：MJCF 语法、求解器、传感器、渲染和 Python API 的主入口。
- [MuJoCo GitHub 仓库](https://github.com/google-deepmind/mujoco)：源码、示例、版本发布和许可证说明。
- [MuJoCo Menagerie](https://github.com/google-deepmind/mujoco_menagerie)：DeepMind 整理的优质机器人模型库，可以直接用于数据生产。
- [dm_control](https://github.com/google-deepmind/dm_control)：控制套件与深度强化学习环境，包含相机与 reward 工具。
- [MJX 文档](https://mujoco.readthedocs.io/en/latest/mjx.html)：JAX 版 GPU 并行仿真，适合大规模数据生产。
- [D4RL](https://github.com/Farama-Foundation/D4RL)：离线 RL 数据集与基准，大量基于 MuJoCo。
- [robosuite](https://robosuite.ai) / [robomimic](https://robomimic.github.io)：基于 MuJoCo 的操作仿真与模仿学习数据集格式。

## 一句话定位

**MuJoCo 在具身数据中的角色，是轻量、高速、可复现的轨迹与接触数据生产层；它为数据管线和训练提供规模与迭代速度，而真实数据负责校准接触、延迟与噪声并完成最终验证。**

## 资料来源

- [MuJoCo 官方文档](https://mujoco.readthedocs.io)
- [MuJoCo GitHub](https://github.com/google-deepmind/mujoco)
- [MuJoCo Menagerie](https://github.com/google-deepmind/mujoco_menagerie)
- [dm_control](https://github.com/google-deepmind/dm_control)
- [D4RL](https://github.com/Farama-Foundation/D4RL)
- [robosuite](https://robosuite.ai) / [robomimic](https://robomimic.github.io)
