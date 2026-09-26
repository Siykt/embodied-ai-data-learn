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

## 本主题论文

以下论文按清单中的主主题归档。跨主题使用时，应重新核对任务、传感器和评测口径。

- [HINT: Human-Intent Inception for Long-Horizon Robot Manipulation](https://arxiv.org/abs/2609.02653)（2609.02653）
- [What Matters, When? Diagnosing and Improving Conditional Visual Grounding in Visuomotor Imitation Policies](https://arxiv.org/abs/2609.05376)（2609.05376）
- [One Word, Different Action: A Real-Robot Benchmark for Language-Conditioned Embodied Reasoning](https://arxiv.org/abs/2609.05260)（2609.05260）
- [GRAVA: Grounded Reasoning-to-Action Representation and Learning for Autonomous Driving](https://arxiv.org/abs/2609.15169)（2609.15169）
- [MIGU: Multimodal Instruction Grounding under Uncertainty for Manipulation Planning](https://arxiv.org/abs/2609.24995)（2609.24995）
