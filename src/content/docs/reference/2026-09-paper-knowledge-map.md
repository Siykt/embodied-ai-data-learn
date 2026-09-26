---
title: 2026 年 9 月具身智能论文知识点索引
description: 汇总 2026 年 8 月 27 日至 9 月 27 日的具身智能论文，按数据主题去重并追溯每篇来源。
---

本索引从同级 `spiders/arxiv/papers/` 的 28 个日期批次读取论文，并按每篇 `published` 字段筛选 **2026-08-27 至 2026-09-27（UTC）**。这段时间有 **314 篇唯一论文**；其中 **278 篇**与本站的数据采集、处理、对齐、标注、质量控制、评估或数据集使用相关，整理为 **26 个独立主题**。另外 **36 篇**保留在末尾的范围外清单，便于复核筛选口径。最近收录的发表时间为 2026-09-24；索引并不声称 9 月 25 日之后没有新论文。

![314 篇论文经发表时间去重和数据相关性判断，归入 26 个知识点主题及范围外清单](/images/docs/paper-knowledge-map-flow.svg)

## 归类与使用方法

每篇论文有一个主主题，避免同一篇文献在目录中重复出现；一篇论文涉及多个问题时，主题文档可交叉引用。主题页重点解释可复用的**数据输入与输出、字段和标签、对齐方式、质量检查、评估边界**，而不按论文篇幅逐篇复述方法。研究结论应回看所链接的论文原文，尤其要核对实验条件与适用场景。

爬虫的中文总结覆盖了部分论文，但不是所有总结都通过事实核验；因此主题文档以原始摘要或论文正文作为事实依据。爬虫抓取的论文配图没有逐张记录再使用许可，本网站使用原创数据流程示意图。

![论文摘要和正文先映射到主题，再提炼可复用的数据契约、质检规则与评估问题](/images/docs/paper-knowledge-map-contract.svg)

## 主题与论文来源

### 远程操作、示教采集与动作重定向

**11 篇。**[阅读主题文档](/guides/demonstration-collection-retargeting/)。

