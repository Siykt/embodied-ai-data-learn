---
title: 仿真开源学习仓库与实践路线
description: 比较 MuJoCo 与 Isaac Lab 的开源学习项目，按模型、状态动作、传感器、数据记录和评估组织分阶段实践路线。
---

学习仿真时，可以先完成一条小型数据链路：加载模型、施加动作、读取状态和传感器、保存一段轨迹，再把它回读出来。随后增加相机、任务变化和并行环境，更容易判断数据在哪里产生、为何发生变化，以及能否用于训练与评估。

本页以 **2026-10-09** 核查的官方文档、仓库说明和示例源码为依据，并提供下方的 Apple Silicon 本机实践记录。仓库默认分支可能继续变化，运行时应固定提交或发布版本；本机结果只适用于记录的系统、版本与验证范围。

## 如何选择第一个项目

| 当前目标与环境 | 推荐入口 | 第一份应交付的数据 |
| --- | --- | --- |
| Apple Silicon Mac，本地理解模型、动作和传感器 | Albusgive 的中文 MuJoCo 教程，配合官方 Python 文档 | 一段带仿真时间、状态、控制输入和传感器布局的轨迹 |
| 已能运行 MuJoCo，希望增加机械臂与相机案例 | LitchiCheng 的中文实例 | 同步保存图像与机器人状态，并说明相机、动作和采样时序 |
| 希望核对基础 API 或学习标准控制任务 | MuJoCo 官方教程、dm_control 官方教程 | 可复现的单次任务记录及奖励、终止条件说明 |
| 已有受支持的 NVIDIA Linux / Windows 环境，希望学习并行任务 | Isaac Lab 官方 Quickstart 与 tutorials | 能按环境和 episode 分开的状态、动作与结束原因 |
| 希望比较状态策略和视觉策略的数据需求 | 官方 IsaacLabTutorial 的 SO101 任务 | 教师动作标签、视觉观测、重置样本与独立评估结果 |

