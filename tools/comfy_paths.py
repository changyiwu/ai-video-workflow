"""ComfyUI 的 input／output 資料夾在哪：Comfy Desktop 放在 ComfyUI 資料夾外（ComfyUI-Shared\\input、output），不能假設是 COMFY_DIR\\input。

順序：環境變數 COMFY_INPUT_DIR／COMFY_OUTPUT_DIR → 問執行中的 ComfyUI（/system_stats 的啟動參數
--input-directory／--output-directory／--base-directory）→ COMFY_DIR\\input、COMFY_DIR\\output。
"""
import json
import os
import urllib.request
from pathlib import Path

HOST = os.environ.get("COMFY_HOST", "http://127.0.0.1:8188")
COMFY_DIR = Path(os.environ.get("COMFY_DIR", r"C:\AI\H3\ComfyUI-0.36.0"))


_ARGS = {}


def _server_args(host):
    if host not in _ARGS:  # 只快取成功的結果：伺服器還沒起來時下次再問
        try:
            with urllib.request.urlopen(host + "/system_stats", timeout=5) as r:
                _ARGS[host] = tuple(json.loads(r.read().decode()).get("system", {}).get("argv", []))
        except Exception:
            return ()
    return _ARGS[host]


def _arg(argv, flag):
    for i, a in enumerate(argv):
        if a == flag and i + 1 < len(argv):
            return argv[i + 1]
        if a.startswith(flag + "="):
            return a.split("=", 1)[1]
    return None


def _dir(kind, host):
    env = os.environ.get(f"COMFY_{kind.upper()}_DIR")
    if env:
        return Path(env)
    argv = _server_args(host or HOST)
    d = _arg(argv, f"--{kind}-directory")
    if d:
        return Path(d)
    base = _arg(argv, "--base-directory")
    return Path(base) / kind if base else COMFY_DIR / kind


def input_dir(host=None):
    return _dir("input", host)


def output_dir(host=None):
    return _dir("output", host)
