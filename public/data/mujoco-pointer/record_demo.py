"""Record an eight-second, time-aligned MuJoCo tutorial dataset.

Run with .venv/bin/python record_demo.py. Each run creates a new outputs folder.
This is a deterministic data-recording demonstration, not a robot task benchmark.
"""

from __future__ import annotations

import csv
import hashlib
import importlib.metadata
import json
import platform
import subprocess
import sys
import uuid
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path

import imageio.v2 as imageio
import imageio_ffmpeg
import mujoco
import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parent
MODEL_PATH = ROOT / "upstream/API-MJCF/pointer.xml"
DURATION = 8.0
STEPS_PER_ACTION = 10
N_ACTIONS = 400
FPS = 25
WIDTH, HEIGHT = 640, 480
SENSOR_INFO = {
    "quat": {"components": ["w", "x", "y", "z"], "unit": "unitless", "frame": "IMU site orientation in world, wxyz quaternion"},
    "ang_vel": {"components": ["x", "y", "z"], "unit": "rad/s", "frame": "IMU site local frame"},
    "accel": {"components": ["x", "y", "z"], "unit": "m/s^2", "frame": "IMU site local specific acceleration; reads +9.81 on z at rest"},
    "pivot_p": {"components": ["value"], "unit": "rad", "frame": "pivot joint position"},
    "pivot_v": {"components": ["value"], "unit": "rad/s", "frame": "pivot joint velocity"},
    "linvel": {"components": ["x", "y", "z"], "unit": "m/s", "frame": "IMU site linear velocity in world frame"},
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git(*args: str) -> str:
    return subprocess.check_output(["git", "-C", str(ROOT / "upstream"), *args], text=True).strip()


def record_states(model: mujoco.MjModel) -> dict[str, np.ndarray]:
    """Hold action[k] across ten physics steps, then refresh derived quantities."""
    data = mujoco.MjData(model)
    control_dt = float(model.opt.timestep) * STEPS_PER_ACTION
    action_time = np.arange(N_ACTIONS, dtype=np.float64) * control_dt
    action = np.column_stack((np.zeros(N_ACTIONS), np.sin(2 * np.pi * 0.4 * action_time)))
    records = {key: [] for key in ("state_time", "qpos", "qvel", "qacc", "state_ctrl", "sensor_values")}

    def capture() -> None:
        # mj_step may leave derived values at the previous integration stage.
        # Recompute them for the stored qpos/qvel, keeping the just-applied ctrl.
        mujoco.mj_forward(model, data)
        records["state_time"].append(float(data.time))
        for name, field in (("qpos", "qpos"), ("qvel", "qvel"), ("qacc", "qacc"), ("state_ctrl", "ctrl"), ("sensor_values", "sensordata")):
            records[name].append(getattr(data, field).copy())

    capture()
    for control in action:
        data.ctrl[:] = control
        for _ in range(STEPS_PER_ACTION):
            mujoco.mj_step(model, data)
        capture()
    arrays = {key: np.asarray(value) for key, value in records.items()}
    arrays.update(
        action_time=action_time,
        action=action,
        action_from_state=np.arange(N_ACTIONS, dtype=np.int64),
        action_to_state=np.arange(1, N_ACTIONS + 1, dtype=np.int64),
        frame_state_index=np.arange(int(DURATION * FPS), dtype=np.int64) * 2,
        frame_time=np.arange(int(DURATION * FPS), dtype=np.float64) / FPS,
    )
    for sensor_id in range(model.nsensor):
        name = model.sensor(sensor_id).name
        start, size = int(model.sensor_adr[sensor_id]), int(model.sensor_dim[sensor_id])
        arrays[f"sensor_{name}"] = arrays["sensor_values"][:, start:start + size].copy()
    return arrays


def verify_states(arrays: dict[str, np.ndarray], repeated: dict[str, np.ndarray]) -> dict:
    assert arrays["action"].shape == (400, 2)
    assert arrays["qpos"].shape == arrays["qvel"].shape == (401, 1)
    assert arrays["sensor_values"].shape == (401, 15)
    assert all(np.isfinite(value).all() for value in arrays.values())
    np.testing.assert_allclose(arrays["state_time"], np.arange(401) * 0.02, atol=1e-10, rtol=0)
    np.testing.assert_allclose(arrays["action_time"], arrays["state_time"][:-1], atol=1e-10, rtol=0)
    np.testing.assert_allclose(arrays["action"][:, 0], 0, atol=0, rtol=0)
    np.testing.assert_allclose(arrays["action"][:, 1], np.sin(2 * np.pi * 0.4 * arrays["action_time"]), atol=0, rtol=0)
    np.testing.assert_array_equal(arrays["state_ctrl"][1:], arrays["action"])
    np.testing.assert_array_equal(arrays["action_from_state"], np.arange(400))
    np.testing.assert_array_equal(arrays["action_to_state"], np.arange(1, 401))
    np.testing.assert_array_equal(arrays["frame_state_index"], np.arange(200) * 2)
    np.testing.assert_allclose(arrays["frame_time"], arrays["state_time"][arrays["frame_state_index"]], atol=1e-10, rtol=0)
    np.testing.assert_allclose(arrays["sensor_pivot_p"], arrays["qpos"], atol=1e-12, rtol=0)
    np.testing.assert_allclose(arrays["sensor_pivot_v"], arrays["qvel"], atol=1e-12, rtol=0)
    np.testing.assert_allclose(arrays["sensor_ang_vel"][:, :2], 0, atol=1e-12, rtol=0)
    np.testing.assert_allclose(arrays["sensor_ang_vel"][:, 2], arrays["qvel"][:, 0], atol=1e-12, rtol=0)
    quat_error = float(np.max(np.abs(np.linalg.norm(arrays["sensor_quat"], axis=1) - 1)))
    assert quat_error < 1e-12
    # A second independent rollout verifies repeatability of the exported samples.
    max_repeat_error = max(float(np.max(np.abs(value - repeated[key]))) for key, value in arrays.items())
    assert max_repeat_error == 0.0
    return {"passed": True, "state_count": 401, "transition_count": 400, "sensor_count": 6, "sensor_dimensions": 15,
            "all_values_finite": True, "quaternion_max_norm_error": quat_error,
            "gyro_z_qvel_max_error": float(np.max(np.abs(arrays["sensor_ang_vel"][:, 2] - arrays["qvel"][:, 0]))),
            "independent_rollout_max_absolute_error": max_repeat_error}


def write_csv(output: Path, arrays: dict[str, np.ndarray]) -> None:
    fields = ["state_index", "state_time_s", "qpos_pivot_rad", "qvel_pivot_rad_s", "qacc_pivot_rad_s2",
              "state_ctrl_motor_Nm", "state_ctrl_vel_rad_s", "outgoing_action_index", "outgoing_action_end_time_s",
              "outgoing_action_motor_Nm", "outgoing_action_vel_rad_s"]
    for name, info in SENSOR_INFO.items():
        fields.extend(f"sensor_{name}_{component}" for component in info["components"])
    with (output / "trajectory.csv").open("w", newline="", encoding="utf-8") as stream:
        writer = csv.writer(stream)
        writer.writerow(fields)
        for k in range(N_ACTIONS + 1):
            outgoing = [k, arrays["state_time"][k + 1], *arrays["action"][k]] if k < N_ACTIONS else ["", "", "", ""]
            writer.writerow([k, arrays["state_time"][k], arrays["qpos"][k, 0], arrays["qvel"][k, 0],
                             arrays["qacc"][k, 0], *arrays["state_ctrl"][k], *outgoing, *arrays["sensor_values"][k]])


def restore(model: mujoco.MjModel, data: mujoco.MjData, arrays: dict[str, np.ndarray], k: int) -> None:
    mujoco.mj_resetData(model, data)
    data.time = arrays["state_time"][k]
    data.qpos[:] = arrays["qpos"][k]
    data.qvel[:] = arrays["qvel"][k]
    data.ctrl[:] = arrays["state_ctrl"][k]
    mujoco.mj_forward(model, data)


def render(output: Path, model: mujoco.MjModel, arrays: dict[str, np.ndarray]) -> dict:
    data = mujoco.MjData(model)
    camera_id = mujoco.mj_name2id(model, mujoco.mjtObj.mjOBJ_CAMERA, "this_camera")
    assert camera_id >= 0
    native_width, native_height = map(int, model.cam_resolution[camera_id])
    # Enlarge the framebuffer only; the model camera's optics and pose stay intact.
    model.vis.global_.offwidth = max(WIDTH, native_width)
    model.vis.global_.offheight = max(HEIGHT, native_height)
    overview = mujoco.MjvCamera()
    overview.type = mujoco.mjtCamera.mjCAMERA_FREE
    overview.lookat[:] = [0.04, 0.0, 0.36]
    overview.distance = 1.55
    overview.azimuth = 120.0
    overview.elevation = -25.0
    frame_std = []
    with mujoco.Renderer(model, height=HEIGHT, width=WIDTH) as renderer:
        with imageio.get_writer(output / "overview.mp4", fps=FPS, codec="libx264", quality=8,
                                pixelformat="yuv420p", macro_block_size=None) as writer:
            for frame_index, state_index in enumerate(arrays["frame_state_index"]):
                restore(model, data, arrays, int(state_index))
                renderer.update_scene(data, camera=overview)
                frame = renderer.render().copy()
                assert frame.shape == (HEIGHT, WIDTH, 3)
                frame_std.append(float(frame.std()))
                assert frame_std[-1] > 1.0, f"Blank overview frame {frame_index}"
                if frame_index == 0:
                    Image.fromarray(frame).save(output / "overview.png")
                writer.append_data(frame)
    restore(model, data, arrays, 0)
    with mujoco.Renderer(model, height=native_height, width=native_width) as renderer:
        renderer.update_scene(data, camera="this_camera")
        camera_image = renderer.render().copy()
        assert float(camera_image.std()) > 1.0, "Blank model camera image"
        Image.fromarray(camera_image).save(output / "camera.png")
    decoded = 0
    with imageio.get_reader(output / "overview.mp4") as reader:
        video_metadata = reader.get_meta_data()
        for frame in reader:
            assert frame.shape == (HEIGHT, WIDTH, 3)
            assert float(frame.std()) > 1.0
            decoded += 1
    assert decoded == 200
    assert abs(float(video_metadata["fps"]) - FPS) < 1e-6
    assert abs(float(video_metadata["duration"]) - DURATION) < 1e-6
    original_camera = ET.parse(MODEL_PATH).find(".//camera[@name='this_camera']")
    return {
        "overview": {"purpose": "External overview for human inspection; not a model camera or sensor image",
                     "camera_type": "free", "lookat_m": overview.lookat.tolist(), "distance_m": overview.distance,
                     "azimuth_degrees": overview.azimuth, "elevation_degrees": overview.elevation,
                     "width": WIDTH, "height": HEIGHT, "fps": FPS, "frame_count": decoded,
                     "frame_state_index": arrays["frame_state_index"].tolist(),
                     "frame_time_s": arrays["frame_time"].tolist(),
                     "mapping": "frame j renders state[2*j], j=0..199; times 0..7.96s. Final state at 8s is in the dataset only.",
                     "png_state_index": 0, "minimum_raw_frame_std": min(frame_std)},
        "camera": {"purpose": "RGB from the model's fixed this_camera at state[0]; original optics and pose",
                   "name": "this_camera", "type": "fixed", "width": native_width, "height": native_height,
                   "state_index": 0, "time_s": 0.0, "xml_attributes": dict(original_camera.attrib),
                   "compiled_intrinsic": model.cam_intrinsic[camera_id].tolist(),
                   "sensor_size": model.cam_sensorsize[camera_id].tolist(),
                   "world_position_m": data.cam_xpos[camera_id].tolist(),
                   "world_rotation_row_major": data.cam_xmat[camera_id].tolist(),
                   "raw_image_std": float(camera_image.std())},
        "validation": {"decoded_frames": decoded, "fps": video_metadata["fps"],
                       "duration_s": video_metadata["duration"], "dimensions": [WIDTH, HEIGHT], "all_frames_nonblank": True},
    }


def main() -> None:
    model = mujoco.MjModel.from_xml_path(str(MODEL_PATH))
    assert model.nq == model.nv == 1 and model.nu == 2 and model.nsensor == 6
    assert float(model.opt.timestep) == 0.002
    timestamp = datetime.now(timezone.utc)
    run_id = timestamp.strftime("%Y%m%dT%H%M%S.%fZ") + "-" + uuid.uuid4().hex[:8]
    output = ROOT / "outputs" / run_id
    output.mkdir(parents=True, exist_ok=False)
    arrays = record_states(model)
    state_validation = verify_states(arrays, record_states(model))
    np.savez_compressed(output / "episode.npz", **arrays)
    write_csv(output, arrays)
    print(f"Recorded 401 states / 400 actions; rendering to {output}", flush=True)
    rendering = render(output, model, arrays)
    # Validate the saved files, in addition to the in-memory recording.
    with np.load(output / "episode.npz", allow_pickle=False) as saved:
        assert set(saved.files) == set(arrays)
        for key, value in arrays.items():
            np.testing.assert_array_equal(saved[key], value)
    with (output / "trajectory.csv").open(encoding="utf-8", newline="") as stream:
        rows = list(csv.DictReader(stream))
    assert len(rows) == 401
    assert sum(bool(row["outgoing_action_index"]) for row in rows) == 400
    assert rows[-1]["outgoing_action_index"] == ""
    textures = []
    for texture in ET.parse(MODEL_PATH).findall(".//texture[@file]"):
        path = (MODEL_PATH.parent / texture.attrib["file"]).resolve()
        textures.append({"path": str(path.relative_to(ROOT)), "sha256": sha256(path)})
    sensors = []
    for i in range(model.nsensor):
        name = model.sensor(i).name
        sensors.append({"name": name, "offset": int(model.sensor_adr[i]), "dimension": int(model.sensor_dim[i]), **SENSOR_INFO[name]})
    manifest = {
        "schema_version": 1, "run_id": run_id, "created_utc": timestamp.isoformat(),
        "purpose": "Deterministic introductory data-recording demonstration; no robot task success rate is measured",
        "source": {"repository": git("remote", "get-url", "origin"), "commit": git("rev-parse", "HEAD"),
                   "upstream_worktree_status": git("status", "--porcelain"),
                   "model_path": str(MODEL_PATH.relative_to(ROOT)), "model_sha256": sha256(MODEL_PATH),
                   "referenced_textures": textures, "script": "record_demo.py", "script_sha256": sha256(Path(__file__))},
        "runtime": {"python": platform.python_version(), "platform": platform.platform(), "machine": platform.machine(),
                    "packages": {name: importlib.metadata.version(name) for name in ("mujoco", "numpy", "pillow", "imageio", "imageio-ffmpeg")},
                    "ffmpeg_version": imageio_ffmpeg.get_ffmpeg_version()},
        "simulation": {"duration_s": DURATION, "physics_timestep_s": 0.002, "physics_hz": 500,
                       "steps_per_action": 10, "control_hz": 50, "state_hz": 50, "initial_state_included": True,
                       "state_count": 401, "action_count": 400, "initial_qpos_rad": [0.0], "initial_qvel_rad_s": [0.0],
                       "integrator": "implicitfast", "randomness": "None; deterministic analytic control, no added sensor noise",
                       "control": ["ctrl[0] = 0 N*m (motor torque)", "ctrl[1] = sin(2*pi*0.4*t[k]) rad/s (velocity target)"]},
        "sampling": {"transition": "action[k] is held on [t[k],t[k+1]) and maps state[k] to state[k+1], k=0..399",
                     "state": "qpos, qvel and all sensors sampled together after mj_forward at each t[k]",
                     "state_ctrl": "state[0] uses zero ctrl; state[k>0] retains action[k-1] during mj_forward. Acceleration sensors therefore use the just-completed interval's control, before the next action is applied.",
                     "action_time": "Nominal interval start time; state_time is actual MuJoCo time with floating-point roundoff",
                     "trajectory_csv": "401 state rows. Outgoing action columns are populated for rows 0..399 and blank on final state row 400.",
                     "units": {"time": "s", "qpos": "rad", "qvel": "rad/s", "qacc": "rad/s^2", "motor_action": "N*m", "velocity_action": "rad/s"}},
        "sensors": sensors,
        "arrays": {key: {"shape": list(value.shape), "dtype": str(value.dtype)} for key, value in arrays.items()},
        "images": rendering,
        "validation": {"states": state_validation, "media": rendering["validation"], "npz_roundtrip_exact": True,
                       "csv_state_rows": len(rows), "csv_action_rows": 400},
        "outputs": {name: {"bytes": (output / name).stat().st_size, "sha256": sha256(output / name)}
                    for name in ("episode.npz", "trajectory.csv", "overview.mp4", "overview.png", "camera.png")},
    }
    (output / "manifest.json").write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    summary = {"directory": str(output), "run_id": run_id, "state_count": 401, "action_count": 400, "sensor_count": 6,
               "sensor_dimensions": 15, "duration_s": DURATION, "video_frames": 200, "video_fps": 25,
               "validation_passed": True, "maximum_repeatability_error": state_validation["independent_rollout_max_absolute_error"],
               "model_sha256": manifest["source"]["model_sha256"], "source_commit": manifest["source"]["commit"]}
    (output / "summary.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    latest = {"directory": str(output), "relative_directory": f"outputs/{run_id}", "run_id": run_id,
              "manifest": str(output / "manifest.json"), "summary": str(output / "summary.json")}
    temporary = ROOT / "outputs" / f".latest-{uuid.uuid4().hex}.json"
    temporary.write_text(json.dumps(latest, indent=2) + "\n", encoding="utf-8")
    temporary.replace(ROOT / "outputs/latest.json")
    print(json.dumps(summary, indent=2), flush=True)


if __name__ == "__main__":
    main()