- [2609.30249](https://arxiv.org/abs/2609.30249) · RAPID: Robot Agentic Programming from Demonstrations（2026-09-24）
- [2609.26520](https://arxiv.org/abs/2609.26520) · MATE: Multi-Agent Virtual Teleoperation Platform for Humanoid Collaboration Data Collection（2026-09-22）
- [2609.20659](https://arxiv.org/abs/2609.20659) · HIL-UMI: Bringing Human-in-the-Loop Post-Training of Vision-Language-Action Models to Universal Manipulation Interface（2026-09-17）
- [2609.18763](https://arxiv.org/abs/2609.18763) · Gated Residual Body-Hand Coordination for Whole-Body Humanoid Teleoperation（2026-09-16）
- [2609.16705](https://arxiv.org/abs/2609.16705) · The Robot Data Factory（2026-09-15）
- [2609.16437](https://arxiv.org/abs/2609.16437) · XRoboToolKit-T: Teleoperation with High Stability and Precision with Tactile Sensing for Contact-rich Manipulation（2026-09-14）
- [2609.15716](https://arxiv.org/abs/2609.15716) · Continuous Manifold-Decomposed Impedance Retargeting for Contact-Rich Imitation Learning（2026-09-14）
- [2609.16041](https://arxiv.org/abs/2609.16041) · MR-GLi: Mixed Reality-Based Gripper-Linked Overlays for Underwater Robot Arm Teleoperation via Bilateral Control（2026-09-11）
- [2609.16040](https://arxiv.org/abs/2609.16040) · Bi-MoDe: Bilateral Control-based Imitation Learning via Modifier-Conditioned Decoding for Modulation of Execution Speed and Contact Intensity（2026-09-11）
- [2609.12384](https://arxiv.org/abs/2609.12384) · Understanding Whole-Body Robot Teleoperation Strategies Under Diverse Task Objectives and Constraints（2026-09-11）
- [2609.06434](https://arxiv.org/abs/2609.06434) · Can People Distinguish Human and AI Agency in Humanoid Teleoperation? A Preliminary Study of Agency Perception（2026-09-06）

### 第一视角/多视角人体与人-物交互重建

**6 篇。**[阅读主题文档](/guides/human-object-interaction-reconstruction/)。

- [2609.30187](https://arxiv.org/abs/2609.30187) · Ego-Exo4D Human Meshes Dataset: 4D Human Motion Reconstruction for Ego-Exo Captures（2026-09-24）
- [2609.19119](https://arxiv.org/abs/2609.19119) · Track, Articulate, Act: Generating Articulation from Casual Human Videos（2026-09-16）
- [2609.16684](https://arxiv.org/abs/2609.16684) · MEgoVista: Multi-view Ego-aware Motion Estimation for Metric 4D Hands and Head in the Wild（2026-09-15）
- [2609.16518](https://arxiv.org/abs/2609.16518) · Beyond Gestures: Estimating Full Hand Pose and Contact Forces from Wrist-Worn Pressure Sensor Array（2026-09-15）
- [2609.14615](https://arxiv.org/abs/2609.14615) · Open-UniMo: Towards Unified Motion-Language Understanding and Generation in the Open World（2026-09-13）
- [2608.27407](https://arxiv.org/abs/2608.27407) · Reconstructing Humans and Objects in Interaction using Large Reconstruction Models（2026-08-27）

### 仿真、合成数据与真实迁移

**10 篇。**[阅读主题文档](/guides/synthetic-data-sim-to-real/)。

- [2609.26795](https://arxiv.org/abs/2609.26795) · φ-RIE: From Photorealistic Reconstruction to Interactive Environments（2026-09-22）
- [2609.24815](https://arxiv.org/abs/2609.24815) · Uranus: Building the Next-Generation Simulation Infrastructure for Embodied AI（2026-09-21）
- [2609.21817](https://arxiv.org/abs/2609.21817) · A Sim-to-Real Integration Pipeline for Training and Deployment of Chunk-Based VLA Manipulation Policies（2026-09-18）
- [2609.20582](https://arxiv.org/abs/2609.20582) · V2-STRep: VLM-Grounded Structured Task Representations for Reusable Robot Skills Acquired from Generated Videos（2026-09-17）
- [2609.19137](https://arxiv.org/abs/2609.19137) · Dreaming the Sound of Contact: Leveraging Video and Audio Generation for Zero-Shot Force-Aware Manipulation and Data Generation（2026-09-16）
- [2609.17521](https://arxiv.org/abs/2609.17521) · PhysStream: Streaming Physics-Grounded Video Generation with Structured Scene Memory and Fine-Grained Motion Control（2026-09-15）
- [2609.16919](https://arxiv.org/abs/2609.16919) · NeuroSymbEAD: A Large Scale Neuro-Symbolic Caption Dataset for Omni-Directional Embodied Autonomous Driving（2026-09-15）
- [2609.06279](https://arxiv.org/abs/2609.06279) · IM-ENGINE: Image Editing for Embodied Data Generation（2026-09-05）
- [2609.02886](https://arxiv.org/abs/2609.02886) · SolarWM: Open Data and Scalable Training for Long-Horizon Video World Models（2026-09-02）
- [2608.27073](https://arxiv.org/abs/2608.27073) · SpatialCrafter: Single Image World Modeling with Generative 3D Proxies（2026-08-27）

### 跨模态传感器与时空对齐

**4 篇。**[阅读主题文档](/guides/multimodal-spatiotemporal-alignment/)。

- [2609.15509](https://arxiv.org/abs/2609.15509) · StereoPatch: Patch-Aligned RGB-Depth Fusion for Spatial Perception in Robot Manipulation（2026-09-14）
- [2609.13053](https://arxiv.org/abs/2609.13053) · Dynin-Robotics: Omnimodal Unified Diffusion Vision-Language-Action Model（2026-09-11）
- [2609.05361](https://arxiv.org/abs/2609.05361) · Development of a Humanoid Robot Prototype for Multimodal Human-Robot Interaction（2026-09-04）
- [2608.30643](https://arxiv.org/abs/2608.30643) · Temporal Forcing: 4D Representation Alignment for Vision-Language-Action Models（2026-08-31）

### 三维几何、目标/部件定位与空间表征

**11 篇。**[阅读主题文档](/guides/3d-spatial-representation-data/)。

- [2609.28184](https://arxiv.org/abs/2609.28184) · VLMs Can Describe, But Not Measure: Object-Centric Scene Understanding for Robotic Manipulation（2026-09-23）
- [2609.20586](https://arxiv.org/abs/2609.20586) · CoRef-GS: Cooperative Referring Gaussian Splatting for Multi-Agent Scene Understanding（2026-09-17）
- [2609.19142](https://arxiv.org/abs/2609.19142) · PointZero: 3D Point Track Completion for Learning Transferable 3D Dynamics（2026-09-16）
- [2609.13812](https://arxiv.org/abs/2609.13812) · GeomVLA: Unifying Scene, Motion, and Action in 3D（2026-09-12）
- [2609.12898](https://arxiv.org/abs/2609.12898) · UniPart: Towards Zero-shot Language-Grounded 3D Part Segmentation for Embodied Interaction（2026-09-11）
- [2609.12874](https://arxiv.org/abs/2609.12874) · VideoTok4D: A 4D-Aware Video Tokenizer for Compact World Representation（2026-09-11）
- [2609.12721](https://arxiv.org/abs/2609.12721) · Improving Imitation Learning Efficiency for Manipulation through Geometric Prior Pretraining（2026-09-11）
- [2609.06256](https://arxiv.org/abs/2609.06256) · GloVLA: Let Geometry Move and Local VLA Interact for Robust Object-Centric Manipulation in Unstructured Environments（2026-09-05）
- [2609.04193](https://arxiv.org/abs/2609.04193) · GIFT: Guided Intermediate Feature Training via Action-Oriented Structural Supervision for Robotic Manipulation（2026-09-03）
- [2608.30451](https://arxiv.org/abs/2608.30451) · SeqAlign3DVG: A Sequence-Aligned Benchmark and Voxel Reasoning Framework for 3D Visual Grounding（2026-08-31）
- [2608.27226](https://arxiv.org/abs/2608.27226) · DINOcular: Self-Supervised Visuospatial Representations（2026-08-27）

### 主动感知、测量与采样

**5 篇。**[阅读主题文档](/guides/active-perception-data/)。

- [2609.21929](https://arxiv.org/abs/2609.21929) · MAAP: Multi-Agent Active Perception for Collaborative Manipulation（2026-09-18）
- [2609.16786](https://arxiv.org/abs/2609.16786) · Optimal Excitation Trajectories for System Identification of Underwater Vehicles（2026-09-15）
- [2609.14219](https://arxiv.org/abs/2609.14219) · Task-Specified Active Metrological Inspection with Measurement-Steered VLA Manipulation and Deterministic Evidence Gating（2026-09-13）
- [2609.12894](https://arxiv.org/abs/2609.12894) · Before the Tipping Point: Force-Guided Active Perception for Shape-Agnostic Estimation of 3D Centers of Mass（2026-09-11）
- [2608.27088](https://arxiv.org/abs/2608.27088) · Active sensing to characterize the heterogeneity of plant stress（2026-08-27）

### 潜在动作与跨本体数据对齐

**8 篇。**[阅读主题文档](/guides/latent-action-cross-embodiment/)。

- [2609.21983](https://arxiv.org/abs/2609.21983) · SkelWAM: A Skeleton-Guided World-Action Model for Zero-Shot Cross-Embodiment Manipulation（2026-09-18）
- [2609.21948](https://arxiv.org/abs/2609.21948) · GALA: Geometry-Aware Latent Action Modeling for Vision-Language-Action Model Pretraining across Embodiments（2026-09-18）
- [2609.17099](https://arxiv.org/abs/2609.17099) · GeoLAM: Learning Geometry-Grounded Latent Actions from Unlabeled Human Videos（2026-09-15）
- [2609.16815](https://arxiv.org/abs/2609.16815) · Rethinking Visual Embodiment Dependence in Visuomotor Policies（2026-09-15）
- [2609.16641](https://arxiv.org/abs/2609.16641) · SAVLA: Symmetry-Aware Vision-Language-Action Models for Robotic Manipulation（2026-09-15）
- [2609.16071](https://arxiv.org/abs/2609.16071) · Schema-Adaptive Action-Conditioned JEPA for Cross-Machine CNC Transfer under Partial Sensor Overlap（2026-09-13）
- [2609.12641](https://arxiv.org/abs/2609.12641) · Breaking the Vision-Action Shortcut: Latent Interface Training for Generalizable Robotics Foundation Models（2026-09-11）
- [2609.02634](https://arxiv.org/abs/2609.02634) · Latent Cluster Analysis for Vision-Language-Action Models（2026-09-02）

### 示教数据筛选、再利用与后训练

**6 篇。**[阅读主题文档](/guides/demonstration-data-curation/)。

- [2609.28314](https://arxiv.org/abs/2609.28314) · TANDEM: Task and Motion Planning with As-Needed Demonstrations for Efficient Vision-Language-Action Model Fine-tuning（2026-09-23）
- [2609.26672](https://arxiv.org/abs/2609.26672) · Imperfection for Precision: Upcycling Imperfect Data for High-Precision Robotic Manipulation（2026-09-22）
- [2609.24996](https://arxiv.org/abs/2609.24996) · Learning Beyond What Humans Can Demonstrate（2026-09-21）
- [2609.19138](https://arxiv.org/abs/2609.19138) · In-Context Robot Learning with VLM Agents（2026-09-16）
- [2609.13851](https://arxiv.org/abs/2609.13851) · ReWeight: Leveraging Human Data for VLA Post-Training via Demonstration Retrieval and Sample Weighting（2026-09-12）
- [2609.12316](https://arxiv.org/abs/2609.12316) · DATAFARM: Distribution-Aligned Task and Motion Planning for Fine-Tuning Vision-Language-Action Models（2026-09-11）

### 模仿学习数据与动作生成

**4 篇。**[阅读主题文档](/guides/imitation-learning-action-data/)。

- [2609.30127](https://arxiv.org/abs/2609.30127) · Faster Visuomotor Policy Learning on Action Manifolds via Riemannian MeanFlow（2026-09-24）
- [2609.15631](https://arxiv.org/abs/2609.15631) · Flow-Matched Motion Priors: Online Optimal-Transport Rewards for Imitation Learning（2026-09-14）
- [2609.15162](https://arxiv.org/abs/2609.15162) · LieSpline-DP: Lie-Group B-Spline Diffusion Policy for Smooth Robot Manipulation（2026-09-14）
- [2609.10405](https://arxiv.org/abs/2609.10405) · Frequency-Conditioned Flow Matching for Vision-Language-Action Models（2026-09-09）

### 世界模型训练数据与物理表征

**22 篇。**[阅读主题文档](/guides/world-model-training-data/)。

- [2609.30214](https://arxiv.org/abs/2609.30214) · Underwater C3-JEPA: An Object-Centric Cross-View World Model for ROV Salvage（2026-09-24）
- [2609.28466](https://arxiv.org/abs/2609.28466) · The Past Frames the Future: Memory for Autoregressive Video Generation（2026-09-23）
- [2609.28414](https://arxiv.org/abs/2609.28414) · Frozen Flows Forget: Diagnosing and Restoring Lost Motion in a Latent-flow World Model（2026-09-23）
- [2609.28393](https://arxiv.org/abs/2609.28393) · PointCast: One World Model for Rigid, Articulated, and Deformable Object Manipulation（2026-09-23）
- [2609.24984](https://arxiv.org/abs/2609.24984) · WorldCrafter: Consistent Video World Model with Implicit 3D-aware Memory（2026-09-21）
- [2609.20709](https://arxiv.org/abs/2609.20709) · MoWAM: Explicit Future Motion Prediction for Efficient World Action Models（2026-09-17）
- [2609.20669](https://arxiv.org/abs/2609.20669) · Learning Foresight without Explicit Trajectories for 3D Diffusion Policies（2026-09-17）
- [2609.17372](https://arxiv.org/abs/2609.17372) · XPACE: Joint World and Action Modeling from Heterogeneous Experience（2026-09-15）
- [2609.16697](https://arxiv.org/abs/2609.16697) · World Models for Embodied Intelligence: From Plausible to Controllable to Actionable（2026-09-15）
- [2609.15570](https://arxiv.org/abs/2609.15570) · DIDO: Distilling Interaction-Centric Dynamics into One-Step Denoising for World Action Models（2026-09-14）
- [2609.14973](https://arxiv.org/abs/2609.14973) · PhysBrain 1.5: From Vision-Language Models to Physical Foundation Models（2026-09-14）
- [2609.16074](https://arxiv.org/abs/2609.16074) · World-Action Models for Robot Learning and Control: A Survey（2026-09-13）
- [2609.14462](https://arxiv.org/abs/2609.14462) · AlayaVista: Streaming World Modeling from Panoramic States to Perspective Video（2026-09-13）
- [2609.12441](https://arxiv.org/abs/2609.12441) · IMPLY: Physically Anchored Consistency for World-Model Rollouts（2026-09-11）
- [2609.10540](https://arxiv.org/abs/2609.10540) · Programmable World Model（2026-09-09）
- [2609.10506](https://arxiv.org/abs/2609.10506) · DUET-DINO: Simultaneous Cross-View World Modeling for Latent Planning in Robot Manipulation（2026-09-09）
- [2609.10464](https://arxiv.org/abs/2609.10464) · Semigroup-JEPA: Latent Dynamics Consistency for Zero-Shot Physics Generalization（2026-09-09）
- [2609.06302](https://arxiv.org/abs/2609.06302) · CST-WM: A Causally Structured World Model for Embodied Visual Tracking（2026-09-05）
- [2608.28491](https://arxiv.org/abs/2608.28491) · AcrossVAM1.0: Particle World Modeling for Text-Assisted Robot Video Prediction（2026-08-28）
- [2608.27406](https://arxiv.org/abs/2608.27406) · CLAP: Cross-Embodiment Video World Models are Zero-Shot Physical Simulators（2026-08-27）
- [2608.27367](https://arxiv.org/abs/2608.27367) · Successive Capacity Growth: Task-Complexity-Driven Width and Depth Expansion for Vision Transformer Encoders in JEPA World Models（2026-08-27）
- [2608.27033](https://arxiv.org/abs/2608.27033) · Riemann-1.0: An Embodied World Action Model for Physical AI（2026-08-27）

### 世界模型规划与决策评估

**12 篇。**[阅读主题文档](/guides/world-model-planning-evaluation/)。

- [2609.30264](https://arxiv.org/abs/2609.30264) · AD-WM: Action-Discriminative World Models for Counterfactual Model Predictive Control（2026-09-24）
- [2609.30247](https://arxiv.org/abs/2609.30247) · Rolling-WAM: World Action Models with Rolling Imagination（2026-09-24）
- [2609.30036](https://arxiv.org/abs/2609.30036) · Aim Short to Reach Far: Your Frozen World Model Can Plan Better Than You Think（2026-09-24）
- [2609.28431](https://arxiv.org/abs/2609.28431) · LiMA: Bridging Long-term Imagination to Real-time Dexterous Manipulation via Asynchronous Diffusion（2026-09-23）
- [2609.28258](https://arxiv.org/abs/2609.28258) · Generalizable Robotic Insertion with World Models（2026-09-23）
- [2609.24868](https://arxiv.org/abs/2609.24868) · DualWAM: Dual-System World Action Models for Asynchronous Global Planning and Local Refinement（2026-09-21）
- [2609.24749](https://arxiv.org/abs/2609.24749) · D-JEPA: A Decision-Aligned Latent World Model（2026-09-21）
- [2609.20575](https://arxiv.org/abs/2609.20575) · Accelerating Visual Policy Learning with Sampling-Based Model Predictive Control（2026-09-17）
- [2609.15801](https://arxiv.org/abs/2609.15801) · When Should a World Model Move? Loss-Conditioned State Execution（2026-09-14）
- [2609.15382](https://arxiv.org/abs/2609.15382) · From Prediction to Decision: World-Model-Guided Action Selection for Continuous Pile Excavation（2026-09-14）
- [2609.14073](https://arxiv.org/abs/2609.14073) · LPA-CWM: A Learned Physical Adjudicator for Motion Reasoning with Counterfactual World Models（2026-09-12）
- [2609.13845](https://arxiv.org/abs/2609.13845) · LePlanner: An Iterative Amortized Controller For World Models（2026-09-12）

### 长时记忆、经验检索与连续视频

**9 篇。**[阅读主题文档](/guides/embodied-memory-experience-data/)。

- [2609.28429](https://arxiv.org/abs/2609.28429) · Watch, Recall, Act: Always-On Robots in Concurrent Embodied Streams（2026-09-23）
- [2609.28256](https://arxiv.org/abs/2609.28256) · MemBodied: Recurrent Associative Memory for Vision-Language-Action Models（2026-09-23）
- [2609.22040](https://arxiv.org/abs/2609.22040) · PRIME: Perception Feedback with Situational Memory Embeddings in VLA Models（2026-09-18）
- [2609.20820](https://arxiv.org/abs/2609.20820) · Workspace Models: Lightweight Robotic Memory via Saliency-Driven Supervision（2026-09-17）
- [2609.16864](https://arxiv.org/abs/2609.16864) · TEMPO: Learning Temporal Context for Dynamic Robot Manipulation（2026-09-15）
- [2609.15976](https://arxiv.org/abs/2609.15976) · MessyMem: Learning-from-Doing Memory for Mobile Manipulation（2026-09-14）
- [2609.14561](https://arxiv.org/abs/2609.14561) · GLAM: Training a latent world model over global spatiotemporal memory for active exploration and navigation（2026-09-13）
- [2609.02780](https://arxiv.org/abs/2609.02780) · ShallowStream: Index Shallow then Answer Deep for Streaming Video Understanding（2026-09-02）
- [2608.27328](https://arxiv.org/abs/2608.27328) · R2M-Bench: Evaluating Revisit Memory via Relative Consistency in Interactive Video World Models（2026-08-27）

### 语言指令、视觉条件与动作对齐

**5 篇。**[阅读主题文档](/guides/language-action-grounding-data/)。

- [2609.24995](https://arxiv.org/abs/2609.24995) · MIGU: Multimodal Instruction Grounding under Uncertainty for Manipulation Planning（2026-09-21）
- [2609.15169](https://arxiv.org/abs/2609.15169) · GRAVA: Grounded Reasoning-to-Action Representation and Learning for Autonomous Driving（2026-09-14）
- [2609.05376](https://arxiv.org/abs/2609.05376) · What Matters, When? Diagnosing and Improving Conditional Visual Grounding in Visuomotor Imitation Policies（2026-09-04）
- [2609.05260](https://arxiv.org/abs/2609.05260) · One Word, Different Action: A Real-Robot Benchmark for Language-Conditioned Embodied Reasoning（2026-09-04）
- [2609.02653](https://arxiv.org/abs/2609.02653) · HINT: Human-Intent Inception for Long-Horizon Robot Manipulation（2026-09-02）

### 任务分解、技能表征与组合

**11 篇。**[阅读主题文档](/guides/robot-skill-composition-data/)。

- [2609.26499](https://arxiv.org/abs/2609.26499) · Generalizing Manipulation Skills with a Local Coding Agent（2026-09-22）
- [2609.18869](https://arxiv.org/abs/2609.18869) · KINO: A Keyframe Interface for VLM Planning and Whole-Body Control in Humanoid Loco-Manipulation（2026-09-16）
- [2609.18813](https://arxiv.org/abs/2609.18813) · Asymptotically Optimal Multi-Robot Task and Motion Planning（2026-09-16）
- [2609.17263](https://arxiv.org/abs/2609.17263) · CAD-Based Relation Learning and Geometric-Symbolic Planning for Robotic Assembly（2026-09-15）
- [2609.16331](https://arxiv.org/abs/2609.16331) · ManiSkillFormer: Demonstration-Free Compositional Manipulation via Task-Conditioned Geometric Contracts（2026-09-14）
- [2609.15587](https://arxiv.org/abs/2609.15587) · An Information-Space Perspective to Scene Graph Sufficiency for Robotic Task Planning（2026-09-14）
- [2609.16056](https://arxiv.org/abs/2609.16056) · Managing Action Preconditions in Neuro-Symbolic RL: Three Placement Strategies for Embodied Agents（2026-09-13）
- [2609.10522](https://arxiv.org/abs/2609.10522) · Show-Harness: Just a VLM Agent Can Play Robots（2026-09-09）
- [2609.05369](https://arxiv.org/abs/2609.05369) · Towards Neuro-Symbolic Procedural Reasoning for Long-Horizon Vision-Language-Action Manipulation（2026-09-04）
- [2608.31167](https://arxiv.org/abs/2608.31167) · SUN: Persistent Programs For Language-Grounded Control-to-Learning-to-Real Policies（2026-08-31）
- [2608.27371](https://arxiv.org/abs/2608.27371) · Embodied Scene Rearrangement Planning（2026-08-27）

### VLA 动作分块、推理延迟与实时执行

**11 篇。**[阅读主题文档](/guides/vla-realtime-execution-data/)。

- [2609.20776](https://arxiv.org/abs/2609.20776) · GeoAAC: Geometry-Based Adaptive Action Chunking from Denoising Trajectories in VLA Policies（2026-09-17）
- [2609.20648](https://arxiv.org/abs/2609.20648) · SkipVLA: Skipping VLA Steps with Classical Planning for Fast Robot Manipulation（2026-09-17）
- [2609.19104](https://arxiv.org/abs/2609.19104) · rMuscle: Robotic Muscle Memory for Efficient Vision-Language-Action Model Inference（2026-09-16）
- [2609.17210](https://arxiv.org/abs/2609.17210) · FluxVLA Engine: A One-Stop VLA Engineering Platform for Embodied Intelligence（2026-09-15）
- [2609.16503](https://arxiv.org/abs/2609.16503) · Dense to MoE Adaptation for Compact Vision Language Action Policies（2026-09-15）
- [2609.15840](https://arxiv.org/abs/2609.15840) · Uncertainty-Guided Sparse Refinement for Action Chunking Transformer Policies（2026-09-14）
- [2609.15322](https://arxiv.org/abs/2609.15322) · Planning in the Backbone: DiffAdapterVLA for Native Continuous Trajectory Generation with Driving VLMs（2026-09-14）
- [2609.14146](https://arxiv.org/abs/2609.14146) · When Faster VLA Deployment Changes Closed-Loop Behavior: Task Success-Latency Analysis of SmolVLA Across PyTorch and ONNX Variants（2026-09-12）
- [2609.13984](https://arxiv.org/abs/2609.13984) · What Makes an Efficient VLA? Navigating Action-Head Design, Scaling, and Latency（2026-09-12）
- [2609.13695](https://arxiv.org/abs/2609.13695) · GROOVE: Geometry-Guided Reduction of Operational-Space Jerk in VLA Execution（2026-09-12）
- [2608.27384](https://arxiv.org/abs/2608.27384) · FlashVLA: Streaming Action Decoding for Fast and Asynchronous VLA Inference（2026-08-27）

### 闭环反馈、失败检测与纠错

**8 篇。**[阅读主题文档](/guides/closed-loop-correction-data/)。

- [2609.30092](https://arxiv.org/abs/2609.30092) · Self-Adaptive VLA for Robust Robot Deployment（2026-09-24）
- [2609.30024](https://arxiv.org/abs/2609.30024) · Body-Grounded Replanning for Physically Adaptive Manipulation（2026-09-24）
- [2609.21908](https://arxiv.org/abs/2609.21908) · CommitFlow: Semantic Commitment Verification and Local Correction for Long-Horizon Robot Manipulation VLA Execution（2026-09-18）
- [2609.20646](https://arxiv.org/abs/2609.20646) · TraceFlow: Guiding Frozen Flow-Matching Robot Policies with Success and Failure Traces（2026-09-17）
- [2609.17404](https://arxiv.org/abs/2609.17404) · Residual Fault Adaptation for Dexterous In-Hand Manipulation Under Runtime Joint Faults（2026-09-15）
- [2609.14633](https://arxiv.org/abs/2609.14633) · REVOLVE: An Automated Closed-Loop Framework for Evolving Robot Manipulation with Minimal Human Intervention（2026-09-13）
- [2609.06508](https://arxiv.org/abs/2609.06508) · VLA-Corrector: Stage-Aware Observable State Understanding for Prompt-Based Closed-Loop Recovery of Vision-Language-Action Policies（2026-09-06）
- [2608.27079](https://arxiv.org/abs/2608.27079) · GRAFT: Grounded and Efficient Online Reinforcement Adaptation for Fine-Grained Robot Manipulation（2026-08-27）

### 触觉、力觉与接触数据

**16 篇。**[阅读主题文档](/guides/tactile-force-contact-data/)。

- [2609.30082](https://arxiv.org/abs/2609.30082) · Real-Time Force Regulation for Whole-Hand Dexterous Grasping（2026-09-24）
- [2609.24976](https://arxiv.org/abs/2609.24976) · DexTacWAM: A Visuo-Tactile World-Action Model for Dexterous Manipulation（2026-09-21）
- [2609.20761](https://arxiv.org/abs/2609.20761) · Agile-WAM: An Agile Tactile World Action Model for Contact-Rich Robot Control（2026-09-17）
- [2609.20649](https://arxiv.org/abs/2609.20649) · DexTouch-WM: Learning Action-Conditioned Tactile World Models from Human Touch for Dexterous Robot Manipulation（2026-09-17）
- [2609.16504](https://arxiv.org/abs/2609.16504) · UniDex-ViTac: Learning Unified Visuo-Tactile Dexterous Manipulation Policy from Human Video Data（2026-09-15）
- [2609.15921](https://arxiv.org/abs/2609.15921) · Touch2Trace: Tactile-Driven Imitation Learning for Dexterous Cable Tracing（2026-09-14）
- [2609.15910](https://arxiv.org/abs/2609.15910) · SlipSense: Multimodal Tactile Learning for Low-Latency and Generalized Slip Detection（2026-09-14）
- [2609.15198](https://arxiv.org/abs/2609.15198) · PredTac: Learning Contact-Rich Manipulation with Predicted Touch（2026-09-14）
- [2609.15012](https://arxiv.org/abs/2609.15012) · Atomic Motion Coordinate for Language-Steerable and Force-Responsive Manipulation（2026-09-14）
- [2609.14156](https://arxiv.org/abs/2609.14156) · Visible Touch: Rendering Contact for Visuomotor Policies（2026-09-12）
- [2609.14133](https://arxiv.org/abs/2609.14133) · Vision-Force Admittance Learning for Peg Insertion into a Movable Hole（2026-09-12）
- [2609.13779](https://arxiv.org/abs/2609.13779) · Force-Aware Reinforcement Learning with Hybrid Sensorless Force Estimation for Wheeled-Legged Loco-Manipulation（2026-09-12）
- [2609.12737](https://arxiv.org/abs/2609.12737) · Control Architecture for Safe Grasping of Fragile Objects Using a Coarse Position-Controlled Gripper（2026-09-11）
- [2609.12549](https://arxiv.org/abs/2609.12549) · STAR: Sparse Tactile Representation Learning in Vision-Tactile-Language-Action Models for Dexterous Manipulation（2026-09-11）
- [2609.05282](https://arxiv.org/abs/2609.05282) · Temporal Tactile Encoding and Compliance for Intent-Aware Robot-to-Human Bimanual Handover（2026-09-04）
- [2609.05266](https://arxiv.org/abs/2609.05266) · TacPAC: Tactile Prediction and Real-Time Action Correction in World-Action Models for Contact-Rich Manipulation（2026-09-04）

### 可变形物体与材质状态数据

**7 篇。**[阅读主题文档](/guides/deformable-material-state-data/)。

- [2609.17035](https://arxiv.org/abs/2609.17035) · SWIM: Vision-Language-Grounded Soft Whole-Body Interactive Manipulation（2026-09-15）
- [2609.12677](https://arxiv.org/abs/2609.12677) · Size Doesn't Matter: Material-State Reinforcement Learning for Excavator Transferable Soil Manipulation（2026-09-11）
- [2609.12634](https://arxiv.org/abs/2609.12634) · Online Material Estimation for Conditioned Diffusion Policy in Shaping Deformable Linear Objects（2026-09-11）
- [2609.12433](https://arxiv.org/abs/2609.12433) · FoldNet++: a Large-Scale Synthetic Dataset for Robotic T-Shirt Folding and Unfolding（2026-09-11）
- [2609.10308](https://arxiv.org/abs/2609.10308) · Deformable Object Manipulation under Partial Observability via Real-Time Full-Shape Estimation（2026-09-09）
- [2609.10243](https://arxiv.org/abs/2609.10243) · FolDeX: A Physical-World Benchmark for Long-Horizon Robotic Manipulation of Deformable Objects（2026-09-09）
- [2608.28570](https://arxiv.org/abs/2608.28570) · ChainSplat: A Physics-Inspired Screw-Theoretic Model for Learning Deformable Linear Object Dynamics from Multi-View RGB Videos（2026-08-28）

### 灵巧手、抓取与双臂操作

**12 篇。**[阅读主题文档](/guides/dexterous-manipulation-data/)。

- [2609.28281](https://arxiv.org/abs/2609.28281) · BrickCraft-Duo: Efficient Dual-Arm Skill Learning and Refinement for Compositional Long-Horizon Assembly（2026-09-23）
- [2609.24896](https://arxiv.org/abs/2609.24896) · Steerable and Reactive Grasping Through Modular Design with a Three-Point Interface（2026-09-21）
- [2609.17172](https://arxiv.org/abs/2609.17172) · Fingers as Legs: Learning Self-Supported Locomotion and Manipulation with an Anthropomorphic Hand（2026-09-15）
- [2609.16586](https://arxiv.org/abs/2609.16586) · ProxiDex: Learning Dynamics-Guided Proximity Policy for Dexterous Manipulation（2026-09-15）
- [2609.16319](https://arxiv.org/abs/2609.16319) · ConGraspXL: Controllable Constraint-Conditioned Dexterous Grasping Motion Synthesis（2026-09-14）
- [2609.14310](https://arxiv.org/abs/2609.14310) · VLBiMan++: Expanding the Generalization Boundary of Vision-Language Anchored One-Shot Bimanual Manipulation（2026-09-13）
- [2609.13761](https://arxiv.org/abs/2609.13761) · Learning In-Hand Object Reaching to General 6D Poses（2026-09-12）
- [2609.12498](https://arxiv.org/abs/2609.12498) · ArtManip: Category-Level Articulated In-Hand Manipulation（2026-09-11）
- [2609.10137](https://arxiv.org/abs/2609.10137) · Assembling Two Parts in One Hand（2026-09-09）
- [2609.05206](https://arxiv.org/abs/2609.05206) · Morphology and actuation as inductive biases in robotic hand manipulation（2026-09-04）
- [2608.28578](https://arxiv.org/abs/2608.28578) · Aero Hand Open: A Simulation-Ready Tendon-Driven Hand for Dexterous Manipulation Learning（2026-08-28）
- [2608.27221](https://arxiv.org/abs/2608.27221) · Tensegrity Continuum Robots Enable Task-Adaptive Morphologies for Cooperative Behaviors（2026-08-27）

### 人形/足式全身运动数据

**21 篇。**[阅读主题文档](/guides/humanoid-locomotion-data/)。

- [2609.28378](https://arxiv.org/abs/2609.28378) · ForgetMimic: Motion Unlearning for Reinforcement Learning Humanoid Control（2026-09-23）
- [2609.26564](https://arxiv.org/abs/2609.26564) · Learning Air-Ground Motion Control with Temporal Mode Switching and Cross-Terrain Tracking（2026-09-22）
- [2609.24840](https://arxiv.org/abs/2609.24840) · PredActor: Predictive Action Diffusion for Steerable Onboard Humanoid Control（2026-09-21）
- [2609.22073](https://arxiv.org/abs/2609.22073) · Duty Factor Predicts Robust Constrained Quadrupedal Locomotion Across Gait Types（2026-09-18）
- [2609.20566](https://arxiv.org/abs/2609.20566) · OmniMimic: Dynamics-completed Motion Augmentation for Multi-style Omnidirectional Quadruped Locomotion（2026-09-17）
- [2609.20558](https://arxiv.org/abs/2609.20558) · Learning Slope-Adaptive Whole-Body Locomotion for Humanoid Robots in Roofing Construction（2026-09-17）
- [2609.18930](https://arxiv.org/abs/2609.18930) · Learning Holistic Whole-Body Loco-Manipulation with a Bipedal Mobile Manipulator（2026-09-16）
- [2609.18732](https://arxiv.org/abs/2609.18732) · PASSAGE: Scaling Scene-Aligned Motion Learning for Perceptive Humanoid Traversal in Cluttered Environments（2026-09-16）
- [2609.16683](https://arxiv.org/abs/2609.16683) · Weave: Learning Whole-Body Dexterous Loco-Manipulation from Human-Object Interactions（2026-09-15）
- [2609.16644](https://arxiv.org/abs/2609.16644) · WholeBodyWAM: Generalizing Pre-trained World-Action Priors to Humanoid Loco-Manipulation via WBC-Grounded Coordination（2026-09-15）
- [2609.16405](https://arxiv.org/abs/2609.16405) · Collision-Aware Humanoid Whole-Body Control under Imperfect Tracking Targets（2026-09-14）
- [2609.15770](https://arxiv.org/abs/2609.15770) · JEPLO: Joint-Embedding Predictive Learning for LiDAR-Based Legged Locomotion（2026-09-14）
- [2609.15213](https://arxiv.org/abs/2609.15213) · X-WBC: A Cross-Embodiment Foundation Model for Humanoid Whole-Body Control（2026-09-14）
- [2609.14647](https://arxiv.org/abs/2609.14647) · Skill Composition for Legged Robot Reinforcement Learning（2026-09-13）
- [2609.14432](https://arxiv.org/abs/2609.14432) · EMoG: Emotion-Modulated Gait Generation for Expressive Humanoid Locomotion（2026-09-13）
- [2609.12400](https://arxiv.org/abs/2609.12400) · Decentralized Evolution of Hexapod Gaits with Independent Leg Controllers（2026-09-11）
- [2609.12347](https://arxiv.org/abs/2609.12347) · DWMP: Leveraging Dual World Models for Humanoid Obstacle Traversal（2026-09-11）
- [2609.10286](https://arxiv.org/abs/2609.10286) · Learning Terrain-Adaptive Humanoid Locomotion on Granular Terrain（2026-09-09）
- [2609.10283](https://arxiv.org/abs/2609.10283) · SwingBot: Learning Whole-Body Brachiation for Humanoid Robots（2026-09-09）
- [2609.10273](https://arxiv.org/abs/2609.10273) · Frame-Coded Legged Locomotion over Noisy Terrain（2026-09-09）
- [2609.03984](https://arxiv.org/abs/2609.03984) · MulDP: Multimodal Diffusion Policy for Autonomous Quadruped Parkour Navigation across Complex Terrains（2026-09-03）

### 导航、地图与可通行性数据

**10 篇。**[阅读主题文档](/guides/navigation-traversability-data/)。

- [2609.21828](https://arxiv.org/abs/2609.21828) · Touvigation: Embodied Adaptive Object Acquisition for Blind and Low-Vision Users in Unfamiliar Indoor Environments（2026-09-18）
- [2609.20604](https://arxiv.org/abs/2609.20604) · Semantic SLAM in Precision Agriculture using Bayesian Inference（2026-09-17）
- [2609.18789](https://arxiv.org/abs/2609.18789) · AdaGeoVLN: Selective Geometry Across Representation Depth and Navigation Time for Vision-Language Navigation（2026-09-16）
- [2609.17257](https://arxiv.org/abs/2609.17257) · Exploring 2D backbone effects for indoor semantic occupancy prediction（2026-09-15）
- [2609.15195](https://arxiv.org/abs/2609.15195) · HarnessVLN: Unifying Training-Free Embodied Navigation through an Agent Harness（2026-09-14）
- [2609.12422](https://arxiv.org/abs/2609.12422) · Hierarchical Belief Modeling for Zero-Shot Opponent Adaptation in Partially Observable Multi-Agent Navigation（2026-09-11）
- [2609.06476](https://arxiv.org/abs/2609.06476) · One MLLM, One Call: Efficient Zero-Shot Vision-and-Language Navigation via Spatial-Aware Waypoints（2026-09-06）
- [2609.06424](https://arxiv.org/abs/2609.06424) · OVMAN: A Task and Benchmark for Open-Vocabulary Motion-Aware Navigation（2026-09-06）
- [2609.06251](https://arxiv.org/abs/2609.06251) · MobileVLA-R1 2.0: RL-Enhanced Reasoning for Mobile Robot Control（2026-09-05）
- [2608.30935](https://arxiv.org/abs/2608.30935) · LightNav-0: Eliciting VLM Spatial Intelligence for Generalist Embodied Navigation（2026-08-31）

### 安全、鲁棒性、隐私与对抗评估

**13 篇。**[阅读主题文档](/guides/robot-safety-robustness-data/)。

- [2609.30258](https://arxiv.org/abs/2609.30258) · Temporal Gradient Inversion for Private Trajectory Reconstruction in Embodied Reinforcement Learning（2026-09-24）
- [2609.22075](https://arxiv.org/abs/2609.22075) · LIMBO: Learning and Internalizing Model-Free Barrier Objectives for Agile and Safe Whole-Body Control（2026-09-18）
- [2609.20822](https://arxiv.org/abs/2609.20822) · Coding Agents with an Obstacle-Aware Harness for Safe Robot Manipulation（2026-09-17）
- [2609.17349](https://arxiv.org/abs/2609.17349) · RobResilience: Implementing and Evaluating a Resilience Framework for Cyber-Physical Embodied Systems（2026-09-15）
- [2609.16724](https://arxiv.org/abs/2609.16724) · CorrRisk-WM: Corridor-Conditioned Risk World Modeling for Safety-Critical Trajectory Planning（2026-09-15）
- [2609.15988](https://arxiv.org/abs/2609.15988) · ResSafe: Learning Safety Filtering with Residual Reinforcement Learning for Humanoids（2026-09-14）
- [2609.15781](https://arxiv.org/abs/2609.15781) · When the World Lies: Backdoor Attacks on Latent World Models for Downstream Control（2026-09-14）
- [2609.15113](https://arxiv.org/abs/2609.15113) · Legislating World-Model-Based Planning with Legal Reasoning（2026-09-14）
- [2609.12371](https://arxiv.org/abs/2609.12371) · READ: Learning Risk-Informed Fields for End-to-End Autonomous Driving（2026-09-11）
- [2609.10292](https://arxiv.org/abs/2609.10292) · Isotropic Embedding Perturbations for Robust Vision Language Encoders（2026-09-09）
- [2609.06326](https://arxiv.org/abs/2609.06326) · Rethinking Safety for Generalist Robots（2026-09-06）
- [2608.30428](https://arxiv.org/abs/2608.30428) · Lies We Can See: Joint Verbal and Non-Verbal Deception by VLM Agents in Embodied Social Interactions（2026-08-31）
- [2608.28518](https://arxiv.org/abs/2608.28518) · When Robots Mishear Us: Mapping the Safety Risks of Voice-Controlled Embodied AI（2026-08-28）

### 基准、质检、成功判定与误差归因

**23 篇。**[阅读主题文档](/guides/embodied-evaluation-data-quality/)。

- [2609.28366](https://arxiv.org/abs/2609.28366) · AnchorReasoning: A Visual Grounding and Causal Reasoning Dataset in Long-Tail Autonomous Driving Scenarios（2026-09-23）
- [2609.28236](https://arxiv.org/abs/2609.28236) · EmbodiedMemory-Bench: Benchmarking Embodied Memory for Long-Horizon Embodied Tasks（2026-09-23）
- [2609.26567](https://arxiv.org/abs/2609.26567) · Beyond End-Task Success: How to Audit Visual Experience Retrieval in Robotics（2026-09-22）
- [2609.24778](https://arxiv.org/abs/2609.24778) · H2RBench: A Real-to-Sim Benchmark for Evaluating Human-to-Robot Transfer（2026-09-21）
- [2609.22055](https://arxiv.org/abs/2609.22055) · Benchmarking World Models for Continual Learning on Compositional Tasks（2026-09-18）
- [2609.21909](https://arxiv.org/abs/2609.21909) · Beyond Kinematics: Benchmarking Simulation Fidelity for Muscle-Driven Imitation Learning（2026-09-18）
- [2609.16745](https://arxiv.org/abs/2609.16745) · The Latent That Never Was: A Forensic Re-run of the CVAE Ablation in Action Chunking Transformer（2026-09-15）
- [2609.16610](https://arxiv.org/abs/2609.16610) · EgoPathBench: Evaluating Zero-Shot Egocentric Waypoint Decision-Making in Vision-Language Models（2026-09-15）
- [2609.16443](https://arxiv.org/abs/2609.16443) · The Neverwhere Visual Parkour Benchmark Suite（2026-09-14）
- [2609.15940](https://arxiv.org/abs/2609.15940) · Beyond Single-Axis Testing: Paired Evaluation of Compound Robustness in Vision-Language-Action Policies（2026-09-14）
- [2609.15726](https://arxiv.org/abs/2609.15726) · Bench2Dex: Benchmarking Visuo-Tactile Bimanual Dexterous Manipulation Across Dexterous Hands（2026-09-14）
- [2609.15005](https://arxiv.org/abs/2609.15005) · IMPACT-VLA: Interaction-aware Multimodal Propagation Attribution via Counterfactual Trajectories for Vision-Language-Action Policies（2026-09-14）
- [2609.14899](https://arxiv.org/abs/2609.14899) · What Makes a 3D Scene Editable? A Factorized Benchmark of Fidelity, Locality, Consistency, and Preservation（2026-09-14）
- [2609.14833](https://arxiv.org/abs/2609.14833) · One Model, Two Physical Stories: Auditing Misalignment in Multi-Modal World Modeling（2026-09-13）
- [2609.14473](https://arxiv.org/abs/2609.14473) · PuzzleMate: Benchmarking MLLMs for Egocentric Puzzle Assistance（2026-09-13）
- [2609.13730](https://arxiv.org/abs/2609.13730) · JumpStart Your Policy Learning with Lessons from 160,000 Training Runs（2026-09-12）
- [2609.13679](https://arxiv.org/abs/2609.13679) · How to Better Train VLAs: Lessons Learned From the REAL-I Challenge at ICRA 2026（2026-09-12）
- [2609.13458](https://arxiv.org/abs/2609.13458) · STAGE: Diagnosing Semantic Transfer at Grounded Execution in Embodied Agents（2026-09-11）
- [2609.13082](https://arxiv.org/abs/2609.13082) · Embodied-BenchForge: A Closed-Loop Agentic Workflow for Embodied Benchmark Construction（2026-09-11）
- [2609.05324](https://arxiv.org/abs/2609.05324) · RoboSPA: Can VLA Models Go Beyond Simple Scenes and Short-Horizon Tasks?（2026-09-04）
- [2609.02688](https://arxiv.org/abs/2609.02688) · From Proxy Learning to Driving Decisions: A Transfer-Based Framework for Evaluating Future-Aware Autonomous Driving Planners（2026-09-02）
- [2608.30536](https://arxiv.org/abs/2608.30536) · Behavior-Skill: A Fine-Grained Benchmark for Evaluating Vision-Language-Action Policies in Long-Horizon Tasks（2026-08-31）
- [2608.27345](https://arxiv.org/abs/2608.27345) · PAWBench: How Far Are We from Probabilistically Aligned World Modeling?（2026-08-27）

### 奖励、价值函数与强化学习反馈

**8 篇。**[阅读主题文档](/guides/reward-value-feedback-data/)。

- [2609.30023](https://arxiv.org/abs/2609.30023) · Res-HIL: Human-Guided Residual Reinforcement Learning for Sample-Efficient Dexterous Manipulation（2026-09-24）
- [2609.22085](https://arxiv.org/abs/2609.22085) · SeeQ: Training Generalist Value Functions for Long-Horizon Robotic Manipulation（2026-09-18）
- [2609.17115](https://arxiv.org/abs/2609.17115) · Intrinsic Robot Rewarding: Reusing VLA Representations for Autonomous Evaluation and Policy Improvement（2026-09-15）
- [2609.15014](https://arxiv.org/abs/2609.15014) · Steering Generative Robot Policies with Lexicographic Preferences（2026-09-14）
- [2609.14878](https://arxiv.org/abs/2609.14878) · Real-World Reinforcement Learning with MPC Scaffolding for Dexterous Manipulation（2026-09-14）
- [2609.14261](https://arxiv.org/abs/2609.14261) · VGFM: Expressive Robot Policies via Dense Value Guidance in Flow Matching（2026-09-13）
- [2609.12749](https://arxiv.org/abs/2609.12749) · SCQ: Stabilizing Conservative Q-Learning with Sigmoid-Bounded Entropy（2026-09-11）
- [2608.30983](https://arxiv.org/abs/2608.30983) · Autonomously Acquiring Robot Manipulation Skills with Language-Driven Quality-Diversity（2026-08-31）

### 轨迹规划、控制与物理约束

**13 篇。**[阅读主题文档](/guides/trajectory-control-constraint-data/)。

- [2609.30213](https://arxiv.org/abs/2609.30213) · ReVAMP: Vector-Accelerated Motion Planning for Kinematically-Constrained Systems via Reparameterization（2026-09-24）
- [2609.30140](https://arxiv.org/abs/2609.30140) · Contact as a Decision Variable: Capability-Tradeoff Contact Selection for Legged Loco-Manipulation（2026-09-24）
- [2609.28377](https://arxiv.org/abs/2609.28377) · Amplify: A Lightweight Library for Reproducible Nonlinear Programming Problems in Robotics（2026-09-23）
- [2609.28299](https://arxiv.org/abs/2609.28299) · Contact-Implicit Stein Projected ADMM for Discovery of Diverse Contact-Rich Manipulation Strategies（2026-09-23）
- [2609.24841](https://arxiv.org/abs/2609.24841) · CAST: Collision-Aware Assembly with Construction Robots using Simultaneous Trajectory Estimation and Planning（2026-09-21）
- [2609.22062](https://arxiv.org/abs/2609.22062) · Gripper-Aware Automatic Dense Packing of Irregular Objects（2026-09-18）
- [2609.21803](https://arxiv.org/abs/2609.21803) · Contact-Rich Motion Planning via GPU-Parallel Mode Evaluation（2026-09-18）
- [2609.18910](https://arxiv.org/abs/2609.18910) · CaSCo: Cascade-Aware Soft-Collision Motion Planning（2026-09-16）
- [2609.15447](https://arxiv.org/abs/2609.15447) · Learning to Exploit Passive Dynamics for Energy-Efficient Target Hopping of a Spring-Legged Quadcopter（2026-09-14）
- [2609.15399](https://arxiv.org/abs/2609.15399) · Dynamics-Informed Reinforcement Learning for Agile and Energy-Efficient Locomotion of a Monopedal Hopping Quadcopter（2026-09-14）
- [2609.14868](https://arxiv.org/abs/2609.14868) · Primitive-Informed Sampling-Based MPC for Multi-Fingered Dexterous Manipulation（2026-09-14）
- [2609.04070](https://arxiv.org/abs/2609.04070) · Continuous Actions from Discrete Minds: Latent-Aligned Planning for End-to-End Autonomous Driving（2026-09-03）
- [2608.27186](https://arxiv.org/abs/2608.27186) · Task-space model-based control of pneumatic soft actuators（2026-08-27）

### 工业、农业、水下、医疗等特定域数据

**12 篇。**[阅读主题文档](/guides/domain-specific-embodied-data/)。

- [2609.24761](https://arxiv.org/abs/2609.24761) · A Switched Adaptive Control Framework for Aerial Manipulators Under Dynamic Transitions（2026-09-21）
- [2609.18881](https://arxiv.org/abs/2609.18881) · Body-Motion Control of a Simulated Aerial Swarm from a First-Person View（2026-09-16）
- [2609.17021](https://arxiv.org/abs/2609.17021) · sensVLA: Spatially-Grounded Vision-Language-Action Model for Autonomous Wheel Loader（2026-09-15）
- [2609.16880](https://arxiv.org/abs/2609.16880) · Artificial Intelligence-Enabled Space Robot Operations: Technologies, Challenges and Prospects（2026-09-15）
- [2609.16696](https://arxiv.org/abs/2609.16696) · IL-ACT: Imitation Learning with Adaptive Cartesian Tracking Control for a 30-ton Excavator（2026-09-15）
- [2609.16369](https://arxiv.org/abs/2609.16369) · Autonomous Droplet Navigation via Model-Based Reinforcement Learning（2026-09-14）
- [2609.16186](https://arxiv.org/abs/2609.16186) · Occupancy Network-Guided Autonomous Robotic Partial Nephrectomy（2026-09-14）
- [2609.15861](https://arxiv.org/abs/2609.15861) · DuctAM: A Duct-Assisted Quadrotor-Based Aerial Manipulator Enabling High-Force Push-and-Pull Interactions（2026-09-14）
- [2609.14254](https://arxiv.org/abs/2609.14254) · Embracing Flow Unsteadiness: A High-Throughput Learning Platform Enables Vortex-Exploiting Bioinspired Propulsion（2026-09-13）
- [2609.14198](https://arxiv.org/abs/2609.14198) · Novel Ex-vivo Calf Brain Model with Integrated Sub-Skull Force Sensors to Access Simulated Neurosurgical Procedures（2026-09-13）
- [2609.12927](https://arxiv.org/abs/2609.12927) · Robust Underwater Grasping of Sloped Objects with a Waterproof Passive Adaptive Gripper（2026-09-11）
- [2609.12883](https://arxiv.org/abs/2609.12883) · From Transportation to Manipulation: Enabling Grasping in Magnetic Robotics（2026-09-11）

## 覆盖审计

下图按主主题统计每页所关联的论文数量。主题大小代表文献记录量，不代表研究质量或数据集价值；少量高质量、可复现的真实数据仍可能比大量不完整数据更有用。

![26 个独立知识点主题的论文数量分布及 36 篇范围外记录](/images/docs/paper-knowledge-map-evaluation.svg)

## 暂未纳入的论文

以下 **36 篇**被关键词检索命中，但原始摘要未直接支撑本站的数据采集、处理、标注、评估或数据集使用主题。此处仅说明文档范围，不评价论文质量；边界案例可在获得更直接的数据证据后重新归类。

- [2609.28416](https://arxiv.org/abs/2609.28416) · Agent-Editing World Model: Rethinking World Modeling for LLM Agents（2026-09-23）
- [2609.28335](https://arxiv.org/abs/2609.28335) · An Open Pipeline and Dashboard for Systemic-Risk Evidence under the EU AI Act's Code of Practice（2026-09-23）
- [2609.28182](https://arxiv.org/abs/2609.28182) · Finite-Sample Probabilistic Safety Certification for AI-Based Grid-Edge Coordination（2026-09-23）
- [2609.26761](https://arxiv.org/abs/2609.26761) · A2M: Trace-Optimized Agent Hijacking in the MCP Ecosystem（2026-09-22）
- [2609.24801](https://arxiv.org/abs/2609.24801) · Decoding Guardrails: XAI-Guided Perturbation Analysis of Prompt Injection Detection（2026-09-21）
- [2609.24742](https://arxiv.org/abs/2609.24742) · LLM-based Conversational AI Knowledge Assistant for MyBuddy Humanoid Robot（2026-09-21）
- [2609.21906](https://arxiv.org/abs/2609.21906) · Intervention Granularity Matters: Coherent Treatment Bundles in Counterfactual Simulation with Clinical World Models（2026-09-18）
- [2609.17325](https://arxiv.org/abs/2609.17325) · Intrinsic Motivation in Reinforcement Learning: A Research Agenda for Adaptive Self-Organisation（2026-09-15）
- [2609.17221](https://arxiv.org/abs/2609.17221) · Grounding SWE-Agent Decisions in Architecture-0 Design: Navigating Unknown Unknowns through Physical Mapping（2026-09-15）
- [2609.16778](https://arxiv.org/abs/2609.16778) · Unifying Semantic Priors and High-Frequency Traces: Enhancing V-JEPA with Mixture-of-Experts for Robust Synthetic Image Forensics（2026-09-15）
- [2609.16679](https://arxiv.org/abs/2609.16679) · AI for Games in the Foundation Model Era（2026-09-15）
- [2609.16436](https://arxiv.org/abs/2609.16436) · Interpreting and Steering LLM Agents for Social Simulations（2026-09-14）
- [2609.16409](https://arxiv.org/abs/2609.16409) · Reasoning with Image Generation（2026-09-14）
- [2609.15975](https://arxiv.org/abs/2609.15975) · Disentangling Representation Evolution in Transformers through Directional Decomposition（2026-09-14）
- [2609.16098](https://arxiv.org/abs/2609.16098) · Universal Defenses for Tool-Integrated LLM Agents Against Adversarial Attacks（2026-09-14）
- [2609.15277](https://arxiv.org/abs/2609.15277) · Artificial entrepreneurial cognition: Locating and causally steering an opportunity recognition dial inside large language models (LLMs)（2026-09-14）
- [2609.15234](https://arxiv.org/abs/2609.15234) · CWM: Controllable White-Box Meta-Prompting for Adaptive Retrieval-Augmented Generation and Reasoning Ability（2026-09-14）
- [2609.14709](https://arxiv.org/abs/2609.14709) · An immune world model for multiscale forecasting and therapeutic hypothesis generation（2026-09-13）
- [2609.14437](https://arxiv.org/abs/2609.14437) · Lightweight Generalized DeepFake Face Detection with WAVIE: Wavelet Augmented Vision Intermediate Embeddings（2026-09-13）
- [2609.16062](https://arxiv.org/abs/2609.16062) · Digital Persuasion: Understanding the Impact of Online Influencers on Public Opinion（2026-09-13）
- [2609.13927](https://arxiv.org/abs/2609.13927) · Exploring napping paradigm for Recurrent Spiking Neural Networks（2026-09-12）
- [2609.13771](https://arxiv.org/abs/2609.13771) · Homeostatic Continual Learning（2026-09-12）
- [2609.13499](https://arxiv.org/abs/2609.13499) · Canaries in the Bank: Auditing User-Level Privacy in Private Evolution（2026-09-11）
- [2609.13352](https://arxiv.org/abs/2609.13352) · Real-time Learning and Evolution in Robotic Art Installations（2026-09-11）
- [2609.12668](https://arxiv.org/abs/2609.12668) · Beyond Ambiguous Visual Cues: Studying Physiological Disruptions and Cross-Modal Inconsistencies in Deepfake Videos（2026-09-11）
- [2609.12606](https://arxiv.org/abs/2609.12606) · Beyond Generation and Accuracy: Diagnosing and Enhancing Visual Chain-of-Thought for Geometry Problem Solving（2026-09-11）
- [2609.10372](https://arxiv.org/abs/2609.10372) · PACE: Perceived-Latency-Aware Cascading Service Routing and Filler Control for QoE-Efficient Retrieval-Augmented Dialogue Serving（2026-09-09）
- [2609.06530](https://arxiv.org/abs/2609.06530) · Selective Knowledge Control for Continual GUI Agent Learning over Application Streams（2026-09-06）
- [2609.05404](https://arxiv.org/abs/2609.05404) · Diffusion TV: Experiencing Diffusion Models through Tangible, Embodied Interaction（2026-09-04）
- [2609.05227](https://arxiv.org/abs/2609.05227) · CABAL: Multi-Agent Simulacra for Tracing the Effects of Collusive Bidding in Peer Review（2026-09-04）
- [2609.02885](https://arxiv.org/abs/2609.02885) · Discriminative World Models for Web Agents（2026-09-02）
- [2609.02797](https://arxiv.org/abs/2609.02797) · Dutch Books for Language Models（2026-09-02）
- [2609.02640](https://arxiv.org/abs/2609.02640) · From Detection to Localization: A Unified Forensics Framework for Fully Synthetic and Tampered Images（2026-09-02）
- [2608.30656](https://arxiv.org/abs/2608.30656) · APT: Anchor-aligned Perturbations for Tamper Localization in Fully Regenerated Images（2026-08-31）
- [2608.28541](https://arxiv.org/abs/2608.28541) · An Enclosed Mode Is a Gauge Choice: Topology Relative to Reach in Certified Code World Models（2026-08-28）
- [2608.28302](https://arxiv.org/abs/2608.28302) · FUSED: Forensic-Semantic Mixture-of-Experts for AI Inpainting Detection and Localization（2026-08-28）

## 来源与更新口径

- 原始记录：`spiders/arxiv/papers/2026-*.json`，以单篇 `published` 和 arXiv ID 为准；`latest.json` 是滚动窗口，不作为全月来源。
- 主题判断：按具身智能**数据**用途归类。纯通用 Web/GUI/LLM 代理、图像取证、非机器人临床/金融/电网研究等不因关键词命中就进入正文。
- 复核方法：可从本页每条 arXiv 链接核对标题、摘要、版本和论文正文。数字结论只应在对应论文的实验设置下解释。
