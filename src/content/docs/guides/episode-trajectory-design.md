---
title: Episode 与 Trajectory 数据设计范式
description: 从具身智能数据角度整理 episode、trajectory、step、transition、窗口采样和元数据索引的常见设计方式。
---

在具身智能数据里，episode 和 trajectory 经常被混着说，但做数据集设计时最好把它们分清楚：

- **Episode** 更强调一次任务尝试的边界：从开始条件、执行过程到结束原因。
- **Trajectory** 更强调随时间展开的状态和动作序列：智能体一路看到了什么、做了什么、到了哪里。

很多真实数据里，一个 episode 里会有一条主 trajectory，也可能有多条并行轨迹，例如双臂、多人、多相机或外部定位系统分别记录自己的时间序列。本文关注的是：采集、处理、标注和训练时，怎样把这些序列组织成稳定、可检查、可复用的数据。

![具身智能数据采集、对齐、标注和评估的整体关系](/images/docs/embodied-ai-data-overview.webp)

## 基本单位

可以把数据从小到大分成四层：

- **Frame / Sample**：某个时间点的观测，例如一帧图像、一条 IMU 读数、一组关节角。
- **Step / Transition**：一次“观测到动作再到下一状态”的学习单位，常见字段是 `observation`、`action`、`reward`、`done`、`next_observation`。
- **Trajectory**：按时间排序的一串 step，重点是连续运动过程。
- **Episode**：一次完整或截断的任务记录，除 trajectory 外，还包含任务、场景、设备、成功状态、终止原因和质检结果。

对机器人操作数据来说，step 通常不只是强化学习里的状态转移。它还要承载多模态数据对齐：

- 图像帧：手眼相机、第三人称相机、深度图或分割图。
- 低维状态：关节角、关节速度、末端位姿、夹爪宽度、力矩或触觉。
- 动作标签：绝对位姿、相对位姿、关节命令、速度命令或未来动作序列。
- 时间字段：设备时间戳、统一时间戳、帧序号、插值标记。
- 质量字段：是否跟踪丢失、是否遮挡严重、是否人工审核通过。

这也是 episode / trajectory 设计最容易出错的地方：看起来只是数组形状问题，实际会影响后续采样、训练目标、评估统计和数据清洗。

## 范式一：Episode 嵌套 Step

这是最直观的结构：数据集由许多 episode 组成，每个 episode 内部保存一串 step。RLDS 就采用这种思路：读取时得到 episode，每个 episode 里再包含 steps，并用 `is_first`、`is_last`、`is_terminal` 等字段描述边界。

适合场景：

- 任务边界非常重要，例如“拿起杯子”“打开抽屉”“移动到目标点”。
- 每次演示有独立的任务指令、初始状态、成功标注和环境配置。
- 希望按 episode 做训练 / 验证划分，避免同一次演示同时出现在训练集和验证集里。

常见字段可以这样组织：

```text
episode
  episode_id
  task_id / language_instruction
  scene_id
  robot_id / operator_id
  start_time / end_time
  success / failure_reason
  quality_flags
  steps
    timestamp
    observation
    action
    reward
    is_first
    is_last
    is_terminal
```

这种设计的优点是语义清楚，适合审核和调试。缺点是当数据量很大、视频很多时，如果每个 episode 都独立成文件，文件数量和打开成本会很高。

## 范式二：Trajectory 分组文件

robomimic 代表了另一种常见设计：一个 HDF5 文件里有 `data/demo_0`、`data/demo_1` 这样的轨迹分组，每个 demo 保存 `states`、`actions`、`rewards`、`dones`、`obs` 和 `next_obs`。这里的 demo 基本就是一条 trajectory，也常被当作 episode 使用。

适合场景：

- 模仿学习或离线强化学习，训练代码希望快速读取固定长度序列。
- 需要把图像、状态、动作放在同一个容器里统一索引。
- 数据规模中等，单文件或少量分片还能接受。

常见结构：

```text
dataset.hdf5
  data
    env_args
    total
    demo_0
      num_samples
      obs
      next_obs
      states
      actions
      rewards
      dones
    demo_1
      ...
  mask
    train
    valid
```

这种设计对训练很友好：随机抽一条 demo，再抽一段连续窗口，就能形成 batch。它的风险是元数据容易被塞在文件属性或外部表里，后期做跨任务筛选、按设备统计质量、按场景追溯问题时会比较吃力。

## 范式三：扁平 Transition 表

D4RL 这类离线强化学习数据常见做法是把所有 transition 拼成几张大数组：`observations`、`actions`、`rewards`、`terminals`、`timeouts`，必要时再提供 `next_observations`。

适合场景：

- 训练算法主要消费 transition，而不是完整 episode。
- 状态和动作都是低维数组，图像和多传感器同步不是重点。
- 希望和 Gym / 离线 RL 工具链保持兼容。

关键设计点是结束标记：

