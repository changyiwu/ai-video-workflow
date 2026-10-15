# skills：做片用的 agent 技能

| 資料夾 | 用途 |
|---|---|
| `ai-drama/` | 編劇技能：九階段流程、16:9 劇本格式、片段切分、審稿清單（改寫自 AI-drama-pound，MIT，見 NOTICE.md） |
| `blender-previs/` | Blender 預演技能：需求訪談、鏡位契約、布置圖規則、提示詞包、檢查清單 |
| `new-film/` | 開新片：執行 `tools/new_film.py`，把 `pipeline/template_local/` 複製成 `films/<片名>/` |

本資料夾是技能的**原始檔**，agent 不會直接從這裡載入。裝成全域技能：說「同步技能」，交給全域技能 `sync-skills` 覆蓋到各 agent 的技能目錄；改了這裡的檔案要再同步一次。

做片入口範本在 [`templates/AGENTS_TEMPLATE.md`](../templates/AGENTS_TEMPLATE.md)：複製到做片資料夾改名 `AGENTS.md`（Claude Code 另加一行 `@AGENTS.md` 的 `CLAUDE.md` 橋接）。

> ⚠️ 兩個技能寫於專案早期（2026-08～09），references 裡還有幾處舊說法，用的時候以 `docs/` 為準（`ai-drama/SKILL.md` 開頭已寫明怎麼對應）：
> - 「Seedance 2.5、每段 30 秒」→ 本機 H3、單鏡 ≤12 秒、對話靠切鏡
> - 「主角」「角色資產/<主角>/角色設定.md」→ 佔位例子，請換成你自己的角色設定檔
> - 「voice-clone 技能」→ VoxCPM2（`make_voxcpm.cmd`；選用 BreezyVoice `make_breezyvoice.cmd`）
> - 首幀 → 本 repo 預設 OpenAI Image 2.5 附定妝照，本機 Qwen-Image-Edit 2511 為備選；定稿用 DMAD 4 步
> - 「14 步＋EasyCache」→ 定稿不開 EasyCache

協作方法（知識庫分層、記憶、工作習慣）見 [docs/05_agent協作與知識庫.md](../docs/05_agent協作與知識庫.md)。
