---
title: Isaac Lab 与具身数据
description: 从机械臂把杯子放到托盘的任务理解 Isaac Lab，学习记录观测与动作、分开并行轨迹，并检查仿真数据的适用范围。
---

驾校会先布置车道、车辆和路障，再安排倒车、转弯等课程。每次练习还要记下学员看到了什么、怎样操作、在哪里失败。想增加练习量，可以同时使用多块场地，但每位学员的记录必须分清。

在本文讨论的集成路线中，**Isaac Sim 类似布置和运转训练场的设施，Isaac Lab 类似组织课程与批量练习的程序**；数据记录器负责整理每次练习。场景的外观和物理效果由具体模型决定，练习成绩也不能直接代表真实表现。

读完本页，你将能说明一次机器人任务要记录什么，以及多个任务同时运行时，怎样保留各自完整、可追溯的轨迹。

## Why｜为什么用 Isaac Lab 生成具身数据

**当你已经能记录一次任务，想增加场景变化和采集数量时，可以考虑 Isaac Lab。** 以“机械臂把杯子放到托盘”为例。一次成功演示只能覆盖一种摆放方式；为了研究失败，还需要改变杯子位置、相机角度或物体摩擦，并记录每次发生了什么。Isaac Lab 可以组织这类重复交互，还能让多个环境同时运行。

<span id="先看结论它在具身数据里做什么"></span>
<span id="作为数据生产层的优势"></span>
<span id="一句话定位"></span>

从数据工作看，它主要帮助你：

- **扩大覆盖**：生成不同初态和任务条件下的完整记录，包含成功与失败。
- **获得标签**：利用引擎中的物体位置、接触和任务条件，为图像与动作附上可追溯标签。
- **尽早检查流程**：在大量采集前发现动作单位、观测时间或结束规则的问题。
- **反复比较**：在规定场景下测试策略，再将结果与真实样本对照。

它适合做数据生成与评估的工作环境。是否得到可用的数据集，还取决于你是否保存了足够的字段、说明和质量检查结果。

![Isaac Lab 将场景和任务组织为多次交互，记录数据、检查质量，再用真实样本校准的闭环](/images/docs/isaac-lab-data-loop.svg)

## What｜Isaac Lab 是什么，一次练习包含哪些数据

**它组织机器人如何开始、观察、行动和结束任务；你要保存的是每次任务中的这些过程与结果。**

### 先分清平台、环境与数据集

沿用放杯子的例子，三者的区别是：

