---
title: 触觉、力觉与接触数据
description: 整理接触事件的多频率采集、标定、预测与操作评估。
---

接触发生在局部且变化快；只看视频，可能错过轻微滑移、夹持力不足或人手真正接管物体的时刻。[双臂人机交接](https://arxiv.org/abs/2609.05282)用触觉时间模式判断交接意图，[SlipSense](https://arxiv.org/abs/2609.15910)明确测滑移检测延迟，[TacPAC](https://arxiv.org/abs/2609.05266)将执行期间到来的触觉反馈用于实时修正。触觉数据的核心是采样时钟、接触位置和实际控制响应的联合记录。

![触觉力觉数据从多频率采集、事件切分到闭环操作验证的流程](/images/docs/tactile-force-contact-data-flow.svg)

## 概念与数据问题

触觉通常指分布式接触压力或形变观测，力觉常指力/力矩测量或估计；二者可互补，但不能混为同一真值。[无力传感器力估计](https://arxiv.org/abs/2609.13779)研究在浮动基座运动操作中估计末端力；[PredTac](https://arxiv.org/abs/2609.15198)从视觉和本体状态预测触觉。预测触觉必须与实测触觉明确区分，训练时也要记录预测所依据的信息范围。

## 采集、处理与对齐

**采集**：触觉阵列、六轴力/力矩、相机、关节状态和夹爪命令分别保留原始采样率与设备时钟。触觉阵列中的单个空间采样点称为触觉单元（taxel）。[STAR](https://arxiv.org/abs/2609.12549)构建同步视觉、触觉与语言标注的双手灵巧操作数据；[UniDex-ViTac](https://arxiv.org/abs/2609.16504)利用人类视频引导仿真生成带指尖接触的机器人示范；[DexTouch-WM](https://arxiv.org/abs/2609.20649)从人类触觉学习动作条件预测。跨人手和机器人手需保存触点映射与本体差异。

**处理和标注**：标接触开始、滑移征兆、稳定抓持、释放和碰撞，并对接触区域及力方向做质量标记。[Touch2Trace](https://arxiv.org/abs/2609.15921)的缆线操作依赖连续压力和摩擦调节，[Vision-Force Admittance Learning](https://arxiv.org/abs/2609.14133)融合异步视觉与高频力反馈，[全手实时力调节](https://arxiv.org/abs/2609.30082)处理变化的多点接触；因此不要把高频信号简单平均成每视频帧一个数。

**表示选择**：[Visible Touch](https://arxiv.org/abs/2609.14156)把接触渲染成视觉输入，[Agile-WAM](https://arxiv.org/abs/2609.20761)和[DexTacWAM](https://arxiv.org/abs/2609.24976)将触觉纳入世界动作模型。派生图像或潜在向量应保留到原始传感器帧的映射。

![触觉样本将传感器标定、时间序列、接触标签和实际动作绑定](/images/docs/tactile-force-contact-data-contract.svg)

## 最小字段契约

字段名是建议的数据接口，不表示所引论文使用完全相同的文件格式。

| 字段 | 记录内容 | 检查重点 |
| --- | --- | --- |
| episode_id / contact_event_id | 任务及接触事件 | 事件边界可回看 |
| sensor_id / calibration_id | 传感器布局、单位、零点 | 接触位置与力可复现 |
| sample_at / clock_domain | 各通道原始时间 | 不同频率插值有依据 |
| taxel_values / force_torque | 压力阵列与力矩原始值 | 饱和、漂移和缺失标记 |
| contact_link / object_id | 接触手指、连杆与物体 | 多点接触分别记录 |
| contact_state / slip_label | 接触、滑移和释放标签 | 标注依据与延迟可追溯 |
| command / applied_motion | 期望与实测调节动作 | 触觉到动作反应时间可算 |
| predicted_touch / source | 推断触觉及其输入来源 | 不和实测值混用 |

## 质控与评估

质检先测零点漂移、饱和、阵列坏点、坐标方向和时钟差；再检查滑移或接触标注的时间误差。评估分事件检测、力/位置估计、控制结果三层：报告检测延迟与误报、估计误差、任务成功及物体损伤。[SlipSense](https://arxiv.org/abs/2609.15910)说明低延迟应单独量化；[易碎物安全抓取](https://arxiv.org/abs/2609.12737)说明抓住物体还不等于安全；[Atomic Motion Coordinate](https://arxiv.org/abs/2609.15012)提示语言引导与力响应的动作目标也要对齐。

![触觉与力觉数据按事件检测、状态估计和控制结果逐层评估](/images/docs/tactile-force-contact-data-evaluation.svg)

## 数据集使用边界

触觉传感器的表面材料、采样率、安装位置和手型会显著改变信号分布。跨平台训练需把设备与标定作为分组变量，并对目标平台单独验证。仿真或预测触觉可扩充训练，但不可作为无偏实测真值；涉及人机接触时还需报告释放过早、拉扯和过力事件。

## 2026 年 10 月补充：接触既是观测，也是监督与动作目标

### 同样的信号可能表达不同的物理意图

[RATE（2610.03538）](https://arxiv.org/abs/2610.03538)用历史预测与告警监督连接触觉和任务风险。相似的信号变化可能是噪声、必要接触或危险前兆，因此风险标签必须连接任务阶段、前置历史和告警依据，不能仅由压力幅值生成。[PalmSpace（2610.10370）](https://arxiv.org/abs/2610.10370)联合表达接触发生、交互模式和手掌参照位置，说明身体表面上的触点需要统一坐标与模式标签；但它是腕戴红外交互输入研究，不能据其结果推断机器人已获得相同的接触力测量能力。跨参与者划分可作为此类人体输入数据的检验方式。

[Factorized Tactile Representation（2610.10510）](https://arxiv.org/abs/2610.10510)把有效接触响应分成接触几何、力分布和时间变化，并分开编码及随机化。数据集可据此分别记录位置、幅值与动态响应误差，避免一种总误差遮住特定通道失效。[RiCo（2610.12333）](https://arxiv.org/abs/2610.12333)则以局部接触表面点及邻域相对几何、运动、物性推断刚体交互。其接触邻域是仿真表示，需要保存采样点身份、邻域规则和物性来源，不能与传感器 taxel 直接等同。

![触觉原始记录经几何与力标定后，可分别形成风险标签、预训练监督和动作力参考；三条用途均保留来源，并使用事件、接触重建和闭环反馈各自验收。](/images/docs/tactile-force-contact-data-october-contact-roles.svg)

### 专家任务与自由交互提供不同监督

[Contact Trajectory Prompting（2610.18848）](https://arxiv.org/abs/2610.18848)将示教中的运动与接触过程作为有序提示，在执行中检索相关信息。**接触轨迹提示**因此不只是动作路径，还指定接触强度和方向；采集要保留接触时序、力坐标及参考示教身份，评估要检查改变参考后是否真的改变了物理行为。

[ForceWAM（2610.18852）](https://arxiv.org/abs/2610.18852)用成功示教学任务相关的视频与六轴力/力矩未来，再用任务与自由交互数据共同训练从这些未来到动作的映射。自由交互提供“动作怎样改变接触”的覆盖，但不天然带任务成功目标。混合时必须标出 `data_role=task/play`、施加动作、力响应及终止原因，分别统计目标轨迹覆盖和接触响应覆盖。

[ILA（2610.18855）](https://arxiv.org/abs/2610.18855)把运动、接触与施力演化共同压缩为可解码交互潜变量，作为动作生成与离线改进的单位。这要求动作与触觉在同一窗口内配对，并保存编码器、解码器及窗口时间；只保留潜变量会失去复查原始力响应的能力。其基于专家一致性的奖励是派生评价，不能等同于真实物体损伤或通用安全标签。

[CW-WAM（2610.30117）](https://arxiv.org/abs/2610.30117)预测时间对齐的运动和接触力旋量块，再由导纳控制器结合实时力反馈执行。**力旋量（wrench）**是三维力与三维力矩组成的六维量，必须同时给出表达坐标系和力矩参考点。预测参考与测得反馈要分字段保留，控制器更新频率、模型查询时刻及中间实际动作也须记录，才能核验“力预测准确”是否转化为执行稳定。

### 训练时有触觉，不等于部署时必须有触觉

[Spark-0（2610.22342）](https://arxiv.org/abs/2610.22342)一方面把触觉手套的接触图投到图像空间监督视觉特征，另一方面以区域力历史和三维触觉单元条件化动作；训练与推理的触觉用途不同。发布数据时应同时保存手套标定、触点到图像的投影、接触可见性及 `train_only/deploy_input` 用途掩码。评估需分别列出仅视觉部署和带触觉部署，不能把训练监督增益解释成运行时传感器收益。

[OpenViTac（2610.10384）](https://arxiv.org/abs/2610.10384)提供仿真与实机配对的接触操作评测，用于比较表示、融合及联合训练。采用其思路时，任务 ID、初始化与成功定义应对应，模拟触觉和实测触觉的来源仍需区分。[Tactile In-Hand Object Rotation（2610.26759）](https://arxiv.org/abs/2610.26759)在不同手指排列下比较触觉条件，说明本体形态也改变接触组织与负载分配。除转动进度外，应按手型记录手指参与、持续时间和指尖负载，不能把手型差异全部归因于传感器。

[Native Visuo-Tactile Policy（2610.26846）](https://arxiv.org/abs/2610.26846)研究通用多模态模型把视觉触觉图像直接作为输入，其摘要实验在模拟基准上进行，并明确提出实物验证需求。可借鉴其视觉/视觉触觉配对比较，但不能据此声明实机力控已获验证；还应保留模型版本、提示示例、场景种子、切向受力与恢复失败切片。

| 数据用途 | 新增记录示例 | 主要验收 |
| --- | --- | --- |
| 风险与模式 | 历史窗口、阶段、告警依据、接触模式 | 必要接触与异常接触的误报/漏报 |
| 接触目标 | 示教提示、运动-力块、坐标与参考点 | 强度/方向遵从及闭环力误差 |
| 预训练监督 | 投影标定、监督掩码、部署模态 | 同数据预算下仅视觉/带触觉对照 |
| 跨域与跨手型 | 仿真/实机配对、手型、传感器布局 | 未见物体、各手指负载、失败类型 |

表中字段为本站建议。十二篇论文覆盖人体输入、仿真交互、预训练与机器人控制，证据范围不同；本段按原始摘要归纳方法和数据需求，不跨论文直接比较成功率，也不把预测触觉、模拟力和实测力合并为一种真值。

## 2026 年 9 月整理来源

以下论文按清单中的主主题归档。跨主题使用时，应重新核对任务、传感器和评测口径。

- [Temporal Tactile Encoding and Compliance for Intent-Aware Robot-to-Human Bimanual Handover](https://arxiv.org/abs/2609.05282)（2609.05282）
- [TacPAC: Tactile Prediction and Real-Time Action Correction in World-Action Models for Contact-Rich Manipulation](https://arxiv.org/abs/2609.05266)（2609.05266）
- [UniDex-ViTac: Learning Unified Visuo-Tactile Dexterous Manipulation Policy from Human Video Data](https://arxiv.org/abs/2609.16504)（2609.16504）
- [Touch2Trace: Tactile-Driven Imitation Learning for Dexterous Cable Tracing](https://arxiv.org/abs/2609.15921)（2609.15921）
- [SlipSense: Multimodal Tactile Learning for Low-Latency and Generalized Slip Detection](https://arxiv.org/abs/2609.15910)（2609.15910）
- [PredTac: Learning Contact-Rich Manipulation with Predicted Touch](https://arxiv.org/abs/2609.15198)（2609.15198）
- [Atomic Motion Coordinate for Language-Steerable and Force-Responsive Manipulation](https://arxiv.org/abs/2609.15012)（2609.15012）
- [Visible Touch: Rendering Contact for Visuomotor Policies](https://arxiv.org/abs/2609.14156)（2609.14156）
- [Vision-Force Admittance Learning for Peg Insertion into a Movable Hole](https://arxiv.org/abs/2609.14133)（2609.14133）
- [Force-Aware Reinforcement Learning with Hybrid Sensorless Force Estimation for Wheeled-Legged Loco-Manipulation](https://arxiv.org/abs/2609.13779)（2609.13779）
- [Control Architecture for Safe Grasping of Fragile Objects Using a Coarse Position-Controlled Gripper](https://arxiv.org/abs/2609.12737)（2609.12737）
- [STAR: Sparse Tactile Representation Learning in Vision-Tactile-Language-Action Models for Dexterous Manipulation](https://arxiv.org/abs/2609.12549)（2609.12549）
- [Agile-WAM: An Agile Tactile World Action Model for Contact-Rich Robot Control](https://arxiv.org/abs/2609.20761)（2609.20761）
- [DexTouch-WM: Learning Action-Conditioned Tactile World Models from Human Touch for Dexterous Robot Manipulation](https://arxiv.org/abs/2609.20649)（2609.20649）
- [DexTacWAM: A Visuo-Tactile World-Action Model for Dexterous Manipulation](https://arxiv.org/abs/2609.24976)（2609.24976）
- [Real-Time Force Regulation for Whole-Hand Dexterous Grasping](https://arxiv.org/abs/2609.30082)（2609.30082）
