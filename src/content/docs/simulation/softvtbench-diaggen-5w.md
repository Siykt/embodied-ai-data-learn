---
title: SoftVTBench 与 DiagGen：资产生成与操作评价
description: 从糕点制作和装盒验收出发，用五个问题理解软体仿真资产、视觉触觉数据与机器人操作评价。
---

想象一家糕点店准备让机器人装盒。店里先要准备不同软硬程度的糕点供它练习，再检查它能不能拿稳、放准，以及有没有把糕点压坏。只看糕点最后进没进盒子，会漏掉夹取过程中的问题。

**DiagGen 对应“准备可供练习的物体”，SoftVTBench 对应“组织练习并记录、评价表现”。** 前者从图片生成虚拟物体，后者让机器人在虚拟任务里操作物体。这个类比解释的是分工：图片无法直接告诉我们真实糕点的硬度，两套项目也还需要资产适配才能连接。

![糕点装盒类比：DiagGen准备带形状和材料假设的虚拟物体，SoftVTBench组织抓取练习并检查过程和结果](/images/docs/simulation-project-roles.svg)

本页依据 2026 年 10 月 13 日核对的论文、源码和公开数据清单整理。两项目的完整流程尚未在本机运行。可直接操作的既有实验仍是 [MuJoCo 旋转关节案例](/simulation/mujoco-data-walkthrough/)。

## Why｜为什么需要这两个项目？

### 先解决“拿什么练习”

一张玩具照片能展示颜色和轮廓。要让机器人抓它，还需要物体的三维形状、内部结构和受力后的变化。比如带挂环的软玩具：主体会被压缩，挂环较硬，连接处还要承受拉力。

DiagGen 尝试从图片生成这些信息，再通过仿真交互检查问题。这样，生成物体时就能发现“连接处一拉就分离”或“软部件几乎不变形”等现象，并返回前面的步骤修正。

### 再解决“怎样才算操作合格”

同一块糕点可能被稳稳放入篮子，也可能被压扁后放进去。SoftVTBench 分别报告任务是否完成、形变是否超过设定范围，让我们能看到两种结果之间的差别。

对数据工作而言，前者影响**样本里的物体是否可信**，后者影响**成功标签是否充分描述操作质量**。这两个问题会直接影响模型学到什么。

## What｜它们分别是什么，交付什么？

### DiagGen：一份可交互的物体资产

可以把资产理解为虚拟物体的“形状、材料与使用说明”。DiagGen 的输入是一张物体图片；输出包括三维网格、部件材料参数、纹理和诊断记录。

为了计算软体形变，流程把物体内部划分为许多小四面体，再给它们分配材料参数。这种把整体拆成小单元计算的方法叫 **FEM（有限元方法）**。

这里先记住三项信息：**哪里是物体、各部分有多容易变形、计算后表现怎样。** 文件名称和数组形状放在文末的技术参考中。

材料数值来自图片语义和预设候选值。例如代码中“柔性橡胶”的候选刚度为 500 万 Pa。描述这类刚度的参数叫**杨氏模量**；在其他条件相同时，数值越大通常越不容易弹性变形。这是生成假设，需要实物测量才能进一步校准。

### SoftVTBench：一次操作的完整记录与评分

SoftVTBench 提供机器人操作任务、演示数据以及策略训练和评测代码。它把任务分成四组，分别改变物体或空间关系，并设置刚体与软体对照。刚体近似保持形状，软体允许内部发生形变。

当前发布清单里有这样一条真实元数据：

> **任务：**把白色旋纹糕点拿起来，放进篮子。
>
> **记录：**Object-Soft 的 task0、demo_0，共 132 个采样步。
>
> **结果标记：**任务成功。

项目标称每秒记录 20 次，132 步对应约 6.6 秒的数据规模。这里核对的是发布清单，未重跑这次操作；“任务成功”标记本身也没有说明形变是否合格。

![一条糕点抓取记录分为机器人可以看到的输入、发出的动作与执行结果，以及仅供评价使用的内部形变信息](/images/docs/simulation-project-data.svg)

一条记录包含相机画面、左右手指的触觉、机器人位置和动作，以及评价所需的形变信息。这里的触觉来自模拟的 GelSight Mini：它用图像和标记点位置表达接触表面的变化。

## Who｜谁生成物体，谁决定动作，谁评分？

这几个名字分别负责不同工作：

