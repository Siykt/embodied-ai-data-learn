---
title: 仿真任务环境、数据生成与记录
description: 从安排一轮轮练习理解任务环境，说明任务怎样变化、谁来执行，以及如何把过程保存成可使用的数据集。
---

学停车时，一轮完整练习不只是转几下方向盘。先摆好车辆和障碍物，再尝试驶入车位，最后判断有没有停稳、碰线或超时。下一轮可以换个起点，但要知道具体换了什么，才好比较进步在哪里。

“机械臂把杯子放到托盘上”也需要这样的组织者：先摆好杯子和托盘，让手臂尝试搬运，再判断杯子是否放稳。记录器则像练习日志，把每轮看到什么、做了什么、结果如何保存下来。

读完本页，你能把一次放杯子的尝试拆成清楚的开始、过程和结束，并知道怎样保存成别人能回看、能训练的数据。本页接着[场景配置](/simulation/simulation-scene-physics/)和[传感器对齐](/simulation/simulation-sensors-timing/)，把已经准备好的场景与观测组织成完整任务。

<span id="1-任务规格先于训练脚本"></span>

## Why｜为什么要先定义任务，再批量采数据？

先说清“怎样算完成”，采出的成功与失败标签才有共同含义。把杯子碰到托盘就结束，与要求夹爪松开后杯子仍稳定放好，是两个不同的判定规则。

例如，我们可以约定这轮练习从杯子放在桌面开始，到它被松开放稳、滑落失败或运行超时为止。这样的约定构成任务规格。杯子能从哪些位置出发、机器人能用哪些观测，也要随规格写清楚。

训练器可以用奖励鼓励某种行为，但数据集仍须单独记录客观事件。较高的奖励不一定代表杯子已经放稳；超时、碰撞失败和人工停止也不能都压成一个含义不明的“结束”。

## What｜是什么把场景变成一轮完整任务？

任务环境把“摆好起点、观察、行动、判断结果”连起来；记录器把这段过程保存下来。一轮可以成功，也可以失败，只要边界清楚、过程完整，都能成为有明确用途的数据。

<span id="2-环境循环与动作时间"></span>

### 环境负责推进，记录器负责留下过程

以放杯子为例：环境摆好杯子、托盘和机械臂，相机先拍下桌面，控制器发出靠近杯子的动作。仿真推进一段时间后，手臂到了新位置，再拍照、再决定下一步。这一过程持续到杯子被放稳，或触发失败、超时等结束条件。

![任务从重置开始，在观测、动作、物理推进与结果判断之间循环，结束后保存一次完整记录](/images/docs/simulation-task-loop.svg)

一次从初始化到结束的任务记录叫 **episode**，可以理解成“一轮尝试”。策略与环境交互、产生运行记录的过程常称为 **rollout**。阅读数据时，首先要找出每一轮从哪里开始、为什么结束。

策略想做的动作与机械臂实际收到的命令可能不同。例如策略要求向托盘移动 10 厘米，安全控制只允许移动 2 厘米。这里的数值用于示意，并非实测；如果只保存原请求，回看数据的人就无法解释手臂为什么只走了一小段。

所以记录要同时留下原请求、实际命令和中间的处理依据。有人接管，或安全控制改变了动作，也应注明发生时刻。具体字段和记录顺序放在附录中。

结束时，分别保存奖励、是否成功和结束原因。例如“杯子放稳”与“还没放下就超时”都会让这一轮停止，但它们对学习算法的意义不同。

<span id="3-程序化任务与领域随机化"></span>

### 每轮改变条件，必须知道改了什么

想让机器人适应不同杯子位置，可以每轮重新摆放杯子；想让它应对材质差异，还可以改变摩擦、质量或光照。这种在规定范围内变化外观、物理和初始条件的方法叫**领域随机化**。

![生成器根据任务规格采样参数，检查物体与目标的约束，再生成可追溯的任务变体](/images/docs/simulation-randomization-flow.svg)

变化仍要守住任务约束：杯子不能一开始就穿进桌面，目标位置应能到达，材质与质量的组合也要有依据。范围太宽可能大量生成无效任务，太窄又只能覆盖固定布局。

一次变化是否有用，还要能追溯。例如杯子这轮更重、下一轮更靠近桌边，记录中应写出实际采用的条件。变化范围可以来自小规模真实采集；没有测量支持、只是研究假设的部分要注明，不能混在一起。

<span id="4-轨迹来源策略示教与脚本"></span>

