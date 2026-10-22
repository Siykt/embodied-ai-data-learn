---
title: 2026 年 10 月论文知识点索引
description: 截至 2026-10-22，从 spiders 筛选 176 篇论文，整理 32 个具身数据主题及逐篇来源、排除理由与证据边界。
---

本页是 **2026 年 10 月截至 22 日**的整理快照。按单篇 `published`（UTC）筛选 **2026-10-01 至 2026-10-22**，当前实际最晚论文发表于 **2026-10-21**。本地 `spiders/arxiv/papers/` 中有 **176 篇唯一论文**符合时间窗口：**167 篇纳入、9 篇范围外，归为 32 个独立主题**，其中更新 29 个已有主题、新增 3 个主题。

![从 52 个日期批次筛选 176 篇论文并归入 32 个独立主题的过程](/images/docs/2026-10-paper-selection.svg)

## 整理范围与复查方法

- 扫描全部 52 个日期命名 JSON，共 524 条记录；13 个批次含本窗口论文。10 月抓取文件可能保存 9 月论文，因此不按文件名算发表月份。
- 按去版本 arXiv ID 去重，本窗口没有重复 ID。`latest.json` 是滚动窗口，不作为独立来源。
- 逐篇阅读原始英文摘要，按采集、处理、对齐、标注、质量控制、评估与数据集使用确定主主题；跨页引用可以重复，统计只算一次。
- 本页反映本地爬取快照，**不是 arXiv 全量，也不是完整 10 月结算**。原始来源与排除理由保存在[可下载的论文追溯清单](/data/2026-10-paper-manifest.json)。清单包含来源记录哈希、日期、主题和证据可用性，不复制论文全文。
- [9 月索引](/reference/2026-09-paper-knowledge-map/)保留原有快照。主题页沿用稳定地址，分别标出 9 月来源与 10 月增量。

## 按数据问题阅读

![从采集、状态表达、监督、闭环改进、物理执行到评估的六组阅读入口](/images/docs/2026-10-paper-reading.svg)

| 独立主题 | 本月论文数 | 本轮变更 |
| --- | ---: | --- |
| [三维空间表征与部件数据](/guides/3d-spatial-representation-data/) | 6 | 补充 10 月进展 |
| [主动感知与任务化测量数据](/guides/active-perception-data/) | 4 | 补充 10 月进展 |
| [闭环纠错与失败经验数据](/guides/closed-loop-correction-data/) | 3 | 补充 10 月进展 |
| [机器人持续学习与经验保留数据](/guides/continual-robot-learning-data/) | 5 | 新建主题 |
| [可变形物体与材质状态数据](/guides/deformable-material-state-data/) | 1 | 补充 10 月进展 |
| [示教采集与动作重定向](/guides/demonstration-collection-retargeting/) | 5 | 补充 10 月进展 |
| [示教数据筛选与再利用](/guides/demonstration-data-curation/) | 2 | 补充 10 月进展 |
| [灵巧操作与双臂装配数据](/guides/dexterous-manipulation-data/) | 3 | 补充 10 月进展 |
| [特定行业具身数据设计](/guides/domain-specific-embodied-data/) | 4 | 补充 10 月进展 |
| [具身数据质量与基准评估](/guides/embodied-evaluation-data-quality/) | 10 | 补充 10 月进展 |
| [具身记忆与经验检索数据](/guides/embodied-memory-experience-data/) | 7 | 补充 10 月进展 |
| [Human-gated DAgger 纠错数据](/guides/human-gated-dagger-correction-data/) | 2 | 补充 10 月进展 |
| [人体与人-物交互重建数据](/guides/human-object-interaction-reconstruction/) | 4 | 补充 10 月进展 |
| [人形与足式全身运动数据](/guides/humanoid-locomotion-data/) | 8 | 补充 10 月进展 |
| [模仿学习动作数据与轨迹表示](/guides/imitation-learning-action-data/) | 1 | 补充 10 月进展 |
| [语言指令与机器人动作对齐数据](/guides/language-action-grounding-data/) | 5 | 补充 10 月进展 |
| [潜在动作与跨本体对齐](/guides/latent-action-cross-embodiment/) | 4 | 补充 10 月进展 |
| [模型条件化数据引擎](/guides/model-conditioned-data-engine/) | 4 | 补充 10 月进展 |
| [多机器人协作与共享状态数据](/guides/multi-robot-coordination-data/) | 6 | 新建主题 |
| [多模态时空对齐数据](/guides/multimodal-spatiotemporal-alignment/) | 3 | 补充 10 月进展 |
| [导航、语义地图与可通行性数据](/guides/navigation-traversability-data/) | 2 | 补充 10 月进展 |
| [个性化偏好与机器人操作数据](/guides/personalized-preference-data/) | 1 | 新建主题 |
| [奖励、价值函数与反馈数据](/guides/reward-value-feedback-data/) | 8 | 补充 10 月进展 |
| [机器人安全与鲁棒性数据](/guides/robot-safety-robustness-data/) | 5 | 补充 10 月进展 |
| [机器人技能组合与任务过程数据](/guides/robot-skill-composition-data/) | 5 | 补充 10 月进展 |
| [合成数据与仿真到真实迁移](/guides/synthetic-data-sim-to-real/) | 5 | 补充 10 月进展 |
| [触觉、力觉与接触数据](/guides/tactile-force-contact-data/) | 12 | 补充 10 月进展 |
| [轨迹规划、控制与物理约束数据](/guides/trajectory-control-constraint-data/) | 4 | 补充 10 月进展 |
| [VLA 模型与主流验证方法](/guides/vla-models-and-evaluation/) | 3 | 补充 10 月进展 |
| [VLA 实时执行与动作分块数据](/guides/vla-realtime-execution-data/) | 4 | 补充 10 月进展 |
| [世界模型规划与决策评估](/guides/world-model-planning-evaluation/) | 6 | 补充 10 月进展 |
| [世界模型训练数据与物理表征](/guides/world-model-training-data/) | 25 | 补充 10 月进展 |

## 证据覆盖与使用限制

![原始摘要、本地全文缓存、派生摘要与官方抽查的覆盖及区别](/images/docs/2026-10-paper-evidence.svg)

全部 176 篇都具有原始摘要，本地另有 17 份全文缓存、144 份中文摘要、143 份自动验证记录；在纳入的 167 篇中，全文缓存为 15 份。自动验证虽然全部为 `pass=true`，但只有 17 份标记获取了额外全文证据。其余记录主要相对于摘要和图注评分，**不能理解为已审核全文或已证实实验可复现**。

本轮额外核对了 10 篇官方摘要的标题、日期和内容，并抽查其中 9 篇官方 HTML 全文；具体 ID 见追溯清单。Dream to Remember（2610.13816）的官方 HTML 在本轮不可用，保留摘要级结论。其余主题主要依据原始摘要提炼数据问题，字段名与验收流程均为本站工程建议。

以下边界影响数据复用：

- 多机器人研究需区分仿真协作、操作者界面实验与真机团队执行，不能将三者视作同一种部署证据。
- LIBERO-PeRM 的任务数包含偏好和无偏好对照，其预定义仿真偏好不能代表长期开放式用户需求。
- AnyGoal 关注熟悉因素的欠覆盖组合，底层动力学保持不变；PhysiCalWorld 仍需同物理配置的轨迹分组，实验是仿真。
- 原始摘要可能简化基线与条件。正文优先解释输入输出、数据约束与评估口径，避免把单篇百分比推广为通用结论。

## 逐篇知识点归属

每篇纳入论文只有一个主主题；下列“数据切入点”用于定位正文，详细字段、图示与质量检查见相应主题页。

### 三维空间表征与部件数据

**6 篇** · [阅读主题文档](/guides/3d-spatial-representation-data/)。

