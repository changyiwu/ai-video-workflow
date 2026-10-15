---
name: new-film
description: 在 ai-video-workflow 專案開一支新的 AI 短片：把 pipeline/template_local/ 複製成 films/<片名>/ 並建好劇本、製作紀錄。當使用者說「開新片」「做一支新片」「建新片資料夾」「新片叫 XXX」時使用。只用在 ai-video-workflow 這個 repo；不在這個 repo 裡就停下來問使用者。
---

# 開新片

## 步驟

1. **確認在 ai-video-workflow 裡**：從目前資料夾往上找，要同時有 `tools/new_film.py` 和 `pipeline/template_local/`，那一層就是 `<repo>`。找不到就停下來，問使用者 repo 在哪，不要自己複製範本。
2. **確認片名**：使用者沒給就問。片名就是資料夾名稱（可用中文），不能含 `< > : " / \ | ? *`，也不能叫「角色」。
3. **執行**（Windows 先 `set PYTHONUTF8=1`，或用 `<repo>\tools\new_film.cmd <片名>`）：
   ```
   python <repo>/tools/new_film.py <片名>
   ```
   - 已經有同名的片會直接停下來，不覆蓋。換片名，或問使用者要不要接著做那支片。
   - `films/AGENTS.md` 不存在時，腳本會從 `templates/AGENTS_TEMPLATE.md` 建一份；提醒使用者把頻道名稱、主角等佔位改掉。
4. **回報**：建立了哪些檔，並提醒 `film.json` 裡還是範例片〈被狗吃掉的作業〉的角色、場景、鏡表。
5. **建議下一步**（不要自己接著做，等使用者說）：
   1. 用 `ai-drama` 技能寫 `films/<片名>/劇本.md`
   2. 把角色、場景、鏡表填進 `film.json`（欄位見 `pipeline/template_local/README.md`）
   3. 照 `pipeline/template_local/README.md` 跑 `make_film.py`，三個人工關卡都要給使用者看

## 不要做的事

- 不要手動複製 `pipeline/template_local/`（會帶到 `out/`、`__pycache__`）。
- 不要把片放在 `pipeline/` 底下：自己的片一律放 `films/`（不進公開 repo）。
