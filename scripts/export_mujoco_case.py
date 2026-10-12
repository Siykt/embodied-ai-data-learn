"""Publish the verified pointer episode as a portable, inspectable case study.

Run with the lab's Python (NumPy required), passing its directory as the argument.
The source recording is never modified; this page intentionally pins its run ID.
"""
import csv
import hashlib
import json
from pathlib import Path
import shutil
import sys

import numpy as np

SITE = Path(__file__).resolve().parents[1]
RUN = "20261009T081729.185908Z-ec50f6d9"


def main():
    lab = Path(sys.argv[1]).resolve()
    source = lab / "outputs" / RUN
    manifest = json.loads((source / "manifest.json").read_text())
    arrays = np.load(source / "episode.npz", allow_pickle=False)
    rows = list(csv.DictReader((source / "trajectory.csv").open()))
    assert len(rows) == 401 and arrays["action"].shape == (400, 2)
    assert arrays["sensor_values"].shape == (401, 15)
    np.testing.assert_array_equal(arrays["frame_state_index"], np.arange(0, 400, 2))
    np.testing.assert_allclose(arrays["frame_time"], arrays["state_time"][::2][:-1], atol=1e-11)
    for name, info in manifest["outputs"].items():
        assert hashlib.sha256((source / name).read_bytes()).hexdigest() == info["sha256"], name
    for k, row in enumerate(rows):
        assert float(row["qpos_pivot_rad"]) == arrays["qpos"][k, 0]
        assert float(row["qvel_pivot_rad_s"]) == arrays["qvel"][k, 0]
        if k < 400:
            assert float(row["outgoing_action_vel_rad_s"]) == arrays["action"][k, 1]
        else:
            assert row["outgoing_action_vel_rad_s"] == ""

    dataset = {
        "runId": RUN,
        "createdUtc": manifest["created_utc"],
        "fps": 25,
        "sensors": manifest["sensors"],
        "frameStateIndex": arrays["frame_state_index"].tolist(),
        "frameTime": arrays["frame_time"].tolist(),
        "states": [{
            "index": k, "time": float(arrays["state_time"][k]),
            "qpos": float(arrays["qpos"][k, 0]),
            "qvel": float(arrays["qvel"][k, 0]),
            "qacc": float(arrays["qacc"][k, 0]),
            "stateCtrl": arrays["state_ctrl"][k].tolist(),
            "action": arrays["action"][k].tolist() if k < 400 else None,
            "sensors": arrays["sensor_values"][k].tolist(),
        } for k in range(401)],
    }
    data_dir = SITE / "src/data"
    public = SITE / "public/data/mujoco-pointer"
    data_dir.mkdir(parents=True, exist_ok=True)
    public.mkdir(parents=True, exist_ok=True)
    encoded = json.dumps(dataset, ensure_ascii=False, allow_nan=False, separators=(",", ":")) + "\n"
    (data_dir / "mujoco-pointer-episode.json").write_text(encoded)
    (public / "episode.json").write_text(encoded)
    for name in (*manifest["outputs"], "manifest.json"):
        shutil.copy2(source / name, public / name)
    summary = json.loads((source / "summary.json").read_text())
    summary["directory"] = "."
    summary["publication_note"] = "Only the local directory was replaced with '.'; numerical results are unchanged."
    (public / "summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n")
    shutil.copy2(lab / "record_demo.py", public / "record_demo.py")
    shutil.copy2(lab / "requirements.lock.txt", public / "requirements.lock.txt")
    shutil.copy2(lab / "upstream/LICENSE", public / "UPSTREAM-LICENSE.txt")
    (public / "README.md").write_text(f"""# MuJoCo 旋转关节实验：固定样本

采集日期：2026-10-09。样本编号：{RUN}。
来源：[Albusgive/mujoco_learning]({manifest['source']['repository']})，
固定提交 `{manifest['source']['commit']}`，模型 `API-MJCF/pointer.xml`。
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
""")
    print(f"Verified and exported: {len(rows)} states, 400 actions, 200 frame mappings → {public}")


if __name__ == "__main__":
    main()