| 论文与发表日期 | 数据切入点 |
| --- | --- |
| [2610.02021 · Task-Adaptive Grounded 3D-Programmers Using 2D VLMs](https://arxiv.org/abs/2610.02021)（2026-10-01） | 统一米制坐标与任务反馈 |
| [2610.02120 · SkeleWAM: Skeleton World-Action Modeling for Efficient Robotic Manipulation](https://arxiv.org/abs/2610.02120)（2026-10-01） | 机器人—物体稀疏三维骨架 |
| [2610.03717 · Less Decoder is More Encoder: Geometric Representation Learning from Novel View Synthesis](https://arxiv.org/abs/2610.03717)（2026-10-02） | 位姿条件多视角几何监督 |
| [2610.06809 · Block Disentanglement in CRL: Bridging Identifiability and Visual State Estimation](https://arxiv.org/abs/2610.06809)（2026-10-05） | 无标签视觉状态与因果干预 |
| [2610.22343 · GeoState: Learning View-Decoupled Geometry States for 3D World Modeling](https://arxiv.org/abs/2610.22343)（2026-10-15） | 多视角几何特征需要区分场景演变与相机运动，并保持 rollout 内统一尺度；跨视角查询与跨数据集评测可暴露逐帧尺度对齐掩盖的误差。 |
| [2610.24705 · Relational Spatial Alignment for Vision-Language-Action Models](https://arxiv.org/abs/2610.24705)（2026-10-17） | 几何监督可约束特征之间的空间关系，而非强制逐点相同；评估应同时检查空间推理、表示退化和真实操作效果，避免仅凭特征相似度验收。 |

### 主动感知与任务化测量数据

**4 篇** · [阅读主题文档](/guides/active-perception-data/)。

| 论文与发表日期 | 数据切入点 |
| --- | --- |
| [2610.03710 · EyeRobot 2.0: Active Gaze for Precise Manipulation without Wrist Cameras](https://arxiv.org/abs/2610.03710)（2026-10-02） | 主动注视和相对注视坐标 |
| [2610.10388 · RoboQuest: Generalist Physical Agents that Search, Inspect and Test](https://arxiv.org/abs/2610.10388)（2026-10-07） | 搜索、检查和试验的证据获取 |
| [2610.12457 · SpatialHarness: Test-Time Spatial Scaffolding for Fine Robotic Manipulation](https://arxiv.org/abs/2610.12457)（2026-10-08） | 虚拟视点与在线场景同步 |
| [2610.30105 · Asymmetric On-Policy Distillation Learns In-Context Exploration](https://arxiv.org/abs/2610.30105)（2026-10-21） | 让学生以自身策略收集历史，再由特权专家为该历史标注动作，可覆盖实际探索状态；需记录何时信息被揭示，并在固定探索预算下评价收益。 |

### 闭环纠错与失败经验数据

**3 篇** · [阅读主题文档](/guides/closed-loop-correction-data/)。

| 论文与发表日期 | 数据切入点 |
| --- | --- |
| [2610.02204 · Reconstruct, Practice, Go Real: Guided Self-Improvement for Embodied Agents](https://arxiv.org/abs/2610.02204)（2026-10-01） | 模拟练习中的失败诊断与技能改进 |
| [2610.14977 · EnactOpt: Diagnosis-Guided Harness Evolution for Embodied Agents](https://arxiv.org/abs/2610.14977)（2026-10-10） | 相邻决策诊断与经验摘要 |
| [2610.18873 · LoopWAM: Closed-Loop Generalist Policy Improvement from Deployment Rollouts](https://arxiv.org/abs/2610.18873)（2026-10-13） | 混合质量 rollout 可保留完整视频监督，同时用质量权重控制动作模仿；记录来源策略、质量、迭代轮次和部署分布，才能追踪失败经验的利用方式。 |

### 机器人持续学习与经验保留数据

**5 篇** · [阅读主题文档](/guides/continual-robot-learning-data/)。

| 论文与发表日期 | 数据切入点 |
| --- | --- |
| [2610.03713 · What Should World Models Forget? Stratified Retention for Continual Adaptation](https://arxiv.org/abs/2610.03713)（2026-10-02） | 不变量与过期实例事实的差异保留 |
| [2610.13816 · Dream to Remember: Continual Steering of Generalist Robot Policies with World Models](https://arxiv.org/abs/2610.13816)（2026-10-09） | 想象回放保留历史机器人技能 |
| [2610.18790 · EqC: Equilibrium Energy Control for Introspective Lifelong Robot Learning](https://arxiv.org/abs/2610.18790)（2026-10-13） | 将能力违例、专家接管和恢复轨迹关联策略更新版本，并保留固定场景评估快照；持续学习既要检验自主能力边界扩展，也需对早期任务检查性能保持。 |
| [2610.18792 · SEAR: Self-Evolving Agentic Robotics](https://arxiv.org/abs/2610.18792)（2026-10-13） | 将保留经验、控制程序及技能版本与任务流关联，在固定预算和冻结经验快照下评测跨任务迁移；分开控制重复尝试、特权状态与场景熟悉度，检验是否真正积累可复用能力。 |
| [2610.24804 · SARAM: Sparse Adapter Allocation with Reuse and Merging for Lifelong Robot Learning](https://arxiv.org/abs/2610.24804)（2026-10-17） | 终身学习数据应保留任务流顺序、历史任务评测和每轮适配器版本，并在固定设备预算下报告旧任务保持、存储增长与控制频率。 |

### 可变形物体与材质状态数据

**1 篇** · [阅读主题文档](/guides/deformable-material-state-data/)。

| 论文与发表日期 | 数据切入点 |
| --- | --- |
| [2610.15073 · Modeling and Control of a Rigid-soft Hybrid-link Humanoid Robot](https://arxiv.org/abs/2610.15073)（2026-10-10） | 刚柔连杆形变与全身控制记录 |

### 示教采集与动作重定向

**5 篇** · [阅读主题文档](/guides/demonstration-collection-retargeting/)。

| 论文与发表日期 | 数据切入点 |
| --- | --- |
| [2610.06850 · InterMimicGen: Scaling Humanoid Loco-Manipulation through Self-Evolving Motion Imitation](https://arxiv.org/abs/2610.06850)（2026-10-05） | 保留接触的人体动作重定向与扩增 |
| [2610.12440 · Generative Neural Retargeting for Human-to-Robot Dexterous Manipulation](https://arxiv.org/abs/2610.12440)（2026-10-08） | 动态可行重定向与稠密接触力标签 |
| [2610.18711 · Steertuning Policies from a Few Human Videos](https://arxiv.org/abs/2610.18711)（2026-10-13） | 100 小时密集标注随机人体交互用于预训练，5 条新任务示教用于适配和采样引导；人体到机器人处理链与新环境留出应共同记录。 |
| [2610.18822 · EgoMatrix: Physically Faithful Dexterous Robot Demonstrations from Egocentric Human Videos](https://arxiv.org/abs/2610.18822)（2026-10-13） | 从手物相对几何和接触重建出发，经重定向与仿真执行生成同步状态、动作和机器人视频；背景扩增应保持物体运动及接触关系不变。 |
| [2610.26762 · DexOAK: Object-Aware Kinematic Retargeting](https://arxiv.org/abs/2610.26762)（2026-10-19） | 重定向应保留手物相对交互图、接触位置、非穿透与自碰撞约束；用未见物体和真实开环重放检验参考是否可用于机器人数据生成。 |

### 示教数据筛选与再利用

**2 篇** · [阅读主题文档](/guides/demonstration-data-curation/)。

| 论文与发表日期 | 数据切入点 |
| --- | --- |
| [2610.18869 · What Matters in Quality-Aware VLA Pretraining: A Benchmark and Empirical Study](https://arxiv.org/abs/2610.18869)（2026-10-13） | 质量标签需保留奖励定义和 episode、动作块等粒度；在相同示教与训练预算下比较筛选策略，利用物体和接触状态重算标签，避免把来源差异误当质量收益。 |
| [2610.20504 · Graph-Reweighted Behavior Cloning with Human Interventions for Precise Robotic Manipulation](https://arxiv.org/abs/2610.20504)（2026-10-14） | 按数据支持内到成功的可达步数对动作块赋权，可复用失败轨迹中的恢复段并降权成功轨迹中的倒退段；保存图连接、干预段和每轮权重便于审计。 |

### 灵巧操作与双臂装配数据

**3 篇** · [阅读主题文档](/guides/dexterous-manipulation-data/)。

| 论文与发表日期 | 数据切入点 |
| --- | --- |
| [2610.12470 · Dex-One2Many: Learning Dexterous Manipulation from a Single Human Demonstration](https://arxiv.org/abs/2610.12470)（2026-10-08） | 单人类视频的关系图与多样初始状态 |
| [2610.26765 · HandsOn: A Large-Scale Simulation Benchmark for Generalizable Dexterous Manipulation](https://arxiv.org/abs/2610.26765)（2026-10-19） | 灵巧操作数据需标注机械臂、手型、物体属性和任务关系，并隔离有目标示教的核心任务与无目标示教的迁移任务，分阶段诊断接触和协调失败。 |
| [2610.29997 · DONIC: Generalist Dexterous Bimanual Tracking Control from Human Demonstrations](https://arxiv.org/abs/2610.29997)（2026-10-21） | 双手示教应记录各手接触角色和共同物体运动，保留视频重建到机器人参考的来源链；验证成功执行回流训练时必须隔离未见轨迹及未见物体评测。 |

### 特定行业具身数据设计

**4 篇** · [阅读主题文档](/guides/domain-specific-embodied-data/)。

| 论文与发表日期 | 数据切入点 |
| --- | --- |
| [2610.10390 · Explicit Geometric Chain-of-Thought for Vision-Language-Action in Autonomous Driving](https://arxiv.org/abs/2610.10390)（2026-10-07） | 自动驾驶决策区域与局部三维监督 |
| [2610.22337 · Sim-to-Real Reinforcement Learning for Path-Safe Target Reaching in Robotic Harvesting of Hydroponic Lettuce](https://arxiv.org/abs/2610.22337)（2026-10-15） | 农业采收轨迹应标记目标、侧向安全走廊、末段接近路径和完整采收结果；只检查终点精度会漏掉植株附近的危险路径与不平滑动作。 |
| [2610.24747 · EndoVLA-OOV: Language-Conditioned Out-of-View Target Acquisition in Robotic Endoscopy](https://arxiv.org/abs/2610.24747)（2026-10-17） | 医学复访数据应关联初始、中间与当前图像、解剖描述和弯曲动作；按镜面湿润、低照度、未见模型及跨本体切分，区分数据规模收益和环境泛化。 |
| [2610.26717 · Robot Learning with Vision-Language-Action Models for Agricultural Manipulation](https://arxiv.org/abs/2610.26717)（2026-10-19） | 番茄场景数据应覆盖植株几何、遮挡、视角和空间位移，区分仿真适配与真实微调来源，并检查本体状态信息对农业分布外操作的贡献。 |

### 具身数据质量与基准评估

**10 篇** · [阅读主题文档](/guides/embodied-evaluation-data-quality/)。

| 论文与发表日期 | 数据切入点 |
| --- | --- |
| [2610.02089 · HumanoidToolBench: Benchmarking Humanoid Tool Use from Selection to Mobile Execution](https://arxiv.org/abs/2610.02089)（2026-10-01） | 工具选择到移动执行的分层评测 |
| [2610.02205 · ROWBench: Do Video Models Render What the Program Specifies?](https://arxiv.org/abs/2610.02205)（2026-10-01） | 程序事件与生成视频的一致性评估 |
| [2610.10409 · RobotWorld: Benchmarking Multimodal Agents for Robot Use Across Diverse Tasks and Embodiments](https://arxiv.org/abs/2610.10409)（2026-10-07） | 跨本体任务、交互预算与执行轨迹 |
| [2610.13829 · MC-EvoBench: Auditing Experience-Driven Self-Improvement in Minecraft Agents](https://arxiv.org/abs/2610.13829)（2026-10-09） | 经验迁移的隔离环境和对照预算 |
| [2610.18699 · RoboFQE: Rollout-Free Evaluation of Visual Robot Policies from Offline Trajectories](https://arxiv.org/abs/2610.18699)（2026-10-13） | 离线策略评估可复用历史视觉轨迹与学习得到的终局成功标注；应分别检验回报估计误差、策略排序和长任务表现，不能将无新 rollout 等同于无评估误差。 |
| [2610.18836 · Plan-Bench: Can Existing VLMs Go Well Beyond Perception to Reason and Plan in Embodied Worlds?](https://arxiv.org/abs/2610.18836)（2026-10-13） | 将高层推理和规划题的空间状态、时间顺序与约束单独标注，能隔离执行器误差；该基准的答题准确率不能替代机器人闭环成功率。 |
| [2610.24801 · When Better Policies Leave Harder Failures: Coverage Shift in VLM Success Monitoring](https://arxiv.org/abs/2610.24801)（2026-10-17） | 策略更新会改变剩余失败的可见性；质量报告需同时记录绝对漏检数、失败条件下漏检率和审计覆盖，尤其保留遮挡造成的边界失败样本。 |
| [2610.26711 · PVBench: Quantifying Physical Plausibility in Video Generation with Object-Level Physical Measurements](https://arxiv.org/abs/2610.26711)（2026-10-19） | 物理视频质检可记录物体六维位姿、尺度、运动及守恒残差，并用人工一致性验证自动评分；视频物理合理性仍不同于动作条件执行可靠性。 |
| [2610.26848 · Where is Physical RSI capability from? An Observational Scaling Law of LLM-as-policy](https://arxiv.org/abs/2610.26848)（2026-10-19） | 评估自我改进应同时报告首次表现、效率、成功、预算与失败后改善，并用移除历史、冻结工作区和新布局对照区分场景适配与可复用经验。 |
| [2610.30043 · TARSphere: A Robot-Oriented Full-Stack Framework for Long-Horizon Embodied Agents in Evolving Physical and Social Environments](https://arxiv.org/abs/2610.30043)（2026-10-21） | 任务数据需对齐语义、因果前提与场景几何，并通过事件状态机记录已完成动作和传递信息；评测应分开覆盖扰动、任务更新、人类协调和碰撞跌倒。 |

### 具身记忆与经验检索数据

**7 篇** · [阅读主题文档](/guides/embodied-memory-experience-data/)。

| 论文与发表日期 | 数据切入点 |
| --- | --- |
| [2610.02162 · World Observer: Joint Actor-Observer Generation for Persistent World Modeling](https://arxiv.org/abs/2610.02162)（2026-10-01） | 视野外状态持续演化 |
| [2610.06843 · Recursive Video In-Context Learning for Agentic Robot](https://arxiv.org/abs/2610.06843)（2026-10-05） | 按事件层级检索示教视频 |
| [2610.10538 · Never Look Back: Understanding Persistence in 3D Object Memory from Egocentric Videos](https://arxiv.org/abs/2610.10538)（2026-10-07） | 持久三维物体位置与历史 |
| [2610.18867 · EmbodiedEvo: Self-improving Coding Agents for Physical Intelligence](https://arxiv.org/abs/2610.18867)（2026-10-13） | 将原始交互历史整理成技能与教训后，应冻结经验集合并留出新场景，分别评测记忆依赖任务、程序复用、接触控制和推理成本。 |
| [2610.20524 · Physical Time as a Missing Dimension of Robot Policy Memory Dynamics](https://arxiv.org/abs/2610.20524)（2026-10-14） | 记忆数据必须保留观测间实际经过时间，而不只保留帧序号；时间干预、遮挡后事件恢复与行为时序应共同用于检验记忆是否利用物理时间。 |
| [2610.22323 · Mem4Act: Learning Effective Latent Memory for Long-Horizon Robotic Manipulation](https://arxiv.org/abs/2610.22323)（2026-10-15） | 历史可按多时间粒度组织，并用问答和关键帧特征共同监督固定大小记忆；需要检验动作策略是否真正使用历史以及哪些证据在压缩中保留。 |
| [2610.24767 · DialogMem: Evaluating Dialogue-Grounded Embodied Memory in 3D Environments](https://arxiv.org/abs/2610.24767)（2026-10-17） | 对话必须按时间连接到具体物体实例及位置；评测应分别诊断记忆形成时的关联、检索正确条目和空间定位，问答改善不代表导航改善。 |

### Human-gated DAgger 纠错数据

**2 篇** · [阅读主题文档](/guides/human-gated-dagger-correction-data/)。

| 论文与发表日期 | 数据切入点 |
| --- | --- |
| [2610.03620 · UniIntervene++: An Adaptive Intervention Agent for Efficient Real-World Reinforcement Learning](https://arxiv.org/abs/2610.03620)（2026-10-02） | 随策略能力调整的控制接管 |
| [2610.10534 · RoboPrompt: Intuitive Robot Policy Steering with Sparse Human Input](https://arxiv.org/abs/2610.10534)（2026-10-07） | 稀疏人工输入转动作草案与DAgger |

### 人体与人-物交互重建数据

**4 篇** · [阅读主题文档](/guides/human-object-interaction-reconstruction/)。

| 论文与发表日期 | 数据切入点 |
| --- | --- |
| [2610.10438 · ECHO: Embodied Camera Observations of Human Object Carrying](https://arxiv.org/abs/2610.10438)（2026-10-07） | 搬运活动与场景目的地标注 |
| [2610.12416 · MAMHOI: Factorizing Scene-Aware Human-Object Interaction through Affordances](https://arxiv.org/abs/2610.12416)（2026-10-08） | 场景可供性与人体物体运动的拆分监督 |
| [2610.26780 · V-JEPA Hand: Simple, Accurate and Fast 3D Hand and Camera Trajectory Recovery from Egocentric Videos](https://arxiv.org/abs/2610.26780)（2026-10-19） | 伪标签与高精度三维标注应注明来源，联合手部存在性、关节和相机运动恢复统一世界坐标；误差评测需要考虑漏检覆盖和世界轨迹漂移。 |
| [2610.29936 · DewHand: Direct Metric World-Space Hand Motion Reconstruction from Egocentric Videos](https://arxiv.org/abs/2610.29936)（2026-10-21） | 重建数据应区分相对对齐误差与米制尺度误差，并为遮挡和视野外手部保留生成不确定性；跨采集设备验证能揭示训练标注的域偏差。 |

### 人形与足式全身运动数据

**8 篇** · [阅读主题文档](/guides/humanoid-locomotion-data/)。

| 论文与发表日期 | 数据切入点 |
| --- | --- |
| [2610.10489 · HuMBLE: Human Motion-Driven Behavior Learning for Embodied Locomotion](https://arxiv.org/abs/2610.10489)（2026-10-07） | 人类步态先验与命令覆盖 |
| [2610.20552 · KinoGen: Customizable Humanoid Loco-Manipulation References via Kinematically Grounded Video Generation](https://arxiv.org/abs/2610.20552)（2026-10-14） | 以标定后的机器人和物体渲染约束双视角生成，再拟合本体配置空间参考；质检应覆盖穿透、足滑、接触保留和指定物体目标的满足情况。 |
| [2610.20606 · Modeling and Understanding Neural Weights of Humanoid Policies with Diffusion](https://arxiv.org/abs/2610.20606)（2026-10-14） | 控制策略权重可作为带本体、训练过程和动作能力标签的样本集合，但生成权重仍需真实执行验证；权重空间规律不等价于完整运动轨迹数据。 |
| [2610.24779 · Learning Structured Locomotion References for Optimization-Based Whole-Body Control](https://arxiv.org/abs/2610.24779)（2026-10-17） | 结构化运动参考需同步记录身体运动、接触力、落脚点和步态时间；在统一扰动网格中做通道消融可区分各参考量对存活率的贡献。 |
| [2610.24847 · DiPLO: Self-distilled Diffusion Planning for Loco-manipulation](https://arxiv.org/abs/2610.24847)（2026-10-17） | 将人体重定向预训练参考、蒸馏阶段与强化学习后训练轨迹分开标记，并检查生成计划是否适配冻结跟踪器的可执行能力。 |
| [2610.30044 · SP-HLM: Sparse-Pose-Driven Motion Generation and Whole-Body Control for Humanoid Loco-Manipulation](https://arxiv.org/abs/2610.30044)（2026-10-21） | 数据接口应对齐五个任务关键位姿、手指关节、完整身体参考和潜在运动先验，保留异步动作块时间，检验空间意图到全身执行的衔接。 |
| [2610.30061 · Test-Time Motion Steering for Perceptive Humanoid Fall Recovery](https://arxiv.org/abs/2610.30061)（2026-10-21） | 恢复数据应覆盖跌倒姿态、地形、支撑转换与最终朝向，并连接动作意图、身体未来状态和控制响应；不同起身方案需按任务目标分别评价。 |
| [2610.30080 · Do Earth-Trained Humanoid Controllers Walk on the Moon? Gravity, Terrain, and Soil Transfer](https://arxiv.org/abs/2610.30080)（2026-10-21） | 重力、地形和土壤接触模型应作为独立数据因子，记录双向迁移及地球性能代价；月面预测必须附带土壤刚度、足压和未见土壤模型的适用范围。 |

### 模仿学习动作数据与轨迹表示

**1 篇** · [阅读主题文档](/guides/imitation-learning-action-data/)。

| 论文与发表日期 | 数据切入点 |
| --- | --- |
| [2610.20429 · When Do Discrete Actions Make Good Continuous Controllers?](https://arxiv.org/abs/2610.20429)（2026-10-14） | 动作量化实验需控制训练数据与预算，分别检查精度、时间及动作维度间的依赖误差、动作块响应性，不能仅凭离散化精度判断可执行性。 |

### 语言指令与机器人动作对齐数据

**5 篇** · [阅读主题文档](/guides/language-action-grounding-data/)。

| 论文与发表日期 | 数据切入点 |
| --- | --- |
| [2610.03615 · Bridging Frontier Reasoning and Robot Execution: From Autonomous Demonstration Generation to Dense Language Supervision](https://arxiv.org/abs/2610.03615)（2026-10-02） | 原语、原子与组合动作的稠密语言监督 |
| [2610.10526 · Rephrase Before You Act: Characterizing and Mitigating Language Sensitivity in Vision-Language-Action Models](https://arxiv.org/abs/2610.10526)（2026-10-07） | 指令改写敏感性与语义等价组 |
| [2610.12386 · ARC: A Reasoning Recipe for Robot Foundation Models](https://arxiv.org/abs/2610.12386)（2026-10-08） | 面向下一动作的因果推理标注 |
| [2610.24885 · Goal Images Are Control Targets: Spatially-Grounded Goal-Image Synthesis for Robotic Manipulation](https://arxiv.org/abs/2610.24885)（2026-10-17） | 目标图像数据应标注正确对象、目标状态及初末编辑区域；质量验收应以动作目标满足和长任务控制成功为主，不能仅用照片真实感或编辑榜单评分。 |
| [2610.26854 · Physical Words: A Vocabulary for Structuring Latent Reasoning in Robot Manipulation](https://arxiv.org/abs/2610.26854)（2026-10-19） | 原子动作词应按时间连接执行阶段、未来观测及可选触觉状态；这种语义与连续物理目标的对齐需要在未见场景和长任务中验证。 |

### 潜在动作与跨本体对齐

**4 篇** · [阅读主题文档](/guides/latent-action-cross-embodiment/)。

| 论文与发表日期 | 数据切入点 |
| --- | --- |
| [2610.03607 · World Action Learning via Interaction-Centric Spectral Latent Guidance](https://arxiv.org/abs/2610.03607)（2026-10-02） | 去除自运动的人类视频潜在动作 |
| [2610.12435 · VioLA: Learning Generalist Humanoid Control Policies from Human Data](https://arxiv.org/abs/2610.12435)（2026-10-08） | 人机共享身体和手部潜在动作 |
| [2610.13732 · LAPT-Scale: Scaling Embodied Policies with Latent Action Pre-Training on Human Videos](https://arxiv.org/abs/2610.13732)（2026-10-09） | 连续潜在动作与转移多信号监督 |
| [2610.18774 · GreenWAM: A World Foundation Model for Robotics](https://arxiv.org/abs/2610.18774)（2026-10-13） | 跨本体数据需要共享解剖动作空间，同时保留机器人家族与原始关节映射；共同动作格式应接受轨迹、深度、三维预测与真实控制的交叉验证。 |

### 模型条件化数据引擎

**4 篇** · [阅读主题文档](/guides/model-conditioned-data-engine/)。

| 论文与发表日期 | 数据切入点 |
| --- | --- |
| [2610.10498 · EmbodiedRSI: Active Continual Robot Learning Through Hypothesis-Guided Co-Evolution](https://arxiv.org/abs/2610.10498)（2026-10-07） | 假设驱动的主动实验与数据回流 |
| [2610.12465 · A Balanced Data Diet: Addressing the Exploration Bottleneck in Mega-Scale RL for Robot Control](https://arxiv.org/abs/2610.12465)（2026-10-08） | 按策略成功边界采样任务配置 |
| [2610.20474 · AdaRSI: On-Demand Recursive Self-Improvement for Embodied Agents](https://arxiv.org/abs/2610.20474)（2026-10-14） | 从保存状态重试失败子步骤，区分调用方式问题与执行能力不足；只为持续失败部分采集和训练，并记录示教数量、预算及跨任务经验来源。 |
| [2610.22362 · CoDA: Co-Evolution of Data Engines and Action Policies](https://arxiv.org/abs/2610.22362)（2026-10-15） | 将环境构造程序、失败诊断、训练程序和学习进展写入共享记录，并保留固定生成预算下的分布外效果，检验生成数据是否针对真实能力缺口。 |

### 多机器人协作与共享状态数据

**6 篇** · [阅读主题文档](/guides/multi-robot-coordination-data/)。

| 论文与发表日期 | 数据切入点 |
| --- | --- |
| [2610.02161 · DuoMind: Enabling Distributed Multi-Robot Coordination with Semantic Communication](https://arxiv.org/abs/2610.02161)（2026-10-01） | 语义通信与分布式任务协调 |
| [2610.02170 · Watch, Infer, Coordinate: Inferring Robot Partner Constraints for Zero-Shot Coordination](https://arxiv.org/abs/2610.02170)（2026-10-01） | 伙伴能力约束的联合行为推断 |
| [2610.15001 · Design and Evaluation of a Collaborative Teleoperation Interface for Multi-Operator Multi-Robot Systems in Challenging Environments](https://arxiv.org/abs/2610.15001)（2026-10-10） | 多操作者共享可视化与协作记录 |
| [2610.15038 · Training-Free Multi-Agent Cooperative Embodied Search from Uncertain Vision-Language Priors](https://arxiv.org/abs/2610.15038)（2026-10-10） | 不确定语义先验和团队联合搜索 |
| [2610.20579 · PingpongDuo: Agile Humanoid Table Tennis Doubles with Safe Team Coordination](https://arxiv.org/abs/2610.20579)（2026-10-14） | 人体双打步法、球飞行与球拍接触测量可分别支持参考动作和仿真标定；轨迹还应标记击球者交替、让位过程及队友碰撞风险。 |
| [2610.22322 · Learning Self-Orchestration in Decentralized Agent Swarms](https://arxiv.org/abs/2610.22322)（2026-10-15） | 多代理轨迹需记录参与竞价、实际执行者、局部反馈与集体结果，以比较协作方式、规模扩展和成员退出；深度研究任务的结果不外推到机器人。 |

### 多模态时空对齐数据

**3 篇** · [阅读主题文档](/guides/multimodal-spatiotemporal-alignment/)。

| 论文与发表日期 | 数据切入点 |
| --- | --- |
| [2610.12451 · VersaCamVLA: Camera-Configurable VLA Policies for Robotic Manipulation](https://arxiv.org/abs/2610.12451)（2026-10-08） | 可变相机集合和位姿多样性 |
| [2610.18872 · EgoExplorer: A Vision-Motion-Touch Observatory for Human Loco-Manipulation In Situ](https://arxiv.org/abs/2610.18872)（2026-10-13） | 人体几何与传感器安装先校准，再补全未观测关节并施加测量、时间连续性和几何约束；应同步保存视频、全身运动、手部关节、触觉与步骤描述。 |
| [2610.26751 · Beyond Omni: A Unified MLLM for Embodied Sensory Understanding](https://arxiv.org/abs/2610.26751)（2026-10-19） | 异质传感数据需要各自表示与语言语义接口，并保留模态特定处理和评测；多模态语料规模不能替代每种传感任务的独立质量验证。 |

### 导航、语义地图与可通行性数据

**2 篇** · [阅读主题文档](/guides/navigation-traversability-data/)。

| 论文与发表日期 | 数据切入点 |
| --- | --- |
| [2610.12368 · LiteNWM: Efficient Latent World Models for Onboard Visual Navigation in the Wild](https://arxiv.org/abs/2610.12368)（2026-10-08） | 共享观测编码的导航候选轨迹评估 |
| [2610.13838 · Mapless, Stabilizing, and Anti-Stuck Flipper Control for Articulated Tracked Robots](https://arxiv.org/abs/2610.13838)（2026-10-09） | 无地图越障的短窗惯性与运动线索 |

### 个性化偏好与机器人操作数据

**1 篇** · [阅读主题文档](/guides/personalized-preference-data/)。

| 论文与发表日期 | 数据切入点 |
| --- | --- |
| [2610.22372 · LIBERO-PeRM: Benchmarking Personalized Robotic Manipulation](https://arxiv.org/abs/2610.22372)（2026-10-15） | 偏好标签应覆盖动作方式、技能选择和用户背景，并与不改变目标的无偏好示教配对；分别评测偏好满足、目标成功、冲突处理与跨布局泛化。 |

### 奖励、价值函数与反馈数据

**8 篇** · [阅读主题文档](/guides/reward-value-feedback-data/)。

| 论文与发表日期 | 数据切入点 |
| --- | --- |
| [2610.02196 · InterEvolve: Test-Time Evolution of Reward Programs for Humanoid Loco-Manipulation](https://arxiv.org/abs/2610.02196)（2026-10-01） | 可验证的分阶段奖励程序 |
| [2610.10437 · Q-Learning with Scalar Adjoint Matching](https://arxiv.org/abs/2610.10437)（2026-10-07） | 离线轨迹的价值估计与真实策略改进 |
| [2610.13943 · Noise Space Learning for VLA Adaptation](https://arxiv.org/abs/2610.13943)（2026-10-09） | 有限交互下的噪声空间后训练 |
| [2610.14936 · CFG-Policy: Unified Diffusion Policy Learning Framework via Classifier-free Guidance](https://arxiv.org/abs/2610.14936)（2026-10-10） | 探索和利用分支的数据分布 |
| [2610.14941 · Compositional Average Velocity Modeling for Efficient Diffusion Offline Reinforcement Learning](https://arxiv.org/abs/2610.14941)（2026-10-10） | 离线RL中的行为约束与候选价值 |
| [2610.20607 · Hierarchical Residual Policy Learning for Real-World Mobile Manipulation with Sparse Human Guidance](https://arxiv.org/abs/2610.20607)（2026-10-14） | 离线基础策略、在线残差和人工干预需分别标识，并保留底盘与机械臂动作关系；干预覆盖率、交互时长和价值对齐效果决定真实数据的利用效率。 |
| [2610.22368 · Value as Memory: Online Value-Guided Post-training for General Robot Policies](https://arxiv.org/abs/2610.22368)（2026-10-15） | 将近期价值预测作为任务进度记忆时，需对齐观测、价值版本、动作和稀疏奖励；并发采集与训练还应记录策略版本，公平比较在线更新和离线更新。 |
| [2610.30097 · AtomicRL: Atomic Reinforcement Learning for Long-Horizon Robotic Manipulation](https://arxiv.org/abs/2610.30097)（2026-10-21） | 奖励与价值数据应保留原子子任务边界，避免失败残差跨边界污染归因；根据子任务掌握程度调整采样时，需记录采样权重和真实迁移结果。 |

### 机器人安全与鲁棒性数据

**5 篇** · [阅读主题文档](/guides/robot-safety-robustness-data/)。

| 论文与发表日期 | 数据切入点 |
| --- | --- |
| [2610.03498 · Detect and Suppress: A Mechanistic Defense against Adversarial Patches in VLA Models](https://arxiv.org/abs/2610.03498)（2026-10-02） | 间歇视觉攻击与条件干预评估 |
| [2610.06814 · TAPDreamer: Transferable Adversarial Patches for World Action Models](https://arxiv.org/abs/2610.06814)（2026-10-05） | 跨任务视觉补丁压力测试 |
| [2610.12432 · FAITH: Feasibility-Aware Safety-Filtered RL for High-Dimensional Systems](https://arxiv.org/abs/2610.12432)（2026-10-08） | 可行/不可行起点与峰值伤害评估 |
| [2610.18843 · LIBERO-RIG: A Hardware-Setup Robustness Benchmark for Vision-Language-Action Models](https://arxiv.org/abs/2610.18843)（2026-10-13） | 在任务保持固定时记录相机安装、标定、增益、控制频率、本体噪声和夹爪磨损等扰动及强度，可区分视觉变化与图像不可见硬件故障。 |
| [2610.20609 · SafeDriveVLA: Navigation-Conditioned World Model Dreaming for Conflict-Aware End-to-End Autonomous Driving](https://arxiv.org/abs/2610.20609)（2026-10-14） | 将正常导航、危险指令和对抗扰动配对，保存遵循指令的预测后果与导航合规模式；闭环语言遵循和碰撞风险应分别评价。 |

### 机器人技能组合与任务过程数据

**5 篇** · [阅读主题文档](/guides/robot-skill-composition-data/)。

| 论文与发表日期 | 数据切入点 |
| --- | --- |
| [2610.12369 · Embodied Turing Machines: Stateful Code for Robot Recursive Self-Improvement](https://arxiv.org/abs/2610.12369)（2026-10-08） | 显式状态与可复用代码技能 |
| [2610.12459 · WorldGuide: Goal-Directed Video World Model for Procedural Task Execution](https://arxiv.org/abs/2610.12459)（2026-10-08） | 逐步骤视频动作与任务完成监督 |
| [2610.18874 · ChunkAct: Action Chunking for Agentic Robotics](https://arxiv.org/abs/2610.18874)（2026-10-13） | 技能数据应包含原语顺序、子目标、块边界和失败返回条件；评测时同时记录任务成功、决策次数与调用成本，区分动作压缩和规划收益。 |
| [2610.24675 · Action-Aligned Latent Planning for Versatile Humanoid Loco-Manipulation](https://arxiv.org/abs/2610.24675)（2026-10-17） | 技能投影应匹配局部状态下的真实控制响应，再聚合闭环潜在轨迹训练规划器；共享技能表示还需验证低频规划与高频反馈的衔接及技能串联。 |
| [2610.30136 · Agentic World Action Models](https://arxiv.org/abs/2610.30136)（2026-10-21） | 机器人及人体轨迹可标注为时间对齐的程序、视频和动作，再提炼重复过程为技能库；应保留参数化程序到真实双臂执行的对应关系并验证指令遵循。 |

### 合成数据与仿真到真实迁移

**5 篇** · [阅读主题文档](/guides/synthetic-data-sim-to-real/)。

| 论文与发表日期 | 数据切入点 |
| --- | --- |
| [2610.06643 · AffordCraft: Scalable Construction of Task-Ready Simulation Assets from Single Images](https://arxiv.org/abs/2610.06643)（2026-10-05） | 任务可用关节资产的检索与验证 |
| [2610.10479 · Agentic RSR: Real-to-Sim-to-Real through Scene Reconstruction and Execution-Grounded Robot Policies](https://arxiv.org/abs/2610.10479)（2026-10-07） | 场景重建到真实执行的任务对齐 |
| [2610.13945 · Splat2Act: From Captured Scenes to Personalized VLA Manipulation](https://arxiv.org/abs/2610.13945)（2026-10-09） | 真实大场景扫描到个性化示教 |
| [2610.18835 · RoboSimStudio: An Interactive Toolkit for Rapid Real2Sim of Robot Manipulation Tasks](https://arxiv.org/abs/2610.18835)（2026-10-13） | 真实交互证据应关联求解器、接触模型、刚度、摩擦和变形参数的修订版本，使 Real2Sim 校准过程和后续迁移结果可以复现。 |
| [2610.26757 · Simulation Priors for Rapid Adaptation in Model-Based RL for Autonomous Racing](https://arxiv.org/abs/2610.26757)（2026-10-19） | 将低精度和高精度仿真轨迹作为有偏先验分别标记，用有限真实交互校正残差；按赛道、地表变化和失败率评价迁移，而非假定仿真物理完全准确。 |

### 触觉、力觉与接触数据

**12 篇** · [阅读主题文档](/guides/tactile-force-contact-data/)。

| 论文与发表日期 | 数据切入点 |
| --- | --- |
| [2610.03538 · RATE: Risk-Aware Tactile Encoding for Contact-rich Robotic Manipulation](https://arxiv.org/abs/2610.03538)（2026-10-02） | 带任务风险的触觉时序标注 |
| [2610.10370 · PalmSpace: Towards a Versatile On-Palm Interaction Space through Unified Touch Modeling](https://arxiv.org/abs/2610.10370)（2026-10-07） | 手掌触摸事件、模式和位置采集 |
| [2610.10384 · OpenViTac: Learning and Benchmarking Visuo-Tactile Policies in a Unified Sim-and-Real Framework](https://arxiv.org/abs/2610.10384)（2026-10-07） | 成对仿真—真实视触觉基准 |
| [2610.10510 · Factorized Tactile Representation and Control for Sim-to-Real Manipulation](https://arxiv.org/abs/2610.10510)（2026-10-07） | 接触几何、力分布和变化的解耦 |
| [2610.12333 · RiCo: Neural Simulation of Rigid-Body Interactions via Local Contact Reasoning](https://arxiv.org/abs/2610.12333)（2026-10-08） | 局部接触几何与刚体相互作用 |
| [2610.18848 · Contact Trajectory Prompting: In-Context Transfer of Contact-Rich Behaviors from a Single Demonstration](https://arxiv.org/abs/2610.18848)（2026-10-13） | 接触示教应按时间保存运动、力强度和作用方向，并通过在线感知检索相应阶段；相似动作轨迹中的不同接触要求需要独立标注。 |
| [2610.18852 · ForceWAM: Decoupling Future and Response Learning from Demo and Play Data for Contact-Rich Manipulation](https://arxiv.org/abs/2610.18852)（2026-10-13） | 成功示教提供任务兼容未来，无目标 play 扩展动作与接触响应覆盖；视频、六轴力矩、动作和刷新频率应对齐，分别评估两类来源的贡献。 |
| [2610.18855 · Interaction Latents as Actions for Contact-Rich Manipulation](https://arxiv.org/abs/2610.18855)（2026-10-13） | 动作监督可以包含触觉交互演变，而不只把触觉作为输入；应保存潜在动作与原始运动、触觉的对应关系，以及成功段重加权和失败段修正来源。 |
| [2610.22342 · Spark-0: Scaling Spatially Aligned Tactile Pretraining for Robot Dexterous Manipulation](https://arxiv.org/abs/2610.22342)（2026-10-15） | 将触觉手套接触映射到图像及三维触点，保存区域力历史与空间对应；分别评测触觉仅用于预训练监督和部署时仍输入触觉的收益。 |
| [2610.26759 · Tactile In-Hand Object Rotation: A Comparative Study of Hand Morphology in Simulation and Hardware](https://arxiv.org/abs/2610.26759)（2026-10-19） | 跨手型比较需统一训练和测试条件，保存每指接触、参与度、累计负载与旋转进度；触觉信息收益应与形态收益分别分析。 |
| [2610.26846 · GPT-6 Astra Is a Native Visuo-Tactile Policy for Contact-Rich Manipulation](https://arxiv.org/abs/2610.26846)（2026-10-19） | 视觉和触觉图像应按控制回合同步，并与仅视觉输入做匹配比较；保存探测、对齐、恢复轨迹和切向载荷失败，真实触觉控制仍需硬件验证。 |
| [2610.30117 · CW-WAM: A Structured Contact-Wrench World Action Model for Force-Sensitive Manipulation](https://arxiv.org/abs/2610.30117)（2026-10-21） | 运动与六维接触力矩块应严格时间对齐，并记录慢速模型查询与快速导纳控制之间的参考更新；力参考误差、波动和任务成功需同时评估。 |

### 轨迹规划、控制与物理约束数据

**4 篇** · [阅读主题文档](/guides/trajectory-control-constraint-data/)。

| 论文与发表日期 | 数据切入点 |
| --- | --- |
| [2610.12404 · A Physics-Informed Collision Learning Framework for Collaborative Robot Motion Generation](https://arxiv.org/abs/2610.12404)（2026-10-08） | 机器人碰撞边界样本与误安全标签 |
| [2610.12431 · Control-Ready Uncertainty for Trajectory Diffusion](https://arxiv.org/abs/2610.12431)（2026-10-08） | 候选轨迹的不确定性标注与校准 |
| [2610.20409 · Hyperspherical Contrastive Representations Unlock Planning and Exploration](https://arxiv.org/abs/2610.20409)（2026-10-14） | 自监督交互可以形成可复用目标状态表示；应记录起终状态、中间路点数及任务难度，以检验自适应路径分段能否支持长任务执行。 |
| [2610.26810 · Bio-inspired Thrust-Assisted Trotting on a legged-Aerial Robot via Real-Time QP-MPC](https://arxiv.org/abs/2610.26810)（2026-10-19） | 助推步态轨迹应同步保存推力矢量、地面反力、关节跟踪和控制周期，并验证摩擦锥及求解时限；少量硬件速度条件的结果需保留测试范围。 |

### VLA 模型与主流验证方法

**3 篇** · [阅读主题文档](/guides/vla-models-and-evaluation/)。

| 论文与发表日期 | 数据切入点 |
| --- | --- |
| [2610.20442 · Towards Agentic Robots: Model, Data, Environment, and Harness](https://arxiv.org/abs/2610.20442)（2026-10-14） | 数据采集筛选、任务环境构造、执行反馈和模型更新应作为机器人系统的独立模块记录，避免只用低层动作预测能力描述整套代理能力。 |
| [2610.30051 · From Reasoning to Action: Benchmarking Frontier AI Models on LIBERO-10 Robot Manipulation Tasks](https://arxiv.org/abs/2610.30051)（2026-10-21） | 标准化评测需记录末端位姿和夹爪工具调用、推理预算及各任务结果；模型推理能力的比较应同时控制动作接口并报告额外推理成本。 |
| [2610.30108 · Multimodal Embodied Agents: A Unified Capability-centric Perspective from Computer-Use to Robot-Use](https://arxiv.org/abs/2610.30108)（2026-10-21） | 把感知、预测、规划、行动和验证分开建立证据与指标，可发现只报告任务成功率时隐藏的预测和验证缺口；数字界面能力不可直接替代机器人能力。 |

### VLA 实时执行与动作分块数据

**4 篇** · [阅读主题文档](/guides/vla-realtime-execution-data/)。

| 论文与发表日期 | 数据切入点 |
| --- | --- |
| [2610.10453 · RFPO: Rectified Flow Policy Optimization for Embodied Control](https://arxiv.org/abs/2610.10453)（2026-10-07） | 数值积分预算与实机动作延迟 |
| [2610.10528 · Long-WAM: Scaling the Context of World-Action Models](https://arxiv.org/abs/2610.10528)（2026-10-07） | 长历史输入与异步动作时延 |
| [2610.13740 · SmolWAM: A Latent World-Action Model for Robotic Manipulation on Edge Devices](https://arxiv.org/abs/2610.13740)（2026-10-09） | 边缘部署的动作块资源预算 |
| [2610.14997 · Barrier-Constrained Guidance For Real-time Asynchronous VLA Execution](https://arxiv.org/abs/2610.14997)（2026-10-10） | 异步动作块的提交边界一致性 |

### 世界模型规划与决策评估

**6 篇** · [阅读主题文档](/guides/world-model-planning-evaluation/)。

| 论文与发表日期 | 数据切入点 |
| --- | --- |
| [2610.03664 · ProAR: Learning Prospective Reasoning with Autoregressive Video Models](https://arxiv.org/abs/2610.03664)（2026-10-02） | 目标帧与中间状态的前瞻监督 |
| [2610.06805 · H-JEPA: End-to-End Learning of Hierarchical World Models for Visual Planning](https://arxiv.org/abs/2610.06805)（2026-10-05） | 分层时间尺度的潜在规划数据 |
| [2610.12407 · LeWAM: A JEPA World Action Model with Diffusion-Steering-Based MPC](https://arxiv.org/abs/2610.12407)（2026-10-08） | 避免模型误差被利用的潜在规划 |
| [2610.18826 · WorldOracle: Benchmarking Action-Conditioned World Models against Real-World Executions](https://arxiv.org/abs/2610.18826)（2026-10-13） | 评估样本应配对真实 rollout 与预测 rollout，并覆盖成功、失败和多阶段执行；分别检查物理状态、交互位置、关键接触区和多视角动作一致性。 |
| [2610.26844 · AnyGoal: On World Model Generalization Beyond Expert Rollouts](https://arxiv.org/abs/2610.26844)（2026-10-19） | 保持单个状态因素和动作仍在训练支持内，只改变它们的组合与目标，可暴露专家轨迹覆盖盲点；预测误差和下游规划成功需要同时检验。 |
| [2610.26845 · Train An Imaginative Agent](https://arxiv.org/abs/2610.26845)（2026-10-19） | 记录候选动作、想象未来、分支及实际观察频率，可检验有限反馈下的规划收益；游戏任务表现应与 PushT 等物理操作结果分开解释。 |

### 世界模型训练数据与物理表征

**25 篇** · [阅读主题文档](/guides/world-model-training-data/)。

| 论文与发表日期 | 数据切入点 |
| --- | --- |
| [2610.02054 · UniWAM: Unified World-Action Model](https://arxiv.org/abs/2610.02054)（2026-10-01） | 人机混合世界动作监督 |
| [2610.02160 · 4Director: Controlling Video World Models with Rigid 3D Geometry](https://arxiv.org/abs/2610.02160)（2026-10-01） | 刚体场景控制与视频标注 |
| [2610.03516 · XGenAct: Geometry-Enhanced World Action Models through Cross-Task Generation](https://arxiv.org/abs/2610.03516)（2026-10-02） | 深度、法线和功能分割的联合监督 |
| [2610.03587 · AVL-JEPA: Preventing Causal Dynamics Information Collapse In Joint Embedding Predictive Architecture World Models](https://arxiv.org/abs/2610.03587)（2026-10-02） | 动作因果信息与视觉扰动对照 |
| [2610.03632 · World Embedding Benchmark](https://arxiv.org/abs/2610.03632)（2026-10-02） | 物理属性标注与表征可恢复性 |
| [2610.06651 · Considering Context: When World Models Need Context Encoders](https://arxiv.org/abs/2610.06651)（2026-10-05） | 历史与环境上下文的预测充分性 |
| [2610.10400 · Self-correction Optimization for Interleaved Multimodal Generation](https://arxiv.org/abs/2610.10400)（2026-10-07） | 交错生成中的事件与状态一致性 |
| [2610.10515 · RoboJEPA: Scaling Robotic Latent World Models](https://arxiv.org/abs/2610.10515)（2026-10-07） | 多本体规模化预测与规划代理指标 |
| [2610.12349 · SplitJEPA: Learning Invariant and Variant Latent Worlds without Reconstruction](https://arxiv.org/abs/2610.12349)（2026-10-08） | 不变与可变潜在因子的配对监督 |
| [2610.12412 · WorldCast: Distributed Multiplayer World Models](https://arxiv.org/abs/2610.12412)（2026-10-08） | 分布式多视图共享实体状态 |
| [2610.12417 · WOVEN: Weaving Visual World Modeling into Multimodal LLMs](https://arxiv.org/abs/2610.12417)（2026-10-08） | 按推理操作组织视觉转移监督 |
| [2610.12464 · What 30,000 Hours of Ego-centric Video Does Not Teach](https://arxiv.org/abs/2610.12464)（2026-10-08） | 第一视角规模与物体交互保真度 |
| [2610.12468 · DreamTrue: Action-Faithful Robot World Model with Counterfactual Post-Training](https://arxiv.org/abs/2610.12468)（2026-10-08） | 动作几何校准、反事实与缺陷标签 |
| [2610.18697 · UniW(A)M: A Unified Mixture-of-Experts Framework for World and World-Action Models](https://arxiv.org/abs/2610.18697)（2026-10-13） | 同一具身轨迹可供世界预测与动作生成使用，但需保存各条件接口、动作块及接口选择结果，以比较联合监督对预测质量和执行成功率的影响。 |
| [2610.22311 · Velox: Spatial Memory Makes World Models Efficient](https://arxiv.org/abs/2610.22311)（2026-10-15） | 历史视频上下文应记录相机视锥、深度覆盖和上下文选择来源；加速评估需同时检查长 rollout 延迟、未覆盖区域表现及导航视频一致性。 |
| [2610.22340 · Dexterity from Supervised Play](https://arxiv.org/abs/2610.22340)（2026-10-15） | 把人工 play、克隆后的自主探索和模型内自博弈分别保留来源；无特定任务示教的交互数据仍须覆盖接触状态，并以真实手内操作验证规划用途。 |
| [2610.22363 · Perceive, Predict, and Plan: a Unified World Action Model for Egocentric Dexterous Manipulation](https://arxiv.org/abs/2610.22363)（2026-10-15） | 统一视频与三维动作样本可通过可见模态随机化用于感知、预测和规划；三种能力应分开验证，生成操作视频的评价不能自动视为真实机器人执行证明。 |
| [2610.22364 · T2-z: Test-Time Optimization of Environment Latents for Robotic World Models](https://arxiv.org/abs/2610.22364)（2026-10-15） | 训练样本应保留环境身份与交互轨迹，测试时隔离用于适配的少量交互和正式评测；无物理参数标签的环境潜变量仍需预测误差和动作成功率双重验证。 |
| [2610.26811 · State World Models: Execute the Rules, Generate the Pixels](https://arxiv.org/abs/2610.26811)（2026-10-19） | 为相同初始图像和动作构造隐藏状态不同的反事实配对，可检验预测是否依赖持久状态；规则执行、三维引导和视频渲染应分别记录与评估。 |
| [2610.26855 · Ropedia W0: Scaling Loco-Manipulation World Models across Embodiments with Human Experience](https://arxiv.org/abs/2610.26855)（2026-10-19） | 把相机位姿表示的移动与投影骨架表示的操作统一，仍须保留本体正运动学、人工关键点修订及质量记录，并使用高质量遥操作留出集验证跨本体泛化。 |
| [2610.29915 · CausalAlign: Causal Alignment of Video Generation Models for Consistent Ego-Motion](https://arxiv.org/abs/2610.29915)（2026-10-21） | 监督相邻帧变化可针对相机运动而非静态外观；检验几何一致性和时间平滑时，还应保留移动操作成功率作为生成数据的具身用途证据。 |
| [2610.29989 · Looking Ahead: Modeling Future Evolution in Autoregressive Video Generation](https://arxiv.org/abs/2610.29989)（2026-10-21） | 以间隔未来视频块作为辅助监督可削弱局部视觉连续性捷径；归档时应注明其证据为视频物理合理性，尚不能推断动作条件控制收益。 |
| [2610.30120 · ALPS: Visual State Encoders for World Models](https://arxiv.org/abs/2610.30120)（2026-10-21） | 视觉预训练可结合语言、像素重建和空间对应监督；统一数据切分下应分别测量物理状态可读性、语言对齐、未来像素重建和策略成功。 |
| [2610.30125 · PhysiCalWorld: In-Context Physics Calibration for World Models](https://arxiv.org/abs/2610.30125)（2026-10-21） | 将一次探索交互片段与后续预测分开存储，可检验无物理参数标签的描述符是否捕捉实例动力学；需要测试训练物理范围外的预测与规划收益。 |
| [2610.30129 · Rethinking Video Autoencoders for Interactive World Models](https://arxiv.org/abs/2610.30129)（2026-10-21） | 评估视频压缩时应按相机是否移动区分空间和时间压缩，联合报告延迟、动作生效时间与运动误差；图像清晰度不能代替动态一致性质检。 |

## 范围外记录

以下 9 篇关键词命中，但当前摘要不足以支撑本站的具身数据主题。排除仅表示文档范围，不是研究质量判断。

| 论文 | 排除理由 |
| --- | --- |
| [2610.03599 · ManifoldSplat: Language-Guided Semantic Shape Editing of 3D Gaussian Head Avatars](https://arxiv.org/abs/2610.03599)（2026-10-02） | 仅讨论语言驱动头部头像编辑、身份和动画保持，摘要未提供机器人交互、具身状态采集或物理任务评估。 |
| [2610.03662 · Forecasting from Counterfactual Simulator Rollouts: A Sim2Real Evaluation](https://arxiv.org/abs/2610.03662)（2026-10-02） | 实证对象为库存控制部署和需求预测，没有机器人、传感器或实体动作轨迹；sim2real词汇不构成具身数据关联。 |
| [2610.06658 · Talk Like You: Imitating How You Speak in Real-Time Talking Head Generation](https://arxiv.org/abs/2610.06658)（2026-10-05） | 研究唇形和说话习惯模仿，未提供机器人动作、物理交互或具身数据使用证据。 |
| [2610.12361 · Cited but Not Consulted: A Counterfactual Audit of Legal Chain-of-Thought Faithfulness](https://arxiv.org/abs/2610.12361)（2026-10-08） | 测试司法与合同推理，不涉及实体控制、传感器、物理环境或具身任务数据。 |
| [2610.12461 · OuroWorld: Bringing Any 3D World Alive as Diverse, Endlessly Looping 3D Cinemagraphs](https://arxiv.org/abs/2610.12461)（2026-10-08） | 目标是静态场景视觉动画与循环自然度，无动作条件、可执行物理交互、机器人评估或数据质量验证。 |
| [2610.13915 · Where to Look Matters: Rethinking Sub-Volume Sampling in 3D Medical Self-supervised Learning](https://arxiv.org/abs/2610.13915)（2026-10-09） | 研究静态医学图像解剖区域抽样，无机器人、实体感知动作闭环或具身数据来源。 |
| [2610.18730 · Learning When to Transfer: Reinforcement Learning for Carbon-Footprint Modeling in New Manufacturing Domains](https://arxiv.org/abs/2610.18730)（2026-10-13） | 研究制造业产品碳排放的表格预测与选择性迁移；embodied 指隐含温室气体排放，未研究机器人感知、动作或物理交互轨迹。 |
| [2610.24738 · Editing Images into Reusable Layers via Compositional Edit-Prior Distillation](https://arxiv.org/abs/2610.24738)（2026-10-17） | 研究通用指令图像编辑及 RGBA 图层分解，摘要没有机器人、物理状态或具身下游验证。 |
| [2610.26828 · Agent World Model in the Wild: Computer-Use Agent Environment Synthesis](https://arxiv.org/abs/2610.26828)（2026-10-19） | 环境与任务专门服务 GUI、MCP、CLI 等计算机操作代理，未涉及机器人或物理感知行动。 |

## 后续补充口径

追加论文时继续以 `published` 和 arXiv ID 更新覆盖清单；同一知识点补充原页面，新的独立数据问题再建页。每次更新同时复查论文版本、字段建议、术语与图示。后续月份的结论不回写为本快照已经拥有的证据。
