"""VoxCPM2（OpenBMB，Apache-2.0）批次生成：模型只載一次。2026-10-14 起本專案的預設配音引擎（角色聲音設計＋台詞都用它）。
挑選沿用 breezyvoice_pick.py（ASR 必須全對＋對照 edge-tts 台灣國語參考音的腔調分數，候選檔名格式相同）。

執行（Voice venv；同一個 cmd 視窗先 call <repo>\\configs\\profile.cmd）：
  "%PY_VOICE%" <repo>\\tools\\voxcpm_batch.py jobs.json

jobs.json（相對路徑以 jobs.json 所在資料夾為準）：
{"out_dir": "voice", "seeds": 8,
 "jobs": [{"name": "ref_zhe", "text": "參考音要念的句子", "control": "聲音描述（英文）", "seed": 7},          ← 聲音設計：單一檔 <out_dir>/<name>.wav
          {"name": "line0", "text": "台詞", "ref_audio": "voice/ref_zhe.wav", "seeds": 8 (選填)}]}       ← 台詞：<out_dir>/cand/<name>_s<seed>.wav
規則：job 有 "seed" → 生一個檔；沒有 → 生 seeds 個候選（給 breezyvoice_pick.py 挑）。有 "ref_audio" 就照它的聲音念（克隆），有 "control" 就照描述設計聲音。
已存在的檔案跳過；紀錄 <out_dir>/vox_log.jsonl。

送進模型前的文字處理（字幕仍用原文）：
- 繁轉簡（繁體字讀音較不穩，原專案實測）。
- VoxCPM2 不支援注音標記：「連假[:ㄐㄧㄚ4]」的標記會被拿掉並印警告；念不準的字請改同音字（寫在 film.json 該句的 "tts"）。
- 阿拉伯整數轉國字；刪節號、破折號改逗號。單字台詞常念成亂音，請寫成兩三個字。"""
import json
import os
import re
import sys
import time
from pathlib import Path

MODEL_PATH = Path(os.environ.get("AI_ROOT", r"C:\AI")) / "Voice" / "models" / "VoxCPM2"  # AI_ROOT = install root (default C:\AI)
DIG = "零一二三四五六七八九"


def int_zh(n):
    if n < 10:
        return DIG[n]
    if n < 100:
        t, o = divmod(n, 10)
        return ("" if t == 1 else DIG[t]) + "十" + (DIG[o] if o else "")
    if n < 1000:
        h, r = divmod(n, 100)
        return DIG[h] + "百" + ("" if r == 0 else ("零" + DIG[r] if r < 10 else ("一" + int_zh(r) if r < 20 else int_zh(r))))
    return "".join(DIG[int(c)] for c in str(n))      # 年份等大數：逐字念


def make_t2s():
    import opencc
    for cfg in ("t2s", "t2s.json"):                   # opencc（官方）與 opencc-python-reimplemented 的設定名寫法不同
        try:
            return opencc.OpenCC(cfg).convert
        except Exception:
            pass
    raise RuntimeError("opencc 無法載入 t2s 設定")


def prep(text, t2s):
    if "[:" in text:
        print(f"[warn] VoxCPM2 不支援注音標記，已拿掉：{text}（念錯請改同音字）", flush=True)
        text = re.sub(r"\[:[^\]]*\]", "", text)
    text = re.sub(r"\d+", lambda m: int_zh(int(m.group())), text)
    return t2s(text.replace("……", "，").replace("——", "，").replace("～", "！").strip())


def main():
    spec_path = Path(sys.argv[1]).resolve()
    spec = json.loads(spec_path.read_text(encoding="utf-8-sig"))
    base = spec_path.parent
    out = (base / spec.get("out_dir", "voice")).resolve()
    out.mkdir(parents=True, exist_ok=True)
    rp = lambda p: str(Path(p) if Path(p).is_absolute() else (base / p).resolve())

    import soundfile as sf
    import torch
    from voxcpm import VoxCPM
    if not MODEL_PATH.exists():
        sys.exit(f"VoxCPM2 model path does not exist: {MODEL_PATH}")
    t2s = make_t2s()
    t0 = time.time()
    model = VoxCPM.from_pretrained(str(MODEL_PATH), load_denoiser=False, optimize=False, device="cuda")
    sr = model.tts_model.sample_rate
    print(f"[load] {time.time() - t0:.1f}s", flush=True)

    for j in spec["jobs"]:
        text = prep(j["text"], t2s)
        if j.get("control"):                         # 聲音設計："(描述)文字"；不給參考音就設計一個新聲音
            text = f"({j['control'].strip()}){text}"
        if "seed" in j:
            todo = [(int(j["seed"]), out / f"{j['name']}.wav")]
        else:
            (out / "cand").mkdir(exist_ok=True)
            todo = [(s, out / "cand" / f"{j['name']}_s{s}.wav") for s in range(1, int(j.get("seeds", spec.get("seeds", 8))) + 1)]
        kw = dict(text=text, cfg_value=float(j.get("cfg", spec.get("cfg", 2.0))), inference_timesteps=int(j.get("steps", spec.get("steps", 10))),
                  normalize=False, denoise=False)
        if j.get("ref_audio"):
            kw["reference_wav_path"] = rp(j["ref_audio"])
        for seed, dst in todo:
            if dst.exists():
                continue
            torch.manual_seed(seed)
            torch.cuda.manual_seed_all(seed)
            t = time.time()
            wav = model.generate(**kw)
            sf.write(str(dst), wav, sr, subtype="PCM_16")
            rec = {"name": j["name"], "seed": seed, "file": dst.name, "text": j["text"], "tts_input": text,
                   "gen_s": round(time.time() - t, 2), "audio_s": round(len(wav) / sr, 2)}
            with open(out / "vox_log.jsonl", "a", encoding="utf-8") as f:
                f.write(json.dumps(rec, ensure_ascii=False) + "\n")
            print(f"[ok] {dst.name} {rec['gen_s']}s", flush=True)
    print(f"[done] total {time.time() - t0:.0f}s peak_vram {torch.cuda.max_memory_allocated() / 2**30:.2f}GB", flush=True)


if __name__ == "__main__":
    main()
