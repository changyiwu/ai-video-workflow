"""Reference video -> pose (skeleton) control video for H3 Fun ControlNet (h3_shot.py spec "control").

Runs ComfyUI's built-in nodes: RT-DETR v4 finds the person each frame, SDPose (whole-body) extracts keypoints
inside that box, SDPoseDrawKeypoints draws them on black. Frames come back as PNG and are encoded here at 24 fps,
fit + padded to the H3 size (default 1344x768, 16:9; a 4:3 source gets black side bars).

Prereqs: setup/downloads_funcontrol.json (sdpose_wholebody_fp16 + rt_detr_v4-x-hgnet_fp16); ComfyUI running
(tools\\start_comfy.cmd).

Usage:
  python <repo>/tools/pose_video.py --video in.mp4 --start 2.833 --end 16 --out pose.mp4 [--no-face] [--preview]
  --preview also writes <out>_preview.mp4: the source with the skeleton drawn on top, to check alignment.
Single-person footage only (keeps the most confident person per frame; --people N for more).
"""
import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile
import time
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import comfy_paths  # noqa: E402  input／output 資料夾（Comfy Desktop 不在 COMFY_DIR 底下）

HOST = os.environ.get("COMFY_HOST", "http://127.0.0.1:8188")
FPS = 24
SDPOSE = "sdpose_wholebody_fp16.safetensors"
RTDETR = "rt_detr_v4-x-hgnet_fp16.safetensors"


def req(path, data=None, timeout=60):
    r = urllib.request.Request(HOST + path, data=json.dumps(data).encode() if data is not None else None,
                               headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(r, timeout=timeout) as f:
        return json.loads(f.read().decode())


def fit_pad(w, h):
    return f"scale={w}:{h}:force_original_aspect_ratio=decrease:flags=lanczos,pad={w}:{h}:(ow-iw)/2:(oh-ih)/2:black,setsar=1"


def build_graph(video, tag, a):
    return {
        "1": {"class_type": "LoadVideo", "inputs": {"file": video}},
        "2": {"class_type": "GetVideoComponents", "inputs": {"video": ["1", 0]}},
        "3": {"class_type": "UNETLoader", "inputs": {"unet_name": RTDETR, "weight_dtype": "default"}},
        "4": {"class_type": "RTDETR_detect", "inputs": {"model": ["3", 0], "image": ["2", 0], "threshold": a.det_threshold,
                                                        "class_name": "person", "max_detections": a.people}},
        "5": {"class_type": "CheckpointLoaderSimple", "inputs": {"ckpt_name": SDPOSE}},
        "6": {"class_type": "SDPoseKeypointExtractor", "inputs": {"model": ["5", 0], "vae": ["5", 2], "image": ["2", 0],
                                                                  "batch_size": 16, "bboxes": ["4", 0]}},
        "7": {"class_type": "SDPoseDrawKeypoints", "inputs": {"keypoints": ["6", 0], "draw_body": True, "draw_hands": not a.no_hands,
                                                              "draw_face": not a.no_face, "draw_feet": a.feet, "stick_width": a.stick,
                                                              "face_point_size": 3, "score_threshold": a.threshold, "draw_head": True}},
        "8": {"class_type": "SaveImage", "inputs": {"images": ["7", 0], "filename_prefix": f"pose_video/{tag}/f"}},
    }


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--video", required=True)
    ap.add_argument("--out", required=True, help="output pose video (.mp4)")
    ap.add_argument("--start", type=float, default=0.0, help="seconds")
    ap.add_argument("--end", type=float, default=None, help="seconds (default: end of video)")
    ap.add_argument("--size", default="1344x768", help="output WxH; source is fit + black-padded")
    ap.add_argument("--max-height", type=int, default=1080, help="detect on frames at most this tall")
    ap.add_argument("--no-face", action="store_true", help="skip the 68 face points (e.g. the new character is not human)")
    ap.add_argument("--no-hands", action="store_true")
    ap.add_argument("--feet", action="store_true", help="also draw the 6 foot points")
    ap.add_argument("--stick", type=int, default=4, help="limb line width at detection resolution")
    ap.add_argument("--threshold", type=float, default=0.3, help="keypoint score threshold")
    ap.add_argument("--det-threshold", type=float, default=0.4, help="person detection threshold")
    ap.add_argument("--people", type=int, default=1)
    ap.add_argument("--preview", action="store_true")
    a = ap.parse_args()

    src, out = Path(a.video).resolve(), Path(a.out).resolve()
    out.parent.mkdir(parents=True, exist_ok=True)
    w, h = (int(v) for v in a.size.lower().split("x"))
    try:
        req("/system_stats", timeout=5)
    except Exception:
        sys.exit(f"ComfyUI is not answering at {HOST}; start it with tools\\start_comfy.cmd")

    tag = f"{out.stem}_{int(time.time())}"
    trim = ["-ss", f"{a.start:.3f}"] + (["-to", f"{a.end:.3f}"] if a.end is not None else [])
    stage_dir = comfy_paths.input_dir(HOST) / "pose_video"
    stage_dir.mkdir(parents=True, exist_ok=True)
    staged = stage_dir / f"{tag}.mp4"
    # Trim + resample to 24 fps first, so the pose frames line up 1:1 with the H3 frames.
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(src), *trim, "-an",
                    "-vf", f"fps={FPS},scale=-2:'min({a.max_height},ih)':flags=lanczos", "-c:v", "libx264", "-crf", "10",
                    "-pix_fmt", "yuv420p", str(staged)], check=True)

    g = build_graph(f"pose_video/{staged.name}", tag, a)
    t0 = time.time()
    pid = req("/prompt", {"prompt": g})["prompt_id"]
    print(f"[queued] {tag}", flush=True)
    while True:
        time.sleep(3)
        hist = req(f"/history/{pid}")
        if pid in hist:
            break
    e = hist[pid]
    if e.get("status", {}).get("status_str") != "success":
        sys.exit(json.dumps(e.get("status", {}), ensure_ascii=False)[:3000])
    frames = [comfy_paths.output_dir(HOST) / "pose_video" / tag / im["filename"] for im in e["outputs"]["8"]["images"]]

    with tempfile.TemporaryDirectory() as td:
        lst = Path(td) / "frames.txt"
        lst.write_text("".join(f"file '{f.as_posix()}'\nduration {1 / FPS:.6f}\n" for f in frames), encoding="utf-8")
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", str(lst), "-r", str(FPS),
                        "-vf", fit_pad(w, h), "-c:v", "libx264", "-crf", "12", "-preset", "slow", "-pix_fmt", "yuv420p", str(out)],
                       check=True)
    if a.preview:
        prev = out.with_name(out.stem + "_preview.mp4")
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(staged), "-i", str(out),
                        # blend in RGB: screen-blending YUV planes tints everything magenta
                        "-filter_complex", f"[0:v]{fit_pad(w, h)},format=gbrp[s];[1:v]format=gbrp[p];[s][p]blend=all_mode=screen,format=yuv420p",
                        "-c:v", "libx264", "-crf", "18",
                        "-pix_fmt", "yuv420p", str(prev)], check=True)
        print(f"[preview] {prev}")
    shutil.rmtree(comfy_paths.output_dir(HOST) / "pose_video" / tag, ignore_errors=True)
    staged.unlink(missing_ok=True)
    print(f"[ok] {out}  {len(frames)} frames ({len(frames) / FPS:.2f}s)  {time.time() - t0:.0f}s", flush=True)


if __name__ == "__main__":
    main()