| 层次 | 在例子中做什么 | 对数据意味着什么 |
| --- | --- | --- |
| [Isaac Sim](/reference/terms/#isaac-sim) | 加载机械臂、杯子和托盘，计算物理与相机画面 | 决定场景、接触和视觉输出的生成条件 |
| [Isaac Lab](/reference/terms/#isaac-lab) | 规定初态、观测、动作、成功条件，并组织并行运行 | 决定每次任务如何开始、推进和结束 |
| 导出的数据集 | 保存图像、动作、状态、时间和结果 | 供下游训练、回放与评估读取 |

Isaac Lab 是开源机器人学习框架，支持强化学习、模仿学习等工作流。“环境”指一套机器人、场景和任务规则；从重置到结束的一次运行叫 [episode](/reference/terms/#episode)。有训练日志或视频，并不意味着上述数据已完整保存。

本页以 Isaac Lab 与 Isaac Sim 集成的路线为例。安装前再查[版本与运行边界](#技术附录版本与运行边界)，确认所选路线能提供需要的物理、图像和传感器输出。

<span id="能生成哪些具身数据"></span>

### 观测数据

对放杯子的机械臂来说，观测可以是腕部相机图像、关节角度和夹爪是否接触物体。应该先列清“机器人看到了什么”，再决定代码里的字段，而不是把所有数组都叫 `obs`。

例如，夹爪伸向杯子时，一张图像回答“杯子看起来在哪里”，关节角度回答“手臂现在怎样弯曲”，接触读数回答“夹爪碰到了什么”。这几项信息互相补充；具体字段可查[观测与记录器清单](#技术附录记录器字段清单)。

不同传感器未必同时更新：相机可能刚好还在使用上一帧，而关节状态已经更新。即使它们在同一次 `step` 中返回，也应核对各自采样时间。图像还要附上相机位置和朝向、内参、分辨率、深度单位，以及分割编号对应的类别或物体。

### 动作、状态与奖励

一条动作应能被解释成具体操作，例如“夹爪沿某坐标系移动 1 厘米”。如果只保存 `[0, 0, 0.01]`，却没说是米、弧度还是归一化值，后续就无法安全重放。

每个控制步至少要对应当前观测、动作生效时间和下一状态。动作还应区分策略请求值、经过限幅等处理后的命令，以及实际发给执行器的控制量。

使用强化学习时，`reward` 表示任务为这一步给出的分数；要保存分项含义。`terminated` 记录任务达到结束条件，`truncated` 记录因时间上限等外部限制被截断。“杯子已放稳”和“时间用完但还拿着杯子”应有不同的结束原因。

### 任务与环境标签

引擎知道杯子在哪里、是否发生接触，因此可以生成目标位姿、碰撞、任务阶段、成功和失败原因等标签。这些由模拟场景直接提供的值称为[仿真真值](/reference/terms/#仿真真值)。

标签要写明来源：引擎直接给出的物体位置，与从相机图像估计的位置，误差性质不同。真实机器人运行时拿不到的真值，可以用于训练监督和评估，但不能悄悄成为策略运行时的输入。

![一次 episode 将观测、动作状态、任务边界与标签连在一起，并附上生成条件和质量信息](/images/docs/isaac-lab-episode-contract.svg)

## Who｜谁负责场景、任务、记录与验收

<span id="isaac-lab-在完整仿真链路中的位置"></span>

**使用框架的人仍要对数据负责：什么算成功、动作代表什么、记录能否重放，都需要项目明确。** 以放杯子为例，职责可以这样划分：

| 负责方 | 要明确的事情 | 应留下的记录 |
| --- | --- | --- |
| 场景与机器人维护者 | 托盘尺寸、机器人关节、碰撞形状、材质和相机是否合适 | 场景资产、单位、坐标和配置版本 |
| 任务编写者 | 从哪里开始、杯子怎样算放稳、什么时候失败或超时 | 观测、动作、重置、奖励和结束规则 |
| 数据采集者 | 在何时取图像与状态，如何分开多次运行 | 记录器版本、时间、episode ID 和字段说明 |
| 验收与评估者 | 数据是否可回读，训练与评估条件是否分开，真实结果有何差异 | 质量报告、划分规则与真实对照结果 |

场景常用 [USD](/reference/terms/#usd) 描述层级和资产引用。固定场景时，应保留文件与依赖资产的可解析版本，仅写“SO101 机械臂”不足以重建当时的实验。

阅读任务源码时，依次找出观测定义、动作处理、重置、奖励、终止和事件配置。官方[任务工作流](https://isaac-sim.github.io/IsaacLab/main/source/overview/core-concepts/task_workflows.html)说明这些部分如何组织；通用数据方法见[场景与物理配置](/simulation/simulation-scene-physics/)、[传感器与时间对齐](/simulation/simulation-sensors-timing/)及[任务与数据生成](/simulation/simulation-task-generation/)。

## Where｜数据在哪里产生，又应保存到哪里

**每次任务各自保存一份轨迹，再连同场景和配置交给训练或评估程序。** 数据产生在每个环境与策略的交互中。例如，两只机械臂同时放杯子，一只已经完成并重开，另一只仍在移动；记录器要为重开的那次任务换一份记录，同时保留另一只机械臂尚未结束的轨迹。

程序中的 `env_id` 常常只是环境在本次运行中的槽位。槽位会反复使用，因此每次重置都需要新的 `episode_id`，并独立记录开始时间、随机种子、任务变体和结束原因。一个环境提前结束，不应让其他环境的轨迹跟着断开或混入新初态。

### 从仿真运行到可用数据集

将记录保存到哪里由项目决定：可以先写本地文件，再交给训练程序或统一数据存储。无论位置如何，先完成以下过程：

1. **固定输入。** 保存框架、引擎、任务代码、场景资产和物理配置的版本。
2. **约定字段。** 给每个观测、动作和标签写明单位、坐标系、采样时间与来源。
3. **分开每次运行。** 以 episode 保存；使用示教或 Mimic 扩增时，还需记录原始示教 ID 和生成设置，说明派生关系。
4. **保存后重新读取。** 检查数组形状、缺失值、时间、图像类别映射和动作含义。
5. **整理可用范围。** 统计不同任务条件下的质量和失败情况，再决定哪些记录进入训练或评估。

官方[保存相机输出指南](https://isaac-sim.github.io/IsaacLab/main/source/how-to/save_camera_output.html)可以帮助完成图像导出。完整 episode 还需要动作、状态、时间和结束原因；这些字段由项目的[数据契约](/reference/terms/#数据契约)约定。

### 数据落盘建议

先把每次练习的条件与结果配对保存：使用哪个机器人和相机、杯子放在哪里、发了什么动作、图像和状态在何时采样，以及最后是否成功。准备实现记录器时，再按[完整字段清单](#技术附录记录器字段清单)逐项检查。

例如，允许杯子横向位置在某个范围内变化，是 `randomization_config`；这一次实际放在什么位置，是 `sampled_parameters`。两者都保留，才能解释某次失败并重建条件。这类有意改变场景或物理参数的做法称为[领域随机化](/reference/terms/#领域随机化)。

![仿真数据与版本、实际随机参数、时间和质量字段一起保存，使下游能追溯每条轨迹](/images/docs/simulator-data-contract.svg)

## When｜何时开始并行采集，何时转向真实验证

**一条记录通过验收后再并行采集，真实机器人部署前再用真实样本检验差异。** 机器和软件是否适用，也要在开始运行前确认。

### 先确认版本和硬件适用

本页所用资料主要面向受支持的 NVIDIA Linux / Windows 环境。具体后端、GPU 与驱动要求见[版本与运行边界](#技术附录版本与运行边界)。

**本页 Isaac Lab 内容依据官方资料整理，尚未在本机完成部署验证。** 已完成的 Apple Silicon 实验是 MuJoCo，详见[本机实践记录](/simulation/open-source-learning-repositories/#apple-silicon-本机实践记录)。准备运行 Isaac Lab 时，应使用所选版本的[安装指南](https://isaac-sim.github.io/IsaacLab/main/source/setup/installation/index.html)，固定与之匹配的代码和资产。

### 质量检查清单

先验收一条短记录，再扩大到多个环境。至少要确认：

| 检查内容 | 进入下一步前应看到什么 |
| --- | --- |
| 时间与动作 | 图像、状态和动作在同一时间轴上可解释；动作单位与生效时刻明确 |
| 坐标与传感器 | 世界、基座、相机和物体坐标已声明；相机参数、深度单位与分割编号齐全 |
| episode 边界 | 每次重置使用新 ID；异步结束的环境不会混写记录 |
| 物理与复现 | 无明显穿透或非物理抖动；固定条件重跑后，有关键状态与结束原因的误差报告 |
| 数据划分 | 训练和评估按场景、物体、初态或任务变体合理隔离 |

可先查看 Isaac Lab 的[可用环境](https://isaac-sim.github.io/IsaacLab/main/source/overview/environments.html)，从一项能够解释成功条件的任务开始。不要仅凭训练程序正常启动，就认定数据记录也已经正确。

<span id="不能替代什么"></span>

### 上真实机器人前，用真实样本检查差异

仿真里杯子不滑，真实夹爪却可能因为摩擦不足而抓不住；仿真相机画面清晰，真实运动中却可能模糊。这些差异都会改变“看到什么、发出什么动作、得到什么结果”的关系。

![从图像、接触、控制延迟和任务分布四个方向对照仿真与真实数据](/images/docs/isaac-lab-sim2real-check.svg)

真实对照应覆盖曝光、噪声、运动模糊、遮挡和反射，也要检查摩擦、执行器延迟、关节回差、丢帧和操作差异。用真实样本调整关键参数，再分别报告仿真与真实的任务成功率、接触失败和控制延迟，并说明样本数与任务条件。

仿真中的高成功率只适用于已测的仿真分布。真实部署的判断需要真实评估，详细流程见[验证与真实迁移](/simulation/simulation-validation-sim2real/)。

## 技术附录：版本与运行边界

<details>
<summary>安装前：核对 Isaac Sim、Kit-less 与硬件支持范围</summary>

**版本范围：**本页主要说明与 Isaac Sim 集成的路线。依据 **2026-10-09** 的核查，Isaac Lab 3.0 开发路线还提供 [Kit-less](/reference/terms/#kit-less) 工作流，也就是不启动 Isaac Sim 的 Kit 应用运行时，部分工作流可使用 [Newton](/reference/terms/#newton) 物理后端。因此，本页的 Isaac Sim 场景、渲染与传感器说明不能套用到所有后端。版本和平台边界见[学习仓库中的版本路线](/simulation/open-source-learning-repositories/#isaac-lab-的版本路线)及[官方 develop 安装指南](https://isaac-sim.github.io/IsaacLab/develop/source/setup/installation/index.html)。

依据本页采用的 2026-10-09 资料，相关安装路径仍以受支持的 NVIDIA Linux / Windows 环境为主；Kit-less 不能被理解为 Apple Silicon 已获官方支持。无窗口运行只是关闭桌面显示，GPU、驱动和后端要求仍需逐项核对。

</details>

## 技术附录：记录器字段清单

<details>
<summary>实现记录器时：查看观测组织与完整 episode 字段</summary>

```text
observation
  cameras.front.rgb              相机彩色图像
  cameras.front.depth            深度及其单位
  cameras.front.segmentation     像素对应的类别或物体编号
  proprioception.joint_position  关节位置
  proprioception.joint_velocity  关节速度
  sensors.imu                    运动传感器读数
  sensors.contact                接触读数
```

这是字段组织示例，需要按实际任务调整。可配置的传感器还包括射线等类型，具体能力依赖所选版本和后端，见[官方传感器概览](https://isaac-sim.github.io/IsaacLab/main/source/overview/core-concepts/sensors/index.html)。

下面是字段清单示意，并非框架自动导出的固定目录：

```text
dataset
  schema_version
  isaac_lab_version / isaac_sim_version
  environment_id / task_id
  environment_code_commit / usd_asset_hashes
  physics_timestep / control_hz / render_hz
  sensor_config / camera_intrinsics / label_id_map
  randomization_config / sampled_parameters
  seed / worker_id
  episodes
    episode_id / env_slot_id / task_variant_id
    observations
    requested_actions / applied_actions / states / rewards
    observation_time / action_time / frame_time
    terminated / truncated / end_reason
    success / quality_flags / label_provenance
```

</details>

<span id="按数据任务查资料"></span>

## 资料来源

| 下一步要做的事情 | 优先阅读的资料 |
| --- | --- |
| 选择匹配的版本与安装路线 | [安装指南](https://isaac-sim.github.io/IsaacLab/main/source/setup/installation/index.html)、[GitHub 仓库](https://github.com/isaac-sim/IsaacLab)、[develop 路线](https://isaac-sim.github.io/IsaacLab/develop/source/setup/installation/index.html) |
| 理解任务如何组织 | [Task Workflows](https://isaac-sim.github.io/IsaacLab/main/source/overview/core-concepts/task_workflows.html)、[Available Environments](https://isaac-sim.github.io/IsaacLab/main/source/overview/environments.html) |
| 配置与保存传感器 | [Sensors](https://isaac-sim.github.io/IsaacLab/main/source/overview/core-concepts/sensors/index.html)、[Save Camera Output](https://isaac-sim.github.io/IsaacLab/main/source/how-to/save_camera_output.html)、[Isaac Sim 文档](https://docs.isaacsim.omniverse.nvidia.com/latest/index.html) |
| 采集示教和扩增轨迹 | [Teleoperation and Imitation Learning with Isaac Lab Mimic](https://isaac-sim.github.io/IsaacLab/main/source/overview/imitation-learning/teleop_imitation.html) |
| 明确可复现的条件和限制 | [Reproducibility and Determinism](https://isaac-sim.github.io/IsaacLab/main/source/features/reproducibility.html) |

官网 `main` 和 `develop` 都会继续变化，正式数据集应固定所用代码与对应文档。与其他工具的比较见[仿真器与具身数据](/simulation/simulators-embodied-data/)。

## 继续阅读

- 上一页：[MuJoCo 与具身数据](/simulation/mujoco-embodied-data/)——用较小的模型理解动作、状态和采样时间的关系。
- 下一页：[仿真开源学习仓库与实践路线](/simulation/open-source-learning-repositories/)——按机器条件和当前能力，选出第一项能完成并验收的练习。
