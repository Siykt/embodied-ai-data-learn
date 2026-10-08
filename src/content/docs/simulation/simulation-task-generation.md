---
title: 仿真任务环境、数据生成与记录
description: 从任务规格、环境循环、随机化和并行采样，到示教、episode 记录、数据集版本及准入检查。
---

场景和传感器准备好后，还需要把它们变成可重复执行的任务。任务环境定义初态、观测、动作、状态推进、成功条件和结束规则；记录器再把每次执行保存为 episode。训练用 rollout、示教轨迹和闭环评测都经过这条链路，但数据准入标准可以不同。

![仿真任务从重置、观测、动作、物理推进到奖励和结束判断的循环](/images/docs/simulation-task-loop.svg)

## 1. 任务规格先于训练脚本

一个任务不能只由奖励函数或环境名称定义。任务规格应包含目标对象、允许初态、动作空间、观测空间、成功与失败条件、最长时长、安全约束以及任务变体。训练器可能把奖励用于优化，但数据集还必须独立保存“客观成功”“超时”“碰撞失败”等事件。

| 字段 | 需要明确的问题 | 下游用途 |
| --- | --- | --- |
| `task_id` 与版本 | 任务目标是否改变过 | 复现和跨版本比较 |
| `variant_id` | 资产、布局、目标位姿如何取样 | 覆盖统计与划分 |
| `observation_spec` | 策略实际能看见什么 | 防止使用特权真值 |
| `action_spec` | 位置、速度、力矩或末端命令，单位和频率 | 训练与回放 |
| `success_rule` | 何时判断成功，是否要求保持一段时间 | 评估指标 |
| `end_reason` | 自然终止、超时、安全停止或记录故障 | 失败分析 |

MuJoCo 提供物理与传感器计算，上层环境通常由项目、dm_control 或其他任务库定义。Isaac Lab 提供任务工作流与环境配置。无论用哪种框架，都要对照环境代码核对 `reset`、`step`、观测、动作处理、奖励和终止的实际语义。

## 2. 环境循环与动作时间

一次环境转移可抽象为：从状态 `s_t` 生成策略可见观测 `o_t`，策略给出动作 `a_t`，动作处理器将其变为执行器命令，物理引擎推进到 `s_{t+1}`，再计算下一观测、奖励、事件和结束标记。控制周期可能包含多个物理小步，因此 `a_t` 的生效时间与 `o_t` 的采样时间都要显式保存。

动作处理器可能做缩放、裁剪、坐标转换、逆运动学或安全过滤。只记录策略原始输出会遗漏机器人真正执行的命令；只记录执行器值又无法复盘策略决策。建议保存 `requested_action`、`applied_action` 和 `action_transform_version`，并记录人工接管或安全控制器覆盖。

奖励、成功与终止应分开。奖励是优化信号，成功是任务结果，`terminated` 表示按任务逻辑结束，`truncated` 表示时间上限或外部限制截断。评价数据还应记录失败原因，而不只是一位 `done`。

记录器的最小顺序可以写成下面的伪代码。关键是先固定 `o_t` 的采样时刻，再记录请求与实际动作，最后写入 `o_{t+1}` 和事件；相机等异步流按自己的时间戳关联。

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

并行环境要为每个槽位分别执行这套边界逻辑。若相机输出比控制慢，应保存最近一帧的原始时间和是否重复使用，而不是复制像素后伪造新的拍摄时间。

## 3. 程序化任务与领域随机化

领域随机化是在规定范围内变化物体位置、质量、摩擦、灯光、相机和噪声等参数，以扩大训练覆盖。它必须服从物理与任务约束：物体不可初始穿透，目标应可达，材质与质量组合应有依据。随机范围太宽可能生成大量无效场景，太窄则训练数据只覆盖固定布局。

![任务规格与随机化参数经过约束检查后生成可追溯任务变体](/images/docs/simulation-randomization-flow.svg)

每次生成保存 `generator_version`、参数范围、随机种子、实际采样值、约束检查结果和拒绝原因。训练、验证、评测的划分应按资产、场景、任务变体族或机器人隔离；随机按帧切分会把同一 episode 泄漏到多个集合。

