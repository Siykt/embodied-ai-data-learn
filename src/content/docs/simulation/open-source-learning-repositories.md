---
title: 仿真开源学习仓库与实践路线
description: 按学习目标和机器条件选择仿真仓库，从第一条可回读轨迹进入相机与并行任务，并查阅本机实验和兼容性记录。
---

学习做实验时，你通常需要三样东西：教材解释原理，器材让实验发生，练习题告诉你这次要验证什么。拿到器材说明书，不等于拿到一套课程；照着做完练习，也还需要留下可检查的实验记录。

仿真学习仓库也有类似分工：有的提供引擎和模型，有的按章节讲解，有的提供完整任务。**同一仓库可能同时包含几种内容，仓库中的示例也不自动等于可用于训练的数据集**。

读完本页，你将能按自己的机器和学习目标选一个起点，并知道第一份练习产物应保存什么、怎样验收。

## Why｜为什么从一段可回读的数据开始学习

**先做出一段自己能解释的数据，比同时安装多个项目更容易确定下一步学什么。** 如果目标是理解具身数据，可以先做一个很小的实验：让指针转动，记录指令、位置和速度，再重新打开保存的文件。这样能直接回答“数字在哪里产生”“动作影响哪一段运动”“文件里的时间与画面怎样对应”。

之后再增加相机、机械臂任务和多个环境，就能逐步检查模型、控制、时间和保存环节。例如，增加相机后，先确认画面中的指针位置与同一时刻的角度记录一致，再继续做更复杂的任务。

**可以先看已运行的[MuJoCo 旋转关节实验](/simulation/mujoco-data-walkthrough/)。** 页面能拖动时间轴，对照画面和原始数值，并下载实际记录的 CSV、NPZ、视频与字段说明。先看到一份完整产物，再读下面的仓库入口，会更容易理解每个项目能帮你补哪一部分。

![学习路线从单模型和固定动作开始，经过轨迹回读与传感器对齐，再进入并行任务和独立评估](/images/docs/simulation-learning-route.svg)

本页资料核查日期为 **2026-10-09**。其中 MuJoCo 有下文所列的 Apple Silicon 实测；Isaac Lab 部分依据仓库与文档整理，**尚未在本机完成部署验证**。默认分支会变化，运行时应固定提交或发布版本。

## What｜这些仓库是什么，分别提供什么

**想看清一条动作与状态记录，先从 MuJoCo 小模型开始；想组织视觉任务与并行采集，再看 Isaac Lab。** 下表各列出一个阅读入口和一个具体目标，第一次只需选一行。

### MuJoCo 学习仓库

