---
title: 浏览器遥操作与众包采集专题
description: 从浏览器控制链路、时间对齐、轨迹 schema 和质量准入角度设计可追溯的众包具身数据采集。
---

浏览器遥操作把“操作者如何控制机器人”变成了可远程、可扩展的采集入口。它降低了设备使用门槛，却也把网络延迟、控制能力差异、任务理解偏差和身份管理带进了数据集。要让众包样本能够训练和评估策略，采集系统必须同时记录操作者输入、设备执行状态、时间关系、质量判断和原始数据血缘。

本文把一次浏览器遥操作视为一个可审计的 episode：浏览器产生输入，控制层把输入映射为动作，仿真器或机器人反馈状态，记录器按设备或仿真时钟写入观测与动作，任务验收再决定该 episode 是否进入候选数据集。网络中继的连接与延迟字段可参考 [TURN 与具身数据实时采集](/guides/turn-for-embodied-data/)，episode 边界和窗口语义可参考 [Episode 与 Trajectory 数据设计](/guides/episode-trajectory-design/)。

![浏览器贡献者输入经过控制映射、环境执行和轨迹记录后进入任务验收的闭环](/images/docs/browser-teleoperation-data-flow.svg)

## 采集链路的时间顺序

一次动作不能只由“浏览器按下了什么键”定义。建议把链路拆成以下事件，并为每个事件保留事件类型、序号和产生它的时钟域：

1. **浏览器 UI 输入**：鼠标、键盘、触控、手柄或屏幕上的位姿控件产生意图，例如“末端向前移动”或“夹爪闭合”。记录控件状态、输入值、客户端序号和 UI 版本。
2. **控制层接收与映射**：服务端或设备端接收输入，检查权限和新鲜度，再将它转换为关节、末端位姿、速度或离散按钮动作。记录映射版本、坐标系、单位、缩放、限幅和是否被安全控制器修改。
3. **仿真或机器人执行**：环境在控制周期中应用动作，产生实际执行状态。记录命令时间、执行时间、控制周期、执行结果、关节限制、碰撞和急停状态。
4. **观测生成**：相机、深度、触觉和本体传感器产生图像或状态；仿真器还可以产生物体真值、接触和渲染参数。观测应使用设备或仿真时钟，并保留采样序号。
5. **动作确认**：记录器将“请求动作”和“实际应用动作”分开保存，并关联确认状态。延迟、丢弃、覆盖、限幅或断连期间的动作不能静默当作已执行。
6. **episode 落盘与验收**：原始输入、执行日志、观测和质量事件先落盘，再根据任务结果和准入规则生成候选 episode。派生标签必须关联处理版本，不能覆盖原始记录。

客户端时间不能替代设备或仿真时钟。浏览器时钟适合回答“操作者何时看到界面、何时发出输入”，设备或仿真时钟才适合回答“动作何时作用于环境、观测何时产生”。两者都应保存，并通过同步事件或估计的传输延迟建立关系；没有可靠同步时，应标记 `alignment_status: unknown`，而不是把接收时间当成采样时间。

## 浏览器端轨迹 schema

下面是一个面向原始记录和质检的最小 schema。它不绑定某个机器人 SDK；`action.requested` 表示控制层收到的请求，`action.applied` 表示环境实际应用的结果。

```yaml
episode:
  episode_id: string
  task_id: string
  instruction: string
  task_version: string
  scene_id: string
  robot_id: string
  operator_id: string
  session_id: string
  control_mapping_version: string
  schema_version: string
  clock_domains:
    client: string
    device_or_sim: string
    server_receive: string
  started_at_device_ns: integer
  ended_at_device_ns: integer
  outcome: success | failure | timeout | interrupted | unknown
  acceptance: pending | accepted | rejected
  rejection_reasons: [string]
  lineage:
    raw_inputs: [uri]
    raw_observations: [uri]
    processing_run_id: string
  steps:
    - step_id: integer
      client_event_time_ms: integer
      receive_time_ms: integer
      observation_time_device_ns: integer
      applied_time_device_ns: integer
      observation:
        image: {stream_id: string, frame_id: integer, uri: string}
        proprioception: {uri: string, sample_id: integer}
        environment_state: {uri: string, source: sim | robot}
      action:
        requested: {type: string, values: [number], frame: string, unit: string}
        applied: {type: string, values: [number], frame: string, unit: string}
        status: applied | dropped | clamped | stale | unknown
      alignment:
        input_to_apply_ms: number
        observation_to_apply_ms: number
        status: aligned | interpolated | gap | unknown
      quality_flags: [string]
```

`operator_id` 应使用受控的化名或内部标识，不把姓名、邮箱等直接写入训练样本。`task_version`、`control_mapping_version` 和 `schema_version` 是后续比较数据质量和复现实验的关键字段。具体的状态、动作和 episode 组织方式可以继续对照 [MuJoCo 与具身数据](/guides/mujoco-embodied-data/)中的控制循环与数据契约。

## 众包样本的准入检查

准入不是给 episode 打一个模糊的“好 / 坏”标签，而是把可训练、可评估、需返工和应拒绝的原因拆开。建议分三层执行：

### 自动检查

