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

## 本主题论文

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
