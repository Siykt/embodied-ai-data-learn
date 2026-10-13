---
title: MuJoCo 与具身数据
description: 从旋转指针的动作与读数理解 MuJoCo，学习保存可回读的轨迹、检查采样时间，并判断何时需要真实设备对照。
---

想象一张可以反复重做实验的工作台：把指针放回同一角度，给它相同的推力，每隔一小段时间记下它转到哪里、转得多快。改变推力或摩擦，再做一次，就能比较两次结果。

MuJoCo 类似这张**放在计算机里的实验台**。机器人和物体是器材，动作是施加的输入，状态与传感器读数是测量记录。真实器材的摩擦、松动和延迟仍需测量，计算机里的实验结果不能自动代替真实结果。

读完本页，你将能说明一条 MuJoCo 轨迹怎样产生、该保存什么，以及扩大采集前怎样检查它是否可用。

## Why｜为什么用 MuJoCo 采集具身数据

**当你想先弄清“一个动作怎样变成下一条数据”时，MuJoCo 是合适的起点。** 假设你要整理“指针收到转速指令后怎样运动”的数据，首先要确认：指令的单位是什么、什么时候生效、下一次读数对应哪个时刻。MuJoCo 可以用一个小模型反复检查这些问题，随后再增加相机、接触和更复杂的任务。

<span id="先看结论它在具身数据里做什么"></span>
<span id="一句话定位"></span>

它适合先完成三件事：