| 角色 | 在例子中做的事 |
| --- | --- |
| DiagGen 的代理与生成工具 | 分割图片中的部件，生成形状，提出材料候选参数 |
| Genesis 仿真器 | 在诊断时计算物体受力后的运动与形变 |
| Isaac Sim 与 Isaac Lab | 为 SoftVTBench 提供机器人场景、物理计算和任务组织 |
| 机器人策略 | 根据画面、触觉、当前状态和指令，决定下一步动作 |
| 记录器与评价器 | 保存过程，再依据任务和形变规则给出结果 |

**策略**可以理解为机器人在练习中使用的“动作选择方法”。SoftVTBench 发布的训练路径使用 π0.5 模型，让它学习视觉、语言和动作之间的关系。

策略只能使用约定的输入。物体内部节点的精确形变属于**特权状态**：仿真器可以读取，真实机器人通常无法直接获得。它可以用于评分，但不能不加区分地塞进策略输入，否则就像考试时把答案一起发给考生。

## Where｜它们处于哪条数据链路，数据去哪里？

### DiagGen：从图片到资产，再用交互检查

流程先清理图片、分割部件、生成三维几何，随后配置材料并构建体积网格。诊断阶段选择物体上的区域施加载荷，观察响应；发现问题后，返回分割、材料或网格步骤重做。

![从物体图片生成资产，经诊断修正，再通过尚需开发的适配环节进入任务、记录和评测流程](/images/docs/simulation-project-bridge.svg)

它的输出可以作为后续仿真的资产来源。要放入 SoftVTBench，还需转换网格和场景格式、统一尺寸与坐标、适配材料、定义任务，并重新确定这个物体允许的形变范围。这一步会影响全部下游记录。

### SoftVTBench：从记录到训练，再回到任务测试

可以顺着一行数据理解训练：机器人先看到当前画面和状态，结合触觉历史，再学习下一步该把夹爪移到哪里。

公开 Object-Soft 触觉训练脚本把动作标签构造成：**下一时刻的末端位置、朝向和单指开度**，一共 7 个数。原始记录中的接触力没有成为这条路径的动作标签。因此，要分别确认“采集了哪些字段”和“训练实际使用哪些字段”。

评价形变时，先去除物体整体的平移和旋转，再看内部节点相对于参考形状变了多少。把糕点搬远与把它压扁，因而能够分开计算。整段过程的最大形变再与该物体的阈值比较。

论文把“完成任务、全程不掉落且峰值形变不超过阈值”的尝试记为 **Safety Success（安全成功）**，这类尝试占全部测试次数的比例就是安全成功率。它衡量这套仿真规则下的通过情况，不能证明真实物体不会损坏；公开评分代码与这份文字定义还有差异，见下一节。

作者在 Object-Soft 上报告：纯视觉策略的任务成功率为 70.4%，安全成功率为 21.4%；视觉加触觉策略分别为 71.8% 和 35.6%。这些是论文报告值，未经本地复现；两组还采用不同的夹爪控制方式，不能把差值全部归因于触觉。

## When｜什么时候选择它们，入门先做到哪一步？

**想理解多模态数据与评价，先读 SoftVTBench 的一条演示。** 把画面、夹爪开度和形变曲线放在同一时间轴上，确认机器人做了什么、结果标签表示什么。

**想研究仿真物体怎样制作，再看 DiagGen 的单个资产。** 从原图追到部件、材料假设和诊断结果，检查每个参数怎样进入模拟器。生成完成以后，仍要判断它适合哪些任务。

在当前 Apple Silicon Mac 上，可以先解析数据、查看视频和资产。完整 SoftVTBench 仿真需要兼容的 NVIDIA 环境；当前 DiagGen 的几何生成、诊断和纹理路径也依赖 CUDA。SoftVTBench 发布训练配置默认使用 8 张 GPU，单卡配置尚未验证；该默认值不是已证明的最低硬件要求。

### 准备复现时，先核对发布版本

源码和数据已经出现一些需要处理的差异：

- **数据数量：**当前四份清单各有 1,000 条演示，共 4,000 条；GitHub README 仍写 1,628 条，Object-Soft 触觉训练脚本还要求 500 条。直接使用当前数据会触发该数量检查。
- **资产位置：**当前数据集没有闭环仿真所需的 USD 场景资产，相关文件在 archive 数据仓库。
- **评分规则：**SoftVTBench 文字定义包含全程不掉落，但已检查的公开评分实现仅判断任务成功和峰值形变，运行器还关闭了掉落终止。复现时需要明确采用哪份规则。
- **启动含义：**DiagGen 的示例命令只初始化运行记录，完整生成还需要代理调度各阶段，并准备模型权重与多个环境。
- **材料生效范围：**DiagGen 推断了摩擦系数，但当前诊断路径未传递逐部件推断摩擦；该路径使用默认线性弹性材料模型。需要核对实际模拟的参数与行为。