## Who｜谁执行任务，又由谁记录来源？

任务可以由人遥控、由写好的程序执行，也可以由正在训练的策略完成。记录器负责注明这一轮是谁控制的，让使用者知道动作从哪里来。

例如人先示范怎样提起杯子、绕开托盘边缘、轻轻放下；随后策略尝试同样的任务。如果策略快把杯子碰倒时由人接管，这段轨迹就不能被当成全由策略独立完成。

有时还会根据一次示范生成更多相似轨迹，例如把杯子换个位置后调整抓取路线。这些新轨迹要保留与原始示范的关系，叫做**数据血缘**。Isaac Lab Mimic 等工具可用于这类扩增，但相似轨迹变多，不等于有了同样多的独立经验。

准备任务的人确认完成规则，控制与记录程序的维护者确认动作和时间，使用数据的人决定哪些记录适合训练或评测。一个人可以承担这些工作，也仍然需要分别检查。

MuJoCo 主要提供物理与传感器计算，上层任务通常另行编写；Isaac Lab 则提供任务工作流和环境配置。工具帮你组织的范围不同，所以使用现成环境时，也要读懂它究竟怎样判定“杯子放好了”。

<span id="5-并行采样与-episode-边界"></span>

## Where｜每轮数据保存在哪里，怎样送入数据集？

图像、动作和结果可以存成不同文件，再用这一轮的编号和时间把它们联系起来。这样打开一条放杯子记录，就能同时找到画面、机械臂的命令和最后的结果。

### 并行运行时，每一轮仍有自己的身份

同时开多个仿真环境，就像多个练习场同时上课。一个场景里的杯子已经放好，另一个可能刚被夹起；每个场景都独立结束和开始新一轮。每次新尝试都要有新的编号，不能只靠“第几个场景”来区分。

![多个仿真环境各自开始与结束任务，记录器按独立 episode 收集数据，再形成版本化数据集](/images/docs/simulation-parallel-recorder.svg)

记录器按 episode 分段，避免把两次练习接成一条轨迹，也避免把一个环境的图像配上另一个环境的动作。如果相机比控制器慢，同一帧可能被多次使用，但必须保留原来的拍摄时间并标记复用。

### 文件分开保存，索引必须连接起来

图像可以存成视频或逐帧文件，关节和动作可以存成数组或表格。无论采用什么格式，都要能通过共同的 episode ID 和时间索引相互对应。

保存前，生产者和使用者还要约定数据结构：每一项叫什么、存什么内容、缺失时怎样表示。这份结构约定叫 **schema**。它和场景、传感器、动作等说明一起交付，别人才能正确读取这些文件。

### 训练与评测要在来源上隔开

如果一次放杯子示范扩增出许多相似轨迹，其中一部分用于训练，另一部分用于测试，成绩可能过于乐观。模型可能只是认出了熟悉的情况。因此先按完整尝试划分，再根据目标把相关示范、杯子或布局放在同一侧，避免把相邻画面随机拆开。

冻结划分规则与成员清单后，再交给训练或[仿真评测](/simulation/simulation-validation-sim2real/)。更完整的记录结构见[Episode 与 Trajectory 数据设计](/guides/episode-trajectory-design/)。

<span id="6-记录后的准入与回读"></span>

## When｜什么时候可以扩大采样或交付下游？

当少量已保存的样本能够正确回看、解释过程和结果时，再扩大采样。先从文件中重看一轮：能否看到夹住杯子，动作能否与画面对上，最后的“成功”是否真的是杯子放稳在托盘上？

样本能读出来之后，还要区分记录完整、物理有效、任务有效，以及适合哪种用途。失败示教可能不适合直接模仿，却能用于纠错训练或安全评测；应记录用途判断和原因，而不是只保留一个“好/坏”标记。

<span id="运行规模与吞吐测量"></span>

扩大并行规模后，速度瓶颈可能转到相机渲染、设备之间的数据传输、编码或磁盘写入。衡量生产能力时，应看“每小时有多少 episode 通过质量检查并完成写盘”，同时报告拒绝数量、原因和有效时长。

如果记录器赶不上仿真，待写入的数据就会堆积，称为**写盘反压**。例如整段任务看起来顺畅，保存的视频却缺了松开夹爪的几帧，这轮记录就不再完整。需要标明缺失和原因，再判断还能用于什么。