- `terminals` 表示任务或环境真正终止，例如摔倒、失败、成功结束。
- `timeouts` 表示因为最大长度或人为切段而截断，不一定代表任务失败。
- 如果只用一个 `done` 字段，后续算法可能分不清“自然结束”和“被切断”。

对具身智能数据来说，扁平 transition 表适合做算法基准，但不适合作为唯一主存储。真实机器人数据通常还需要 episode 级元数据：采集设备、标定版本、环境布局、操作者、任务语言、质检状态和原始文件路径。

## 范式四：文件分片加元数据索引

当数据扩展到大量机器人、相机和 episode 时，越来越多格式会把“物理存储”和“逻辑 episode”拆开。LeRobot v3 的思路就是：低维时序数据放 Parquet，视频放 MP4 分片，episode 边界、offset、schema、统计量和任务描述放在 metadata 里。

![多源数据经过时间与空间对齐后，才能形成可训练的 episode 索引](/images/docs/data-alignment-calibration.webp)

适合场景：

- episode 数量很多，不想让每条演示都对应一堆小文件。
- 图像或视频占主要体积，需要用视频编码节省空间。
- 希望支持远程流式读取、按任务筛选、按 episode offset 快速定位。
- 数据会持续追加，需要稳定的 schema 和版本管理。

常见结构：

```text
dataset
  meta
    info.json
    stats.json
    tasks.jsonl
    episodes
  data
    parquet shards
  videos
    camera-specific mp4 shards
```

这种范式很适合具身智能数据平台。它把 episode 当成逻辑对象，而不是文件对象：一个视频分片里可以包含多个 episode；一个 episode 的 RGB、深度、状态和动作也可以分布在不同文件里，通过 metadata 重新拼出来。

代价是数据写入和校验要更严谨。比如保存时必须正确写入 episode 起止 offset、帧率、时间戳、视频编码参数和特征 schema，否则训练时看到的窗口可能会跨 episode、错相机或错时间。

## 范式五：窗口化序列样本

策略模型通常不会直接吃完整 episode，而是吃固定长度窗口。比如 diffusion policy、Transformer policy 或 RNN policy 常会取：

- 过去 `N` 帧观测作为上下文。
- 当前或未来 `M` 步动作作为监督目标。
- 可选的语言指令、目标图像或任务 ID 作为条件。

因此数据集要明确窗口语义：

- `observation_horizon`：模型能看到多长历史。
- `action_horizon`：一次预测多少未来动作。
- `prediction_delay`：动作标签相对观测是否有延迟。
- `stride`：窗口滑动步长。
- `pad_before` / `pad_after`：episode 开头和结尾是否填充。

一个常见错误是只保存 `action[t]`，但训练时实际需要 `action[t:t+M]`。如果没有清楚定义动作相对哪一帧，就会出现“图像里还没接触物体，动作标签已经开始夹紧”的错位。

## 范式六：多轨迹 Episode

具身智能数据经常不是单智能体单相机。一个 episode 里可能同时有：

- 机器人本体轨迹：底盘、机械臂、夹爪。
- 相机轨迹：头部相机、手眼相机、外部相机。
- 人类演示轨迹：手部、头部、工具或 UMI 夹爪。
- 物体轨迹：关键物体的位姿、接触状态或语义状态。
- 地图轨迹：SLAM 位姿、回环修正前后位姿、参考真值轨迹。

![Ego 采集数据进入世界坐标和操作表示的流程](/images/docs/ego-world-operation-overview.webp)

这类数据的 episode 设计重点不是“把所有字段堆在一起”，而是声明清楚坐标系和时间关系：

- 哪条轨迹是主时间轴。
- 哪些数据是原始采样，哪些是插值或重采样。
- 位姿是在相机坐标、机器人基座坐标、桌面坐标还是世界坐标。
- 多机器人或双臂的命名是否稳定，例如 `robot0`、`robot1`、`camera0`、`camera1`。
- 轨迹修正后，旧版本是否保留，评估用哪一个版本。

UMI 这类数据就是典型例子：一段视频既是视觉观测，又是 SLAM 输入，还要通过 ArUco 和标定转换成夹爪 TCP 轨迹。episode 不是简单的视频切片，而是多相机重叠时间段、夹爪身份、SLAM 质量和操作轨迹共同确定的逻辑样本。

## 边界设计

Episode 边界是数据质量的核心。常见边界策略有：

- **人工触发边界**：采集员按键开始 / 结束，语义清楚，但容易有多余等待帧。
- **任务事件边界**：根据成功检测、接触事件、导航到点等事件切段，适合自动化评估。
- **固定长度边界**：按最大帧数或时间切段，便于训练，但容易切断完整动作。
- **多设备重叠边界**：以多个相机或多个传感器共同在线的时间段为 episode，适合多视角数据。
- **后处理有效边界**：根据 SLAM、标定、遮挡、图像质量过滤后重新裁剪，只保留可用片段。

建议把结束原因拆开保存，而不是只留一个 `done`：