这里的 **episode** 是一次从环境重置到任务结束或超时的完整交互过程；同一任务的多次运行应有不同 episode ID。完整数据字段可对照[仿真数据契约](/simulation/simulators-embodied-data/#通用数据契约)。

![从 MuJoCo 单模型、轨迹记录和传感器对齐，逐步进入 Isaac Lab 并行任务与独立评估的学习路线](/images/docs/simulation-learning-route.svg)

## MuJoCo 学习仓库

MuJoCo 是物理引擎。它的 **MJCF** 是用于描述机器人、场景、执行器和传感器的 XML 格式；`MjModel` 保存编译后的模型配置，`MjData` 保存运行中的状态。先分清这两部分，才能理解模型版本和每步数据为什么都需要记录。

| 项目 | 教学内容与具体入口 | 依赖与适用范围 | 许可 |
| --- | --- | --- | --- |
| [Albusgive/mujoco_learning](https://github.com/Albusgive/mujoco_learning) | 中文 MJCF 建模、Python / C++ API、传感器、渲染、射线测距；从 [Python 第一课](https://github.com/Albusgive/mujoco_learning/tree/main/Python/Chapter1-view%26step)开始 | 第一课只需 `mujoco` 和 Python 标准库；后续相机课增加 OpenCV 等依赖。适合先建立轻量数据循环 | [MIT](https://github.com/Albusgive/mujoco_learning/blob/main/LICENSE) |
| [LitchiCheng/mujoco-learning](https://github.com/LitchiCheng/mujoco-learning) | 中文机械臂控制、相机标定、传感器、抓取与数据采集；可先读 [control_joint_pos.py](https://github.com/LitchiCheng/mujoco-learning/blob/main/control_joint_pos.py) | README 的完整安装面向 Ubuntu / WSL2；主要环境还含训练、运动学和数据工具。Mac 上应逐例核对依赖 | [源码 MIT](https://github.com/LitchiCheng/mujoco-learning/blob/main/LICENSE)；README 声明文档为 CC BY 4.0 |
| [google-deepmind/mujoco](https://github.com/google-deepmind/mujoco) | 官方 [Python tutorial.ipynb](https://github.com/google-deepmind/mujoco/blob/main/python/tutorial.ipynb)，讲模型、状态、步进、接触、传感器与渲染 | 原生 Python 包包含引擎；Notebook 的安装单元面向 Colab NVIDIA GPU / EGL，本地需调整安装与渲染设置 | [源码 Apache-2.0](https://github.com/google-deepmind/mujoco/blob/main/LICENSE)；`doc` 目录文档、图像和视频为 CC BY 4.0 |
| [google-deepmind/dm_control](https://github.com/google-deepmind/dm_control) | 官方 [tutorial.ipynb](https://github.com/google-deepmind/dm_control/blob/main/tutorial.ipynb)，包括模型组合、观测、环境与控制任务；[viewer 示例](https://github.com/google-deepmind/dm_control/blob/main/dm_control/viewer/README.md)可加载现成任务 | 比原生 MuJoCo 多一层环境抽象和依赖；README 有 macOS Homebrew Python / GLFW 指引；Notebook 同样有 Colab 专用设置 | [Apache-2.0](https://github.com/google-deepmind/dm_control/blob/main/LICENSE) |

### 用 Albusgive 的第一课建立数据循环

[课程目录](https://github.com/Albusgive/mujoco_learning/blob/main/directory.md)先介绍模型，再介绍接口。`Python/Chapter1-view&step/view.py` 加载 `API-MJCF/pointer.xml`，向速度执行器写入控制量，推进物理状态，并同步交互窗口。模型包含关节位置、关节速度、陀螺仪、加速度计等传感器，适合继续练习数据读取。

阅读时依次找出四个位置：模型加载、`ctrl` 写入、`mj_step` 调用、状态读取。`ctrl` 的含义由执行器定义决定：速度执行器的输入不能直接解释成力矩。采集时还应说明观测在步进前还是步进后读取，避免把动作和下一状态错配。

示例使用相对于当前工作目录的模型路径，应从章节目录启动。在已安装原生 MuJoCo、且桌面图形环境可用的 macOS 上，对应入口是：

```sh
cd 'mujoco_learning/Python/Chapter1-view&step'
mjpython view.py
```

这里的目录名取决于克隆位置。保留完整仓库结构，因为 `pointer.xml` 还引用了 `MJCF/asset/desert.png`。`mjpython` 是 MuJoCo 在 macOS 上提供的专用启动器；官方要求使用它运行 `launch_passive` 被动查看器，见 [Python 文档](https://mujoco.readthedocs.io/en/stable/python.html#passive-viewer)。它解决启动线程要求，实际显示仍取决于可用的窗口和图形环境。

用于固定参考的 Albusgive 提交为 `8b9354d8559f4951990ece9aeacb2fa5d13d0a86`，该提交日期为 **2026-03-16**。仓库的最近推送时间可能晚于默认分支提交日期，两者不能混写为“代码更新日期”。

### 从 LitchiCheng 的实例进入相机与采集

该项目的价值在于把机械臂状态、相机、标定、传感器和抓取过程放进具体场景。建议先运行依赖较少的单例，再按需要增加模块：

1. `control_joint_pos.py`：读取模型和关节位置，观察关节变化；该文件导入 MuJoCo、NumPy、GLFW 和 SciPy。
2. `get_camera_pic.py`：读取相机图像，核对颜色通道、图像方向、相机配置和采样时刻。
3. `sensordata.py`：按传感器名称及数组地址读取数据，并与状态字段对照；它还依赖项目的可视化模块。
4. `automated_pickup_place_advanced.py`：进一步阅读任务阶段、采集触发、成功条件与记录器。

每份示例都应从源码确认导入项和模型路径。仓库的 `requirements.txt` 包含 `evdev`、`python-xlib`、`triton` 等与特定平台相关的包；当前 `pyproject.toml` 还包括 PyTorch、LeRobot、Pinocchio 与 KDL 工具。完整环境与最小示例的需求有明显差别，不能把整个依赖清单当作 Mac 入门必需项。

![模型与配置经过控制步进产生状态、传感器和图像，再按时间对齐形成 episode 并进行质量检查的数据流程](/images/docs/simulation-local-data-flow.svg)

## Apple Silicon 本机实践记录

本次在 **macOS 26.6.2、arm64、Python 3.12.14** 上建立独立实验目录 `~/Documents/work/mujoco-learning-lab`，使用 MuJoCo 3.15.0、NumPy 2.5.3、Pillow 12.3.0 与 ImageIO 2.38.1。上游代码位于 `upstream/`，使用前述固定提交；依赖版本保存在 `requirements.lock.txt`。实验使用 `pointer.xml`，包含一个旋转关节、两个执行器和六个传感器。

在该本地实验目录中，可双击以下入口：

| 入口 | 用途 |
| --- | --- |
| `start.command` | 在后台启动浏览器查看器，服务已运行时复用；启动后手动打开 `http://127.0.0.1:8765/` |
| `stop.command` | 停止本实验的查看器服务；关闭浏览器标签不会停止后台服务 |
| `record.command` | 在独立模型上重新生成一份八秒数据样例，保存到新的 `outputs/<运行编号>/` |
| `native-viewer.command` | 可选的原版第一课入口，通过 `mjpython` 启动，要求会话具有可用桌面显示器 |
| `README.md` | 查看操作方法、模型与课程入口、输出说明和环境恢复步骤 |

浏览器中的 `vel` 是目标角速度，单位为 rad/s；`motor` 是力矩输入，单位为 N·m。可使用 Pause / Run 暂停或继续，拖动和滚轮调整视角。`record.command` 生成固定控制演示，不记录浏览器中的手动操作；新一次输出的位置也会写入 `outputs/latest.json`。

### 查看器与渲染的验证范围

| 验证项 | 实际结果 | 对学习与数据工作的含义 |
| --- | --- | --- |
| 模型加载与 CPU 步进 | 成功运行 500 个物理步，对应 1 秒仿真时间，并读取六个传感器 | 可独立验证状态和传感器，无需先打开交互窗口 |
| 原生被动查看器 | 当前会话未成功：GLFW 返回空显示器列表，在 `_glfwGetVideoModeCocoa` 崩溃 | 这是本次会话的窗口显示路径问题；使用 `mjpython` 仍不能保证显示器可用 |
| 离屏 `Renderer` | 成功生成概览视频、概览图和模型相机图 | 可继续进行数据记录与图像质量检查 |
| 官方实验性 `experimental.studio` 浏览器查看器 | 成功显示模型，并通过暂停、缩放及 Controls 面板操作检查；面板初始值为 `motor=0` 与 `vel=1` | 可在浏览器中理解场景和执行器；实验性接口需要固定 MuJoCo 版本 |

[GLFW](/reference/terms/#glfw) 是用于创建窗口、图形上下文和处理输入的库。此次原生窗口失败与离屏渲染成功分别记录，不能相互替代。浏览器查看器服务经检查只监听本机回环地址，本次入口为 `http://127.0.0.1:8765/`；该地址指向访问者自己的电脑，只有相应本地服务运行时可用。[实验性接口](/reference/terms/#实验性接口)意味着它仍可能随版本变化，升级前应重新验证启动和交互行为。

![本地离屏渲染的 pointer 模型概览：棋盘地面上的圆柱支架、旋转指针和蓝色传感器位置标记](/images/docs/mujoco-local-pointer.png)

图：2026-10-09 本地生成的 `overview.png`，模型来自 [Albusgive/mujoco_learning](https://github.com/Albusgive/mujoco_learning) 的 MIT 许可仓库，固定提交与资产来源见本文及实验 manifest。本图是供人检查场景的外部概览视角；模型传感器相机的输出另存为 `camera.png`。

### 八秒轨迹记录与回读结果

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

### 状态、动作与传感器如何对齐

在每个状态采样时刻，记录器先调用 `mj_forward`，根据当前 `qpos`、`qvel` 和控制量重新计算派生量与传感器，然后一起保存。`mj_forward` 不推进时间；这一步使保存的关节状态、加速度和传感器对应同一个状态时刻。

动作与状态使用明确的区间关系：

```text
state[k] -- action[k] 保持在 [t[k], t[k+1]) --> state[k+1]
```

`action[k]` 是接下来一个区间的输入；`state_ctrl[k]` 是计算当前状态派生量时保留的控制。初态的 `state_ctrl[0]` 为零，后续 `state_ctrl[k] = action[k-1]`。因此某一时刻的加速度传感器按刚结束区间的控制刷新，而不是按尚未施加的下一个动作刷新。把两列合并会改变数据语义。

CSV 每行保存一个状态及其向外发出的动作，最后一行只有 8 秒时的最终状态，动作列留空。概览视频第 `j` 帧对应 `state[2*j]`，时间从 0 到 7.96 秒；8 秒最终状态保存在轨迹中。`frame_state_index` 和 `frame_time` 明确保存这种对应关系，避免通过视频序号猜测时间。

`overview.mp4` 和 `overview.png` 使用人为设置的外部视角，用于查看指针是否运动、场景是否正确。`camera.png` 才来自模型定义的固定相机，并保留其光学配置和位姿。两者应作为不同的数据来源标注，不能把概览视频当作机器人相机观测。

## Isaac Lab 学习仓库

Isaac Lab 组织机器人学习环境、动作与观测、任务规则和训练评估工作流。对于数据学习，重点是找出每个观测的来源、动作如何变成控制量、何时重置，以及并行环境怎样分开记录。

| 项目 | 建议阅读顺序 | 数据视角的收获 | 许可与版本边界 |
| --- | --- | --- | --- |
| [isaac-sim/IsaacLab](https://github.com/isaac-sim/IsaacLab) | 对应版本的 [Quickstart](https://isaac-sim.github.io/IsaacLab/develop/source/setup/quickstart.html) → `scripts/tutorials` → 环境与传感器配置 | 从空场景到机器人、相机、动作、重置与并行环境，理解数据产生位置 | 主框架 BSD-3-Clause，Mimic 部分 Apache-2.0；以各目录许可为准。核查时 `develop` 为 3.0 开发路线 |
| [isaac-sim/IsaacLabTutorial](https://github.com/isaac-sim/IsaacLabTutorial) | SO101 放置小瓶：状态策略 → 相机策略蒸馏 → 视觉策略训练与评估 | 比较完整状态、腕部图像、自身状态、教师动作标签、重置样本和成功判定 | [Apache-2.0](https://github.com/isaac-sim/IsaacLabTutorial/blob/main/LICENSE)；Python 3.12，锁定特定 Isaac Lab 提交，按仓库自身说明运行 |
| [Lab-of-AI-and-Robotics/IsaacLab-Tutorial](https://github.com/Lab-of-AI-and-Robotics/IsaacLab-Tutorial) | SKKU 社区教程，从 Unitree Go2 到 H1，按十章阅读；第二、三章起使用独立分支 | 把资产、运动学、动作、奖励、课程和评估连接起来，分析这些配置怎样改变数据分布 | [Apache-2.0](https://github.com/Lab-of-AI-and-Robotics/IsaacLab-Tutorial/blob/main/LICENSE)，部分代码沿用上游 BSD-3-Clause；不可默认与当前 3.0 API 兼容 |

### 官方实作：状态观测如何转向相机观测

IsaacLabTutorial 当前使用 SO101 机械臂把小瓶放入架子，提供三种任务：

| 任务 | 策略可见输入 | 学习时应检查的数据 |
| --- | --- | --- |
| `IsaacTutorial-Place-Vial-SO101` | 完整状态 | 关节、物体位姿、动作、奖励、阶段标记和终止条件 |
| `IsaacTutorial-Place-Vial-SO101-Camera-Distillation` | 腕部 RGB 与机器人自身状态 | 学生实际访问的状态、对应图像、教师动作标签及动作裁剪规则 |
| `IsaacTutorial-Place-Vial-SO101-Camera` | 腕部 RGB 与机器人自身状态 | 图像噪声与随机化、训练观测、评估初态及成功率 |

第一种与第三种使用 [PPO（近端策略优化）](/reference/terms/#ppo)，一种根据环境交互和奖励更新策略的方法。第二种使用[策略蒸馏](/reference/terms/#策略蒸馏)：让依赖相机的学生策略学习状态教师给出的动作。该仓库采用 [DAgger](/reference/terms/#dagger) 式收集，即学生执行动作、教师为学生到达的状态提供动作标签；这些标签的采样来源需要随训练配置保存。

训练可使用覆盖不同任务阶段的重置样本，评估则从规定的初始状态开始。两种分布应分别说明：能从接近完成的阶段重置并训练，并不直接证明策略可以从完整任务起点成功执行。具体定义以仓库 `reset`、`mdp` 和 `utils/evaluation.py` 为准。

核查时，项目在 [pyproject.toml](https://github.com/isaac-sim/IsaacLabTutorial/blob/main/pyproject.toml) 中固定 Isaac Lab 提交 `f754f2965af9d6aa4f2e18d7d6d3ddf8f8471c69`，并维护自己的依赖锁文件。README 使用的 `presets=` 参数属于这套固定环境；不要直接替换成另一版本文档中的命令参数。

### 社区章节：从环境定义理解数据分布

SKKU 教程的第一章使用内置示例，第二、三章共用 [`chapter2_3`](https://github.com/Lab-of-AI-and-Robotics/IsaacLab-Tutorial/tree/chapter2_3)，后续是 `chapter4` 至 `chapter10`。每章代表一份阶段代码，阅读下一章前应确认所在分支及对应的 Isaac Lab 版本。

可以把章节内容转换为数据问题：更换机器人后关节布局是否改变；自定义动作的单位和范围是什么；奖励修改是否改变成功样本的定义；课程是否改变速度与地形分布；训练与评估是否用了不同的随机化配置。这些问题比仅复现一条训练命令更能帮助建立可用的数据集。

![并行仿真环境各自重置和结束，记录器按环境槽位与 episode 边界整理轨迹](/images/docs/simulation-parallel-recorder.svg)

## 分阶段实践与验收

| 阶段 | 推荐材料 | 需要完成的产物 | 进入下一阶段前的检查 |
| --- | --- | --- | --- |
| 1. 单模型与物理步进 | Albusgive 第一课、MuJoCo 官方基础 API | 模型版本、初态和一段固定动作序列 | 状态数值有限、维度正确；仿真时间按物理步长推进 |
| 2. 状态与动作记录 | MuJoCo `MjData`、简单记录器 | 时间、`qpos`、`qvel`、`ctrl`、传感器布局与结束原因 | 说明采样发生在步进前还是后；保存实际控制量；轨迹能回读 |
| 3. 图像与传感器对齐 | Albusgive 传感器课、LitchiCheng 相机实例 | RGB / 深度与状态时间表、相机配置、单位和坐标系 | 图像方向、深度尺度与颜色通道正确；不同采样率的对齐规则明确 |
| 4. 任务与数据质量 | dm_control 或机械臂抓取实例 | 多条成功与失败 episode，任务条件和质量报告 | 区分自然终止与时间截断；按场景、物体和初态划分训练与评估 |
| 5. 并行与视觉策略 | Isaac Lab Quickstart、SO101 实作 | 独立 episode、教师标签、随机化参数和独立评估记录 | 环境重置不串轨迹；评估初态固定；逐项说明策略可见与仅供训练的信息 |

**回读验收**是把保存的数据重新加载，检查形状、时间、动作语义和关键状态；它不要求先训练出高成功率策略。可以从几十步开始，对同一模型和初态重放固定动作，比较关键状态和接触事件。跨引擎版本、求解器或硬件时，应报告允许的数值差异，避免默认逐位一致。

## 版本兼容与运行环境

### Apple Silicon 的本地起点

核查时 [MuJoCo 3.15.0 的 PyPI 文件](https://pypi.org/project/mujoco/3.15.0/#files)包含 macOS arm64 原生包，要求 Python ≥3.10。普通 MuJoCo 物理仿真可以使用 CPU，不要求 CUDA。模型数值步进、离屏渲染、原生窗口和浏览器查看器是不同验证项，某一种成功不能推断其余都可用。

官方 MuJoCo 和 dm_control Notebook 的安装单元包含 Colab、NVIDIA 驱动检测及 EGL 配置。[EGL](/reference/terms/#egl) 是图形上下文接口，该处配置针对其云端 Linux 渲染环境；Mac 不应原样执行这些设置。可先阅读模型和仿真单元，按本机 Python 包与渲染支持选择入口。

### Isaac Lab 的版本路线

核查时，Isaac Lab `develop` 文档采用 3.0 路线。完整 Isaac Sim 工作流与新的 [Kit-less](/reference/terms/#kit-less) 路线需要分开理解：Kit-less 指不启动 Isaac Sim 的 Kit 应用运行时，部分工作流通过 [Newton](/reference/terms/#newton) 物理后端运行，因此“Isaac Lab 必须先安装 Isaac Sim”已不能概括所有新路径。

但这不意味着 Apple Silicon 获得官方支持。当前[安装指南](https://isaac-sim.github.io/IsaacLab/develop/source/setup/installation/index.html)列出的安装路径仍为 Linux / Windows，并使用 CUDA；IsaacLabTutorial 的环境配置也未包含 macOS。Apple Silicon 与某些受支持服务器同为 ARM 架构，不能据此推断操作系统、图形驱动和依赖兼容。

实践中可在 Mac 上完成 MuJoCo 的模型与数据契约练习，再把 Isaac Lab 任务放到符合对应版本要求的 NVIDIA Linux / Windows 机器。选择远程工作站时，应核对所选后端与渲染需求：无窗口运行只是关闭桌面显示，并不自动取消 GPU 或驱动要求。

### 为每次运行保留兼容性记录

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

## 许可与数据使用边界

开源代码许可、机器人资产许可、文档许可和导出数据的使用条件需要分别检查。MIT、Apache-2.0 与 BSD-3-Clause 是不同的开源软件许可；分发代码或改编作品时，应保留相应通知并遵守具体条款。

仓库根目录的许可通常不能直接覆盖它引用的所有网格、纹理、机器人资产或外部数据。固定模型时同时保存资产来源与许可；引用教程图文时核对文档许可；发布采集数据前确认包含的图像、资产衍生内容和真实数据允许相应使用。Isaac Lab 的开源许可也不自动替代 Isaac Sim、第三方资产或其他依赖各自的条款。

如果某个练习输出只有视频或训练日志，应称为演示或运行记录。可供下游训练的数据集还需要观测、动作、时间、episode 边界、版本和质量字段；这些要求见[MuJoCo 与具身数据](/simulation/mujoco-embodied-data/)、[Isaac Lab 与具身数据](/simulation/isaac-lab-embodied-data/)及[验证与真实迁移](/simulation/simulation-validation-sim2real/)。

## 来源与核查范围

核查日期：**2026-10-09**。仓库内容与安装要求会变化，以下链接以官方或项目维护者的原始资料为主：

- MuJoCo：[Python 文档](https://mujoco.readthedocs.io/en/stable/python.html)、[官方教程](https://github.com/google-deepmind/mujoco/blob/main/python/tutorial.ipynb)、[PyPI 3.15.0 文件](https://pypi.org/project/mujoco/3.15.0/#files)。
- 中文 MuJoCo 教程：[Albusgive 目录](https://github.com/Albusgive/mujoco_learning/blob/main/directory.md)、[LitchiCheng README](https://github.com/LitchiCheng/mujoco-learning#readme)与 [pyproject.toml](https://github.com/LitchiCheng/mujoco-learning/blob/main/pyproject.toml)。
- dm_control：[README 与 macOS 安装说明](https://github.com/google-deepmind/dm_control#readme)、[官方教程](https://github.com/google-deepmind/dm_control/blob/main/tutorial.ipynb)。
- Isaac Lab：[官方仓库](https://github.com/isaac-sim/IsaacLab)、[develop 安装要求](https://isaac-sim.github.io/IsaacLab/develop/source/setup/installation/index.html)、[Quickstart](https://isaac-sim.github.io/IsaacLab/develop/source/setup/quickstart.html)及[完整 Isaac Sim 工作流的系统要求](https://docs.isaacsim.omniverse.nvidia.com/latest/installation/requirements.html)。
- SO101 实作：[IsaacLabTutorial README](https://github.com/isaac-sim/IsaacLabTutorial#readme)、[固定上游版本的配置](https://github.com/isaac-sim/IsaacLabTutorial/blob/main/pyproject.toml)。
- 社区章节：[SKKU IsaacLab-Tutorial README](https://github.com/Lab-of-AI-and-Robotics/IsaacLab-Tutorial#readme)及其分章分支。
