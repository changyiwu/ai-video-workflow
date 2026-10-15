# AI 影片工作流（專案藍圖）

> 本檔為跨 Agent 通用的專案藍圖（AGENTS.md 開放標準）。任何 Agent 的每個 session 都應先讀本檔＋`handoff.md`。
> Claude Code 預設只在沒有 `CLAUDE.md` 時才讀 `AGENTS.md`，故由 `CLAUDE.md` 的 `@AGENTS.md` import 本檔（`CLAUDE.md` 只有這一行）；Claude 專屬規範寫在本檔〈Claude Code 專屬〉一節。

## 專案簡介
在 16GB VRAM＋64GB RAM 的本機，用開源模型（MiniMax H3、Qwen-Image 2.1／Edit、VoxCPM2、MiniMax Music 3；選用 BreezyVoice＋Breeze TTS 2）製作 1–3 分鐘、16:9、24fps 的原創 AI 短片。改作自 [mathruffian-dot/shanshiba-workflow-16gvram-64gram](https://github.com/mathruffian-dot/shanshiba-workflow-16gvram-64gram)，來源與修改內容見 `NOTICE.md`。

## 關鍵時程

## 目標與路線圖
- [x] 階段一：複製上游 repo、移除原作者個人資訊、加上來源標示、專案初始化
- [ ] 階段二：照 `AGENT_SETUP.md` 檢查硬體（`python setup/detect_hardware.py`）、安裝環境與下載模型
  - [ ] 桌機 Comfy Desktop 補齊（`AGENT_SETUP.md` §2a）：補裝 7 個套件、FlashVSR 節點、下載 DMAD／FlashVSR
  - [ ] 建 `C:\AI\Voice` 語音環境並下載 VoxCPM2
  - [ ] 設定 `OPENAI_API_KEY`，生一張圖驗證 Image 2.5 模型 ID
- [ ] 階段三：跑 `setup/smoke_test.py` 與 `pipeline/demo_local/run_demo.py` 驗證
  - [ ] VoxCPM2 預設配音流程（`voxcpm_batch.py`＋挑音）實機驗證：台灣腔、聽寫通過率、速度
- [ ] 階段三之二：RTX Spark 筆電上機驗證（照 `docs/hardware_rtxspark.md`「第一次上機」，結果回填該文件）
- [ ] 階段四：建立自己的角色設定，用 `pipeline/template_local/` 做第一支片

## 資料夾結構
```
README.md / AGENT_SETUP.md     專案說明、給 agent 的安裝手冊
NOTICE.md                      來源與作者、本分支修改清單（必須保留）
LICENSE / LICENSE-docs.md      MIT（程式）／CC BY-NC 4.0（文件素材）
THIRD_PARTY_NOTICES.md         第三方模型與工具授權
docs/                          總覽、端到端流程、規則與踩坑、自審清單、安裝、硬體說明
tools/                         全域工具（各腳本直接用這裡，不再複製到 C:\AI\tools）
films/                         自己的片與角色資產（.gitignore，不進 repo；規則見 films/AGENTS.md）
pipeline/                      template_local（新片範本）、demo_local（安裝驗證）、example_D-7（上游範例，缺角色資產，不能直接照跑）
setup/                         模型下載清單、套件清單、smoke_test、硬體偵測、16GB 模擬測試
cloud/                         H3 送 Google Colab 跑
sfx/                           Freesound CC0 音效
templates/                     片尾範本、法陣素材
agent/                         AGENTS_TEMPLATE.md（做片入口範本）、ai-drama 編劇技能、blender-previs 技能
configs/profile.cmd            桌機（16GB VRAM＋64GB RAM）環境變數
configs/profile_rtxspark.cmd   RTX Spark 筆電（Windows on Arm＋64GB 統一記憶體）環境變數
setup/spark_check.py、setup/env/arm64/   RTX Spark 相容性檢查與 ARM64 套件清單
```

## 專案專屬規則

### 授權與來源
- **僅限非商業用途**：文件素材為 CC BY-NC 4.0；Qwen-Image 2.1、Breeze TTS 2（選用配音引擎才會用到）只能非商用。要營利前先照 `THIRD_PARTY_NOTICES.md` 替換模型。
- **必須保留來源標示**：`LICENSE`、`LICENSE-docs.md`、`THIRD_PARTY_NOTICES.md`、`NOTICE.md`、`agent/skills/ai-drama/NOTICE.md`、`agent/skills/ai-drama/LICENSE-AI-drama-pound.txt` 不可刪除或移除原作者署名；修改上游文件時在 `NOTICE.md` 的修改清單補一筆。

### 生圖
- 預設 OpenAI Image 2.5（`gen_image.py` 預設後端），本機 Qwen-Image 為備選；金鑰由使用者自己設定（`OPENAI_API_KEY`／`OPENAI_KEY_FILE`），agent 不經手、不寫進 repo。
- `run_demo.py`、`smoke_test.py` 固定 `--backend local`（驗證本機安裝用）。
- 要用 OpenAI 生圖但沒有 API 金鑰時，可改呼叫全域技能 `agent-draw`：它的路線 C 會交給本機已用 ChatGPT 登入的 Codex CLI 代為生圖（扣訂閱額度、不需金鑰）。呼叫時直接把輸出資料夾與檔名指定成 `make_film.py` 要的位置（`out/chars/<角色>.png`、`out/masters/<名稱>.png`、`out/first/<鏡號>.png`），`make_film.py` 看到檔案已存在就會沿用；走路線 B（`draw.py`）時檔名會被加時間戳，要再改名。這條路不經過 `gen_image.py`，`out/image_backends.json` 不會記到——全部用 `agent-draw` 時片尾會預設寫「OpenAI Image 2.5」，混用本機 Qwen 時會只寫 Qwen，出片前要核對片尾的生圖工具名稱，不對就改 `film.json` 片尾的 `tools`。附定妝照當參考圖的做法尚未實測。

### 配音
- 預設引擎 VoxCPM2（聲音設計＋台詞，`tools/voxcpm_batch.py`）；`VOICE_ENGINE=breezyvoice` 改用 Breeze TTS 2＋BreezyVoice（台灣腔較準、可標注音，但官方以 Linux 為準，RTX Spark 大概率裝不起來）。
- 挑音兩個引擎共用 `breezyvoice_pick.py`；VoxCPM2 不支援注音標記，念錯的字改同音字。
- 聽寫（ASR）一律經 `tools/stt.py` 的 `load_asr()`，不要直接 import `faster_whisper`：Windows on Arm 沒有 ctranslate2，靠它自動改用 openai-whisper。
- 工具一律直接跑 repo 的 `tools/`（入口腳本預設就找它，`make_*.cmd` 用自己所在的資料夾），不要再複製到 `C:\AI\tools`；要改位置才設 `AI_TOOLS`。新寫的腳本找工具也要用相對 repo 的路徑，不要寫死 `C:\AI\tools`。

### ComfyUI
- 桌機用 Comfy Desktop 的 ComfyUI（`configs\profile.cmd` 自動偵測），連接、背景啟動、模型位置照全域技能 `agent-comfyui`；不要另外在 `C:\AI\H3` 裝一份。
- 工具讀寫 ComfyUI 的 input／output 一律經 `tools/comfy_paths.py`，不要寫死 `COMFY_DIR\input`／`output`（Desktop 放在 `ComfyUI-Shared`）。
- 跑本專案前先關掉 Desktop 視窗，由 `tools\start_comfy.cmd` 在背景啟動，才會帶上 `--reserve-vram 1.5`。Desktop 自動更新後先跑 `smoke_test.py`，補裝的套件或 FlashVSR 節點不見了就照 `AGENT_SETUP.md` §2a 重裝。

### 兩台硬體
- 桌機：RTX 5060 Ti 16GB＋64GB RAM，用 `configs\profile.cmd`。筆電：RTX Spark（Windows on Arm、64GB 統一記憶體），用 `configs\profile_rtxspark.cmd`。
- 改 `setup/env/requirements_*.txt` 後要跑 `python setup/spark_check.py --wheels --emit` 重產 ARM64 清單，並看 diff 有沒有不合理的版本跳動。
- 判斷套件有沒有 ARM64 版不要只看 PyPI：NVIDIA 的套件（如 `nvidia-vfx`）在 PyPI 只放 wheel-stub 空殼，真正的 wheel 在 pypi.nvidia.com；也要核對 wheel 的 Python 版本（cpXY／abi3）。

### 做片
- 自己的片一律放 `films/<片名>/`（從 `pipeline/template_local/` 複製，`repo_dir` 維持 `../..`）；`films/` 已列入 `.gitignore`，只走雲端硬碟、沒有 GitHub 備份。
- 頻道與角色的做片規則在 `films/AGENTS.md`（`films/CLAUDE.md` 橋接），角色資產在 `films/角色/`；不要把這些寫進本檔或 `pipeline/`。
- `films/AGENTS.md` 是從 `agent/AGENTS_TEMPLATE.md` 改寫的獨立檔：改了範本裡的通用規則，要手動同步過去。

### 安全與隱私
- **不放個資與金鑰**：不 commit 真人照片、克隆聲音／參考音、API 金鑰（`.env`）、模型權重、成片影片。本 repo 為**公開** repo。

## 同步層級（本專案初始化至第 3 層級）

| 層級 | 平台 | 位置 | 讀取時機 |
|------|------|------|---------|
| L1 | 本地（GDrive） | `AGENTS.md`＋`handoff.md`（不進 git，只走雲端硬碟）＋`CLAUDE.md`（橋接） | 每個 session |
| L2 | GitHub | changyiwu/ai-video-workflow（公開） | 指定時 |
| L3 | Obsidian | ai-video-workflow/專案工作流程.md | 有需要時 |

## 三個檔案的職責（依「時效性」分家，不是依「詳細程度」）

| 檔案 | 時效 | 寫入方式 | 放什麼 |
|------|------|---------|--------|
| `handoff.md` | **只對下一個 session 有效**，過期即丟 | 每次收工**整份重寫** | 做到哪、下一步、**這次**的暫時 workaround |
| `AGENTS.md`（本檔） | **長期有效**，每個 session 都適用 | 只有規則本身變了才改 | 目標、路線圖、常設規則、結構 |
| Obsidian（L3）／`git log` | **歷史**：發生過什麼、為什麼 | 只增不刪 | 決策紀錄、踩坑完整版、逐次進度 |

驗收標準：**`handoff.md` 整份刪掉，不應損失任何長期資訊**——會的話代表該升級進本檔卻沒升級。

**本檔不要出現的東西**（會無限膨脹，且開工每次都要重讀）：
- ❌ `## 最近進度`／逐次工作紀錄 → 有 L3 寫 Obsidian「🗓️ 最近更動紀錄」；沒有就靠 `git log`（所以 commit 訊息要寫「做什麼＋為什麼」）
- ❌ 決策記錄、取捨理由、踩坑經過的完整版 → Obsidian「決策紀錄」「🕳️ 踩坑筆記」
- ✅ 只留「結論式的規則」：踩過的坑收斂成一條**祈使句**寫進〈工作約定〉或〈專案專屬規則〉，理由那一大段留在 Obsidian

## 工作約定
- 任何 Agent、任何電腦：**開工先讀 `handoff.md`，收工必更新 `handoff.md`**
- `handoff.md` **不進 git**（含真實電腦名與本機絕對路徑），已列入 `.gitignore`，跨電腦靠雲端硬碟同步——不要把它加回版控
- 修改共用檔案前先讀最新內容，避免覆蓋其他 Agent 的變更
- 所有回應與文件使用繁體中文
- 修改前先確認計畫，優先保留原有資料結構
