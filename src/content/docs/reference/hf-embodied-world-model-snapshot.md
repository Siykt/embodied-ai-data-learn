---
title: Hugging Face 具身世界模型资料快照（2026 年 11 月）
description: 截至 2026 年 11 月 6 日，整理 Hugging Face 上可核验的具身世界模型、动作条件预测模型、数据集与演示空间。
---

**快照截止：2026 年 11 月 6 日（UTC+8）。** 本页按 Hugging Face Hub 在该日期可访问的模型、数据集和 Space 仓库归档，重点覆盖机器人操作、移动与导航，以及与物理交互直接相关的预测模型和数据。它是一个时间点的资源清单，不是排行榜；仓库可能改名、删除、转为私有或更新，链接内容也会继续变化。

“世界模型”在 Hub 上没有统一标签。为减少漏项，本次以 `world model`、`world-model`、`world action model`、`robotics`、`embodied`、`physical AI`、`latent action` 等关键词检索模型、数据集和 Space，并沿模型卡中的论文、基础模型和数据集链接扩展。逐项纳入条件是：仓库说明或其关联论文明确涉及具身交互状态预测、动作条件未来预测、机器人世界模型训练/评测，或直接承载这类项目的交互演示。仅标题含 world、一般视频生成、游戏代理、自动驾驶通用模型及普通 VLA 检查点不因关键词命中自动纳入。搜索与逐项筛选是按截止日冻结的；后续新增内容留待下一快照。

![快照按模型、数据、评估与交互演示四类资源建立索引](/images/docs/hf-world-model-snapshot-map.svg)

## 快速索引

| 资源类型 | 重点内容 | 如何用于数据工作 |
| --- | --- | --- |
| 模型与权重 | 物理一致视频预测、机器人动作条件视频、潜在状态规划 | 核对输入条件、动作语义、控制频率、本体与可用权重 |
| 数据集与评测集 | 物理视频偏好、机器人演示、潜在动作轨迹和预测误差案例 | 检查数据许可、来源、状态/动作标签和训练测试边界 |
| Space 与项目演示 | 在线交互、预测结果浏览、世界模型基准展示 | 用于快速理解接口；不能把演示结果当作可复现实验 |
| 关联项目与论文 | 同一项目的模型、数据和研究说明 | 顺着来源关系回到论文与数据协议，避免孤立解读权重 |

![具身世界模型项目把观测、动作、预测后果、真实结果与评测关联起来](/images/docs/hf-world-model-snapshot-lineage.svg)

## 模型与检查点

以下按模型卡所述用途归类。仓库存在不等于模型可直接运行：有些需要自定义代码、特定基础模型、专用推理管线或成套数据；具体许可和依赖以仓库当前卡片为准。

### 直接面向机器人交互与动作后果

