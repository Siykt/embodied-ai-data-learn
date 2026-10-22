---
title: 具身记忆与经验检索数据
description: 设计跨任务、跨视角和长时间运行的记忆记录、检索标签与效果评估。
---

机器人在不同房间和不同时间执行任务时，过去的观察和失败可能再次有用。[MessyMem](https://arxiv.org/abs/2609.15976)把互动中发现的知识用于移动操作，[Watch, Recall, Act](https://arxiv.org/abs/2609.28429)关注持续流中的指令变化和过去动作，[MemBodied](https://arxiv.org/abs/2609.28256)研究依赖早期观察的操作任务。记忆数据因此必须保存“何时何地获得、后来何时被检索、是否真的改变行动”。

![连续具身数据从事件切分、记忆编码到检索并验证行动价值的流程](/images/docs/embodied-memory-experience-data-flow.svg)

## 概念与数据问题

情景记忆保存一次事件及其上下文；空间记忆保存位置、物体和可通行关系；工作记忆保留当前任务所需的少量信息。[GLAM](https://arxiv.org/abs/2609.14561)在全局时空记忆上学习导航预测，[Workspace Models](https://arxiv.org/abs/2609.20820)用任务显著性监督压缩操作历史。压缩后仍要能定位原始视频或动作轨迹，避免把模型生成的摘要当成不可更正的事实。

## 采集、处理与对齐

**采集**：连续保存视频、机器人位姿、动作、任务指令、结果和环境变化。对同一物体或地点保留稳定 ID，并在场景重访时记录新旧状态。[R2M-Bench](https://arxiv.org/abs/2608.27328)指出绝对画面相似可能只是场景几乎没变，因此应记录中间动作和实际视角变化。

**处理与检索**：按访问、操作、发现、失败和修正切分事件，建立时间与空间索引。[ShallowStream](https://arxiv.org/abs/2609.02780)采用轻索引再深入读取的思路处理视频流；[TEMPO](https://arxiv.org/abs/2609.16864)强调动态操作需要时间上下文；[PRIME](https://arxiv.org/abs/2609.22040)让情境记忆反馈到驾驶感知。检索日志应同时保存查询、候选和最终使用的证据，便于判断相关信息是否被遗漏。

![具身记忆记录的时空索引、事件内容、来源证据与检索结果关系](/images/docs/embodied-memory-experience-data-contract.svg)

## 最小字段契约

字段名是建议的数据接口，不表示所引论文使用完全相同的文件格式。

| 字段 | 记录内容 | 检查重点 |
| --- | --- | --- |
| stream_id / episode_id | 连续流及任务片段 | 跨 episode 时间轴可连通 |
| event_id / event_type | 访问、接触、发现、失败等事件 | 事件边界可回看 |
| observed_at / location_id | 时间与地图位置 | 重访时同地点可匹配 |
| object_id / state_change | 对象身份和状态变化 | 区分位置变动与身份变化 |
| evidence_uri / frame_range | 原始视频、传感器和动作证据 | 摘要可追溯 |
| memory_text / embedding_version | 结构化事实及检索表示 | 模型版本与更新保留 |
| retrieval_query / candidate_ids | 查询与候选记忆 | 可算召回和误检 |
| used_memory_ids / outcome | 实际使用的证据及任务结果 | 不能把检索命中当成功 |

## 质控与评估

质检既看事件时间和对象身份是否正确，也看检索是否带来行动收益。重访评估应以有变化和无变化的场景分别统计，避免静止场景抬高相似度；[R2M-Bench](https://arxiv.org/abs/2608.27328)提供这一问题的评测视角。长时任务还要比较有无记忆时的成功率、重复搜索次数、错误动作与检索延迟。[MessyMem](https://arxiv.org/abs/2609.15976)和[MemBodied](https://arxiv.org/abs/2609.28256)提示需要覆盖“过去才有的信息”，而不能全靠当前帧完成的任务。

![具身记忆按重访一致性、检索价值和长期任务收益评估](/images/docs/embodied-memory-experience-data-evaluation.svg)

## 数据集使用边界

记忆可能过期：抽屉已被打开、物体已移动、指令已撤销。数据应记录有效时间和冲突证据，执行前重新确认关键状态。[Watch, Recall, Act](https://arxiv.org/abs/2609.28429)所涉及的持续任务尤其不能假设 episode 重置。检索质量与控制质量分开报告；通用视频问答成绩不能直接等于机器人长期行动能力。

## 2026 年 10 月进展：记忆需要证据位置、物理时间和可检索对象

### 从保存历史转向保存可核验的事件

[RV-ICL](https://arxiv.org/abs/2610.06843)把示教视频组织成整段、阶段、时刻与短片的层级，规划时先看概览，遇到具体接触再读取细节。建议为事件保存 `parent_event_id`、`event_type`、`frame_range`、`contact_window` 和原始文件地址；关键帧可以做索引，但不能替代抓持是否稳定的连续证据。

[Ledger](https://arxiv.org/abs/2610.10538)在第一视角视频中维护物体位置、历史和上下文，累积重复证据后才记录移动。[World Observer](https://arxiv.org/abs/2610.02162)则在生成世界里用独立观察者跟踪视野外演化。两者都涉及“看不见后状态如何延续”，但前者来自观测关联，后者包含生成状态。建议增加 `state_source=observed/predicted`、`last_confirmed_at`、`move_evidence_ids`，不要把预测的视野外变化写成实测事实。

![记忆由原始事件、对象关联和实际时间构建，在检索时回到证据，并分别评价形成、检索和行动收益](/images/docs/embodied-memory-experience-data-october-evidence.svg)

### 相同帧数可能代表不同的物理过程

[Temporal Flow Policy](https://arxiv.org/abs/2610.20524)显示观测序列的顺序之外，还需保留实际经过的时间。物体在遮挡后出现的位置、等待多久后执行下一步，都可能依赖真实间隔。这种根据真实时间更新的表示可称为物理时间记忆。记录 `elapsed_seconds` 时应同时保存设备时间域和缺帧标记，避免把低帧率、网络延迟和真实等待混为一谈。质检可在相同历史上改变提供的时间间隔，观察动作是否按预期提前或延后，并检查这是否符合真实任务。

[Mem4Act](https://arxiv.org/abs/2610.22323)用多时间粒度聚合历史，再结合问答和关键帧特征重建监督固定大小记忆。压缩记忆的验收不能只看向量长度：应保留被监督的事实、关键帧及时间范围，分别测试事实可恢复性和动作策略是否真正使用历史。移除早期关键事件、打乱无关片段和提供正确历史是不同对照，不能合并成一个“无记忆”基线。

### 对话与经验摘要都需要绑定对象和来源

[DialogMem](https://arxiv.org/abs/2610.24767)把带位姿 RGB-D 流与对话对齐，区分对象关联、条目检索和空间定位。仅把“我把杯子移到窗边”加入文本，可能改善问答，却未让导航找到正确实例；建议保存 `utterance_id`、`object_instance_id`、`location_version` 与关联置信度，并将三阶段错误分别标注。

[EmbodiedEvo](https://arxiv.org/abs/2610.18867)把交互历史整理为可复用技能和教训，再冻结经验去测新场景。摘要应链接原始失败和修复证据，评测应注明经验快照、构建场景和未见场景，防止把反复尝试的熟悉度当作泛化。长期训练中的遗忘、回放及参数版本另见[机器人持续学习数据](/guides/continual-robot-learning-data/)；本页重点是记忆内容怎样形成、检索并影响当前行动。

### 10 月来源与逐篇数据启示

以下为截至 2026 年 10 月 22 日、按论文 `published` 时间筛选的本主题主归类来源。字段与质检要求为本站结合论文设计的数据建议，不表示论文采用同名 schema；复现定量结果时，应回到论文全文核对数据划分和实验协议。

| 论文 | 数据启示与使用边界 |
| --- | --- |
| [World Observer](https://arxiv.org/abs/2610.02162)（2610.02162） | 视野外状态持续演化 |
| [RV-ICL](https://arxiv.org/abs/2610.06843)（2610.06843） | 按事件层级检索示教视频 |
| [Ledger](https://arxiv.org/abs/2610.10538)（2610.10538） | 持久三维物体位置与历史 |
| [EmbodiedEvo](https://arxiv.org/abs/2610.18867)（2610.18867） | 将原始交互历史整理成技能与教训后，应冻结经验集合并留出新场景，分别评测记忆依赖任务、程序复用、接触控制和推理成本。 |
| [Temporal Flow Policy](https://arxiv.org/abs/2610.20524)（2610.20524） | 记忆数据必须保留观测间实际经过时间，而不只保留帧序号；时间干预、遮挡后事件恢复与行为时序应共同用于检验记忆是否利用物理时间。 |
| [Mem4Act](https://arxiv.org/abs/2610.22323)（2610.22323） | 历史可按多时间粒度组织，并用问答和关键帧特征共同监督固定大小记忆；需要检验动作策略是否真正使用历史以及哪些证据在压缩中保留。 |
| [DialogMem](https://arxiv.org/abs/2610.24767)（2610.24767） | 对话必须按时间连接到具体物体实例及位置；评测应分别诊断记忆形成时的关联、检索正确条目和空间定位，问答改善不代表导航改善。 |

## 2026 年 9 月整理来源

以下论文按清单中的主主题归档。跨主题使用时，应重新核对任务、传感器和评测口径。

- [R2M-Bench: Evaluating Revisit Memory via Relative Consistency in Interactive Video World Models](https://arxiv.org/abs/2608.27328)（2608.27328）
- [ShallowStream: Index Shallow then Answer Deep for Streaming Video Understanding](https://arxiv.org/abs/2609.02780)（2609.02780）
- [TEMPO: Learning Temporal Context for Dynamic Robot Manipulation](https://arxiv.org/abs/2609.16864)（2609.16864）
- [MessyMem: Learning-from-Doing Memory for Mobile Manipulation](https://arxiv.org/abs/2609.15976)（2609.15976）
- [GLAM: Training a latent world model over global spatiotemporal memory for active exploration and navigation](https://arxiv.org/abs/2609.14561)（2609.14561）
- [Workspace Models: Lightweight Robotic Memory via Saliency-Driven Supervision](https://arxiv.org/abs/2609.20820)（2609.20820）
- [PRIME: Perception Feedback with Situational Memory Embeddings in VLA Models](https://arxiv.org/abs/2609.22040)（2609.22040）
- [Watch, Recall, Act: Always-On Robots in Concurrent Embodied Streams](https://arxiv.org/abs/2609.28429)（2609.28429）
- [MemBodied: Recurrent Associative Memory for Vision-Language-Action Models](https://arxiv.org/abs/2609.28256)（2609.28256）
