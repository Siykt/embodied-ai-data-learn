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

## 本主题论文

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