| 仓库 | 方向与数据关联 | 阅读时核对 |
| --- | --- | --- |
| [NU-World-Model-Embodied-AI/FlashWAM-RoboTwin](https://huggingface.co/NU-World-Model-Embodied-AI/FlashWAM-RoboTwin) | RoboTwin 场景的世界动作模型，提供机器人动作条件的生成式预测权重；关联 RoboTwin 轨迹数据。 | 训练数据版本、机器人/任务覆盖、动作条件格式、蒸馏与推理配置；生成视频是否对应可执行的控制量。 |
| [motus-robotics/Motus](https://huggingface.co/motus-robotics/Motus) | 面向双臂操作的 VLA 与世界模型联合系统，涉及潜在动作和动作生成。 | 世界预测与策略输出的边界、潜在动作的解码方式、数据本体和闭环评估。 |
| [thuml/rt1-world-model-single-step-base](https://huggingface.co/thuml/rt1-world-model-single-step-base) | 基于 RT-1 机器人操作数据的单步视频世界模型基线。 | 单步预测范围、动作/帧对应关系及仿真或真机测试设置。 |
| [thuml/rt1-world-model-multi-step-base](https://huggingface.co/thuml/rt1-world-model-multi-step-base) | RT-1 多步预测基线，用于检查滚动预测中的误差积累。 | 多步预测时是否重新观测、预测步长和真实后续帧的配对方法。 |
| [thuml/rt1-world-model-single-step-rlvr](https://huggingface.co/thuml/rt1-world-model-single-step-rlvr) | 单步模型的强化学习式验证/优化版本。 | 优化目标与基础模型的差异，以及收益是否由真实机器人结果支持。 |
| [thuml/rt1-world-model-multi-step-rlvr](https://huggingface.co/thuml/rt1-world-model-multi-step-rlvr) | 多步模型的强化学习式验证/优化版本。 | 与多步基线使用相同的输入、预测跨度和评测条件。 |
| [LIN-linlin/4D-World-Models-Robotic-Manipulation](https://huggingface.co/LIN-linlin/4D-World-Models-Robotic-Manipulation) | 面向机器人操作的 4D 世界表示与策略/扩散模型资源，关联 LIBERO。 | 4D 表征是否含显式时间、物体状态和动作信息；LIBERO 结果不等于真机泛化。 |
| [vla-ustc/world_model_libero_action_default](https://huggingface.co/vla-ustc/world_model_libero_action_default) | Emu3 系列的 LIBERO 动作条件世界模型检查点之一。 | 该仓库是多种数据量、帧设置、夹爪编码和增强方案中的具体变体；需跟踪模型卡所列训练配方。 |
| [vla-ustc/world_model_simplerenv_30k_fulltune](https://huggingface.co/vla-ustc/world_model_simplerenv_30k_fulltune) | Emu3 在 SimplerEnv 任务上的世界模型微调检查点。 | 训练集环境与评测环境是否重合，以及视频预测与机器人成功率是否分别报告。 |
| [iantc104/wmil_peg_in_hole_world_model](https://huggingface.co/iantc104/wmil_peg_in_hole_world_model) | 插孔装配任务的世界模型资源。 | 观测、插入动作、接触阶段与成功判据是否能在数据中对齐。 |
| [iantc104/wmil_peg_in_hole_inverse_world_model](https://huggingface.co/iantc104/wmil_peg_in_hole_inverse_world_model) | 与插孔任务关联的逆世界模型资源。 | “逆模型”输出的变量含义、动作单位和可执行性边界。 |
| [open-gigaai/Giga-World-1](https://huggingface.co/open-gigaai/Giga-World-1) | 与机器人和交互式物理场景相关的生成式世界模型项目。 | 确认模型卡中的交互接口、机器人任务证据和权重/代码依赖，勿仅凭生成质量判断控制用途。 |
| [BLM-Lab/Boundless-World-Model](https://huggingface.co/BLM-Lab/Boundless-World-Model) | 标注为机器人、动作条件和视频生成的模型资源。 | 检查动作标签是否明确映射到机器人控制，以及对比测试是否包含真实执行结果。 |
| [jepa-world-models/h-jepa](https://huggingface.co/jepa-world-models/h-jepa) | 用于机器人规划的分层 JEPA 世界模型，采用不同层级/跨度的预测表征。 | 区分潜在预测误差、规划质量和闭环任务结果；核对层级时间尺度。 |
| [NU-World-Model-Embodied-AI/phyworld](https://huggingface.co/NU-World-Model-Embodied-AI/phyworld) | 物理一致的视频世界模型，关联 PhyGround 数据及物理偏好优化流程。 | 物理合理性监督、相机运动与对象运动、预测条件，以及模型评估是否覆盖具身可控性。 |
| [acvlab/ABot-World-0-5B-LF](https://huggingface.co/acvlab/ABot-World-0-5B-LF) | 大规模真实世界视频预训练的前瞻式视频模型，位于物理 AI/世界模型交界。 | 其通用真实视频预测能力不自动等于机器人动作条件预测；纳入数据训练前确认动作监督和交互协议。 |
| [yuanty/fastwam](https://huggingface.co/yuanty/fastwam) | 面向 LIBERO、RoboTwin 的高效世界动作模型。 | 对照不同基准、本体、动作时域和低延迟推理下的闭环成绩。 |
| [hustvl/FasterWAM](https://huggingface.co/hustvl/FasterWAM) | 面向机器人学习与操作的快速世界动作模型。 | 区分模型生成速度、真实控制频率和动作执行后的成功率。 |
| [vernerobotics/v0.5-base](https://huggingface.co/vernerobotics/v0.5-base)、[v0.5-libero](https://huggingface.co/vernerobotics/v0.5-libero)、[v0.5-robotwin](https://huggingface.co/vernerobotics/v0.5-robotwin) | 同一 Verne 世界动作模型系列的基础、LIBERO 和 RoboTwin 版本。 | 记录各变体训练数据与评测环境，避免将 benchmark 微调结果和通用基础模型混为一谈。 |
| [black-forest-labs/flux-3-action-base](https://huggingface.co/black-forest-labs/flux-3-action-base)、[flux-3-action-so101](https://huggingface.co/black-forest-labs/flux-3-action-so101) | 基础世界动作模型及 SO-101 机器人相关变体。 | 核对动作表示、机器人本体、底层执行接口和权重许可。 |
| [GEAR-Dreams/DreamZero-DROID](https://huggingface.co/GEAR-Dreams/DreamZero-DROID) | DROID 数据相关的动作预测/视频生成世界模型。 | 配对检查点与其 DROID 数据版本；注意仓库注明的非商业许可及真实执行评测边界。 |
| [J1dan/MiniWAM](https://huggingface.co/J1dan/MiniWAM) | 面向 LIBERO、RoboTwin 的轻量世界动作模型。 | 将压缩或轻量化效果与任务成功率、预测误差和控制延迟共同评估。 |
| [Efficient-Large-Model/Long-WAM-YAM](https://huggingface.co/Efficient-Large-Model/Long-WAM-YAM) | 面向长时域动作预测的世界动作模型，关联 ABC-130K。 | 检查预测跨度、动作块长度、训练集覆盖及长时误差积累。 |
| [flex-pi/flexpi-libero](https://huggingface.co/flex-pi/flexpi-libero)、[flexpi-libero-fulljoint-star](https://huggingface.co/flex-pi/flexpi-libero-fulljoint-star)、[flexpi-pretrain-rgb-preview](https://huggingface.co/flex-pi/flexpi-pretrain-rgb-preview) | FlexPi 系列的 LIBERO 操作、全关节和预训练检查点。 | 它关联多种机器人操作数据集；需逐项核对 RGB/深度输入、关节动作表示和训练混合比例。 |
| [ShilongZou/Pelican-Sim1.0](https://huggingface.co/ShilongZou/Pelican-Sim1.0) | Cosmos 系列基础上的动作条件物理 AI/机器人视频模型。 | 确认仿真场景、动作标签与真实机器人控制之间的迁移证据。 |
| [nvidia/Cosmos3-H-Embodied-Nano](https://huggingface.co/nvidia/Cosmos3-H-Embodied-Nano) | 面向手术机器人/医疗机器人场景的世界模型及策略评测资源。 | 专业领域数据需核查许可、模拟/临床差异、动作和安全约束；其适用性限于对应任务证据。 |
| [tencent/Hy-Nomas](https://huggingface.co/tencent/Hy-Nomas) | 交互式视频与摄像机控制模型，属于相邻的可控世界生成资源。 | 不是通用机器人策略；只有模型卡的交互条件与任务协议吻合时才纳入具身实验。 |
| [miniFranka/agentic-wam-pretrain-yamego3k-soup-e1](https://huggingface.co/miniFranka/agentic-wam-pretrain-yamego3k-soup-e1) | 关联 Yamego 视频数据的 Agentic WAM 预训练权重。 | 核验视频来源、动作编码和代码策略接口；预训练 checkpoint 不代表可直接部署。 |
| [x-square-robot/wall-oss-1.0-lite-robodojo](https://huggingface.co/x-square-robot/wall-oss-1.0-lite-robodojo)、[Robbyant-Research/zero-wam-posttrain-robotwin](https://huggingface.co/Robbyant-Research/zero-wam-posttrain-robotwin) | WALL 与 Zero-WAM 相关的机器人/Robotwin 权重或后训练资源。 | 核对它们是否实现显式未来预测或世界动作建模；若只是策略后训练，作为相邻资源而非世界模型本体使用。 |
| [DAGroup-PKU/HumanWAM-Vanilla-Exploration](https://huggingface.co/DAGroup-PKU/HumanWAM-Vanilla-Exploration) | 以人类视频和 RoboTwin 数据探索世界动作模型扩展的检查点。 | 人类视频中的动作需要映射到机器人可执行空间，不能把人类视角视频直接等同机器人示教。 |

### 物理评价与相关表征模型

| 仓库 | 方向与数据关联 | 阅读时核对 |
| --- | --- | --- |
| [NU-World-Model-Embodied-AI/phyjudge-9B](https://huggingface.co/NU-World-Model-Embodied-AI/phyjudge-9B) | 对物理视频结果作判别/评价的模型，关联 PhyGround。 | 这是评价器而非机器人策略；核对偏好标注、评测集污染与评价器和人工判断的一致性。 |
| [senngadaisuki/disentangled-latent-action-world-models](https://huggingface.co/senngadaisuki/disentangled-latent-action-world-models) | 将潜在动作与视频世界模型解耦的表征学习资源。 | 潜在动作可解释性、与真实机器人动作的映射及跨本体有效性。 |

Emu3 LIBERO 系列还有 `world_model_libero_action_8k_tune`、`..._s4k`、`..._s6k`、`..._wgripper`、`..._wgripper_waug`、`..._4k_4frms_tune` 等变体；SimplerEnv 系列还有 `world_model_simplerenv_action_30k_tune_s10k/s20k/s30k` 和 `world_model_simplerenv_action_30k_from_loraworld_s10k/s20k/s30k`。这些是同一实验族的不同训练配方，逐仓库清单可从 [vla-ustc 的 Hub 搜索](https://huggingface.co/vla-ustc?search=world_model)与 [Emu3 模型搜索](https://huggingface.co/models?search=world_model+Emu3)复核。使用时应把检查点哈希、训练量、数据源、是否包含夹爪、帧率和增强策略作为配对实验的基本元数据。

![模型输出须和输入条件、动作序列及实测结果成对核验](/images/docs/hf-world-model-snapshot-audit.svg)

## 数据集、轨迹与评测资源

| 仓库 | 资源类型 | 对世界模型工作的价值与边界 |
| --- | --- | --- |
| [NU-World-Model-Embodied-AI/phyground](https://huggingface.co/datasets/NU-World-Model-Embodied-AI/phyground) | 物理视频与偏好/评价相关数据 | 可用于物理一致性判断和模型偏好训练。逐项核对视频来源、标注字段、许可和机器人动作条件；物理视频偏好数据不等同于机器人轨迹。 |
| [VinayMohan/latent-action-world-model-data](https://huggingface.co/datasets/VinayMohan/latent-action-world-model-data) | RoboSuite/Panda 相关的具身视频与潜在动作数据 | 关注潜在动作如何从演示中抽取、是否保留本体状态与相机标定，以及能否关联原始执行。 |
| [Nielsenc/robot-world-model-videos](https://huggingface.co/datasets/Nielsenc/robot-world-model-videos) | 机器人世界模型视频样本 | 核对样本来源、动作是否同步、视频是否有 episode 与任务元数据；数据量标签小不代表覆盖充分。 |
| [robbyant/robotwin-clean-and-aug-lerobot](https://huggingface.co/datasets/robbyant/robotwin-clean-and-aug-lerobot) | RoboTwin 清洗与增强的 LeRobot 轨迹 | 是 FlashWAM-RoboTwin 等工作关联的数据源之一。保留清洗前后关系、仿真场景/任务划分和增强派生链。 |
| [agibot-world/AgiBotWorld-Alpha](https://huggingface.co/datasets/agibot-world/AgiBotWorld-Alpha) | 大规模机器人操作数据 | 可作为动作条件预测和操作模型的训练/对照来源；确认本体、动作空间、任务标签、时间戳与版本。 |
| [OpenGalaxea/Galaxea-Open-World-Dataset](https://huggingface.co/datasets/OpenGalaxea/Galaxea-Open-World-Dataset) | 双臂机器人开放场景数据 | 对跨场景、长时任务和双臂交互有参考价值；按任务和采集条件分层，避免仅按随机帧切分。 |
| [acvlab/ABot-World-Explorer-500h](https://huggingface.co/datasets/acvlab/ABot-World-Explorer-500h) | 大规模真实世界视频数据 | 属于世界模型的广域视频预训练来源；若没有配对机器人动作与控制结果，应按视频预训练数据使用而非机器人交互监督。 |
| [ClarusC64/robotics-world-model-consistency-v0.1](https://huggingface.co/datasets/ClarusC64/robotics-world-model-consistency-v0.1) | 机器人世界模型一致性评测样本 | 可用来检查描述或预测在连续状态中的一致性；需回看数据卡确认题目构造、标注来源和指标解释。 |
| [ClarusC64/robotics-world-model-coherence-drift-v0.1](https://huggingface.co/datasets/ClarusC64/robotics-world-model-coherence-drift-v0.1) | 长序列连贯性漂移评测样本 | 适合研究预测随时间累积的状态漂移；不能代替像素预测、状态误差和闭环执行三类评估。 |
| [mikusama99/action-world-model-sample-300](https://huggingface.co/datasets/mikusama99/action-world-model-sample-300) | 动作世界模型视频样本集 | 属于更广义的动作视频资源；只有确认其中具身/机器人样本比例、动作标签和来源后，才适合作为机器人训练数据。 |
| [mikusama99/action-world-model-atlas-1500-media-20260914](https://huggingface.co/datasets/mikusama99/action-world-model-atlas-1500-media-20260914) | 动作世界模型媒体索引/样本集 | 可作资源发现入口；逐条核对视频版权、实体类别、动作条件和可获取性，不能把媒体汇编直接视作清洗后的训练集。 |

### 移动机器人、自动驾驶与通用物理场景资源

这些资源服务于更广义的具身系统或物理场景建模，不应与桌面机械臂操作结果直接并表；但它们覆盖移动主体、仓储机器人和多传感器环境，是具身世界模型资料的一部分。

| 仓库 | 场景 | 使用边界 |
| --- | --- | --- |
| [nvidia/PhysicalAI-WorldModel-Synthetic-Autonomous-Driving-Scenarios](https://huggingface.co/datasets/nvidia/PhysicalAI-WorldModel-Synthetic-Autonomous-Driving-Scenarios) | 自动驾驶世界模型合成场景 | 用于移动主体和道路场景的预测/仿真研究；注意合成来源、传感器配置、交通参与者轨迹与真实道路分布差异。 |
| [nvidia/PhysicalAI-WorldModel-Synthetic-Warehouse-Operations-Scenes](https://huggingface.co/datasets/nvidia/PhysicalAI-WorldModel-Synthetic-Warehouse-Operations-Scenes) | 仓储操作合成场景 | 关注移动机器人、货物和人员之间的空间与时间关系；验证安全和碰撞指标时须区分渲染标签与实物测量。 |
| [nvidia/PhysicalAI-WorldModel-Synthetic-Digital-Human-Scenes](https://huggingface.co/datasets/nvidia/PhysicalAI-WorldModel-Synthetic-Digital-Human-Scenes) | 数字人和物理场景合成数据 | 可研究人与机器人共处环境的场景变化；若没有机器人动作与后果配对，不属于动作条件机器人轨迹。 |
| [nvidia/PhysicalAI-Robotics-Open-H-Embodiment](https://huggingface.co/datasets/nvidia/PhysicalAI-Robotics-Open-H-Embodiment) | H-Embodiment 机器人示教与相关训练数据 | Cosmos3-H-Embodied-Nano 等模型卡关联的数据资源；要保留不同机器人和任务的本体元数据、许可与相机/控制时间线。 |

数据集在 Hub 上存在，不能替代数据审查。正式训练前应下载或查看数据卡，并登记仓库 revision、许可、数据来源、去重方式、跨集合泄漏检查、时间同步、机器人本体和动作语义。对模型生成的未来视频，应标记为合成/想象轨迹，与真实执行观测分别存放。

## Hugging Face Papers 与项目论文

Hub 模型卡会用 `arxiv:` 标签或正文关联论文。以下是本清单中模型/数据资源直接关联、且有 Hugging Face Papers 页面可访问的代表性来源；论文用于还原训练方法与评估协议，仓库权重则用于核对实际发布内容。两者版本和实验设置可能并不完全一致。

| Hugging Face Papers | 关联仓库或主题 |
| --- | --- |
| [RT1 World Model: Learning to Predict Robot Manipulation Videos with Action](https://huggingface.co/papers/2505.13934) | `thuml/rt1-world-model-*`：单步、多步预测及 RLVR 变体。 |
| [Motus](https://huggingface.co/papers/2512.13030) | `motus-robotics/Motus`：双臂操作、VLA 与世界模型协同。 |
| [PhyWorld](https://huggingface.co/papers/2605.19242) | `NU-World-Model-Embodied-AI/phyworld` 与 `phyground`：物理一致视频生成与偏好监督。 |
| [PhyJudge](https://huggingface.co/papers/2605.10806) | `NU-World-Model-Embodied-AI/phyjudge-9B`：物理视频评价。 |
| [FlashWAM](https://huggingface.co/papers/2606.05254) | `NU-World-Model-Embodied-AI/FlashWAM-RoboTwin`：RoboTwin 世界动作模型。 |
| [Giga-World-1](https://huggingface.co/papers/2607.02642) | `open-gigaai/Giga-World-1`：生成式世界模型与机器人场景。 |
| [H-JEPA](https://huggingface.co/papers/2610.06805) | `jepa-world-models/h-jepa`：层级预测和机器人规划。 |

这些页面中的论文版本会持续更新；若要复现实验，应固定论文版本、代码提交、数据集 revision 与 checkpoint SHA，并查看模型卡是否明确提供同一配置。

## Space 与可交互演示

| Space | 内容线索 | 适合的用途 |
| --- | --- | --- |
| [hugging-apps/uranus-embodied-world-model](https://huggingface.co/spaces/hugging-apps/uranus-embodied-world-model) | 具身世界模型交互入口 | 查看交互形式与输入输出；页面存活和可用性随 Space 状态变化。 |
| [hugging-apps/kairos-world-action-model](https://huggingface.co/spaces/hugging-apps/kairos-world-action-model) | 世界动作模型演示入口 | 观察动作条件预测界面；核对后端模型与可复现实验说明。 |
| [Bariona/fact-world-action-model](https://huggingface.co/spaces/Bariona/fact-world-action-model) | 标记为机器人世界模型/视频预测的演示 | 用作在线体验入口，不应将交互生成画面作为模型能力的独立证据。 |
| [FINAL-Bench/worldmodel-bench](https://huggingface.co/spaces/FINAL-Bench/worldmodel-bench) | 具身世界模型基准或排行榜入口 | 查看任务与评估组织；比较前确认不同模型的输入、采样预算和硬件条件一致。 |
| [FINAL-Bench/World-Model](https://huggingface.co/spaces/FINAL-Bench/World-Model) | 具身/交互式世界模型演示 | 适合理解交互接口与基准任务，不等价于独立复现。 |
| [1x-technologies/1X_World_Model_Challenge_Home](https://huggingface.co/spaces/1x-technologies/1X_World_Model_Challenge_Home) | 1X 世界模型挑战赛说明入口 | 查阅任务定义和数据挑战信息；挑战赛规则需固定到当时版本。 |
| [1x-technologies/1X_World_Model_Challenge_Sampling](https://huggingface.co/spaces/1x-technologies/1X_World_Model_Challenge_Sampling) | 挑战赛相关采样/评测工具入口 | 复核采样协议和任务边界。 |
| [1x-technologies/1X_World_Model_Challenge_Compression](https://huggingface.co/spaces/1x-technologies/1X_World_Model_Challenge_Compression) | 挑战赛压缩赛道入口 | 关注压缩后模型的质量、延迟和执行成功率权衡。 |
| [Ethgar/world-models](https://huggingface.co/spaces/Ethgar/world-models) | 标记为 robotics、JEPA、MPPI 的项目页面 | 作为规划与世界模型的相关入口；核实其代码、checkpoint 和运行记录。 |
| [WitneyWW/tactile-world-model-rollouts](https://huggingface.co/spaces/WitneyWW/tactile-world-model-rollouts) | 触觉世界模型 rollout 浏览 | 关注视觉与触觉同步、接触时刻和预测结果是否能追溯到真实观测。 |
| [WitneyWW/view-tactile-world-model-rollouts](https://huggingface.co/spaces/WitneyWW/view-tactile-world-model-rollouts) | 触觉世界模型结果查看器 | 辅助检查生成/预测 rollout 的呈现；查看器本身不是模型或数据集。 |

Space 属于可变服务：构建依赖、GPU 配额、睡眠状态和后端版本都会影响结果。若要引用某次演示结果，应同时保存访问日期、代码 revision、模型 revision、输入样本和输出文件。

## 按数据使用任务选择

| 你要完成的工作 | 可从这些资源开始 | 必须补齐的证据 |
| --- | --- | --- |
| 训练物理合理的视频预测器 | PhyWorld、PhyGround、ABot 视频资源 | 动作条件、真实状态标签、对象交互和跨场景留出集 |
| 预测机器人动作后果 | FlashWAM、RT-1 WM、Emu3 LIBERO/SimplerEnv 检查点 | 观测与命令延迟、动作时间范围、真实 rollout 配对 |
| 做潜在动作或分层规划 | H-JEPA、Motus、latent-action 数据 | 表征到机器人控制的映射、层级跨度与闭环成功率 |
| 测量长时预测漂移 | RT-1 多步版本、Coherence Drift 数据 | 逐步误差曲线、重置/再观测条件、未见任务分层 |
| 检查物理评价能力 | PhyJudge、PhyGround、一致性数据 | 人工复核、评测集隔离、对操作成功的相关性 |
| 快速了解在线交互 | 对应 Space | 固定 revision 和输入；把演示与正式评测区分开 |

## 使用前的仓库核验清单

1. 将 `org/repo` 与 revision SHA 一起记录；主分支会变，页面当前内容不是本快照的原始副本。
2. 阅读模型卡或数据卡，记录许可证、训练数据、基础模型、依赖、自定义代码和用途限制。
3. 对视频与动作检查时间基准、帧率、控制频率、动作单位、坐标系、episode 边界和相机运动。
4. 分开统计真实数据、仿真数据、合成数据、模型想象轨迹和增强副本；保存每一层的来源关系。
5. 评估预测时同时报告视觉/状态预测误差、物理约束、动作候选排序和闭环任务结果；不要用单一视频质量指标推断执行能力。
6. 训练/验证/测试按场景、物体、任务、演示者和机器人本体分组切分，防止近重复轨迹泄漏。

相关主题：[世界模型训练数据与物理表征](/guides/world-model-training-data/)、[世界模型规划与决策评估](/guides/world-model-planning-evaluation/)、[潜在动作与跨本体对齐](/guides/latent-action-cross-embodiment/)和[具身智能数据术语表](/reference/terms/)。
