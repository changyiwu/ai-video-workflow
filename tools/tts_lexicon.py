"""讀音替換表（tts-lexicon.md）：送進 TTS 前把念錯的詞換成念得對的寫法，字幕照原文。2026-10-20 從 agent-video-specs 移植。
表在 repo 根目錄的 tts-lexicon.md，格式與規則寫在表的開頭。agent-video-specs 根目錄也有一份同格式的表（兩個 repo 都公開，
各自單獨下載就能用）；兩個 repo 放在同一層時兩份合併讀取，通用條目兩份都要加。

找表的順序（近的覆蓋遠的，同一個原文以近的為準）：
  同層 agent-video-specs 的 tts-lexicon.md（有就合併）
  → 本 repo 的表：TTS_LEXICON（有設就用它）或 repo 根目錄的 tts-lexicon.md
  → 從起點資料夾（例如 films/<類型>/<片名>/out/）往上每一層的 tts-lexicon.md（片子資料夾放一份只對該片生效）。
本專案套用的地方：voxcpm_batch.py（念台詞前）、gen_voice.py（edge-tts 答案卷、單句生成）、voice_pick.py（聽寫比對的標準）、
recast.py voice。每段文字只套一次；film.json 的 "tts" 照樣可用，表會再套在它上面。

試表（Voice venv 或任何 Python）：python tools/tts_lexicon.py [起點資料夾] "要念的句子" """
import os
import re
import sys
from pathlib import Path

NAME = "tts-lexicon.md"
REPO = Path(__file__).resolve().parents[1]
SIBLING = REPO.parent / "agent-video-specs" / NAME   # 同層另一個 repo 的同名表，有就合併
HEAD = ("原文", "改寫")


def master():
    p = os.environ.get("TTS_LEXICON")
    return Path(p).expanduser() if p else REPO / NAME


def lexicon_files(start=None):
    """回傳要讀的表，遠的在前、近的在後"""
    files = [SIBLING, master()]
    if start:
        s = Path(start).resolve()
        s = s.parent if s.is_file() else s
        files += reversed([d / NAME for d in (s, *s.parents)])
    seen, out = set(), []
    for f in files:
        if f.is_file() and f.resolve() not in seen:
            seen.add(f.resolve()); out.append(f)
    return out


def cells(line):
    s = line.strip()[1:]                                 # 去掉開頭的 |
    if s.endswith("|") and not s.endswith("\\|"):
        s = s[:-1]
    out = []
    for c in re.split(r"(?<!\\)\|", s):
        c = c.strip().replace("\\|", "|")
        if len(c) >= 2 and c[0] == c[-1] == "`":         # `GPT four` 這種用反引號標出空白的寫法
            c = c[1:-1]
        out.append(c)
    return out


def parse(path):
    """只讀表頭是「原文｜改寫」的 Markdown 表格；其他段落、表格都當說明"""
    table, inside = {}, False
    for n, line in enumerate(Path(path).read_text(encoding="utf-8-sig").splitlines(), 1):
        if not line.lstrip().startswith("|"):
            inside = False
            continue
        c = cells(line)
        if tuple(c[:2]) == HEAD:
            inside = True
            continue
        if not inside or all(re.fullmatch(r":?-+:?", x) for x in c if x):
            continue
        if len(c) < 2 or not c[0] or not c[1]:
            raise SystemExit(f"{path}:{n} 格式不對（| 原文 | 改寫 | 說明 |，原文、改寫都不能空）：{line}")
        table[c[0]] = c[1]
    return table


def load_lexicon(start=None, quiet=False):
    table = {}
    files = lexicon_files(start)
    for f in files:
        table.update(parse(f))
    if not quiet:
        print(f"[lexicon] 讀音替換表 {len(table)} 條：" + ("、".join(str(f) for f in files) if files else f"找不到 {NAME}，不做替換"), flush=True)
    return table


def speakable(text, table):
    """長的原文先比對，一次掃完：換過的結果不會再被其他條目換"""
    if not table:
        return text
    pat = re.compile("|".join(re.escape(k) for k in sorted(table, key=len, reverse=True)))
    return pat.sub(lambda m: table[m.group(0)], text)


if __name__ == "__main__":
    a = sys.argv[1:]
    if not a:
        sys.exit(__doc__)
    start, text = (a[0], a[1]) if len(a) > 1 else (None, a[0])
    for s in (sys.stdout, sys.stderr):
        try:
            s.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass
    print(speakable(text, load_lexicon(start)))
