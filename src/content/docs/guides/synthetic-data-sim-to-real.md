---
title: 合成数据与仿真到真实迁移
description: 从可交互场景构造、合成监督到 sim-to-real 对照，建立合成数据的物理与任务质量检查。
---

合成具身数据由仿真、生成模型或图像编辑产生，目标是提供带状态、动作和结果的可执行经验。仿真到真实迁移（sim-to-real）考察用此类数据训练或选择的策略，在真实设备和环境中是否仍有效。

[IM-ENGINE](https://arxiv.org/abs/2609.06279)把图像编辑后的目标经显式三维恢复和物理修正转为机器人监督；[φ-RIE](https://arxiv.org/abs/2609.26795)把照片级重建中的物体做成可移动仿真资产；[Uranus](https://arxiv.org/abs/2609.24815)研究按关节轨迹条件生成连续多视角视频。它们分别强调语义、可交互物理状态和动作条件一致性。

![真实场景与任务种子经合成生成、物理校正和数据准入后，再与真实机器人闭环结果对照。](/images/docs/synthetic-data-sim-to-real-flow.svg)

## 输入、输出与处理链

输入是任务目标、场景资产、机器人模型和生成条件；输出是与图像、状态真值及执行动作互相一致的合成 episode，并附物理检查与真实对照记录。图像编辑、场景重建和视频生成各有不同的真值来源，必须写清哪些量由仿真给出、哪些由模型预测。

1. 定义任务、机器人、资产与生成器版本；锁定真实评估切片。
2. 生成场景或目标状态，保留分割、深度、物理参数和动作条件。
3. 运行碰撞、支撑、接触与轨迹可执行性检查，剔除仅视觉合理的样本。
4. 对照真实采集的分布和闭环结果，记录迁移差距与失败类型。

### 时间与空间对齐

合成 RGB、深度、分割与状态真值必须共享同一渲染时刻、相机内外参和对象 ID。动作条件既要保留请求轨迹，也要记录仿真实际执行轨迹。重建场景中被搬动资产与补全背景要用同一对象身份连接，避免外观变化与物理状态相互矛盾。

![合成数据契约连接生成器和资产种子、同帧视觉及物理真值、执行动作与真实迁移证据。](/images/docs/synthetic-data-sim-to-real-contract.svg)

## 最小数据字段

| 字段组 | 建议字段 | 用途 |
| --- | --- | --- |
| 生成血缘 | `generator_version、asset_version、seed、source_scene` | 复现同一合成样本 |
| 任务条件 | `task_id、goal_state、robot_model、domain_params` | 定义训练目标与随机化 |
| 多模态观测 | `rgb、depth、segmentation、camera_pose` | 像素与三维真值配准 |
| 物理状态 | `object_pose、contact、mass、friction` | 验证交互合理性 |
| 动作轨迹 | `commanded_action、executed_action、collision_event` | 防止视觉与控制脱节 |
| 迁移标记 | `real_pair_id、domain_gap、split、qc_status` | 定位真实差距与准入 |

生成器版本、原始场景和资产版本决定样本的可复现性；评估切片必须能追溯是否与训练生成素材共享来源。

![合成数据评估把跨视角视觉一致性、接触动作可重放性和未见真实场景成功率分开。](/images/docs/synthetic-data-sim-to-real-evaluation.svg)

## 质量控制与评估

合成样本先过多视角外观与物理可交互性检查，再用真实设备检验迁移。视觉可信、物理可执行和真实闭环收益不能合并成同一个分数：

- 渲染检查外观、遮挡和跨视角身份一致性；物理检查接触、穿透、支撑和动作可执行性。
- 分别报告任务条件覆盖与合成成功率，避免生成失败被筛掉后分布变窄。
- 真实对照按物体、场景、相机和机器人分层；模拟成绩仅能作为真实迁移的代理指标。
- 资产或生成器版本变化要重新建立基线，不把不同仿真协议的成功率直接相减。

| 评估层 | 指标或证据 | 判读要点 |
| --- | --- | --- |
| 视觉一致性 | 跨视角/时间外观误差 | 对象身份保持 |
| 物理可用性 | 接触、碰撞、动作重放 | 任务结果可复现 |
| 真实迁移 | 仿真与实机闭环差距 | 按未见域分层 |

## 数据集使用边界

合成数据适合扩充难例、目标状态和可观测中间标签，也适合先在仿真中筛选策略。生成器可能复制训练场景或掩盖真实传感器噪声；评估集要按原始场景、资产和真实采集批次隔离。[H2RBench](https://arxiv.org/abs/2609.24778)提供标准化人到机器人迁移比较，但其仿真与实机相关性不应无条件推广到其他任务。

## 本页术语

本页使用的关键术语：

- **合成数据**：由仿真或生成过程产生、可追溯其生成条件的数据。
- **仿真到真实迁移**：在仿真数据上形成的能力转用于真实设备的过程。
- **域差距**：仿真与真实在观测、动力学或任务分布上的差异。

## 2026 年 10 月补充：任务可用资产与物理校准记录

### 仿真重建需要能接受任务检查

[AffordCraft（2610.06643）](https://arxiv.org/abs/2610.06643)根据照片与任务从已有可动资产库检索、拟合物体，保留部件与关节结构。它提供了与逐图生成不同的来源链：发布资产时要保存库条目、部件映射、拟合变换和任务操作部位。质检应检查放置后能否稳定、关节能否执行目标运动，而非仅检查渲染相似度；库覆盖率变化也可能改变生成数据的类别分布。

[Agentic RSR（2610.10479）](https://arxiv.org/abs/2610.10479)从工作区视频恢复米制场景，在 MuJoCo 中检查任务交互，再把策略输入从特权物体状态逐渐转向视觉观测。数据应记录每个阶段策略实际可见的输入，防止仿真真值悄悄进入实机评估。共同任务接口可以连接仿真与实机，但场景深度/外观误差和实机任务结果仍须分别保留。

![照片资产检索与场景扫描分别形成视觉和碰撞资产，物理修订记录接触参数变化，仿真轨迹再连接实机残差与迁移评估。](/images/docs/synthetic-data-sim-to-real-october-task-assets.svg)

[Splat2Act（2610.13945）](https://arxiv.org/abs/2610.13945)把手机扫描得到的场景外观与碰撞几何结合，自动发现承放物体的表面并用仿真专家生成抓取示教。两阶段适配区分公共物体与用户物体。这里的**场景数字孪生**指用于对应真实场景的数字表示，其渲染外观与碰撞几何是不同数据层。应记录扫描 ID、承放表面、物体来源和个性化阶段；目标场景内适配结果不能直接表述为未见家庭泛化。

### 物理参数是数据版本的一部分

[RoboSimStudio（2610.18835）](https://arxiv.org/abs/2610.18835)把求解器、接触模型、物理参数显式开放给人或代理迭代修订，并研究视觉评估和力反馈。这提示真实到仿真流程应保留“观测证据—参数修改—回放结果”的修订日志。同一条控制轨迹换求解器后得到不同接触力，属于新的派生标签版本，不能覆盖旧值。

[Simulation Priors for Rapid Adaptation（2610.26757）](https://arxiv.org/abs/2610.26757)在自动赛车中混合不同保真度的仿真轨迹，再用有限真实交互修正世界模型。这里的仿真是有偏先验，并未假定完全准确。数据整理应标出保真度、赛道/路面、适配轮次与真实残差，避免把同一赛道在线采样同时用于适配和最终留出测试；赛车结果也不能直接替代机械臂接触任务验证。

| 需要新增的追溯链 | 关键字段示例 | 下游用途 |
| --- | --- | --- |
| 资产检索与拟合 | `library_asset_id、fit_transform、joint_schema` | 复现可动结构与类别覆盖 |
| 视觉/物理双层场景 | `scan_id、render_asset、collision_asset、support_surface` | 核对任务接触与视觉观测 |
| 物理修订 | `solver_version、contact_model、parameter_diff、replay_id` | 重算受影响的状态与力标签 |
| 跨域适配 | `fidelity_tag、policy_input_mask、adaptation_round、real_pair_id` | 区分真值监督、部署输入与实机收益 |

字段是本站建议，论文描述来自本地原始摘要。上述不同管线没有统一的“仿真质量分”；按资产稳定性、任务可执行性、物理残差和留出实机结果分别验收，才知道新增合成样本是否真的补足目标数据。

## 2026 年 9 月整理来源

以下为该主题在 2026-08-27 至 2026-09-27 采集批次中的全部主归类论文；每条均链接原始 arXiv 页面。

- [SpatialCrafter: Single Image World Modeling with Generative 3D Proxies](https://arxiv.org/abs/2608.27073)（2608.27073）
- [SolarWM: Open Data and Scalable Training for Long-Horizon Video World Models](https://arxiv.org/abs/2609.02886)（2609.02886）
- [IM-ENGINE: Image Editing for Embodied Data Generation](https://arxiv.org/abs/2609.06279)（2609.06279）
- [NeuroSymbEAD: A Large Scale Neuro-Symbolic Caption Dataset for Omni-Directional Embodied Autonomous Driving](https://arxiv.org/abs/2609.16919)（2609.16919）
- [PhysStream: Streaming Physics-Grounded Video Generation with Structured Scene Memory and Fine-Grained Motion Control](https://arxiv.org/abs/2609.17521)（2609.17521）
- [Dreaming the Sound of Contact: Leveraging Video and Audio Generation for Zero-Shot Force-Aware Manipulation and Data Generation](https://arxiv.org/abs/2609.19137)（2609.19137）
- [V2-STRep: VLM-Grounded Structured Task Representations for Reusable Robot Skills Acquired from Generated Videos](https://arxiv.org/abs/2609.20582)（2609.20582）
- [A Sim-to-Real Integration Pipeline for Training and Deployment of Chunk-Based VLA Manipulation Policies](https://arxiv.org/abs/2609.21817)（2609.21817）
- [Uranus: Building the Next-Generation Simulation Infrastructure for Embodied AI](https://arxiv.org/abs/2609.24815)（2609.24815）
- [φ-RIE: From Photorealistic Reconstruction to Interactive Environments](https://arxiv.org/abs/2609.26795)（2609.26795）