- 身份、任务版本、机器人配置和 schema 版本齐全，episode ID 唯一；
- 客户端输入、服务端接收、设备或仿真时间均有序，且同步偏差在任务阈值内；
- 请求动作与实际应用动作数量可关联，过期、丢弃、限幅和断连区间有明确状态；
- 图像、状态和动作的帧数、采样率、episode 边界和 URI 可解析；
- 轨迹能在仿真或安全回放环境中重放，且不违反关节、速度、碰撞和工作空间约束；
- 原始文件、处理运行、标注和质量分数之间存在可追溯的血缘关系。

### 规则与人工检查

自动检查通过后，按任务协议检查是否真的完成了目标：物体是否被正确放置、是否发生掉落、是否需要人工接管、说明中的禁止动作是否被违反。人工审核应看到输入视频、动作确认、环境结果和质量事件，而不是只看一段剪辑后的视频。

### 分层结果

将结果分为 `accepted`、`accepted_for_evaluation_only`、`needs_review` 和 `rejected`。例如，任务失败但时间和动作完整的 episode 可以作为失败评估集；存在不可解释时间缺口的 episode 不应进入训练集；隐私暴露、身份异常或无法确认数据来源的记录应直接拒绝并保留拒绝原因。

![众包轨迹从身份与版本检查开始，经时间同步、物理回放和质量评分筛选为可训练或评估数据](/images/docs/crowdsourced-trajectory-quality.svg)

## 众包风险与控制措施

### 重复刷任务与身份异常

同一操作者反复提交同一场景、相同轨迹或短时间内不可能完成的数量，会让数据分布被少数样本放大。使用任务分配日志、设备或浏览器会话标识、轨迹相似度、完成时长和抽样复核组合判断，不要仅靠 IP 地址。重复样本应去重或降权，同时保留原始提交和判定规则版本。

### 控制水平差异

众包操作者的熟练程度、输入设备和操作策略不同。记录训练阶段、操作者自评不够，应增加控制频率、修正次数、急停次数、动作平滑度、任务时长和人工接管等客观字段。质量分数用于筛选和分层，不应把“动作更像专家”自动等同于“任务一定成功”。

### 控制延迟与网络波动

浏览器显示的观测可能已经滞后，操作者发出的动作也可能排队。记录 RTT、抖动、丢包、重连、视频帧到达时间和输入到实际执行的延迟，并把断连区间切成独立质量片段。网络指标应作为质量上下文进入 episode，而不是修改设备采样时间；连接层的记录方式可参考 [TURN 与具身数据实时采集](/guides/turn-for-embodied-data/)。

### 任务说明歧义

同一句自然语言可能允许多种终止状态或操作顺序。发布任务前用少量试采集验证说明，定义成功条件、失败条件、允许的恢复动作和停止条件；在数据中保存展示给操作者的 `instruction` 原文与 `task_version`，不要只保存后台任务 ID。

### 隐私与数据血缘

浏览器采集可能包含操作者画面、语音、家庭环境、姓名或地理线索。采集前说明用途和保存期限，对人脸、屏幕内容和非任务区域做最小化处理；访问权限、脱敏运行和派生文件都要记录。数据集发布时，使用不可逆或受控的操作者化名，保留从公开样本回溯到授权记录的内部链路。

## 面向不同训练阶段的字段

### Pre-training 示范

预训练更看重覆盖面、动作与观测的对应关系和可复用的语言条件。除了常规的观测、请求 / 实际动作和时间字段，建议保留：

- 多样化的 `instruction`、目标描述和任务版本；
- 完整的 `operator_id` 化名、设备类型和控制映射版本，用于分层分析；
- 动作单位、坐标系、控制频率、观测到动作延迟和插值状态；
- 成功、失败、超时和中断等结果，以及人工审核和质量分数；
- 原始视频、状态、输入事件、标注和处理运行的血缘 URI。

低质量但语义明确的失败轨迹可以单独作为负例或恢复数据使用；它们不应和通过准入的示范混成一个无标记集合。

### Post-training 纠错

后训练纠错关注“策略在哪里出错、怎样修正”，字段需要更细地描述差错前后关系：

- `policy_version`、预测动作、操作者接管时间和接管原因；
- 错误类型、错误发生的 step、修正动作、恢复是否成功；
- 策略置信度、候选动作、人工选择理由和任务约束；
- 原始尝试与纠错尝试的 `parent_episode_id`，以及对应的场景和物体状态；
- 安全停止、碰撞风险、隐私审核和是否允许回放训练的授权标记。

这样可以将纠错样本用于行为克隆、偏好比较或失败恢复训练，同时避免把人工介入后的动作误标成原策略自主完成。VLA 的数据契约和分层评估还可参考 [VLA 模型与主流验证方法](/guides/vla-models-and-evaluation/)。

## 交付前检查清单

在把众包数据交给下游使用前，至少回答这些问题：

1. 能否从一个训练窗口回溯到 episode、原始输入、设备观测、处理版本和授权记录？
2. 能否区分操作者发出的动作、控制层修改后的动作和机器人实际应用的动作？
3. 能否用设备或仿真时钟重建观测与动作的先后，而不是依赖浏览器接收时间？
4. 能否按任务版本、操作者、网络质量、机器人和结果分桶评估，而不是只报告总量？
5. 被拒绝或仅供评估的样本是否保留明确原因，并且不会误入训练 split？

浏览器降低了采集入口的成本，但不会自动生成高质量轨迹。可用的众包数据来自一条完整闭环：输入可解释、动作可确认、时间可对齐、结果可验收、质量可分层、血缘可追溯。只有这样，远程操作产生的 episode 才能稳定地服务于预训练示范、后训练纠错和真实闭环评估。
