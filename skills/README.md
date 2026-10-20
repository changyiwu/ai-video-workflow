# skills：做片用的 agent 技能

| 資料夾 | 用途 |
|---|---|
| `ai-film/` | 做片全流程：開新片（`tools/new_film.py`）→ 需求訪談 → 編劇與鏡表 →（選用）Blender 預演 → 填 `film.json` → `make_film.py` 三個人工關卡 → 自審交付。編劇部分改寫自 AI-drama-pound（MIT，見 `ai-film/NOTICE.md`） |

`ai-film/` 的結構：`SKILL.md` 是全片流程與「現在該讀哪份」的對照，細節依階段放在 `references/`（`interview.md`、`script/`、`previs/`、`film-json.md`、`production.md`、`review.md`）。2026-10-15 由 `ai-drama`、`blender-previs`、`new-film` 三個技能合併而成。

本資料夾是技能的**原始檔**，agent 不會直接從這裡載入。裝成全域技能：說「同步技能」，交給全域技能 `skill-sync` 覆蓋到各 agent 的技能目錄；改了這裡的檔案要再同步一次。技能要用的腳本放在 `tools/`，不要放進技能資料夾（全域副本不在 repo 裡，找不到 repo 的檔案）。

做片入口範本在 [`templates/AGENTS_TEMPLATE.md`](../templates/AGENTS_TEMPLATE.md)：`new_film.py` 在 `films/AGENTS.md` 不存在時會自動複製過去並加 `CLAUDE.md` 橋接，不用手動建。

> 編劇與預演的 references 原寫於上游早期（2026-08～09，雲端 Seedance、每段 30 秒、`角色資產/`、voice-clone 技能），2026-10-15 併入 `ai-film` 時已改成本 repo 的做法（本機 H3 單鏡 ≤12 秒、`films/角色/<角色>/README.md`、VoxCPM2、首幀預設 Image 2.5、定稿 DMAD 4 步不開 EasyCache）。若還看到跟 `docs/` 衝突的說法，以 `docs/` 為準並回頭修技能。

協作方法（知識庫分層、記憶、工作習慣）見 [docs/05_agent協作與知識庫.md](../docs/05_agent協作與知識庫.md)。
