---
title: 多模态时空对齐数据
description: 整理视觉、深度、状态、动作和力觉等模态的时钟、坐标、可见性与融合质量。
---

多模态时空对齐把来自不同频率、时钟和坐标系的观测映射到可解释的共同事件。空间配准说明一个深度点或力方向位于哪个坐标系；时间对齐说明该观测对应哪次动作前后。融合模型只有在这些关系明确时，才可从多模态数据学习控制。

[Temporal Forcing](https://arxiv.org/abs/2608.30643)指出单帧三维几何难区分相似外观但历史不同的状态，采用时序 4D 表征对齐；[StereoPatch](https://arxiv.org/abs/2609.15509)在共享图像 patch 网格上把经注册的米制深度与 RGB 特征对应；[Dynin-Robotics](https://arxiv.org/abs/2609.13053)把语言、视觉观测、目标和动作表示为离散 token，在共享轨迹模型中学习动作及下一观测预测。这些工作说明“都有传感器流”与“可对齐用于动作预测”是两件事。

![RGB、深度和机器人状态经时钟映射与坐标标定形成历史窗口，随后核验融合误差和闭环效果。](/images/docs/multimodal-spatiotemporal-alignment-flow.svg)

## 输入、输出与处理链

输入是 RGB、深度、本体状态、力觉等原始流及各自时间源；输出是以动作实际生效事件为锚点、带标定变换和缺失掩码的对齐窗口。融合前要保留每个传感器的采样时刻，避免后处理抹掉真实延迟。

1. 列出各传感器采样率、时间源和坐标系，记录硬件同步或软件时钟映射。
2. 校准相机、深度、末端和机器人基座的内外参；保留原始测量和变换版本。
3. 把观测与动作按事件时间配对，显式记录插值、重采样和延迟补偿。
4. 输出模态可用性掩码与误差，让训练器能够避开错配区间。

### 时间与空间对齐

推荐以动作实际生效时刻为锚点，保留相机曝光、深度采样、状态读取和策略推理的原始时间戳。RGB-depth 像素对应要用已注册深度和相机模型核验，不能只按数组位置拼接。历史窗口也需固定长度和采样规则，避免训练与部署看到不同的时间跨度。

![多模态契约记录采样接收生效时刻、相机与机器人坐标变换，以及插值缺失掩码。](/images/docs/multimodal-spatiotemporal-alignment-contract.svg)

## 最小数据字段

| 字段组 | 建议字段 | 用途 |
| --- | --- | --- |
| 身份 | `episode_id、sensor_id、sample_id` | 连接原始流与派生特征 |
| 时钟 | `clock_id、t_capture、t_receive、t_apply` | 量化延迟及因果顺序 |
| 标定 | `intrinsics、extrinsics、frame_id、calib_version` | 复现空间配准 |
| 观测 | `rgb、depth、proprioception、force` | 保存原始多模态值 |
| 处理 | `resample_rule、interpolation_mask、history_window` | 说明派生输入如何形成 |
| 质量 | `sync_residual、registration_error、valid_mask` | 筛除错配样本 |

同一数组下标不代表同一物理时刻或同一空间位置；派生输入必须保留原始时间戳、标定版本和重采样规则。

![对齐评估分别量化设备时钟残差、RGB 深度空间配准误差和错配对控制任务的影响。](/images/docs/multimodal-spatiotemporal-alignment-evaluation.svg)

## 质量控制与评估

多模态质量的首要风险是时钟漂移、像素错配和训练部署模态不一致。验证应先检查时间及空间残差，再看融合是否改善闭环控制：

- 检查时钟漂移、乱序、丢帧、重采样比例和跨传感器残差。
- 在深度边界、遮挡、反光和运动物体上核验 RGB-depth 配准，分区报告误差。
- 以任务关键状态检查历史窗口是否真能区分当前相似但演化不同的状态。
- 对缺失模态保留掩码与原因，禁止用零值静默伪装有效传感器数据。

| 评估层 | 指标或证据 | 判读要点 |
| --- | --- | --- |
| 时间 | 时钟残差与端到端延迟 | 按设备/事件分层 |
| 空间 | 重投影与 RGB-D 配准 | 按遮挡/距离分层 |
| 任务 | 闭环成功与错配消融 | 与单模态基线比较 |

## 数据集使用边界

对齐数据可用于融合编码器、4D 状态表征和动作条件模型。离线时间戳匹配不能保证部署时仍有相同延迟；上线后应重新测量时钟与处理链。若某模态仅在训练时提供，例如外部真值，其标签必须标成训练专用，不能作为部署策略的默认输入。

## 本页术语

本页使用的关键术语：

- **时空对齐**：建立跨传感器事件的共同时间和坐标关系。
- **空间配准**：把不同传感器测量转换到同一几何参照的过程。
- **观测混叠**：不同真实状态在当前观测上看起来相似，需借助历史或其他模态区分。

## 本月相关论文

以下为该主题在 2026-08-27 至 2026-09-27 采集批次中的全部主归类论文；每条均链接原始 arXiv 页面。

- [Temporal Forcing: 4D Representation Alignment for Vision-Language-Action Models](https://arxiv.org/abs/2608.30643)（2608.30643）
- [Development of a Humanoid Robot Prototype for Multimodal Human-Robot Interaction](https://arxiv.org/abs/2609.05361)（2609.05361）
- [Dynin-Robotics: Omnimodal Unified Diffusion Vision-Language-Action Model](https://arxiv.org/abs/2609.13053)（2609.13053）
- [StereoPatch: Patch-Aligned RGB-Depth Fusion for Spatial Perception in Robot Manipulation](https://arxiv.org/abs/2609.15509)（2609.15509）
