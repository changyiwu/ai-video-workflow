"""開新片：把 pipeline/template_local/ 複製成 films/<片名>/。

用法：python tools/new_film.py <片名>

- 只複製 film.json、make_film.py、review.py（跳過 out/、__pycache__、README.md；說明請看範本的 README.md）。
- film.json 的 title 換成片名，repo_dir 維持 "../.."。
- 另外建空的 劇本.md、製作紀錄.md。
- films/AGENTS.md 不存在時（新電腦、新頻道），從 templates/AGENTS_TEMPLATE.md 建一份，並加 CLAUDE.md 橋接。
- films/<片名>/ 已存在就停下來，不覆蓋。
"""
import json
import re
import shutil
import sys
from datetime import date
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
TEMPLATE = REPO / "pipeline" / "template_local"
FILMS = REPO / "films"
COPY = ["film.json", "make_film.py", "review.py"]
BAD_CHARS = '<>:"/\\|?*'


def main():
    if len(sys.argv) != 2 or not sys.argv[1].strip():
        sys.exit("用法：python tools/new_film.py <片名>")
    name = sys.argv[1].strip()
    if any(c in name for c in BAD_CHARS) or name in (".", "..") or name == "角色":
        sys.exit(f"片名不能用：{name!r}（不能含 {BAD_CHARS}，也不能叫「角色」）")

    dst = FILMS / name
    if dst.exists():
        sys.exit(f"已經有這支片了，不覆蓋：{dst}")

    created = []
    if not (FILMS / "AGENTS.md").exists():
        FILMS.mkdir(exist_ok=True)
        shutil.copyfile(REPO / "templates" / "AGENTS_TEMPLATE.md", FILMS / "AGENTS.md")
        (FILMS / "CLAUDE.md").write_text("@AGENTS.md\n", encoding="utf-8")
        created += ["films/AGENTS.md（從 templates/AGENTS_TEMPLATE.md 建立，請改成自己的頻道規則）", "films/CLAUDE.md"]

    dst.mkdir(parents=True)
    for f in COPY:
        shutil.copy2(TEMPLATE / f, dst / f)

    # 只換 title 那一行，保留 film.json 原本的排版
    fj = dst / "film.json"
    text = fj.read_text(encoding="utf-8")
    text, n = re.subn(r'^(\s*"title":\s*)".*?"', lambda m: m.group(1) + json.dumps(name, ensure_ascii=False),
                      text, count=1, flags=re.M)
    if n != 1:
        sys.exit("film.json 找不到 title 欄位，範本格式可能改了")
    cfg = json.loads(text)  # 確認仍是合法 JSON
    if cfg.get("repo_dir") != "../..":
        print(f"注意：film.json 的 repo_dir 是 {cfg.get('repo_dir')!r}，放在 films/<片名>/ 應該是 \"../..\"")
    fj.write_text(text, encoding="utf-8")

    today = date.today().isoformat()
    (dst / "劇本.md").write_text(f"# {name}：劇本\n\n> 用 ai-drama 技能寫；定稿後把鏡表填進 film.json 的 shots。\n", encoding="utf-8")
    (dst / "製作紀錄.md").write_text(f"# {name}：製作紀錄\n\n## {today} 開新片\n\n- 從 pipeline/template_local/ 建立。\n", encoding="utf-8")

    for c in created:
        print("建立", c)
    print(f"建立 films/{name}/：{'、'.join(COPY)}、劇本.md、製作紀錄.md")
    print("film.json 目前還是範例片〈被狗吃掉的作業〉的角色、場景與鏡表，要換成自己的。")
    print("下一步：用 ai-drama 技能寫劇本 → 填 film.json → 照 pipeline/template_local/README.md 跑 make_film.py")


if __name__ == "__main__":
    main()