- **记录动作的结果**：保存每个时刻的关节位置、速度、控制输入和传感器读数，形成连续的[轨迹数据](/reference/terms/#轨迹数据)。
- **增加实验覆盖**：更换起始位置、物体质量或摩擦，观察哪些条件容易失败，并保留每次实际使用的参数。
- **检验数据能否使用**：先生成几十步数据，保存后重新读取，确认训练程序能正确找到“当前观测、当前动作、下一观测”。

这也是它在具身数据工作中的主要价值：用较小的模型快速检查采集流程，再扩大轨迹数量。若想先看到实际结果，可打开本站已运行的[旋转关节实验](/simulation/mujoco-data-walkthrough/)，对照画面、时间和原始数值。

![MuJoCo 从场景模型、动作和物理步进生成轨迹，再经过记录与质量检查进入数据集的流程](/images/docs/mujoco-data-flow.svg)

## What｜MuJoCo 是什么，输出又是什么

**它根据你给的模型和指令计算运动，输出可以保存的位置、速度和传感器读数。** [MuJoCo](/reference/terms/#mujoco) 是 Google DeepMind 维护的开源[物理引擎](/reference/terms/#物理引擎)，全名是 Multi-Joint dynamics with Contact；物理引擎就是根据模型与当前状态，计算下一小段时间内物体怎样运动的软件。

例如，“让指针以目标速度转动”需要先定义指针与转轴，再定义接收速度指令的执行器。引擎据此计算运动；“转到某个角度算成功”“每次保存哪些列”则需要任务程序和记录器来规定。

### MJCF：场景即数据契约

[MJCF](/reference/terms/#mjcf) 是 MuJoCo 使用的 XML 模型文件。可以把它理解为实验器材和设置的清单：物体长什么样、关节怎样连接、质量和摩擦是多少、用什么驱动、在哪里测量。

同一条控制指令，放在不同执行器或摩擦设置下，可能产生完全不同的运动。因此数据集要保存 MJCF、它引用的网格和纹理，以及对应版本或哈希。[哈希](/reference/terms/#哈希)是用于识别文件内容的摘要，可帮助检查模型是否被改过。这些信息是[数据契约](/reference/terms/#数据契约)的一部分，也就是数据提供方与使用方对字段含义和生成条件的共同约定。

MuJoCo 也能导入 [URDF](/reference/terms/#urdf) 机器人描述，但转换可能丢失或改写信息，转换设置也要记录。修改模型时可查[常见 MJCF 项目](#技术附录mjcf-文件中的常见项目)。

<span id="能生成哪些数据"></span>

### 状态与传感器

先看一个可读懂的记录：指针在某个角度，程序发出“转得快一些”的指令，过一段时间后，再记下它的新角度和速度。这里要分清**发出的指令**与**实际发生的运动**；目标速度改变了，实际速度可能还在逐渐追上它。

读懂这样的记录只需先找到时间、位置、速度、控制指令和传感器读数。编写记录器时，再查[状态与传感器字段表](#技术附录状态与传感器字段)。

### 时间、控制与采样

可以先把记录理解成：“先拍下指针的位置，发出指令，等一段时间，再拍下新位置。”对应的训练样本是：

```text
当前观测 → 在这段时间施加的动作 → 下一观测
```

实现时，`mj_step` 表示推进物理仿真。记录器必须说明观测在推进前还是推进后读取，以及一个动作会保持多少个物理步。相机可能拍得更慢，所以图像、状态和动作的数组下标相同，不代表它们发生在同一时刻。

每步应保留仿真时间、控制步序号，以及观测、动作和图像各自的时间。改变采样频率或动作保持方式时，要更新配置版本。相关概念见[物理步长与控制周期](/reference/terms/#物理步长与控制周期)。

### 动作与奖励

一次从环境重置到结束的完整过程称为 [episode](/reference/terms/#episode)。如果任务使用奖励指导学习，还会记录 `reward`，并说明各奖励项的含义。

结束原因同样属于数据：`terminated` 通常表示任务达到规定的结束条件，`truncated` 表示因时间上限等外部限制而截断。例如“已经转到目标位置”和“时间用完但还没转到”需要分开。具体安全停止属于哪一类，应由任务定义明确规定。

### 渲染与仿真真值

Python 的 `Renderer` 可以在不打开交互窗口的情况下生成 RGB、深度和分割图；这称为离屏渲染。引擎还可以提供物体位姿、接触点、接触力和质心等[仿真真值](/reference/terms/#仿真真值)，用于制作标签和自动检查。

例如，用物体真实位置为图像制作标签很方便，但真实机器人运行时可能只能看相机图像。应标明哪些字段是策略运行时能看到的观测，哪些只用于训练或评估，避免把真实设备拿不到的答案直接喂给策略。

## Who｜谁负责模型、任务和数据质量

<span id="mujoco-在完整仿真链路中的位置"></span>

**引擎负责算运动，采集项目负责让别人读懂并复用结果。** 在小项目里，一人可能兼任下列工作；职责分开说明，是为了知道出现问题时该检查哪里。

| 负责方 | 要做的工作 | 交付给下一环节的内容 |
| --- | --- | --- |
| 模型维护者 | 配置机器人、物体、执行器、接触与传感器 | MJCF、资产版本、单位和关节布局 |
| 任务编写者 | 定义初始状态、动作含义、成功条件与结束规则 | 能解释的任务配置与固定动作样例 |
| 数据采集者 | 在正确时刻读取字段，按 episode 保存 | 带时间、动作说明和结束原因的记录 |
| 数据验收者 | 回读、重放、检查异常，并与真实样本比较 | 质量报告、适用范围及训练评估划分 |

[dm_control](/reference/terms/#dm_control)、robosuite 等上层项目可以提供现成任务，MuJoCo Menagerie 可以提供机器人模型。复用这些项目能减少建模工作，但仍需检查它们的观测、动作与结束条件是否符合自己的数据需求。

通用方法可继续阅读[场景与物理配置](/simulation/simulation-scene-physics/)、[传感器与时间对齐](/simulation/simulation-sensors-timing/)和[任务与数据生成](/simulation/simulation-task-generation/)。

## Where｜数据保存在哪里，又流向哪里

<span id="常见数据形态"></span>

**把轨迹和“这次实验怎么做的”保存在一起，交给下一位使用者。** 保存位置和文件格式应方便下游程序重新读取，模型、配置与版本说明也要随附。

小实验可以先保存一份便于逐行查看的 CSV，再附上模型和说明清单。需要多组数组或图像时，可选择 [NPZ](/reference/terms/#npz) 或 [HDF5](/reference/terms/#hdf5)。这些格式决定数据怎样放进文件，动作的单位和采样时间仍要另外说明；接入已有训练项目时，查[常见格式与项目约定](#技术附录常见数据格式)。

### 数据落盘建议

以指针实验为例，应一起保存“用了哪个模型、何时发出什么指令、指针怎样运动、为什么结束”。如果程序要求的速度被限幅，还要同时留下请求值和实际控制量。拍摄图像时，再附上相机配置和图像时间；实现记录器时可查[完整字段清单](#技术附录记录器字段清单)。

![每个 episode 附带生成条件、观测动作、仿真标签与质量字段，供下游训练和评估使用](/images/docs/simulator-data-contract.svg)

保存完之后，先抽一条记录重新读取，核对初态、最后状态和动作生效顺序。能成功写出文件，只说明保存步骤完成；回读结果正确，才能证明下游至少能按约定使用它。

## When｜何时扩大采集，何时需要真实验证

**先确认一条短轨迹能读懂、能回读，再增加数量；准备给真实机器人使用时，再用真实样本对照。**

<span id="质量检查清单"></span>

### 先通过小样本验收，再增加数量

先用固定模型、初态和动作做一小段记录，并检查：

- **时序正确**：时间没有倒退，动作与下一状态对应，图像有自己的采样时间。
- **字段明确**：传感器布局、动作单位和坐标系完整，数字有限且维度正确。
- **结束明确**：每条 episode 有开始和结束原因，采样窗口不跨越两次实验。
- **运动合理**：没有明显穿透、异常抖动或不合理接触力。
- **能够对照**：重复固定实验，比较前若干步状态和结束原因，记录误差范围。

通过后，再增加物体、场景和初态；训练与评估应按这些条件合理隔离，避免评估只检验已见过的固定布局。

### 批量生成与 MJX 的使用边界

单条记录稳定后，再考虑同时生成许多条轨迹。[MJX](/reference/terms/#mjx) 提供批量计算能力；迁移时仍需用相同模型和动作检查数据是否一致，具体方法见[批量运行附录](#技术附录mjx-批量运行)。

### 与真实数据的关系

准备把数据用于真实机器人时，需要真实样本校准。比如仿真中的指针能立即追上速度指令，真实电机却可能先等待通信、再逐渐加速；忽略这段延迟，动作与结果的关系就会偏离实际。

![用真实设备对照 MuJoCo 的接触、执行器、控制频率和传感器，定位影响数据使用的差异](/images/docs/mujoco-real-check.svg)

重点比较摩擦与接触、关节阻尼和回差、执行器延迟与饱和、实际控制频率，以及传感器噪声和丢帧。MuJoCo 可以稳定求解某组参数，但稳定运行并不证明参数符合真实材质。具体接触设置可查下方[模型附录](#技术附录mjcf-文件中的常见项目)。

用真实少量样本调整关键设置后，分别报告仿真与真实的成功率、失败原因和样本范围。完整方法见[验证与真实迁移](/simulation/simulation-validation-sim2real/)。如果数据需求转向复杂视觉、USD 场景和大量相机渲染，可进一步比较[Isaac Lab](/simulation/isaac-lab-embodied-data/)。

## 技术附录：MJX 批量运行

<details>
<summary>扩大采集时：查看 MJX 适用范围与对照要求</summary>

若主要需要大量关节状态和动作轨迹，可在原生 MuJoCo 参考任务稳定后评估 [MJX](/reference/terms/#mjx)。MJX 使用 JAX 支持批量计算，适合同时推进许多条轨迹；具体模型支持范围和性能见 [MJX 官方说明](https://mujoco.readthedocs.io/en/stable/mjx.html)。

迁移前用同一模型、初态和动作做小批量对照，比较状态、接触事件、结束条件和成功率。编译耗时、支持特性和数值结果都可能不同。报告生成速度时，应写明是否包含图像渲染和文件保存，这样“每秒多少步”才可以比较。

</details>

## 技术附录：状态与传感器字段

<details>
<summary>编写记录器时：查看状态、控制量和传感器字段</summary>

先看一条记录想回答什么，再看字段名称：

| 想知道的事情 | 常用字段 | 阅读时需要注意 |
| --- | --- | --- |
| 仿真进行了多久 | `time` | 这是仿真时间，不等于电脑实际花费的时间 |
| 关节或物体在哪里 | `qpos` | 位置表示取决于关节类型；自由关节还包含用四元数表示的朝向 |
| 它怎样运动 | `qvel`、`qacc` | 分别是速度、加速度，含义和维度要结合模型解释 |
| 发给执行器什么指令 | `ctrl` | 可能是位置、速度或力矩输入，取决于执行器定义 |
| 传感器测到了什么 | `sensordata` | 需要按传感器名称、地址和维度拆分，并标明单位与坐标系 |
| 力来自哪里 | `qfrc_actuator`、`qfrc_constraint`、`qfrc_applied` | 分别保留来源，不要混成含义不明的一列力 |

有动态执行器时，还可能需要 `act` 保存执行器内部状态。并非每个任务都要保存所有字段，但每个已保存字段都要有解释。例如只有一串 15 个数字，却没有传感器布局，使用方就无法知道哪些是角速度、哪些是加速度。

</details>

## 技术附录：常见数据格式

<details>
<summary>接入训练项目时：查看 CSV、NPZ、HDF5 与项目约定</summary>

| 下游用途 | 可参考的形式 | 需要另行核对 |
| --- | --- | --- |
| 检查小型采集实验 | CSV 表格、NPZ 命名数组与说明清单 | 每列含义、时间关系、单位和版本 |
| 使用历史离线强化学习数据 | D4RL 中的 observations、actions、rewards、terminals 等字段 | 不同版本如何表示超时与结束，不能只凭字段名推断 |
| 机械臂模仿学习 | robosuite / robomimic 常见的 HDF5 文件，按 episode 分组 | 环境配置、图像、动作、状态及结束标记的具体定义 |
| 生成控制或视觉任务记录 | dm_control 的观测、奖励、环境步进和渲染接口 | 仍需按项目要求实现记录和导出 |

CSV 适合逐行查看；[NPZ](/reference/terms/#npz) 可以保存多个命名数组；[HDF5](/reference/terms/#hdf5) 可以把数组按层级组织在文件中。格式只解决如何装数据，含义仍要由随附说明解释。

</details>

## 技术附录：MJCF 文件中的常见项目

<details>
<summary>修改模型时：查看 MJCF 标签与接触设置</summary>

初次阅读只需先找到机器人、执行器和传感器。需要修改模型时，再按下表查对应项目；以下是用途速查，不表示 XML 的完整嵌套结构。

| 项目 | 描述什么 | 为什么影响数据 |
| --- | --- | --- |
| `asset` | 网格、材质、纹理 | 决定部分几何和视觉内容 |
| `worldbody`、`joint` | 场景层级、物体、关节 | 决定连接关系、运动方式和状态维度 |
| `tendon` | 肌腱路径与驱动耦合 | 改变约束及力的传递 |
| `actuator` | motor、position、velocity 等执行器 | 决定 `ctrl` 应解释成什么输入 |
| `sensor`、`camera` | 传感器与相机 | 决定读数布局、测量位置与观察视角 |
| `option`、`size`、`default` | 仿真选项、容量与默认设置 | 求解和默认参数可能改变运动结果 |

`solref`、`solimp` 等接触设置的含义和校准应参考 [MuJoCo 官方文档](https://mujoco.readthedocs.io/en/stable/)。

</details>

## 技术附录：记录器字段清单

<details>
<summary>导出数据时：查看生成条件与 episode 的完整字段</summary>

下面是一份字段清单示意，并非 MuJoCo 会自动生成的目录。它把“这次怎么采的”和“每次采到了什么”放在一起：

```text
dataset
  schema_version
  mujoco_version / mjx_version
  mjcf_model（版本或哈希，以及导出/转换配置）
  asset_hashes（网格、纹理等外部资产）
  task_id / environment_id
  seed / worker_id
  physics_timestep / control_hz / render_hz
  solver_settings（迭代次数、容差、积分器）
  sensor_layout（名称、地址、维度、单位、坐标系）
  episodes
    episode_id
    observations / actions / states / rewards
    observation_time / action_time / frame_time
    requested_action / applied_control
    terminated / truncated / end_reason
    success / quality_flags
```

其中 `requested_action` 是程序希望执行的动作，`applied_control` 是处理后实际发给执行器的输入。若动作被限幅，两者可能不同。输出图像时，还要附上相机位姿、内参或可恢复内参的配置、分辨率、渲染设置和深度单位。

</details>

<span id="按数据任务查资料"></span>

## 资料来源

| 需要继续解决的问题 | 官方或项目资料 |
| --- | --- |
| 模型、关节与传感器怎样定义 | [MJCF XML Reference](https://mujoco.readthedocs.io/en/stable/XMLreference.html)、[Modeling](https://mujoco.readthedocs.io/en/stable/modeling.html) |
| 如何加载、推进与读取状态 | [Python API](https://mujoco.readthedocs.io/en/stable/python.html)、[Simulation](https://mujoco.readthedocs.io/en/stable/programming/simulation.html) |
| 状态维度、接触和力怎样解释 | [API Types](https://mujoco.readthedocs.io/en/stable/APIreference/APItypes.html)、[Computation](https://mujoco.readthedocs.io/en/stable/computation/index.html) |
| 是否适合批量运行 | [MJX 官方说明](https://mujoco.readthedocs.io/en/stable/mjx.html) |
| 从现成模型和任务起步 | [MuJoCo Menagerie](https://github.com/google-deepmind/mujoco_menagerie)、[dm_control](https://github.com/google-deepmind/dm_control) |
| 读取已有轨迹格式 | [D4RL](https://github.com/Farama-Foundation/D4RL)、[robosuite](https://robosuite.ai)、[robomimic](https://robomimic.github.io) |

模型与接口以 [MuJoCo 官方文档](https://mujoco.readthedocs.io/en/stable/)为准，版本变化见 [GitHub 发布记录](https://github.com/google-deepmind/mujoco/releases)。使用当前在线文档时，应核对它与实际运行版本是否一致。

## 继续阅读

- 上一页：[验证与真实迁移](/simulation/simulation-validation-sim2real/)——理解仿真记录通过检查后，还需要哪些真实样本证据。
- 下一页：[Isaac Lab 与具身数据](/simulation/isaac-lab-embodied-data/)——把一条轨迹的记录要求扩展到视觉任务和多个并行环境。