MuJoCo 是计算物体运动的物理引擎。它使用 [MJCF](/reference/terms/#mjcf) 文件描述机器人、场景、执行器和传感器。学习时先分清模型设置与每时刻的读数；接口名称见[练习附录](#用-albusgive-的第一课建立数据循环)。

| 项目 | 先读哪里 | 第一轮学习的具体目标 |
| --- | --- | --- |
| [Albusgive/mujoco_learning](https://github.com/Albusgive/mujoco_learning) | 中文[课程目录](https://github.com/Albusgive/mujoco_learning/blob/main/directory.md)与 [Python 第一课](https://github.com/Albusgive/mujoco_learning/tree/main/Python/Chapter1-view%26step) | 用指针模型找出模型加载、动作输入、物理推进和状态读取；后续再学传感器、渲染与射线测距 |
| [LitchiCheng/mujoco-learning](https://github.com/LitchiCheng/mujoco-learning) | [control_joint_pos.py](https://github.com/LitchiCheng/mujoco-learning/blob/main/control_joint_pos.py)，再看相机与抓取实例 | 把机械臂状态和图像一起保存，解释相机、标定与采样时间 |
| [google-deepmind/mujoco](https://github.com/google-deepmind/mujoco) | 官方 [Python tutorial.ipynb](https://github.com/google-deepmind/mujoco/blob/main/python/tutorial.ipynb) | 核对模型、状态、步进、接触、传感器与渲染接口的准确含义 |
| [google-deepmind/dm_control](https://github.com/google-deepmind/dm_control) | 官方 [tutorial.ipynb](https://github.com/google-deepmind/dm_control/blob/main/tutorial.ipynb)与 [viewer 示例](https://github.com/google-deepmind/dm_control/blob/main/dm_control/viewer/README.md) | 从单模型进入现成任务，理解观测、奖励和任务结束规则 |

选定示例后，再查[练习入口与固定版本](#技术附录练习入口与固定版本)，按这个示例需要的依赖准备环境。

### Isaac Lab 学习仓库

当你已经能解释一条轨迹，再考虑多个任务一起运行。[Isaac Lab](/reference/terms/#isaac-lab) 组织机器人、场景、动作和任务规则，可以把每个环境看作一份独立练习。从一次重置到结束的完整过程叫 [episode](/reference/terms/#episode)，多次练习需要不同的 ID。

| 项目 | 先读哪里 | 第一轮学习的具体目标 |
| --- | --- | --- |
| [isaac-sim/IsaacLab](https://github.com/isaac-sim/IsaacLab) | 对应版本的 [Quickstart](https://isaac-sim.github.io/IsaacLab/develop/source/setup/quickstart.html)，再看 `scripts/tutorials` | 找到机器人、相机、动作和重置位置，确认多个环境如何分开记录 |
| [isaac-sim/IsaacLabTutorial](https://github.com/isaac-sim/IsaacLabTutorial) | SO101 机械臂把小瓶放进架子的实作 | 对比使用完整状态和使用腕部图像的策略，理解教师动作标签和独立评估 |
| [Lab-of-AI-and-Robotics/IsaacLab-Tutorial](https://github.com/Lab-of-AI-and-Robotics/IsaacLab-Tutorial) | SKKU 社区十章教程，从 Unitree Go2 到 H1 | 检查更换机器人、动作、奖励或地形课程后，采集的数据怎样变化 |

这些材料需要的版本可能不同。选定一项后，按它自己的说明准备环境；具体差别见[Isaac Lab 的版本路线](#isaac-lab-的版本路线)。

![并行环境可以在不同时间结束和重置，记录器应按每次 episode 分开保存轨迹](/images/docs/simulation-parallel-recorder.svg)

## Who｜谁维护示例，谁对采集的数据负责

**教程作者提供示例，你的采集项目负责确认最终记录是否能用。** 官方仓库负责提供和说明框架接口，社区教程作者负责各自的课程示例；保存的字段能否用于后续训练和评估，仍需在自己的实验中检查。

例如，教程成功让机械臂动起来后，还需要有人确定动作单位、记录时间、成功条件和数据划分。可以把工作分为三项：运行者固定代码与环境，记录者说明并保存数据，验收者重新读取样本并检查质量。在个人学习中，这三项可以由同一个人完成。

复用和发布时，还要分别核对代码、教程图文与模型资产的许可；具体项目的声明保留在[许可与数据使用边界](#许可与数据使用边界)。

## Where｜在哪里运行，实验文件保存在哪里

<span id="版本兼容与运行环境"></span>

**Apple Silicon 可以从本页已实测的 MuJoCo 小实验开始；Isaac Lab 需要另行准备受支持的运行环境。** 先决定运行哪个示例，再按该示例的安装说明核对机器条件；具体版本与平台差别见[运行环境附录](#技术附录版本与运行环境)。

### Apple Silicon 本机实践记录

本页已有一个旋转指针的本地实验，文件保存在 `~/Documents/work/mujoco-learning-lab`。它用一个旋转关节、两个执行器和六个传感器，生成八秒的状态、动作和画面记录。环境版本、启动入口和输出位置见[本机环境与操作入口](#本机环境与操作入口)。

这次实验中，CPU 物理步进、离屏渲染和浏览器查看器成功，原生窗口未成功；**Isaac Lab 尚未在本机完成部署验证**。记录程序使用固定控制演示，浏览器里的手动操作不会自动写入这份记录。

![模型和配置经过控制步进产生状态、传感器与图像，再按时间对应关系保存为可回读的实验记录](/images/docs/simulation-local-data-flow.svg)

完整错误位置、八秒输出和回读结果保留在[本机实验附录](#技术附录本机实验结果与时序约定)。它们描述的是本次固定环境中的结果。

## When｜何时选择一个仓库，何时进入下一阶段

<span id="如何选择第一个项目"></span>

**能重新读取并解释上一阶段的产物，就可以进入下一阶段。** 如果使用 Apple Silicon 且刚开始学习，可选 Albusgive 第一课配合官方 MuJoCo 文档；已能记录状态后，再用 LitchiCheng 增加机械臂和相机。需要标准任务时读 dm_control；有匹配的 NVIDIA Linux / Windows 环境，并且已经能解释单条轨迹时，再进入 Isaac Lab 并行任务。

<span id="分阶段实践与验收"></span>

进度应以能交付的记录判断。每一阶段先完成一个小样例：

1. **让模型动起来**：保存初态和固定动作，解释指针怎样运动。
2. **保存并重新读取**：把时间、位置、速度和指令对应起来。
3. **加入图像**：确认画面里的运动与状态记录发生在同一时刻。
4. **加入任务**：同时收集成功与失败，写明每次为什么结束。
5. **增加并行环境**：让每次任务各自保存完整轨迹，再做独立评估。

需要逐项验收时，可展开[分阶段产物与检查表](#技术附录分阶段产物与检查表)。

“回读验收”就是重新加载自己保存的数据，检查字段形状、时间、动作含义和关键状态。开始时几十步就足够发现问题，不必先训练出高成功率策略。重复固定实验时，跨引擎版本、求解器或硬件可能出现数值差异，应记录误差，不能默认完全一致。

完整字段要求见[MuJoCo 与具身数据](/simulation/mujoco-embodied-data/)、[Isaac Lab 与具身数据](/simulation/isaac-lab-embodied-data/)及[仿真数据契约](/simulation/simulators-embodied-data/#通用数据契约)。只有视频或训练日志的产物，应称为演示或运行记录；要交给下游训练，还需补齐观测、动作、时间、边界与质量说明。

## 技术附录：许可与使用范围

### 许可与数据使用边界

<details>
<summary>复用或发布时：查看各仓库的代码、文档与资产许可</summary>

复用前应区分代码、文档和模型资产的许可。以下是核查时的主要声明，具体使用仍以对应文件和目录为准：

| 项目 | 主要许可 |
| --- | --- |
| Albusgive | [MIT](https://github.com/Albusgive/mujoco_learning/blob/main/LICENSE) |
| LitchiCheng | [源码 MIT](https://github.com/LitchiCheng/mujoco-learning/blob/main/LICENSE)；README 声明文档为 CC BY 4.0 |
| MuJoCo 官方仓库 | [源码 Apache-2.0](https://github.com/google-deepmind/mujoco/blob/main/LICENSE)；`doc` 目录文档、图像和视频为 CC BY 4.0 |
| dm_control | [Apache-2.0](https://github.com/google-deepmind/dm_control/blob/main/LICENSE) |
| Isaac Lab | 主框架 BSD-3-Clause；Mimic 部分 Apache-2.0，按目录核对 |
| IsaacLabTutorial | [Apache-2.0](https://github.com/isaac-sim/IsaacLabTutorial/blob/main/LICENSE) |
| SKKU IsaacLab-Tutorial | [Apache-2.0](https://github.com/Lab-of-AI-and-Robotics/IsaacLab-Tutorial/blob/main/LICENSE)，部分代码沿用上游 BSD-3-Clause |

仓库根目录的许可通常不能直接覆盖外部网格、纹理、机器人资产或数据。固定模型时保留来源与许可；分发代码、引用教程图文或发布数据时，分别核对相应条款。Isaac Lab 的开源许可也不自动替代 Isaac Sim 和第三方资产的条款。

</details>

## 技术附录：版本与运行环境

### Apple Silicon 的本地起点

<details>
<summary>安装 MuJoCo 时：核对 Apple Silicon 与 Notebook 的环境差别</summary>

核查时 [MuJoCo 3.15.0 的 PyPI 文件](https://pypi.org/project/mujoco/3.15.0/#files)包含 macOS arm64 原生包，要求 Python ≥3.10。普通物理仿真可以使用 CPU，不要求 CUDA。模型计算、离屏渲染、原生窗口和浏览器查看器是不同能力，需要分别验证。

官方 MuJoCo 和 dm_control Notebook 含有针对 Colab、NVIDIA 驱动与 [EGL](/reference/terms/#egl) 的安装单元；其中 EGL 用于建立图形上下文，该处设置面向云端 Linux 渲染环境。Mac 应按本机支持调整安装与渲染步骤。dm_control 还多一层环境组织和依赖，可参照其 README 的 macOS Homebrew Python / GLFW 指引。

LitchiCheng README 的完整安装主要面向 Ubuntu / WSL2。先阅读单例导入项和模型路径，再决定本机需要安装什么。

</details>

### Isaac Lab 的版本路线

<details>
<summary>安装 Isaac Lab 时：核对后端、操作系统与固定版本</summary>

三项材料的版本并不统一：SO101 实作锁定特定提交，SKKU 按章节分支组织代码。选择一项材料后，应先按它自己的环境说明运行。

依据 2026-10-09 的核查，Isaac Lab `develop` 使用 3.0 路线，包含完整 Isaac Sim 工作流，以及新的 [Kit-less](/reference/terms/#kit-less) 路线。Kit-less 意味着不启动 Isaac Sim 的 Kit 应用运行时，部分工作流可使用 [Newton](/reference/terms/#newton) 物理后端。

这一区别不代表 Apple Silicon 已获官方支持。核查时的[安装指南](https://isaac-sim.github.io/IsaacLab/develop/source/setup/installation/index.html)仍列出 Linux / Windows 路径并使用 CUDA，IsaacLabTutorial 的配置也未包含 macOS。同为 ARM 架构，不能推断操作系统、图形驱动和依赖都兼容。

可在 Mac 上先完成 MuJoCo 的模型和记录练习，再到符合所选版本要求的 NVIDIA Linux / Windows 机器学习 Isaac Lab。远程运行也要核对物理后端和渲染需求：无窗口运行不会自动取消 GPU 和驱动要求。

</details>

## 技术附录：分阶段产物与检查表

<details>
<summary>验收练习时：核对每个阶段的产物和通过条件</summary>

| 阶段 | 推荐材料 | 应交付什么 | 进入下一步前检查什么 |
| --- | --- | --- | --- |
| 1. 单模型与物理步进 | Albusgive 第一课、官方基础接口 | 模型版本、初态和固定动作序列 | 状态数值有限、维度正确，仿真时间按步长推进 |
| 2. 状态与动作记录 | MuJoCo `MjData` 与简单记录器 | 时间、位置、速度、实际控制量、传感器布局及结束原因 | 能重新读取；说明观测在步进前还是后采样 |
| 3. 图像与传感器对齐 | Albusgive 传感器课、LitchiCheng 相机实例 | 图像与状态时间表、相机参数、单位和坐标系 | 图像方向、颜色与深度尺度正确，不同采样率有明确对应规则 |
| 4. 任务与数据质量 | dm_control 或机械臂抓取实例 | 成功和失败 episode、任务条件和质量报告 | 区分自然结束与时间截断，训练评估按场景、物体或初态划分 |
| 5. 并行与视觉策略 | Isaac Lab Quickstart、SO101 实作 | 独立 episode、教师动作标签、随机参数和评估记录 | 环境重置不串轨迹，明确策略真正能看到的信息，评估初态固定 |

</details>

## 技术附录：练习入口与固定版本

下面内容供选定项目后查阅。先按上面的路线确定一项练习，再使用对应的命令和版本。

### 用 Albusgive 的第一课建立数据循环

<details>
<summary>开始第一课时：查看接口、启动方法与固定提交</summary>

可以先把“器材设置”和“每时刻读数”分开理解：在 Python 接口中，前者主要由 `MjModel` 保存，后者由 `MjData` 保存。

Albusgive 第一课只需 `mujoco` 与 Python 标准库，后续相机课会增加 OpenCV 等依赖。LitchiCheng 完整环境还包含训练和运动学工具；应按具体示例核对依赖，不能把整个清单当作 Mac 入门的必要条件。以下按第一课说明源码与启动入口。

[课程目录](https://github.com/Albusgive/mujoco_learning/blob/main/directory.md)先介绍模型，再介绍接口。`Python/Chapter1-view&step/view.py` 加载 `API-MJCF/pointer.xml`，向速度执行器写入控制量，推进物理状态，并同步交互窗口。模型包含关节位置、关节速度、陀螺仪、加速度计等传感器，适合继续练习数据读取。

阅读时按“准备器材 → 给出指令 → 等待运动 → 读取结果”的顺序找代码：模型加载对应准备器材，`ctrl` 保存指令，`mj_step` 推进一小段物理时间，随后读取状态。指令含义由执行器决定：给速度执行器的是目标速度，不能直接当成力矩。保存时还要写明是在步进前还是步进后读数，才能配对动作与下一状态。

示例使用相对于当前工作目录的模型路径，应从章节目录启动。在已安装原生 MuJoCo、且桌面图形环境可用的 macOS 上，对应入口是：

```sh
cd 'mujoco_learning/Python/Chapter1-view&step'
mjpython view.py
```

这里的目录名取决于克隆位置。保留完整仓库结构，因为 `pointer.xml` 还引用了 `MJCF/asset/desert.png`。`mjpython` 是 MuJoCo 在 macOS 上提供的专用启动器；官方要求使用它运行 `launch_passive` 被动查看器，见 [Python 文档](https://mujoco.readthedocs.io/en/stable/python.html#passive-viewer)。它解决启动线程要求，实际显示仍取决于可用的窗口和图形环境。

用于固定参考的 Albusgive 提交为 `8b9354d8559f4951990ece9aeacb2fa5d13d0a86`，该提交日期为 **2026-03-16**。仓库的最近推送时间可能晚于默认分支提交日期，两者不能混写为“代码更新日期”。

</details>

### 从 LitchiCheng 的实例进入相机与采集

<details>
<summary>增加机械臂与相机时：查看示例顺序和依赖</summary>

该项目的价值在于把机械臂状态、相机、标定、传感器和抓取过程放进具体场景。建议先运行依赖较少的单例，再按需要增加模块：

1. `control_joint_pos.py`：读取模型和关节位置，观察关节变化；该文件导入 MuJoCo、NumPy、GLFW 和 SciPy。
2. `get_camera_pic.py`：读取相机图像，核对颜色通道、图像方向、相机配置和采样时刻。
3. `sensordata.py`：按传感器名称及数组地址读取数据，并与状态字段对照；它还依赖项目的可视化模块。
4. `automated_pickup_place_advanced.py`：进一步阅读任务阶段、采集触发、成功条件与记录器。

每份示例都应从源码确认导入项和模型路径。仓库的 `requirements.txt` 包含 `evdev`、`python-xlib`、`triton` 等与特定平台相关的包；当前 `pyproject.toml` 还包括 PyTorch、LeRobot、Pinocchio 与 KDL 工具。完整环境与最小示例的需求有明显差别，不能把整个依赖清单当作 Mac 入门必需项。

</details>

### 官方实作：状态观测如何转向相机观测

<details>
<summary>阅读 SO101 任务时：查看三种任务、教师标签与评估约定</summary>

IsaacLabTutorial 当前使用 SO101 机械臂把小瓶放入架子，提供三种任务：

| 任务 | 策略可见输入 | 学习时应检查的数据 |
| --- | --- | --- |
| `IsaacTutorial-Place-Vial-SO101` | 完整状态 | 关节、物体位姿、动作、奖励、阶段标记和终止条件 |
| `IsaacTutorial-Place-Vial-SO101-Camera-Distillation` | 腕部 RGB 与机器人自身状态 | 学生实际访问的状态、对应图像、教师动作标签及动作裁剪规则 |
| `IsaacTutorial-Place-Vial-SO101-Camera` | 腕部 RGB 与机器人自身状态 | 图像噪声与随机化、训练观测、评估初态及成功率 |

可以先理解成两种学习方式：机器人自己练习并根据得分调整，或跟着老师给出的动作学习。第一种与第三种任务使用 [PPO（近端策略优化）](/reference/terms/#ppo)，根据环境交互和奖励更新策略。第二种使用[策略蒸馏](/reference/terms/#策略蒸馏)，让依赖相机的学生学习能读取完整状态的教师。这里采用 [DAgger](/reference/terms/#dagger) 式收集：学生先执行动作，教师再为学生实际到达的状态提供动作标签，因此要保存标签来自怎样的采样过程。

训练可使用覆盖不同任务阶段的重置样本，评估则从规定的初始状态开始。两种分布应分别说明：能从接近完成的阶段重置并训练，并不直接证明策略可以从完整任务起点成功执行。具体定义以仓库 `reset`、`mdp` 和 `utils/evaluation.py` 为准。

核查时，项目在 [pyproject.toml](https://github.com/isaac-sim/IsaacLabTutorial/blob/main/pyproject.toml) 中固定 Isaac Lab 提交 `f754f2965af9d6aa4f2e18d7d6d3ddf8f8471c69`，并维护自己的依赖锁文件。README 使用的 `presets=` 参数属于这套固定环境；不要直接替换成另一版本文档中的命令参数。

</details>

### 社区章节：从环境定义理解数据分布

<details>
<summary>阅读 SKKU 章节时：查看分支顺序和数据问题</summary>

SKKU 教程的第一章使用内置示例，第二、三章共用 [`chapter2_3`](https://github.com/Lab-of-AI-and-Robotics/IsaacLab-Tutorial/tree/chapter2_3)，后续是 `chapter4` 至 `chapter10`。每章代表一份阶段代码，阅读下一章前应确认所在分支及对应的 Isaac Lab 版本。

可以把章节内容转换为数据问题：更换机器人后关节布局是否改变；自定义动作的单位和范围是什么；奖励修改是否改变成功样本的定义；课程是否改变速度与地形分布；训练与评估是否用了不同的随机化配置。这些问题比仅复现一条训练命令更能帮助建立可用的数据集。

</details>

### 为每次运行保留兼容性记录

<details>
<summary>保存实验时：查看版本、硬件与任务配置清单</summary>

至少记录以下配置，才能解释后续数据差异：

```text
repository_url / commit
python_version / dependency_lock
engine_version / physics_backend / renderer
os / cpu_arch / gpu / driver
model_hash / asset_versions
physics_timestep / control_period / camera_period
seed / reset_configuration / task_configuration
data_schema_version / recorder_version
```

社区旧章节、官方当前开发文档和特定教程的锁定环境可能属于不同版本。学习时先选择一套相互匹配的代码与文档，再有目的地升级；升级后用固定模型、初态和动作做小规模对照，并检查导出字段与任务成功定义。

</details>

## 技术附录：本机实验结果与时序约定

本节保留 2026-10-09 的实际运行证据。它说明这次环境中哪些路径成功、哪些失败，不能据此推断所有版本与机器都会得到同样结果。

### 本机环境与操作入口

<details>
<summary>操作本地实验时：查看软件版本、启动与记录入口</summary>

本次实际实验目录为 `~/Documents/work/mujoco-learning-lab`，运行环境是 **macOS 26.6.2、arm64、Python 3.12.14**，使用 MuJoCo 3.15.0、NumPy 2.5.3、Pillow 12.3.0 与 ImageIO 2.38.1。上游代码保存在 `upstream/`，依赖版本保存在 `requirements.lock.txt`。

实验中的 `pointer.xml` 只有一个旋转关节、两个执行器和六个传感器，适合看清数据关系。在该目录里，可双击以下入口：

| 入口 | 用途 |
| --- | --- |
| `start.command` | 在后台启动浏览器查看器；服务已运行时复用，随后手动打开 `http://127.0.0.1:8765/` |
| `stop.command` | 停止本实验的查看器服务；关闭浏览器标签不会停止后台服务 |
| `record.command` | 在独立模型上重新生成八秒数据样例，写入新的 `outputs/<运行编号>/` |
| `native-viewer.command` | 通过 `mjpython` 启动原版第一课，要求当前会话有可用桌面显示器 |
| `README.md` | 查看操作方法、课程入口、输出说明和环境恢复步骤 |

浏览器中，`vel` 是目标角速度，单位 rad/s；`motor` 是力矩输入，单位 N·m。Pause / Run 用于暂停与继续，拖动和滚轮用于调整视角。**`record.command` 使用固定控制演示，不录制浏览器中的手动操作。** 最新输出位置会写入 `outputs/latest.json`。

</details>

### 查看器与渲染的验证范围

<details>
<summary>查验本机结果时：查看成功路径、窗口失败和显示范围</summary>

| 验证项 | 实际结果 | 对学习与数据工作的含义 |
| --- | --- | --- |
| 模型加载与 CPU 步进 | 成功运行 500 个物理步，对应 1 秒仿真时间，并读取六个传感器 | 可独立验证状态和传感器，无需先打开交互窗口 |
| 原生被动查看器 | 当前会话未成功：GLFW 返回空显示器列表，在 `_glfwGetVideoModeCocoa` 崩溃 | 这是本次会话的窗口显示路径问题；使用 `mjpython` 仍不能保证显示器可用 |
| 离屏 `Renderer` | 成功生成概览视频、概览图和模型相机图 | 可继续进行数据记录与图像质量检查 |
| 官方实验性 `experimental.studio` 浏览器查看器 | 成功显示模型，并通过暂停、缩放及 Controls 面板操作检查；面板初始值为 `motor=0` 与 `vel=1` | 可在浏览器中理解场景和执行器；实验性接口需要固定 MuJoCo 版本 |

[GLFW](/reference/terms/#glfw) 是用于创建窗口、图形上下文和处理输入的库。此次原生窗口失败与离屏渲染成功分别记录，不能相互替代。浏览器查看器服务经检查只监听本机回环地址，本次入口为 `http://127.0.0.1:8765/`；该地址指向访问者自己的电脑，只有相应本地服务运行时可用。[实验性接口](/reference/terms/#实验性接口)意味着它仍可能随版本变化，升级前应重新验证启动和交互行为。

</details>

![本地离屏渲染的 pointer 模型概览：棋盘地面上的圆柱支架、旋转指针和蓝色传感器位置标记](/images/docs/mujoco-local-pointer.png)

图：2026-10-09 本地生成的 `overview.png`，模型来自 [Albusgive/mujoco_learning](https://github.com/Albusgive/mujoco_learning) 的 MIT 许可仓库，固定提交与资产来源见本文及实验 manifest。本图是供人检查场景的外部概览视角；模型传感器相机的输出另存为 `camera.png`。

### 八秒轨迹记录与回读结果

<details>
<summary>查验数据产物时：查看文件、采样数值与回读结果</summary>

在实验目录内，`record_demo.py` 运行一次确定性控制演示。它将力矩执行器设为零，向速度执行器发送频率为 0.4 Hz 的正弦目标速度。记录结果位于：

```text
outputs/20261009T081729.185908Z-ec50f6d9/
  episode.npz       状态、动作、传感器和帧映射数组
  trajectory.csv    便于逐行查看的状态与动作表
  manifest.json     版本、单位、时序、相机、哈希与验证结果
  summary.json      本次记录的简要统计
  overview.mp4      供人检查的外部概览视频
  overview.png      初态的外部概览图
  camera.png        模型 this_camera 的初态图像
```

[NPZ](/reference/terms/#npz) 是 NumPy 用于保存多个命名数组的容器；数组本身不解释单位、动作语义或采样时序，因此需要同时保留 manifest。这里的 [manifest](/reference/terms/#manifest) 是数据说明清单，记录每份产物如何生成和验证。

| 项目 | 本次记录与验证结果 |
| --- | --- |
| 时长与物理推进 | 8 秒；物理步长 0.002 秒，即 500 Hz |
| 控制与状态采样 | 50 Hz；一个动作保持 10 个物理步；401 个状态对应 400 个动作区间 |
| 传感器 | 六个传感器、合计 15 维，分别记录名称、切片、单位和坐标系 |
| 概览视频 | 25 fps、200 帧、640 × 480；全部帧可解码且非空白 |
| 模型相机图 | `this_camera` 在初态的单张 RGB 图，按原始配置输出 1280 × 1080；本例未记录它的连续视频 |
| 数值与回读 | 数值有限，时间与维度检查通过；NPZ 回读与内存数组完全一致；CSV 有 401 行状态、400 行有效动作 |
| 独立重复 | 同一环境、模型和确定性控制下，第二次独立推进的已记录数组最大绝对差为 0 |

这份记录用于验证数据链路，**没有测量任务成功率**。独立重复误差为零只描述本次固定环境中的对照结果，不能推断不同引擎版本、平台、初态或真实机器人上的误差也为零。

</details>

### 状态、动作与传感器如何对齐

<details>
<summary>实现记录器时：查看控制区间、状态和视频帧的对应关系</summary>

记录一个时刻时，需要让位置、速度和传感器描述的是同一瞬间。为此，记录器先调用 `mj_forward`：它根据当前 `qpos`、`qvel` 和控制量重新计算派生量与传感器，但不推进时间，随后再把它们一起保存。

动作与状态使用明确的区间关系：

```text
state[k] -- action[k] 保持在 [t[k], t[k+1]) --> state[k+1]
```

这里有两件不同的事：“刚才用什么指令运动到这里”，以及“接下来准备发什么指令”。`state_ctrl[k]` 记录前者，用于计算当前状态的派生量；`action[k]` 记录后者，作用于下一个时间区间。初态 `state_ctrl[0]` 为零，后续 `state_ctrl[k] = action[k-1]`。所以当前加速度读数对应刚结束区间的控制，不能与尚未施加的新动作混为一列。

CSV 每行保存一个状态及其向外发出的动作，最后一行只有 8 秒时的最终状态，动作列留空。概览视频第 `j` 帧对应 `state[2*j]`，时间从 0 到 7.96 秒；8 秒最终状态保存在轨迹中。`frame_state_index` 和 `frame_time` 明确保存这种对应关系，避免通过视频序号猜测时间。

`overview.mp4` 和 `overview.png` 使用人为设置的外部视角，用于查看指针是否运动、场景是否正确。`camera.png` 才来自模型定义的固定相机，并保留其光学配置和位姿。两者应作为不同的数据来源标注，不能把概览视频当作机器人相机观测。

</details>

## 来源与核查范围

核查日期：**2026-10-09**。仓库内容与安装要求会变化，以下链接以官方或项目维护者的原始资料为主：

- MuJoCo：[Python 文档](https://mujoco.readthedocs.io/en/stable/python.html)、[官方教程](https://github.com/google-deepmind/mujoco/blob/main/python/tutorial.ipynb)、[PyPI 3.15.0 文件](https://pypi.org/project/mujoco/3.15.0/#files)。
- 中文 MuJoCo 教程：[Albusgive 目录](https://github.com/Albusgive/mujoco_learning/blob/main/directory.md)、[LitchiCheng README](https://github.com/LitchiCheng/mujoco-learning#readme)与 [pyproject.toml](https://github.com/LitchiCheng/mujoco-learning/blob/main/pyproject.toml)。
- dm_control：[README 与 macOS 安装说明](https://github.com/google-deepmind/dm_control#readme)、[官方教程](https://github.com/google-deepmind/dm_control/blob/main/tutorial.ipynb)。
- Isaac Lab：[官方仓库](https://github.com/isaac-sim/IsaacLab)、[develop 安装要求](https://isaac-sim.github.io/IsaacLab/develop/source/setup/installation/index.html)、[Quickstart](https://isaac-sim.github.io/IsaacLab/develop/source/setup/quickstart.html)及[完整 Isaac Sim 工作流的系统要求](https://docs.isaacsim.omniverse.nvidia.com/latest/installation/requirements.html)。
- SO101 实作：[IsaacLabTutorial README](https://github.com/isaac-sim/IsaacLabTutorial#readme)、[固定上游版本的配置](https://github.com/isaac-sim/IsaacLabTutorial/blob/main/pyproject.toml)。
- 社区章节：[SKKU IsaacLab-Tutorial README](https://github.com/Lab-of-AI-and-Robotics/IsaacLab-Tutorial#readme)及其分章分支。

## 继续阅读

- 上一页：[Isaac Lab 与具身数据](/simulation/isaac-lab-embodied-data/)——理解视觉任务、并行环境和完整轨迹之间的关系。
- 下一页：[MuJoCo 旋转关节实验](/simulation/mujoco-data-walkthrough/)——拖动时间轴，把一次动作、状态变化与实际画面逐项对照。
