---
title: 语言指令与机器人动作对齐数据
description: 整理指令、视觉目标、手势、任务阶段与可执行动作之间的对齐关系。
---

语言动作对齐要回答“这句话此刻指向场景中的哪个对象、要求机器人做什么”。同一个词在不同场景可能对应不同动作，少量措辞变化也可能改变任务。[One Word, Different Action](https://arxiv.org/abs/2609.05260)用任务保持与任务改变的指令对评估决策不变性和敏感性；[HINT](https://arxiv.org/abs/2609.02653)关注稀疏高层意图与不断变化的视觉输入。数据集不能只存单句指令和最终成功标记。

![语言指令经场景指代和任务阶段解析后绑定机器人动作的流程](/images/docs/language-action-grounding-data-flow.svg)

## 概念与数据问题

指代定位是把语言或手势中的“这个”“左边的杯子”连接到图像区域、三维对象和坐标系；条件视觉 grounding 是根据任务阶段选择此刻真正相关的视觉目标。[What Matters, When?](https://arxiv.org/abs/2609.05376)研究视觉相似干扰物和阶段变化下的错误；[MIGU](https://arxiv.org/abs/2609.24995)结合语言、手势及几何证据处理不确定指代。若目标仍有歧义，应把多个候选及其置信度留下，而非强行生成唯一标签。

## 采集、处理与对齐

**采集**时保留原始指令、说话/手势时间、场景图像、相机标定、任务阶段和执行动作。对驾驶或移动场景，还需保留道路/路线语境；[GRAVA](https://arxiv.org/abs/2609.15169)把动作相关语言引用与二维视觉线索及可执行驾驶动作放在同一表示中。

**标注与对齐**时分开记录语言跨度、被指对象、关系、目标位姿与动作约束。一个指令可以在不同阶段绑定不同对象：抓取时关注物体，放置时关注容器。[What Matters, When?](https://arxiv.org/abs/2609.05376)提示应随阶段验证视觉注意对象；[HINT](https://arxiv.org/abs/2609.02653)提示还需记录高层意图和中途环境变化。手势或视觉证据与语音不同步时，应标注实际可用时间，避免把未来信息泄漏给模型。

![语言、视觉或手势证据、任务阶段和动作目标构成的对齐样本](/images/docs/language-action-grounding-data-contract.svg)

## 最小字段契约

字段名是建议的数据接口，不表示所引论文使用完全相同的文件格式。

| 字段 | 记录内容 | 检查重点 |
| --- | --- | --- |
| episode_id / stage_id | 任务及当前阶段 | 阶段切换可定位 |
| instruction_text / issued_at | 原始指令和时间 | 保留改写与否定词 |
| gesture_track / observed_at | 手势轨迹及可用时间 | 视觉和语音时间对齐 |
| referent_ids / confidence | 目标候选及置信度 | 歧义不伪作唯一真值 |
| image_region / world_pose | 二维区域与三维目标坐标 | 标定版本可追溯 |
| action_goal / frame_id | 末端、导航或驾驶动作目标 | 坐标系和单位明确 |
| semantic_pair_id / pair_type | 同义或关键差异指令对 | 比较时场景保持一致 |
| outcome / failure_type | 实际执行与错误类型 | 区分指代错和控制错 |

## 质控与评估

应做三层检查：标注者能否从原始观测复核指代；相近表达能否给出一致决策；关键字、否定或约束变化时动作能否正确改变。[One Word, Different Action](https://arxiv.org/abs/2609.05260)提供成对真实机器人协议，[MIGU](https://arxiv.org/abs/2609.24995)说明多模态证据可能冲突。报告时分别统计指代定位、动作目标与闭环成功，不让成功率掩盖语言误解。

![语言动作对齐的语义不变性、变化敏感性与真实执行评估](/images/docs/language-action-grounding-data-evaluation.svg)

## 数据集使用边界

语言标注可能只反映一位操作者的习惯。跨说话人、口音、指令改写、相似物体与遮挡要单独划分测试集。二维视觉指代不能自动当作三维可抓取位姿；执行前还需校验几何、碰撞和时间有效性。驾驶数据与机械臂数据的动作含义不同，不应只因共享语言模板就混用标签。

## 2026 年 10 月进展：从整段指令扩展到动作阶段与可验证目标

### 给每一句话指定有效的动作区间

[Bridging Frontier Reasoning and Robot Execution](https://arxiv.org/abs/2610.03615)将语言监督分为原语、原子和组合三个粒度，同时用自动生成示教连接高层推理与本地执行。标注不宜把整段任务描述复制到每一帧：应保存 `language_level`、`parent_segment_id`、`valid_from`、`valid_until`，让阶段指令与动作窗口相连；自动示教和人类示教仍需区分来源及纠正片段。

[ARC](https://arxiv.org/abs/2610.12386)在已有 DROID 演示上自动标注“下一动作为何合适、预期产生什么效果”。这类动作因果说明应绑定标注时可见的观测、下一动作和后态检查，不宜直接把生成文本当成事实真值。建议分开存储 `rationale_text`、`predicted_effect`、`observed_effect` 与人工或程序复核状态；这样才能判断推理说明正确、执行却失败，还是说明本身就指向错误目标。

![语言监督沿任务、阶段和原子动作逐级对齐，再用对象、目标状态与实际后态检查语言是否真正约束执行](/images/docs/language-action-grounding-data-october-levels.svg)

### 同义改写与目标改变需要不同标签

[Rephrase Before You Act](https://arxiv.org/abs/2610.10526)研究仅改措辞就引起的机器人性能变化。改写评估应保持物体、初始状态和任务含义一致，同时保留 `paraphrase_group_id`、原句、改写规则版本和执行结果。生成改写规则所用任务必须与正式留出任务分开，否则可能把任务熟悉度当作语言稳健性。相反，“轻放”和“快速放下”可能改变动作约束，不应未经审核标成语义等价。

[Physical Words](https://arxiv.org/abs/2610.26854)以原子动作词连接未来视觉及可选触觉表征。原子动作词是“抓取、推、释放”等短动作语义锚点；它们的数值动作随对象、阶段和本体变化。标注应保留词边界、未来预测跨度和接触证据，同一个词下面还需检查物理响应是否一致。词序预测准确并不自动证明动作安全或接触正确。

### 目标图像也是一种动作标签

[Goal Images Are Control Targets](https://arxiv.org/abs/2610.24885)把目标图像质量拆为对象选择、目标状态和外观质量，指出通用编辑分数不能代替机器人控制效用。建议保存初始与最终编辑区域、被操作对象 ID、目标空间关系和生成来源，并在连续多步骤任务中检查误差是否累积。生成目标只是期望状态，不能混入实际完成图像作为成功真值。语言、推理文本、动作词和目标图像最终都应回到同一组可观察的对象与后态检查。

### 10 月来源与逐篇数据启示

以下为截至 2026 年 10 月 22 日、按论文 `published` 时间筛选的本主题主归类来源。字段与质检要求为本站结合论文设计的数据建议，不表示论文采用同名 schema；复现定量结果时，应回到论文全文核对数据划分和实验协议。

| 论文 | 数据启示与使用边界 |
| --- | --- |
| [Bridging Frontier Reasoning and Robot Execution](https://arxiv.org/abs/2610.03615)（2610.03615） | 原语、原子与组合动作的稠密语言监督 |
| [Rephrase Before You Act](https://arxiv.org/abs/2610.10526)（2610.10526） | 指令改写敏感性与语义等价组 |
| [ARC](https://arxiv.org/abs/2610.12386)（2610.12386） | 面向下一动作的因果推理标注 |
| [Goal Images Are Control Targets](https://arxiv.org/abs/2610.24885)（2610.24885） | 目标图像数据应标注正确对象、目标状态及初末编辑区域；质量验收应以动作目标满足和长任务控制成功为主，不能仅用照片真实感或编辑榜单评分。 |
| [Physical Words](https://arxiv.org/abs/2610.26854)（2610.26854） | 原子动作词应按时间连接执行阶段、未来观测及可选触觉状态；这种语义与连续物理目标的对齐需要在未见场景和长任务中验证。 |

## 2026 年 9 月整理来源

以下论文按清单中的主主题归档。跨主题使用时，应重新核对任务、传感器和评测口径。

- [HINT: Human-Intent Inception for Long-Horizon Robot Manipulation](https://arxiv.org/abs/2609.02653)（2609.02653）
- [What Matters, When? Diagnosing and Improving Conditional Visual Grounding in Visuomotor Imitation Policies](https://arxiv.org/abs/2609.05376)（2609.05376）
- [One Word, Different Action: A Real-Robot Benchmark for Language-Conditioned Embodied Reasoning](https://arxiv.org/abs/2609.05260)（2609.05260）
- [GRAVA: Grounded Reasoning-to-Action Representation and Learning for Autonomous Driving](https://arxiv.org/abs/2609.15169)（2609.15169）
- [MIGU: Multimodal Instruction Grounding under Uncertainty for Manipulation Planning](https://arxiv.org/abs/2609.24995)（2609.24995）
