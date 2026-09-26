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

## 本月相关论文

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
