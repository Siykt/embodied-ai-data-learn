---
title: 具身数据质量与基准评估
description: 设计可追溯的任务、标注、切分和误差归因，避免单一成功率掩盖数据与执行缺陷。
---

具身基准是一套可复现的**数据、任务、执行协议和评分规则**，不只是任务清单。相同模型在不同场景构成、示教预算或部署接口下的成绩可能不可比。[H2RBench](https://arxiv.org/abs/2609.24778)针对人到机器人迁移统一真实人体视频与仿真机器人演示的比较设置；[REAL-I 经验总结](https://arxiv.org/abs/2609.13679)则指出离线动作预测指标难以预示闭环成功。评估设计应从数据契约开始。

![具身基准从任务意图、数据工件、执行协议到审计结果的构建流程](/images/docs/embodied-evaluation-data-quality-flow.svg)

## 构建可审计的评估单元

先定义任务初态、允许操作、目标谓词、时间/碰撞限制、终止条件和可观测证据。每个 episode 保存场景版本、物体实例、指令、策略版本、随机种子、执行日志与评分器版本。[Embodied-BenchForge](https://arxiv.org/abs/2609.13082)强调基准构建中间工件的依赖与逐项核验；因此场景生成、标注、脚本和评分器要分别有版本与校验结果。

对长时任务，记录子技能进入、完成、失败和重试事件。[Behavior-Skill](https://arxiv.org/abs/2608.30536)做细粒度技能评价；[EmbodiedMemory-Bench](https://arxiv.org/abs/2609.28236)要求智能体从交互历史更新记忆，再在后续任务中使用。两类基准都需要保存阶段间状态，而不只报最终成功。

![基准评估包中任务版本、原始观测、过程事件与评分证据的关系](/images/docs/embodied-evaluation-data-quality-contract.svg)

## 最小数据契约

| 对象 | 建议字段 | 复现检查 |
| --- | --- | --- |
| 任务定义 | `task_spec_id`, `initial_state`, `goal_predicates`, `termination_rules` | 目标是否可由观测或独立测量判定 |
| 数据来源 | `scene_id`, `object_ids`, `demo_source`, `annotation_version`, `license` | 训练与测试是否共享原始轨迹或派生样本 |
| 执行过程 | `episode_id`, `policy_hash`, `seed`, `observation_log`, `action_log`, `events` | 失败可否逐步回放 |
| 分数与证据 | `metric_version`, `success`, `stage_scores`, `failure_cause`, `review_status` | 自动评分与人工复核有无冲突 |

## 质量控制与误差归因

![具身评估从感知、语义、动作和环境四个层次追溯失败](/images/docs/embodied-evaluation-data-quality-evaluation.svg)

评估至少分开四类错误：感知或定位错误、语义理解正确但动作未随之改变、动作可行却控制失败，以及环境或评分器缺陷。[STAGE](https://arxiv.org/abs/2609.13458)用固定观测、仅改变指令语义的反事实样本检验语义是否真正进入动作；[IMPACT-VLA](https://arxiv.org/abs/2609.15005)利用反事实轨迹做多模态归因。反事实成对样本必须除测试变量外保持观测、初态和控制条件一致。

只汇总平均成功率会隐藏脆弱点。按任务阶段、物体、场景、视觉条件和干扰组合切片；[复合鲁棒性配对评估](https://arxiv.org/abs/2609.15940)提示单轴扰动得分不能代替组合条件。[RoboSPA](https://arxiv.org/abs/2609.05324)关注复杂场景和长时任务，[Bench2Dex](https://arxiv.org/abs/2609.15726)关注跨灵巧手的视觉触觉双臂操作，[Neverwhere](https://arxiv.org/abs/2609.16443)关注视觉跑酷；综合报告要保留各自测试轴。

划分数据时按原始场景、物体实例、人体视频、演示者和任务组合成组，所有增强及转码版本跟随原样本。报告示教数量、机器人监督量、超参数搜索预算和置信区间。[JumpStart](https://arxiv.org/abs/2609.13730)的大规模实验显示算法排名受调参与基准组成影响；因此公开选择协议，避免只展示最优检查点。对世界模型、仿真器和视觉检索，分别核对预测校准 [PAWBench](https://arxiv.org/abs/2608.27345)、神经肌肉行为与动作外观差异 [肌肉驱动仿真保真度](https://arxiv.org/abs/2609.21909)、以及检索规则与经验库质量 [视觉经验检索审计](https://arxiv.org/abs/2609.26567)。

## 2026 年 10 月：从总体成功率走向证据与覆盖审计

截至 **2026-10-22**。以下增量依据本月论文，字段设计和验收步骤是本站工程建议。

### 一条评估记录需要说明到底测了哪一层

10 月的基准覆盖高层计划、程序化视频、完整机器人执行和持续改进，评分不能直接互换。[Plan-Bench（2610.18836）](https://arxiv.org/abs/2610.18836)有意隔离动作执行；[RobotWorld（2610.10409）](https://arxiv.org/abs/2610.10409)则要求仿真中的机器人闭环任务执行，并设置交互预算。两者应分别标注 `evaluation_layer=planning` 与 `execution`。前者回答计划是否合理，后者才覆盖控制和任务终点。

[HumanoidToolBench（2610.02089）](https://arxiv.org/abs/2610.02089)把选工具与移动执行连起来；[TARSphere（2610.30043）](https://arxiv.org/abs/2610.30043)进一步在物理仿真与受约束的虚拟角色交互中，用事件驱动任务状态表示环境变化、任务更新和人类协作。建议每个终点标签关联阶段验证器、触发事件和当时任务版本，尤其不能将完成旧指令当作完成更新后的任务。

![从总体成功率走向证据与覆盖审计的数据记录与评估关系](/images/docs/embodied-evaluation-data-quality-october-data.svg)

### 真值、代理测量与自动评审分层保存

[ROWBench / PROWBench（2610.02205）](https://arxiv.org/abs/2610.02205)提供程序记录的实体状态和时间事件，可以检查视频是否呈现了可观察后果。[PVBench（2610.26711）](https://arxiv.org/abs/2610.26711)从目标级物理量估计视频的合理性。前者的引擎记录和后者从画面估计出的量不是同一证据等级；后者需保留尺度标定与估计误差，遮挡期间不应捏造物体状态。原记录标题写 ROWBench，摘要将基准称作 PROWBench，本页保留这一名称差异以便检索。

[RoboFQE（2610.18699）](https://arxiv.org/abs/2610.18699)研究从离线轨迹估计目标策略的折扣回报。**离策略评估**是在不重新执行目标策略的条件下，利用已有行为数据估计其表现。数据应保存行为策略版本、终止标记、奖励来源和状态动作覆盖；学习得到的终点成功标签需要独立审计。可报告回报误差和策略排序一致性，但估计值不能替代真实部署验证。

### 任务变好时，评审未必更容易

[Coverage Shift（2610.24801）](https://arxiv.org/abs/2610.24801)展示策略改进后，残余失败可能集中在更难看出的状态。设总执行数为 N，真实失败数为 F，被评审误接受的失败数为 M，至少同时报告 `M/N`（全部执行中的漏报）与 `M/F`（条件漏报）；F 为零时后者应标为不可估计。仅看前者下降，可能掩盖评审对残余失败更迟钝。

同时记录审计覆盖了哪些高度、遮挡、接触和阶段切片。成功评审模型、用于训练筛选的评审模型和最终真值来源分别版本化。不要让同一个自动裁判既负责训练样本准入，又独自证明最终质量。

### 经验迁移要重置环境并匹配预算

[MC-EvoBench（2610.13829）](https://arxiv.org/abs/2610.13829)只允许声明的智能体产物跨源任务和目标任务边界；[PhysRSI-eval（2610.26848）](https://arxiv.org/abs/2610.26848)区分首次表现、效率、成功、预算与从失败改进。实践中记录跨边界的记忆/程序清单，重置目标世界，匹配交互步数，并保留无经验、相关、无关和打乱经验对照。若早期阶段一直失败，后续阶段能力属于未观测，不能直接标为缺乏。

### 2026 年 10 月来源与数据启示

以下说明以原始摘要为依据；具体性能数字与复现实验应继续核对论文正文。

| 论文 | 数据启示 |
| --- | --- |
| [2610.02089 · HumanoidToolBench: Benchmarking Humanoid Tool Use from Selection to Mobile Execution](https://arxiv.org/abs/2610.02089) | 含仿真及真实人形机器人示教集和分层任务指标。 |
| [2610.02205 · ROWBench: Do Video Models Render What the Program Specifies?](https://arxiv.org/abs/2610.02205) | 包含可回放实体状态、时间戳事件和同步视图，可用于世界模型数据审计。 |
| [2610.10409 · RobotWorld: Benchmarking Multimodal Agents for Robot Use Across Diverse Tasks and Embodiments](https://arxiv.org/abs/2610.10409) | 84类机器人仿真任务具有可执行成功检查，可分析感知/控制/恢复错误。 |
| [2610.13829 · MC-EvoBench: Auditing Experience-Driven Self-Improvement in Minecraft Agents](https://arxiv.org/abs/2610.13829) | Minecraft为交互环境边界，提供声明工件、状态重置和成对源目标评估；不能替代物理机器人实验。 |
| [2610.18699 · RoboFQE: Rollout-Free Evaluation of Visual Robot Policies from Offline Trajectories](https://arxiv.org/abs/2610.18699) | 利用离线机器人轨迹估计策略回报，是具身数据评估的直接研究。 |
| [2610.18836 · Plan-Bench: Can Existing VLMs Go Well Beyond Perception to Reason and Plan in Embodied Worlds?](https://arxiv.org/abs/2610.18836) | 评测面向物理任务的空间、时间与多步规划，属于执行前能力的边界评估。 |
| [2610.24801 · When Better Policies Leave Harder Failures: Coverage Shift in VLM Success Monitoring](https://arxiv.org/abs/2610.24801) | 研究机器人策略改善后成功监测器的失败分布变化，直接关乎质量评估。 |
| [2610.26711 · PVBench: Quantifying Physical Plausibility in Video Generation with Object-Level Physical Measurements](https://arxiv.org/abs/2610.26711) | 虽面向视频生成，但包含机器人等物理主体并提供可测物理指标，属于具身合成数据质量边界。 |
| [2610.26848 · Where is Physical RSI capability from? An Observational Scaling Law of LLM-as-policy](https://arxiv.org/abs/2610.26848) | 对物理自我改进的机器人任务、交互预算和失败学习进行系统评测。 |
| [2610.30043 · TARSphere: A Robot-Oriented Full-Stack Framework for Long-Horizon Embodied Agents in Evolving Physical and Social Environments](https://arxiv.org/abs/2610.30043) | 在物理和社会约束下评测长任务机器人，含可执行技能、场景与人类交互。 |

## 2026 年 9 月来源

本页索引收录 2026-08-27 至 2026-09-27 发表、归入本主题的论文。

- [PAWBench: How Far Are We from Probabilistically Aligned World Modeling?](https://arxiv.org/abs/2608.27345)（2608.27345）
- [Behavior-Skill: A Fine-Grained Benchmark for Evaluating Vision-Language-Action Policies in Long-Horizon Tasks](https://arxiv.org/abs/2608.30536)（2608.30536）
- [From Proxy Learning to Driving Decisions: A Transfer-Based Framework for Evaluating Future-Aware Autonomous Driving Planners](https://arxiv.org/abs/2609.02688)（2609.02688）
- [RoboSPA: Can VLA Models Go Beyond Simple Scenes and Short-Horizon Tasks?](https://arxiv.org/abs/2609.05324)（2609.05324）
- [The Latent That Never Was: A Forensic Re-run of the CVAE Ablation in Action Chunking Transformer](https://arxiv.org/abs/2609.16745)（2609.16745）
- [EgoPathBench: Evaluating Zero-Shot Egocentric Waypoint Decision-Making in Vision-Language Models](https://arxiv.org/abs/2609.16610)（2609.16610）
- [The Neverwhere Visual Parkour Benchmark Suite](https://arxiv.org/abs/2609.16443)（2609.16443）
- [Beyond Single-Axis Testing: Paired Evaluation of Compound Robustness in Vision-Language-Action Policies](https://arxiv.org/abs/2609.15940)（2609.15940）
- [Bench2Dex: Benchmarking Visuo-Tactile Bimanual Dexterous Manipulation Across Dexterous Hands](https://arxiv.org/abs/2609.15726)（2609.15726）
- [IMPACT-VLA: Interaction-aware Multimodal Propagation Attribution via Counterfactual Trajectories for Vision-Language-Action Policies](https://arxiv.org/abs/2609.15005)（2609.15005）
- [What Makes a 3D Scene Editable? A Factorized Benchmark of Fidelity, Locality, Consistency, and Preservation](https://arxiv.org/abs/2609.14899)（2609.14899）
- [One Model, Two Physical Stories: Auditing Misalignment in Multi-Modal World Modeling](https://arxiv.org/abs/2609.14833)（2609.14833）
- [PuzzleMate: Benchmarking MLLMs for Egocentric Puzzle Assistance](https://arxiv.org/abs/2609.14473)（2609.14473）
- [JumpStart Your Policy Learning with Lessons from 160,000 Training Runs](https://arxiv.org/abs/2609.13730)（2609.13730）
- [How to Better Train VLAs: Lessons Learned From the REAL-I Challenge at ICRA 2026](https://arxiv.org/abs/2609.13679)（2609.13679）
- [STAGE: Diagnosing Semantic Transfer at Grounded Execution in Embodied Agents](https://arxiv.org/abs/2609.13458)（2609.13458）
- [Embodied-BenchForge: A Closed-Loop Agentic Workflow for Embodied Benchmark Construction](https://arxiv.org/abs/2609.13082)（2609.13082）
- [Benchmarking World Models for Continual Learning on Compositional Tasks](https://arxiv.org/abs/2609.22055)（2609.22055）
- [Beyond Kinematics: Benchmarking Simulation Fidelity for Muscle-Driven Imitation Learning](https://arxiv.org/abs/2609.21909)（2609.21909）
- [H2RBench: A Real-to-Sim Benchmark for Evaluating Human-to-Robot Transfer](https://arxiv.org/abs/2609.24778)（2609.24778）
- [Beyond End-Task Success: How to Audit Visual Experience Retrieval in Robotics](https://arxiv.org/abs/2609.26567)（2609.26567）
- [AnchorReasoning: A Visual Grounding and Causal Reasoning Dataset in Long-Tail Autonomous Driving Scenarios](https://arxiv.org/abs/2609.28366)（2609.28366）
- [EmbodiedMemory-Bench: Benchmarking Embodied Memory for Long-Horizon Embodied Tasks](https://arxiv.org/abs/2609.28236)（2609.28236）