这些差异说明，实验需要一起记录代码版本、数据版本、资产版本和评分规则。适合学习的下一步是一个可解释的小样本，而后再扩大采集或训练规模。

## 技术参考与来源

<details>
<summary>查看文件、数组和训练转换的具体约定</summary>

DiagGen 的 `final_mesh.mesh` 保存体积网格；`heterogeneous_params.npz` 保存部件与四面体的材料数组；`inferred_params.json` 保存材料假设。`volume_topology.json` 与 `metric_mesh_scaling.json` 分别说明体积结构与尺度，`final_export_manifest.json` 列出产物及来源。

SoftVTBench 数据卡描述原始 `actions` 为 `(T,13)`，包含末端位姿、夹爪标量和左右指力。`gripper_marker_motion` 为 `(T,2,2,99,2)`：时间、两指、参考/当前、99 个点、xy 坐标。这里保存的是坐标，不能直接当作已相减的位移。

公开触觉训练路径将每指最近 8 帧拼成一张触觉图，并将动作改为 `state[t+1]`，最后一帧重复末状态。训练输入和动作单位、历史窗口应与在线运行保持一致。

</details>

查阅基线：SoftVTBench `58056111f01e05bf1a4ae1dee75db4e3d9e7c5be`；DiagGen `3d2d3779613b9253109f63e1ff345b11c9097b70`；数据集 `fd2793a19310b5ba4ac6518f9a17ff43d56f6651`。发布状态以这些版本为准。

- [SoftVTBench 仓库](https://github.com/TuojingAI/SoftVTBench/tree/58056111f01e05bf1a4ae1dee75db4e3d9e7c5be)、[论文](https://arxiv.org/abs/2607.04234)、[固定版本数据说明](https://huggingface.co/datasets/Arthur12137/SoftVTBench/blob/fd2793a19310b5ba4ac6518f9a17ff43d56f6651/README.md)、[Object-Soft 清单](https://huggingface.co/datasets/Arthur12137/SoftVTBench/blob/fd2793a19310b5ba4ac6518f9a17ff43d56f6651/object-soft/manifest.jsonl)、[归档资产](https://huggingface.co/datasets/Arthur12137/SoftVTBench-archive)。
- SoftVTBench：[数据数量检查与动作转换](https://github.com/TuojingAI/SoftVTBench/blob/58056111f01e05bf1a4ae1dee75db4e3d9e7c5be/openpi/scripts/train_object_soft_pi05_tactile_targetnext_7d_a800_20260626.sh#L71-L166)、[评分实现](https://github.com/TuojingAI/SoftVTBench/blob/58056111f01e05bf1a4ae1dee75db4e3d9e7c5be/experiments/common/softvtbench_metrics.py#L82-L91)、[掉落终止配置](https://github.com/TuojingAI/SoftVTBench/blob/58056111f01e05bf1a4ae1dee75db4e3d9e7c5be/SoftVTBench/benchmarks/common/closedloop_policy_inference.py#L89-L94)、[夹爪模式](https://github.com/TuojingAI/SoftVTBench/blob/58056111f01e05bf1a4ae1dee75db4e3d9e7c5be/openpi/scripts/train_softvtbench.sh#L30-L34)。
- [DiagGen 仓库与启动说明](https://github.com/diaggen/diaggen/tree/3d2d3779613b9253109f63e1ff345b11c9097b70)、[论文](https://arxiv.org/abs/2609.23103)、[材料候选表](https://github.com/diaggen/diaggen/blob/3d2d3779613b9253109f63e1ff345b11c9097b70/hag4r/tools/material_inference.py#L1081-L1090)、[导出参数](https://github.com/diaggen/diaggen/blob/3d2d3779613b9253109f63e1ff345b11c9097b70/hag4r/tools/volumetric_meshing.py#L1228-L1251)、[诊断材料配置](https://github.com/diaggen/diaggen/blob/3d2d3779613b9253109f63e1ff345b11c9097b70/hag4r/tools/genesis/config.py#L563-L600)。
