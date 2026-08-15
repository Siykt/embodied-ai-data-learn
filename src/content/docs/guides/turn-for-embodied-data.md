---
title: TURN 与具身数据实时采集
description: 从 WebRTC 连接、远程遥操作和数据质量角度说明 TURN 的作用、边界与记录要求。
---

TURN（Traversal Using Relays around NAT）是 WebRTC 体系里的中继服务。当控制端和机器人端处于不同局域网、运营商网络或严格防火墙之后，双方无法直接建立媒体或数据连接时，TURN 服务器代替其中一方接收并转发数据。

它首先是**连接基础设施**，不是新的传感器格式、数据集 schema 或标注协议。放在具身数据管线里看，TURN 解决的是“采集端发出的画面、状态和控制消息能否及时到达机器人端”，而不是“这些消息代表什么”。

![浏览器与机器人无法直连时通过 TURN 中继的 WebRTC 连接路径](/images/docs/turn-connection-path.svg)

## TURN 与 STUN、ICE 的关系

这几个词经常一起出现，但职责不同：

| 组件 | 作用 | 对具身采集的意义 |
| --- | --- | --- |
| NAT | 把局域网地址转换为公网可见地址 | 让控制端和设备端无法天然互相访问 |
| STUN | 帮设备发现自己的公网映射地址 | 先尝试低成本、低延迟的端到端连接 |
| TURN | 提供公网可访问的中继地址并转发流量 | 直连失败时保住远程视频、控制和状态通道 |
| ICE | 收集并测试多种连接候选路径 | 在直连与中继之间自动选择可用路径 |

理想情况下，ICE 会优先选择端到端路径；只有直连不可用时才退回 TURN。TURN 因此是可靠性兜底，不代表所有流量都必须经过中继。

## 它在具身数据中的角色

### 1. 支撑远程采集与遥操作

远程操作者可能在办公室，机器人在实验室或另一处场地。WebRTC 可以同时承载相机视频、机器人状态、控制指令和数据通道；TURN 让这条链路不依赖双方都拥有公网入站地址。

典型过程是：

1. 控制端和机器人端通过信令交换连接信息；
2. ICE 先测试本地、STUN 发现的公网地址和 TURN 候选；
3. 直连失败时，两端向 TURN 建立出站连接；
4. 视频、音频、状态或控制消息经过 TURN 转发；
5. 采集服务将收到的多路流按时间戳写入原始记录，并形成 episode。

TURN 只负责第 3、4 步附近的网络可达性。它不负责传感器时间同步、相机标定、动作定义或任务成功判定。

### 2. 影响数据质量，而不是直接提供数据语义

中继会增加网络路径和服务负载，可能带来更高的往返时延（RTT）、抖动、丢包、重连和视频降码率。对具身数据，这些网络现象可能变成：

- 视频帧到达延迟，导致观测与控制动作错位；
- 控制消息排队或丢失，使执行轨迹出现异常；
- 断连后出现不连续时间段，episode 边界需要重新判断；
- 编码器降级后画质下降，影响视觉标注和模型输入；
- 服务器过载或地区路由变化，使同一采集流程质量不稳定。

所以不能只保存“TURN 连接成功”。应把连接路径和质量指标作为采集 session 的质量上下文，与原始传感器数据一起留存。

![TURN 连接事件如何进入具身数据质检与数据血缘](/images/docs/turn-data-lineage.svg)

## 建议记录的字段

TURN 本身的日志通常不是训练样本，但其中一部分应进入可追溯的 session 或 episode 元数据：

```text
connection
  protocol: webrtc
  selected_candidate_type: host | srflx | relay
  turn_region, turn_provider, allocation_id
  started_at, ended_at, reconnect_count
quality
  rtt_ms, jitter_ms, packet_loss_rate
  frames_sent, frames_received, frames_dropped
  bitrate_kbps, resolution, codec
alignment
  capture_timestamp_domain, receive_timestamp_domain
  estimated_transport_delay_ms, max_allowed_skew_ms
episode
  interrupted, interruption_intervals, quality_flags
```

`relay` 表示选择了 TURN 中继候选；它不等于数据一定损坏，但应触发更细的质量分析。采集端应优先保留设备产生的采集时间戳，接收时间只能作为网络观测，不能直接替代传感器时间。

## 采集设计与质量控制

### 传输层与记录层分离

尽量在设备端或靠近传感器的位置写入原始流，远程端再通过网络同步副本。这样短暂断连不会把“网络没收到”误写成“传感器没有产生”。每份派生数据都要标记来源：设备原始记录、接收端录制、还是断连后的补传结果。

### 区分不同通道的容错策略

视频通常可以接受有限丢帧并依靠时间戳标记缺口；机器人状态适合保留序号、采集时间和接收时间；控制消息则需要明确是否可靠传输、是否有序、是否过期即丢弃。不能用同一套重试策略覆盖画面和动作。

### 把网络事件纳入 episode 边界

若断连期间无法确认机器人动作或观测，应该标记不确定区间，而不是静默拼接前后数据。后续可选择裁剪该区间、作为失败样本，或单独评估网络鲁棒性。边界规则必须版本化。

### 评估时按连接路径分桶

比较数据集或模型时，建议分别统计 `host`、`srflx` 和 `relay` 路径，以及不同 RTT、丢包和重连次数的子集。否则模型性能变化可能被网络质量差异掩盖。

## 安全、成本与合规

TURN 能看到自己转发的加密 WebRTC 包的流量元数据，但通常不能直接解码 DTLS-SRTP 保护的媒体内容。实际部署仍应考虑：

- 使用短时凭证和最小权限，限制谁可以申请 relay allocation；
- 限制带宽、并发数、IP 范围和会话时长，防止中继被滥用；
- 记录必要的审计信息，不把原始视频或机器人控制日志无限期保存在 TURN 主机；
- 对人脸、家庭环境、地理位置和语音等内容按数据集隐私策略处理；
- 预估中继带宽成本，尤其是多路高分辨率视频和长时间采集。

## 结论

TURN 在具身数据中的核心角色可以概括为：**远程数据采集和遥操作的网络可达性兜底层**。它让观测、状态和控制流在复杂网络中保持可用，但不会自动保证时间对齐、空间标定、动作标签或数据质量。建设可靠的具身数据集时，应把 TURN 作为连接层纳入采集审计，把 RTT、丢包、重连和中继路径转化为质量字段，并据此决定 episode 是否可训练、可评估。

## 资料

- [RFC 5766: Traversal Using Relays around NAT (TURN)](https://www.rfc-editor.org/rfc/rfc5766)
- [RFC 8445: Interactive Connectivity Establishment (ICE)](https://www.rfc-editor.org/rfc/rfc8445)
- [WebRTC 1.0: Real-Time Communication Between Browsers](https://www.w3.org/TR/webrtc/)