可以用小规模真实采集估计摩擦、传感器噪声或执行器延迟的合理范围，再在仿真中扩展。范围来自哪些实测证据、哪些只是研究假设，应分别标注。

## 4. 轨迹来源：策略、示教与脚本

同一任务可以由不同控制来源生成数据：随机策略用于覆盖或边界测试，训练策略用于闭环 rollout，人类遥操作用于示教，脚本或规划器可产生参考轨迹。每条 episode 要保存 `controller_type`、策略或脚本版本、操作者或设备化名、是否有人工接管以及控制器切换时刻。

示教扩增还需要数据血缘：原始示教 ID、片段分段、目标任务变体、生成器版本和派生轨迹 ID。Isaac Lab Mimic 等工具能从示教生成更多轨迹，但扩增数量不等于独立信息量；评估划分应避免同一原始示教的派生样本跨训练与测试。

## 5. 并行采样与 episode 边界

并行环境通常共享同一批处理循环，但各环境可能在不同时间 reset。`env_id` 只是当前运行的槽位，槽位复用后要分配新的 `episode_id`。记录器必须按 `episode_id` 分段，不能把一个槽位上的两次尝试拼成一条轨迹，也不能在写盘时把不同环境的图像和动作交叉配对。

![多个并行环境的独立 episode 汇入记录器并生成版本化数据集](/images/docs/simulation-parallel-recorder.svg)

### 运行规模与吞吐测量

并行环境数量增加后，瓶颈可能从物理计算转到相机渲染、GPU/CPU 数据传输、编码或磁盘写入。对数据生产真正有意义的吞吐是“通过质量准入且已落盘的有效 episode/小时”，不是单纯的物理步/秒。性能报告应给出硬件、环境数量、物理/控制/渲染频率、图像分辨率、保存模态、压缩方式和失败重试数。

批量运行还要处理写盘反压：记录器跟不上仿真时，不能静默丢帧或把旧帧当成新观测。为每条流保存连续序号和丢样计数；当缓存溢出、编码失败或进程重启时，将受影响 episode 标为不完整，并记录恢复点。多 worker 的随机种子应从运行 ID、worker ID 和 episode 序号确定，避免不同 worker 重复生成同一任务变体。

落盘前定义文件格式和 schema：图像可以用视频或逐帧图像保存，低维数据可用结构化数组或表格保存，但必须有共同的 episode 与时间索引。图像编码、深度量化、压缩方式和缺失值规则会改变下游可用性，应作为数据集版本的一部分。

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
  rewards / events / terminated / truncated / end_reason
  success / quality_flags / provenance
```

## 6. 记录后的准入与回读

先回读少量样本，检查图像可解码、数组形状和类型、时间单调性、坐标单位、观测动作顺序、episode 结束原因和标签映射；再跑批量统计。质量准入应区分“记录完整”“物理有效”“任务有效”“可用于某个下游用途”。失败轨迹可能不适合模仿学习，却可能是安全评测和纠错训练的重要样本。

对于大规模生成，要同时报告成功写入的 episode 数、拒绝数、失败原因分布、有效训练时长、图像/传感器覆盖以及磁盘和渲染开销。单独报告物理步吞吐会高估真实数据生产能力。

下游的[仿真验证、评测与真实迁移](/simulation/simulation-validation-sim2real/)负责建立评估划分、物理校验和真机对照；episode 结构的进一步设计见[Episode 与 Trajectory 数据设计](/guides/episode-trajectory-design/)。

## 官方资料

- [MuJoCo Simulation](https://mujoco.readthedocs.io/en/stable/programming/simulation.html) 与 [Python API](https://mujoco.readthedocs.io/en/stable/python.html)：仿真推进、状态与控制接口。
- [Isaac Lab Task Workflows](https://isaac-sim.github.io/IsaacLab/main/source/overview/core-concepts/task_workflows.html) 与 [Available Environments](https://isaac-sim.github.io/IsaacLab/main/source/overview/environments.html)：环境结构和任务示例。
- [Isaac Lab 示教与 Mimic](https://isaac-sim.github.io/IsaacLab/main/source/overview/imitation-learning/teleop_imitation.html)：示教采集和轨迹扩增示例。
