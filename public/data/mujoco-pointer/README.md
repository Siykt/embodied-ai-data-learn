# MuJoCo 旋转关节实验：固定样本

采集日期：2026-10-09。样本编号：20261009T081729.185908Z-ec50f6d9。
来源：[Albusgive/mujoco_learning](https://github.com/Albusgive/mujoco_learning.git)，
固定提交 `8b9354d8559f4951990ece9aeacb2fa5d13d0a86`，模型 `API-MJCF/pointer.xml`。
模型来源许可见 UPSTREAM-LICENSE.txt（MIT）。MuJoCo 为 Apache-2.0。

CSV、NPZ、manifest、概览视频和两张图像逐字节保留原始记录；
summary 仅将本机绝对目录改为相对目录。episode.json 是供网页阅读的派生文件，
保留全部 401 个状态、400 个动作、传感器数值与 200 帧映射，未做平滑或降精度。
文件哈希与数据单位见 manifest.json。原始 CSV 为 26 列。

网页视频是外部概览，camera.png 仅是模型固定相机的初态单帧。
这是单关节、无任务成功标签的控制记录，不是抓取或视觉策略训练数据集。
网页不会跟随实时查看器或新的本地记录自动更新。

record_demo.py 和 requirements.lock.txt 是本次记录脚本与依赖锁。
复现需在脚本所在目录克隆上述仓库为 upstream，切到固定提交，
在 Python 3.12 环境安装锁定依赖，再运行 record_demo.py。
它会创建新的 outputs/<run_id>，不覆盖本样本。