```text
end_reason:
  success
  task_failure
  operator_stop
  timeout
  sensor_lost
  calibration_invalid
  manual_reject
```

这样后续可以分别处理“任务失败但数据真实”“传感器坏了不可用”“人为切断但前半段可训练”等情况。

## 数据字段建议

一个面向具身智能数据集的 episode 元数据可以包含：

- `episode_id`：全局唯一，合并多个数据源时也不冲突。
- `task_id` / `instruction`：任务类别和自然语言指令。
- `scene_id`：场景、房间、桌面或仿真环境。
- `robot_id` / `hardware_config`：机器人、夹爪、相机和传感器配置。
- `operator_id` / `policy_id`：数据来源是人、专家策略、探索策略还是混合策略。
- `start_time` / `end_time` / `duration`：原始时间范围。
- `num_steps` / `fps` / `control_hz`：序列长度和采样率。
- `coordinate_frames`：世界坐标、基座坐标、相机坐标和 TCP 坐标说明。
- `calibration_version`：标定文件版本。
- `success` / `score` / `end_reason`：任务结果。
- `quality_flags`：缺帧、漂移、遮挡、时间不同步、人工审核状态。
- `source_paths`：原始视频、日志、传感器文件和处理产物路径。

Step 级字段可以包含：

- `timestamp`：统一时间戳。
- `observation.*`：图像、深度、点云、状态、语言上下文。
- `state.*`：机器人内部状态或仿真状态。
- `action.*`：控制命令或未来动作标签。
- `reward` / `discount`：强化学习需要时保留。
- `is_first` / `is_last` / `is_terminal` / `is_timeout`：边界标记。
- `alignment_status`：是否原始帧、插值帧、缺失补齐或低置信度。

字段命名不一定要完全照搬某个格式，但同一个数据集内部必须稳定。尤其是 `action` 的单位、坐标系、时间偏移和归一化范围，应该写进 schema，而不是只靠训练代码默认理解。

## 质量检查重点

![视频、IMU、SLAM 轨迹和夹爪状态需要在 episode 内保持时间一致](/images/docs/umi-data-quality-check.webp)

整理 episode / trajectory 时，至少检查这些问题：

- Episode ID 是否唯一，合并数据集后是否仍唯一。
- 每个 episode 的 step 数、视频帧数、动作长度是否一致或有明确 offset。
- `is_first`、`is_last`、`is_terminal`、`timeout` 是否互相矛盾。
- 窗口采样是否会跨 episode。
- 训练 / 验证 / 测试划分是否按 episode 划分，而不是按 frame 随机打散。
- 多相机帧率不同的时候，是否记录了插值或最近邻匹配策略。
- 位姿轨迹是否声明坐标系，是否和相机、夹爪、地图使用同一套标定。
- 图像压缩、resize、裁剪、遮罩是否会改变模型需要看的关键接触区域。
- 成功 / 失败标签是否来自可靠规则或人工复核。
- 被过滤的 episode 是否保留过滤原因，方便回溯采集问题。

一个实用原则是：训练时采样出来的任意窗口，都应该能回溯到原始 episode、原始时间戳、原始文件和质检记录。否则模型表现异常时，很难判断是算法问题、动作标签问题，还是采集对齐问题。

## 设计取舍

不同范式没有绝对好坏，可以按使用目标选择：

| 目标 | 更适合的范式 | 主要注意点 |
| --- | --- | --- |
| 快速做模仿学习实验 | Trajectory 分组文件 | 保证图像、状态、动作长度一致 |
| 离线强化学习基准 | 扁平 transition 表 | 区分 terminal 和 timeout |
| 多任务机器人数据平台 | 文件分片加元数据索引 | 保证 episode offset 和 schema 可校验 |
| 人类演示到机器人策略 | 多轨迹 episode | 明确坐标系、标定版本和动作时间偏移 |
| 长时序模型训练 | 窗口化序列样本 | 防止窗口跨 episode 和标签错位 |

如果刚开始设计自己的具身智能数据格式，可以先用一个简单判断：

- **逻辑上按 episode 管理**：采集、质检、划分和评估都围绕 episode。
- **物理上按分片存储**：大规模图像和低维数组可以合并成较大的 Parquet、HDF5、Zarr 或视频文件。
- **训练时按窗口读取**：模型看到的是固定长度片段，但片段必须能回到原始 episode。

这样既能保留任务语义，也能兼顾训练吞吐和长期维护。

## 资料来源

- [RLDS 数据格式](https://github.com/google-research/rlds)
- [robomimic 数据集结构](https://robomimic.github.io/docs/datasets/overview.html)
- [D4RL 数据集接口](https://github.com/Farama-Foundation/D4RL)
- [LeRobotDataset v3 设计说明](https://github.com/huggingface/lerobot/blob/main/docs/source/lerobot-dataset-v3.mdx)
- [LeRobot 数据集工具](https://huggingface.co/docs/lerobot/using_dataset_tools)