最后检查覆盖：任务变体是否足够，图像与传感器是否齐全，成功和失败条件是否都有记录。通过这些检查后，再扩大运行或发布给下游，才能知道增加的计算真正变成了可用数据。

## 技术附录：记录顺序与清单

<details>
<summary>单个环境的记录顺序示例</summary>

任务规格应写明目标对象、允许初态、可用观测、动作语义、成功与失败条件、最长时长和安全约束。任务有版本，布局或目标变化对应任务变体 ID。核对项目代码或框架中 `reset`、`step`、奖励与终止的实际含义；MuJoCo 上层任务也可由 dm_control 等库组织。

```text
reset(task_variant, seed) -> initial_state, episode_id
while episode_open:
  o_t, observation_time = sample_policy_observation()
  requested_action = controller(o_t)
  applied_action, action_time = transform_and_apply(requested_action)
  advance_physics_until_next_control_tick()
  o_t1, reward, events, end_reason = collect_transition()
  record(episode_id, o_t, requested_action, applied_action,
         o_t1, reward, events, observation_time, action_time)
finalize_episode(success, terminated, truncated, quality_flags)
```

相机等异步流按各自时间戳关联。这里的 `action_time` 在实际结构中还应区分命令发出与生效时刻。并行环境分别维护边界；多个工作进程的随机种子可由运行 ID、进程 ID 和 episode 序号确定，避免不同进程反复生成相同任务。

动作可能经过缩放、裁剪、坐标转换、逆运动学或安全过滤；保存请求、实际输入、转换器版本与接管事件。控制周期可以包含多个物理小步。`terminated` 表示按任务逻辑结束，`truncated` 表示因时间上限或外部限制被截断，不能只保留一个 `done`。

随机化保存生成器版本、参数范围、随机种子、实际采样值与拒绝原因。控制来源包括随机策略、训练策略、人类遥操作、脚本或规划器，并保留版本、操作者或设备化名及切换时刻。示教扩增另存原始示教 ID、片段分段、目标任务变体和生成器版本。

</details>

<details>
<summary>数据集与 episode 的字段示例</summary>

`env_id` 表示运行槽位，`episode_id` 标识这一次尝试；同一槽位开始新任务时要换 episode ID。数据划分按完整 episode，并按目标隔离资产、场景、任务变体族、机器人或原始示教来源。

```text
dataset_manifest
  schema_version / dataset_version / creation_run_id
  engine_version / task_version / asset_hashes
  sensor_manifest / action_spec / randomization_config
  split_manifest / quality_rule_version
episode
  episode_id / task_variant_id / controller_version
  initial_state / sampled_parameters / seed
  streams[stream_id, timestamp, data_ref]
  transitions[o_t, requested_action, applied_action, o_t+1]
  action_transform_version / control_override_events
  rewards / events / terminated / truncated / end_reason
  success / quality_flags / provenance
```

性能报告还应附硬件、并行环境数量、物理/控制/渲染频率、图像分辨率、保存模态、压缩方式、失败重试数，以及磁盘与渲染开销。只有这些条件一致，生产吞吐才有可比性。

数据集版本还应固定图像编码、深度量化、压缩与缺失值规则。回读检查解码、数组形状与类型、时间单调性、单位与坐标、观测动作顺序、标签映射与结束原因。记录各流的连续序号和丢样计数；缓存溢出、编码失败或进程重启影响的 episode 标为不完整，并留下恢复点。

</details>

## 官方资料

- [MuJoCo Simulation](https://mujoco.readthedocs.io/en/stable/programming/simulation.html) 与 [Python API](https://mujoco.readthedocs.io/en/stable/python.html)：仿真推进、状态与控制接口。
- [Isaac Lab Task Workflows](https://isaac-sim.github.io/IsaacLab/main/source/overview/core-concepts/task_workflows.html) 与 [Available Environments](https://isaac-sim.github.io/IsaacLab/main/source/overview/environments.html)：环境结构和任务示例。
- [Isaac Lab 示教与 Mimic](https://isaac-sim.github.io/IsaacLab/main/source/overview/imitation-learning/teleop_imitation.html)：示教采集和轨迹扩增示例。

上一章[传感器、渲染与时间对齐](/simulation/simulation-sensors-timing/)解决了记录怎样对应，本章把它们保存成一轮轮完整尝试。下一章[仿真验证、评测与真实迁移](/simulation/simulation-validation-sim2real/)继续判断：这些放杯子数据是否可信，在真实机械臂上又能说明什么。
