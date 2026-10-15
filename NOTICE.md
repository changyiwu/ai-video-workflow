# 來源與作者（NOTICE）

本專案是以下開源專案的修改版（fork），**原作者與授權資訊必須保留**：

| 項目 | 內容 |
|---|---|
| 上游專案 | [mathruffian-dot/shanshiba-workflow-16gvram-64gram](https://github.com/mathruffian-dot/shanshiba-workflow-16gvram-64gram) |
| 原作者 | 山獅霸的多重宇宙（<https://github.com/mathruffian-dot>） |
| 取得版本 | 2026-10-11，`main` 分支 commit `32f0267` |
| 程式碼授權 | MIT，見 [LICENSE](LICENSE)（`tools/flashvsr_cli.py` 例外為 GPL-3.0-or-later，見檔頭） |
| 文件與素材授權 | CC BY-NC 4.0（姓名標示、非商業），見 [LICENSE-docs.md](LICENSE-docs.md) |
| 第三方模型與工具 | 各自授權，見 [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md) |
| 編劇技能上游 | `agent/skills/ai-drama/` 改寫自 [POUND0423/AI-drama-pound](https://github.com/POUND0423/AI-drama-pound)（MIT），見該資料夾 `NOTICE.md` 與 `LICENSE-AI-drama-pound.txt` |

上游作者的其他硬體版本（本專案為 16GB VRAM＋64GB RAM 版）：

| 上游 repo | 硬體 |
|---|---|
| [shanshiba-workflow-32gvram-64gram](https://github.com/mathruffian-dot/shanshiba-workflow-32gvram-64gram) | 32GB VRAM＋64GB RAM |
| [shanshiba-workflow-16gvram-64gram](https://github.com/mathruffian-dot/shanshiba-workflow-16gvram-64gram) | 16GB VRAM＋64GB RAM（本專案來源） |
| [shanshiba-workflow-16gvram-32gram](https://github.com/mathruffian-dot/shanshiba-workflow-16gvram-32gram) | 16GB VRAM＋32GB RAM |
| [shanshiba-workflow-colab](https://github.com/mathruffian-dot/shanshiba-workflow-colab) | Google Colab 雲端 |

## 本分支的修改（2026-10-11，changyiwu）

- 移除原作者個人資訊：本人克隆聲音的名稱與相關描述、頻道品牌名稱、頻道宣傳文字、作者個人 repo 連結（只保留在本檔與授權檔作為來源標示）。
- 原頻道固定主角的名稱：在技能文件中改為佔位的「主角」／「阿凱」；在 `pipeline/example_D-7/` 範例中改為「老師」。
- 編劇技能資料夾 `agent/skills/shanshiba-drama/` 改名為 `agent/skills/ai-drama/`，所有引用路徑同步更新。
- 片尾範本預設標題改為「我的頻道」（請在 config 的 `title` 改成自己的頻道名）。
- `pipeline/example_D-7/youtube/影片資訊_metadata.md` 去除頻道名稱與標籤，改為 `<你的頻道名>` 佔位。
- README 改寫為本分支版本；新增本檔；`LICENSE` 追加本分支修改者版權行；`LICENSE-docs.md` 追加修改聲明。
- 新增 RTX Spark 筆電（Windows on Arm）支援：`configs/profile_rtxspark.cmd`、`docs/hardware_rtxspark.md`、`setup/spark_check.py`、`setup/env/arm64/`；`setup/detect_hardware.py` 加入 ARM64／統一記憶體偵測。
- 生圖預設改為 OpenAI Image 2.5、本機 Qwen 為備選：`tools/gen_image.py` 新增 `--backend`／`IMAGE_BACKEND`／`IMAGE_FALLBACK`；`make_film.py` 片尾名單依實際後端；`run_demo.py`、`smoke_test.py` 固定本機（它們是安裝驗證）。
- 文件補上無 API 金鑰時的替代生圖路線：改呼叫全域技能 `agent-draw`（交給 Codex CLI 以 ChatGPT 訂閱生圖），見 `README.md`、`docs/06_安裝.md` §6。
- 2026-10-14 配音預設引擎改為 VoxCPM2（聲音設計＋台詞），Breeze TTS 2＋BreezyVoice 改為選用（`VOICE_ENGINE=breezyvoice`）：新增 `tools/voxcpm_batch.py`、`tools/make_voxcpm.cmd`；修改 `pipeline/template_local/make_film.py`、`film.json`、`pipeline/demo_local/run_demo.py`、`setup/smoke_test.py`、`setup/detect_hardware.py`，以及 `README.md`、`AGENT_SETUP.md`、`docs/01`、`docs/02`、`docs/03`、`docs/06`、`docs/hardware_rtxspark.md`、`THIRD_PARTY_NOTICES.md`、`agent/` 下的說明與 `agent/skills/ai-drama/SKILL.md`。
- 2026-10-14 聽寫（ASR）加 openai-whisper 備援（給 Windows on Arm 用）：`tools/stt.py` 新增 `load_asr()`，`tools/breezyvoice_pick.py`、`pipeline/template_local/review.py` 改用它。
- 2026-10-14 `nvidia-vfx` 升到 0.2.0.0（API 向下相容，`tools/upscale_vsr.py` 不用改；0.2.0.0 起在 pypi.nvidia.com 有 win_arm64 版）：更新 `setup/env/requirements_h3_venv.txt`、`requirements_voice_venv.txt` 與重產的 ARM64 清單；`setup/spark_check.py` 改為也查 pypi.nvidia.com；更正 `configs/profile_rtxspark.cmd`、`docs/hardware_rtxspark.md`、`setup/detect_hardware.py` 中「RTX VSR 沒有 ARM64 版」的說法。
- 2026-10-14 `setup/spark_check.py` 修正：win_arm64 wheel 要符合 Python 版本才算可裝；自動找 ARM64 替代版只接受同一個大版號；`triton-windows` 改註明有 ARM64 版但先不裝。重產 ARM64 清單（numba 0.68、llvmlite 0.50；cryptography 回到原版本），`docs/hardware_rtxspark.md` 更新掃描結果。
- 2026-10-14 `agent/CLAUDE.md範本.md`、`README.md` 釐清首幀指令 `--model qwen-edit` 只在退回本機時作用（預設 Image 2.5 時不作用）。
- 2026-10-14 `agent/skills/ai-drama/NOTICE.md` 改動表中上游頻道固定主角的名稱改為佔位說法（原作者署名不變）。
- 2026-10-14 編劇技能 `agent/skills/ai-drama/` 改成本機 H3 版本：`references/workflow.md` 全文改寫為白話；`references/segmentation.md` 由「≤30 秒片段＋LoRA caption」改寫為「每鏡 ≤12 秒的鏡表」並對應 `film.json`（移除上游角色資產檔名與服裝）；`references/checklists.md` 的技術可行性與切分段落、`references/format.md`、`SKILL.md` 版本說明同步更新。
- 2026-10-14 Blender 預演技能 `agent/skills/blender-previs/` 移除指向上游私人知識庫的路徑（`專案現況.md`、`資源索引/AI短片/…`、`角色資產/…`、上游片的 `.blend`）：`SKILL.md`〈開工前必讀〉改指 `handoff.md`、`films/`、`docs/`，〈固定規格〉生圖改為 Image 2.5 預設；`references/shot-contract.md`「現成可沿用（小吃店）」改寫為「沿用既有場景」；`references/interview.md`、`references/checklists.md` 路徑同步更新。上游片的版本代號（`v5`、`V5_` 物件前綴、`eatery_v5_reusable.blend`、鏡號實例）改為「上游範例片」與 `<前綴>_` 等通用寫法（`references/blender-rules.md`、`prompt-package.md`、`shot-contract.md`、`interview.md`）。
- 2026-10-14 Blender 改用一般安裝版（5.1 以上），操作方式改照全域技能 `agent-blender`：`docs/06_安裝.md` 移除 `C:\AI\Blender\` portable、新增 §6b；`agent/skills/blender-previs/references/blender-rules.md`〈前置〉改為背景 runner／官方 MCP 兩種模式並移除上游的外掛名稱、版本與工具名；`SKILL.md` 同步。
- 2026-10-15 工具改為直接用 repo 的 `tools/`，不再複製到 `C:\AI\tools`：`pipeline/template_local/make_film.py`、`review.py`、`pipeline/demo_local/run_demo.py`、`setup/smoke_test.py`、`setup/16gb_sim/` 的 `AI_TOOLS` 預設改為相對 repo；`tools/make_voxcpm.cmd`、`make_breezyvoice.cmd` 改用 `%~dp0`，`tools/qwen21_face_refine.py` 改用自身所在資料夾；`configs/profile*.cmd` 加 `PYTHONDONTWRITEBYTECODE=1`；`README.md`、`AGENT_SETUP.md`（§2e 移除 xcopy）、`docs/` 與 `agent/` 下文件的 `C:\AI\tools\` 改為 `<repo>\tools\`。`pipeline/example_D-7/` 為上游原樣，未改。
- 2026-10-15 支援直接使用 Comfy Desktop 的 ComfyUI：新增 `tools/comfy_paths.py`（input／output 資料夾改問執行中的 ComfyUI），`gen_image.py`、`h3_shot.py`、`gen_music3.py`、`gen_music.py`、`qwen21_face_refine.py` 改用它；`QWEN_EDIT_UNET`、`MUSIC3_DIT` 可指定模型檔名；`tools/start_comfy.ps1` 可在背景啟動 Desktop 安裝的 ComfyUI、`make_shot.ps1` 改用 `PY_H3`；`setup/download.py` 新增 `COMFY_MODELS_DIR`／`COMFY_DIR` 對應；`configs/profile.cmd` 自動偵測 Desktop；`AGENT_SETUP.md` 新增 §2a（原自行安裝改為 §2a′）、`docs/06_安裝.md` 同步。
- 2026-10-15 `agent/CLAUDE.md範本.md` 改名為 `agent/AGENTS_TEMPLATE.md`，開頭說明改為「改名 `AGENTS.md`，Claude Code 另加 `@AGENTS.md` 橋接」；`README.md`、`AGENT_SETUP.md`、`agent/README.md`、`docs/05_agent協作與知識庫.md` 的引用同步。
- 2026-10-15 移除 `agent/` 資料夾：技能改放根目錄 `skills/`（`ai-drama`、`blender-previs` 原樣搬移，`agent/README.md` 改為 `skills/README.md`），`AGENTS_TEMPLATE.md` 改放 `templates/`；新增開新片腳本 `tools/new_film.py`、`tools/new_film.cmd` 與技能 `skills/new-film/`；`README.md`、`AGENT_SETUP.md`、`LICENSE-docs.md`、`THIRD_PARTY_NOTICES.md`、`docs/02`、`docs/05`、`docs/06`、`pipeline/template_local/README.md`、`cloud/README.md` 的路徑與開新片做法同步。
- 2026-10-15 `skills/ai-drama`、`skills/blender-previs`、`skills/new-film` 合併為單一技能 `skills/ai-film/`：`ai-drama` 的 references 移到 `references/script/`（鏡表加「畫面裡的角色」單人／同框註記與「運鏡」欄），`blender-previs` 的 Blender 專用部分移到 `references/previs/`，需求訪談改為劇情面＋製作面合一的 `references/interview.md`，新增 `references/film-json.md`、`production.md`、`review.md`（由原 previs 的提示詞、鏡位契約、檢查清單中通用的部分改寫）；`ai-drama` 的 `NOTICE.md`、`LICENSE-AI-drama-pound.txt` 原樣保留在 `skills/ai-film/`。`tools/new_film.py` 另建 `需求確認.md`。`AGENTS.md`、`README.md`、`AGENT_SETUP.md`、`LICENSE-docs.md`、`THIRD_PARTY_NOTICES.md`、`docs/01`、`docs/02`、`docs/05`、`docs/06`、`templates/AGENTS_TEMPLATE.md`、`pipeline/template_local/README.md`、`tools/h3_shot.py` 註解的引用同步。
- 2026-10-15 語音環境位置改為可設定：`tools/make_voxcpm.cmd`、`make_breezyvoice.cmd` 改讀 `PY_VOICE`、`PY_BREEZYVOICE`、`AI_ROOT`（預設仍是 `C:\AI`）；`configs/profile.cmd`、`profile_rtxspark.cmd` 依 `AI_ROOT` 設定 `PY_VOICE`、`PY_BREEZE`、`PY_BREEZYVOICE` 的預設值；`AGENT_SETUP.md` 第 2 節補說明。
- 2026-10-15 `docs/06_安裝.md` §1 新增〈為什麼模型權重與 venv 不放進 repo〉，`README.md`〈這個 repo 沒有放的東西〉的模型權重一列連過去。
- 其餘程式邏輯、模型下載清單、音效（Freesound CC0）與圖片素材未修改。
- 2026-10-15 更正「`nvvfx`（RTX VSR）只有 Windows」的說法（pypi.nvidia.com 有 Linux x64 版，Colab 不裝是因為未實測）：`cloud/README.md` 踩坑表、`cloud/vm/install_full.sh` 註解、`setup/smoke_test.py` 註解與略過訊息；行為不變。
- 2026-10-15 清掉退役的 `C:\AI\tools` 路徑與上游資料夾慣例：`make_film.py`、`run_demo.py`、`tools/h3_shot.py` 的「ComfyUI 沒開」錯誤訊息改指 repo 的 `tools\start_comfy.cmd`，`tools/` 九支腳本與兩支入口腳本的用法說明改為 `<repo>\tools\`；`make_film.py`、`run_demo.py` 的 `PY_*` 預設與分軌模型資料夾改依 `AI_ROOT`；`pipeline/README.md` 開頭改指 `new_film.py`，原〈開新片〉改名為 example_D-7 舊流程；`templates/AGENTS_TEMPLATE.md` 改成 `films/` 慣例（`new_film.py` 直接複製成 `films/AGENTS.md`），`README.md`、`AGENT_SETUP.md`、`skills/README.md` 的用法同步；`setup/16gb_sim/README.md` 註明腳本寫死上游路徑；`skills/ai-film/references/script/` 的「角色設定檔」補上 `films/角色/<角色>/README.md`，`skills/README.md` 的舊說法對照表改為已清理說明。
- 2026-10-15 生圖改為 Image 2.5 失敗就停、不自動退回本機 Qwen（`tools/gen_image.py` 的 `IMAGE_FALLBACK` 預設改 `0`）；角色定妝預設改為兩張多格圖：轉面圖 `<角色>_turn.png`（全身正、3/4、側、背）＋表情表 `<角色>_expr.png`（六格，附轉面圖生成），首幀兩張都附並在提示詞寫明不要照抄格子版面；單張半身照只在 `IMAGE_BACKEND=local`（千問備選）時使用（`pipeline/template_local/make_film.py` 的 `chars`、`frames`；只用 Image 2.5 時生圖階段不再要求 ComfyUI 開著）。`AGENTS.md`、`README.md`、`docs/03`、`docs/06`、`docs/07`（新增 §0）、`pipeline/template_local/README.md`、`templates/AGENTS_TEMPLATE.md`、`skills/ai-film/`（`SKILL.md`、`film-json.md`、`production.md`）同步。
- 2026-10-15 沒有 OpenAI 金鑰時生圖自動改走 Codex CLI 內建生圖（ChatGPT 訂閱）：新增 `tools/codex_image.py`；`tools/gen_image.py` 新增 `codex` 後端與 `IMAGE_CODEX`（有金鑰但 API 失敗仍停下）；`tools/img25.py` 金鑰另可讀 `~/.openai.env`（`OPENAI_API_KEY=` 格式）；`pipeline/template_local/make_film.py` 記錄 `codex` 後端、片尾寫「OpenAI 生圖（Codex）」。`AGENTS.md`、`README.md`、`docs/06`、`pipeline/template_local/README.md`、`skills/ai-film/references/`（`production.md`、`film-json.md`）同步，原「手動呼叫 `agent-draw` 代生圖」的說明改為自動流程。
- 2026-10-15 `docs/02_端到端流程.md` 片尾、上架資訊改為選用（本分支目前不上 YouTube，預計發社群）：總表兩列標「選用」、人工驗收移到自審；§11 補「刪 `film.json` 的 `ending` 即跳過」與不做片尾時要在貼文標示 AI 生成；§13 改名〈封面與上架資訊（選用）〉並補發社群所需的最小內容。
- 2026-10-15 同上，`README.md`（流程一覽、步驟表第 9 列）、`docs/01_總覽與架構.md`（目標改為預設發社群）、`skills/ai-film/references/`（`interview.md` 選問加片尾／上架、`review.md` 沒片尾時交付貼文用 AI 標示、`film-json.md`、`production.md`）同步改為片尾與上架資訊選用。
- 2026-10-15 `docs/05_agent協作與知識庫.md` 改寫成本分支實際做法：入口改為 `AGENTS.md`（`CLAUDE.md` 橋接）＋`handoff.md`＋`films/AGENTS.md`，知識庫分層對應到 `docs/`、Obsidian／`git log`、`films/`；記憶改為只放單機專屬的事（Claude 記憶每台電腦各一份、不同步），退件規則改寫進 `films/AGENTS.md`；技能段改為單一 `ai-film` 與「同步技能」流程；雙機協作改為多台電腦靠雲端硬碟＋GitHub。`docs/01`（知識層架構圖、協作列）、`templates/AGENTS_TEMPLATE.md`、`skills/ai-film/`（`SKILL.md`、`references/review.md`）的「退件理由寫進記憶」同步改寫。
- 2026-10-15 OpenAI 生圖改為 Codex CLI 第一優先、Image 2.5 API 金鑰第二：`tools/gen_image.py` 預設後端改為 `auto`（這台 Codex 能用就用 Codex，不能用才看金鑰，都不行就停；選定後生成失敗也停、不改試另一個），移除 `IMAGE_CODEX`；`tools/codex_image.py` 新增 `available()`；`pipeline/template_local/make_film.py` 的 `IMAGE_BACKEND` 預設改 `auto`。`AGENTS.md`、`README.md`、`docs/02`、`docs/06` §6（改寫）與環境變數表、`docs/07`、`pipeline/template_local/README.md`、`templates/AGENTS_TEMPLATE.md`、`skills/ai-film/`（`SKILL.md`、`references/production.md`）同步。
- 2026-10-15 OpenAI 生圖改回 Image 2.5 API 優先、Codex CLI 次之（API 能確定模型是 Image 2.5，Codex 內建生圖的模型版本無法從外部確認）：`tools/gen_image.py` 的 `auto` 改為有金鑰走 API、沒金鑰才走 Codex；`tools/codex_image.py`、`pipeline/template_local/make_film.py` 註解同步；`AGENTS.md`、`README.md`、`docs/02`、`docs/06` §6 與工具表、`docs/07`、`pipeline/template_local/README.md`、`templates/AGENTS_TEMPLATE.md`、`skills/ai-film/`（`SKILL.md`、`references/production.md`）同步。`docs/06` 工具表與 `tools/breezyvoice_batch.py` 的「一鍵」改為「一鍵執行」。
- 2026-10-15 `docs/07_本地角色與首幀.md` 改名為 `docs/07_角色與首幀.md`（內容不只本機做法：§0 是預設的 OpenAI 生圖、§3 起雲端本機通用）：標題與開頭說明改寫、§0 標題改為〈預設：OpenAI 生圖的轉面圖＋表情表〉並更新實測狀態；`README.md`、`docs/02`、`setup/lora/README.md`、`templates/AGENTS_TEMPLATE.md`、`skills/ai-film/SKILL.md` 的連結同步。
