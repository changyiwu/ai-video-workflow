# AGENT_SETUP：給 AI agent 的安裝手冊

> 寫給 Claude Code、Codex 等 AI agent：照順序做，每一步做完都有「怎麼確認成功」。人也可以照著做。
> 全程只在 Windows 11＋NVIDIA 顯卡上驗證過。所有影像、聲音、音樂都在本機生成；agent 本身可以用雲端模型。

## 0. 先確認這台電腦用哪一份 repo

```
python setup\detect_hardware.py
```

> **RTX Spark 筆電（Windows on Arm＋統一記憶體）**：`detect_hardware.py` 會自動辨識。不要照下面第 1–2 節裝（套件全是 x64 版），改照 [docs/hardware_rtxspark.md](docs/hardware_rtxspark.md) 的「第一次上機」，設定檔用 `configs\profile_rtxspark.cmd`。
>
> 本專案是 16GB VRAM＋64GB RAM 版。其他硬體版本是上游原作者（mathruffian-dot）維護的 repo，見 [NOTICE.md](NOTICE.md)。

| 顯卡 | 記憶體 | 該用的版本（上游 repo 名稱） |
|---|---|---|
| 32GB（RTX 5090） | 64GB 以上 | `shanshiba-workflow-32gvram-64gram` |
| 16GB（RTX 4080／5070 Ti／5080） | 64GB | `shanshiba-workflow-16gvram-64gram` |
| 16GB | 32GB | `shanshiba-workflow-16gvram-32gram` |
| 12GB 以下、記憶體不到 32GB、沒有 NVIDIA 顯卡、Mac | — | **`shanshiba-workflow-colab`**：H3 送 Google Colab 跑（要 Google AI 方案或 Colab 運算單元），見 `cloud/README.md` |

如果推薦的不是 16GB VRAM＋64GB RAM 版，**停下來告訴使用者**，請他改用上游對應的 repo。四份的流程一樣，差在 `docs/hardware.md` 和 `configs/profile.cmd`；每一份都有 `cloud/`，所以本機版的人也可以把 H3 送到 Colab 加速。

> **用 Colab 時（cloud/）**：本手冊第 1–3 節只需要做你本機要跑的部分（例如只裝語音環境），Colab 上的環境由 `python cloud/colab_h3.py start` 自動裝好（**預設完整安裝，同第一份完整版**；只要 H3 時加 `--h3-only` 比較快）；本機什麼都跑不動就只要裝 Colab CLI，然後 `start`。**登入 `colab usage` 一定要讓使用者自己在終端機操作**（瀏覽器授權、貼授權碼），agent 不要經手授權碼。先告訴使用者 Colab 的 G4 機房在美國／歐盟、H3 授權排除這些地區，由使用者決定是否使用（`cloud/README.md` 開頭）。

再讀 `docs/hardware.md`，了解這個配置的預期速度、顯存、記憶體和風險。

## 1. 前置軟體

| 項目 | 版本（原專案） | 怎麼確認 |
|---|---|---|
| Windows | 11 | `winver` |
| NVIDIA 驅動 | 610.88（要支援 CUDA 13.0） | `nvidia-smi` 右上角 CUDA Version ≥ 13.0 |
| Python | 3.12（3.12.10–3.12.14 都可）；選用的 BreezyVoice 另需 3.10（用 uv 安裝即可） | `py -3.12 --version` |
| uv | 任意（裝套件用；選用的 BreezyVoice 環境也靠它裝 Python 3.10：`pip install uv`） | `uv --version` |
| Git | 任意 | `git --version` |
| ffmpeg／ffprobe | 9.0.1 full build，要在 PATH | `ffmpeg -version` |
| 硬碟 | C 槽至少 250GB 可用（必要模型約 150GB），NVMe SSD | `detect_hardware.py` |
| 分頁檔 | Windows 預設「系統管理」即可，不要設成固定的小數字 | 系統 → 進階系統設定 → 效能 → 虛擬記憶體（**這是系統設定，要請使用者自己確認或改**） |

## 2. 資料夾與 Python 環境（必裝兩個，選用兩個）

ComfyUI 有兩種裝法：**已經有 Comfy Desktop 就直接用它**（2a，模型共用、不用另外裝 ComfyUI）；沒有才自己裝在 `C:\AI\H3`（2a′）。語音環境裝在 `C:\AI`（不要放進雲端硬碟同步的資料夾）；工具不用裝，直接用 repo 的 `tools/`（2e）。

**順序很重要：先做完第 2 節（尤其是 clone ComfyUI），再做第 3 節下載模型。** 部分模型清單會寫進 `ComfyUI-0.36.0\models\`，先下載的話資料夾已經存在，`git clone` 會因為目錄不是空的而失敗。

**套件一律用 uv 裝**（比 pip 快很多；2026-10-07 全新安裝實測，pip 下載部分大檔只有 100–200 kB/s，H3 環境卡了 20 分鐘以上，改 uv 1.5 分鐘裝完）。四份清單都是原專案 `pip freeze` 的完整結果，所以都加 `--no-deps` 照清單裝，不要讓 pip／uv 自己重新解依賴（語音環境的 voxcpm 依賴會跟鎖定的 fsspec 衝突，照清單裝則沒問題）。uv 也卡住時，見文末常見問題。

```
mkdir C:\AI\Voice
```
（自己裝 ComfyUI 時再建 `C:\AI\H3`；要裝選用配音引擎時再建 `C:\AI\BreezeTTS`、`C:\AI\BreezyVoice`。）

### 2a. 主環境：Comfy Desktop（已安裝時用這個）

連接、背景啟動、模型位置的通用做法以全域技能 `agent-comfyui` 為準；本專案只多做下面三件事。`configs\profile.cmd` 偵測到 Desktop（預設安裝名稱 `ComfyUI`）就自動改用它：`COMFY_DIR`、`PY_H3` 指向 Desktop 安裝裡的 `ComfyUI` 與 `.venv`，模型用 `ComfyUI-Shared\models`，`tools\start_comfy.cmd` 會在背景啟動它（不開 Desktop 視窗，帶上本硬體的 `--reserve-vram 1.5`）。工具的 input／output 資料夾會自動問執行中的 ComfyUI，不用設。

> Desktop 安裝改過名稱：先 `set DESKTOP_COMFY=<安裝路徑>\ComfyUI` 再 `call configs\profile.cmd`。不想用 Desktop：`set DESKTOP_COMFY=none`。
> **Desktop 視窗開著時會佔用 8188 埠**，這時 `start_comfy` 不會再啟動，也就沒有 `--reserve-vram 1.5`。跑本專案前先關掉 Desktop 視窗。

1. **補套件**（Desktop 的 `.venv` 只缺這幾個；`--no-deps` 只裝缺的，不動 Desktop 的 torch）：
   ```
   call <repo>\configs\profile.cmd
   uv pip install --python "%PY_H3%" --no-deps nvidia-vfx==0.2.0.0 gguf==0.19.0 accelerate==1.15.0 triton-windows==3.8.0.post28 numba==0.67.0 llvmlite==0.49.0 "diffusers @ https://github.com/huggingface/diffusers/archive/e0abab83b5df05de9e7abd788643c1a7c1e42e28.zip" --extra-index-url https://pypi.nvidia.com --index-strategy unsafe-best-match
   ```
   版本照 `setup\env\requirements_h3_venv.txt`。安裝前先告訴使用者會改動 Desktop 的環境。
2. **自訂節點**：只需要 FlashVSR（照 `setup\custom_nodes.txt` 的 commit clone 到 `%COMFY_DIR%\custom_nodes\ComfyUI-FlashVSR_Ultra_Fast`）。RTX VSR 直接用 `nvidia-vfx` 套件，不用裝節點。
3. **模型**：Desktop 範本下載過的大多能直接用（H3 主模型、NVFP4 文字編碼器、Qwen-Image 2.1、Qwen-Image-Edit int8、Music 3），第 3 節只要補 DMAD 與 FlashVSR。`profile.cmd` 會把檔名對到 Desktop 的版本（`H3_CLIP`、`QWEN_EDIT_UNET`、`MUSIC3_DIT`）。

確認：`"%PY_H3%" -c "import torch, nvvfx, gguf;print(torch.__version__, torch.cuda.is_available())"` → `True`。

⚠️ **Desktop 會自動更新 ComfyUI**（有時連 `.venv` 一起換）。更新後先重跑一次 `smoke_test.py`；套件或節點不見了就重做上面 1、2。

### 2a′.（沒有 Comfy Desktop 時）自己安裝 C:\AI\H3

**ComfyUI 資料夾名稱請照抄 `ComfyUI-0.36.0`**（裡面放的是 0.37.0，名稱是歷史原因，很多腳本寫死這個路徑）。`profile.cmd` 偵測不到 Desktop 時就用這裡。

```
git clone https://github.com/comfyanonymous/ComfyUI C:\AI\H3\ComfyUI-0.36.0
cd C:\AI\H3\ComfyUI-0.36.0 && git checkout v0.37.0
py -3.12 -m venv C:\AI\H3\venv
uv pip install --python C:\AI\H3\venv\Scripts\python.exe --no-deps -r <repo>\setup\env\requirements_h3_venv.txt --extra-index-url https://download.pytorch.org/whl/cu130 --index-strategy unsafe-best-match
copy <repo>\setup\extra_model_paths.yaml C:\AI\H3\ComfyUI-0.36.0\extra_model_paths.yaml
```
自訂節點照 `setup\custom_nodes.txt` clone 到 `ComfyUI-0.36.0\custom_nodes\` 並 checkout 指定 commit。**節點自己的 requirements.txt 不用另外裝**（需要的套件，例如 triton-windows、nvidia-vfx，已經在上面的清單裡）。
確認：`C:\AI\H3\venv\Scripts\python.exe -c "import torch;print(torch.__version__, torch.cuda.is_available())"` → `2.14.0+cu130 True`

### 2b. 語音環境 C:\AI\Voice（⭐ VoxCPM2 預設配音引擎：聲音設計＋所有台詞；faster-whisper、分軌、聲調比對）

```
py -3.12 -m venv C:\AI\Voice\venv
uv pip install --python C:\AI\Voice\venv\Scripts\python.exe --no-deps -r <repo>\setup\env\requirements_voice_venv.txt --extra-index-url https://download.pytorch.org/whl/cu130 --index-strategy unsafe-best-match
```
確認：`C:\AI\Voice\venv\Scripts\python.exe -c "import voxcpm, faster_whisper, audio_separator, stable_whisper, edge_tts;print('ok')"` → `ok`

### 2c.（選用）Breeze TTS 2 環境 C:\AI\BreezeTTS（`VOICE_ENGINE=breezyvoice` 時設計新角色的參考音）

2026-10-14 起預設配音引擎改為 VoxCPM2，2c、2d 只有要用選用引擎（台灣腔較準、可標注音）時才裝。兩者官方都以 Linux 為準，下面是上游作者在 Windows 跑通的非官方裝法；Breeze TTS 2 權重非商用。

```
git clone https://github.com/breezeblue-ai/breeze-tts C:\AI\BreezeTTS\breeze-tts
py -3.12 -m venv C:\AI\BreezeTTS\venv
uv pip install --python C:\AI\BreezeTTS\venv\Scripts\python.exe --no-deps -r <repo>\setup\env\requirements_breeze_venv.txt --extra-index-url https://download.pytorch.org/whl/cu128 --index-strategy unsafe-best-match
```
（Breeze 用 cu128 的 torch，跟另外兩個環境不同，這是原專案實際狀態。）

### 2d.（選用）BreezyVoice 環境 C:\AI\BreezyVoice（`VOICE_ENGINE=breezyvoice` 時念台詞）

BreezyVoice（聯發科＋台大，Apache-2.0）是選用的台詞配音引擎：用角色參考音念任何台詞，台灣國語腔，念不準的字可直接標注音。官方安裝說明只有 Linux 版（文字正規化需要的 pynini 在 PyPI 只有 Linux wheel，細節見 `docs/06_安裝.md` §5b），下面是原專案在 Windows 上實際跑通的非官方裝法：

```
git clone --recurse-submodules https://github.com/mtkresearch/BreezyVoice C:\AI\BreezyVoice\code
cd C:\AI\BreezyVoice\code && git checkout d592c9d3e8927a0f53f68616387060dcd32a05ea && git submodule update --init --recursive
uv python install 3.10
uv venv --python 3.10 C:\AI\BreezyVoice\venv
uv pip install --python C:\AI\BreezyVoice\venv\Scripts\python.exe "setuptools<70" wheel
uv pip install --python C:\AI\BreezyVoice\venv\Scripts\python.exe --no-build-isolation --no-deps -r <repo>\setup\env\requirements_breezyvoice_venv.txt --index-strategy unsafe-best-match --extra-index-url https://download.pytorch.org/whl/cu128
xcopy /E /I <repo>\setup\breezyvoice\winstub C:\AI\BreezyVoice\winstub
```
- 一定要 `--no-deps` 照清單裝：`g2pw` 會要求編不起來的舊版 transformers；`openai-whisper` 要先有 `setuptools<70` 再用 `--no-build-isolation` 建置；`HyperPyYAML` 要 `ruamel.yaml<0.18`（清單已鎖）。
- `winstub`：官方的文字正規化（WeTextProcessing）需要 pynini，Windows 裝不了，用這個直通替身取代。**它不會把數字轉成國字**，`breezyvoice_batch.py` 會自動轉阿拉伯整數，其他（小數、英文縮寫）請在台詞裡寫成國字。
- 第一次執行會自動下載 g2pW 注音模型（607MB，到 `C:\AI\BreezyVoice\code\G2PWModel`）和 bert-base-chinese 的 tokenizer（不到 1MB）。
- 確認：`C:\AI\BreezyVoice\venv\Scripts\python.exe -c "import torch;print(torch.__version__, torch.cuda.is_available())"` → `2.7.1+cu128 True`

### 2e. 工具

不用複製：`make_film.py`、`run_demo.py`、`smoke_test.py` 預設直接用 repo 的 `tools/`（要放別處才設 `AI_TOOLS`）。repo 放在 Google 雲端硬碟時，把 repo 資料夾設成「可離線使用」（或雲端硬碟用鏡像模式），否則串流模式下工具檔可能只在雲端，離線時會失敗。

## 3. 下載模型（全部鎖定版本、逐檔驗證雜湊、可續傳）

cmd 視窗：
```
cd <repo>\setup
for %f in (downloads.json downloads_uncensored.json downloads_dmad.json downloads_qwen_image.json downloads_qwen_image_edit.json downloads_music3.json downloads_voxcpm2.json downloads_breeze_tts2.json downloads_breezyvoice.json downloads_flashvsr.json) do C:\AI\H3\venv\Scripts\python.exe download.py %f
```
（寫進 .bat 檔要把 `%f` 改成 `%%f`。）PowerShell：
```
cd <repo>\setup
foreach ($f in 'downloads.json','downloads_uncensored.json','downloads_dmad.json','downloads_qwen_image.json','downloads_qwen_image_edit.json','downloads_music3.json','downloads_voxcpm2.json','downloads_breeze_tts2.json','downloads_breezyvoice.json','downloads_flashvsr.json') { C:\AI\H3\venv\Scripts\python.exe download.py $f }
```
**用 Comfy Desktop 時**：先 `call <repo>\configs\profile.cmd`（它設的 `COMFY_MODELS_DIR`、`COMFY_DIR` 讓 `download.py` 把模型放進 Desktop 的資料夾），用 `"%PY_H3%"` 代替上面的 `C:\AI\H3\venv\Scripts\python.exe`，**只跑 `downloads_dmad.json`、`downloads_flashvsr.json`、`downloads_voxcpm2.json`**（其他 Desktop 已經有，或改用 Desktop 的版本；要用選用配音引擎再加 Breeze 兩份）。

每份清單跑完會印 `downloaded N, already present M, failed K`，全部成功才印 `ALL DOWNLOADS VERIFIED`（有失敗時結束碼非 0，重跑會從斷點續傳、已驗證的檔案自動跳過）。大檔用 SHA-256 驗證，小設定檔用 Hugging Face 公布的 git 雜湊驗證。

| 清單 | 內容 | 大小 |
|---|---|---|
| `downloads.json` | H3 主模型（剪枝 int8）、官方 NVFP4 文字編碼器、影音 VAE | 約 41GB |
| `downloads_uncensored.json` | H3 文字編碼器 int8（**本工作流實際使用的那顆**） | 24.6GB |
| `downloads_dmad.json` | DMAD 4 步 LoRA（下載後要轉檔，見下） | 2.6GB |
| `downloads_qwen_image.json` | Qwen-Image 2.1 int8＋文字編碼器＋VAE（角色定妝照、LoRA 首幀） | 16.1GB |
| `downloads_qwen_image_edit.json` | Qwen-Image-Edit 2511 fp8＋文字編碼器＋VAE（**預設的首幀做法**） | 28.1GB |
| `downloads_music3.json` | MiniMax Music 3 | 11.1GB |
| `downloads_voxcpm2.json` | VoxCPM2 主權重（**預設配音引擎**） | 4.6GB（另需同 repo 的 config／tokenizer 小檔，見下） |
| `downloads_breeze_tts2.json` | 選用：Breeze TTS 2（含 tokenizer、audio_tokenizer；`VOICE_ENGINE=breezyvoice` 時設計參考音） | 7.1GB |
| `downloads_breezyvoice.json` | 選用：BreezyVoice-300M（`VOICE_ENGINE=breezyvoice` 時念台詞） | 3.0GB |
| `downloads_flashvsr.json` | FlashVSR v1.1 | 6.3GB |
| 選用 | `downloads_action_loras.json`（動作 LoRA）、`downloads_funcontrol.json`（舞蹈骨架控制） | — |

另外四個會自動下載的：
- VoxCPM2 小檔：`C:\AI\Voice\venv\Scripts\python.exe -c "from huggingface_hub import snapshot_download as s; s('openbmb/VoxCPM2', revision='32279effe8c19989596f05d353d1447f51d9e915', local_dir=r'C:\AI\Voice\models\VoxCPM2')"`
- faster-whisper large-v3：`C:\AI\Voice\venv\Scripts\python.exe -c "from faster_whisper import WhisperModel; WhisperModel('large-v3', device='cpu', download_root='C:/AI/Voice/models/whisper')"`
- g2pW 注音模型（選用）：第一次跑 BreezyVoice 時自動下載（見 2d）。
- BS-RoFormer：第一次跑 `audio-separator` 時自動下載到 `C:\AI\Voice\models\separator`（`smoke_test.py` 會觸發）。

DMAD 轉檔：
```
C:\AI\H3\venv\Scripts\python.exe <repo>\tools\dmad_lora_convert.py C:\AI\H3\ComfyUI-0.36.0\models\loras\dmad_raw\dmad_minimax_h3_4step_lora_critic.safetensors C:\AI\H3\ComfyUI-0.36.0\models\loras\dmad_h3_4step_lora_critic_comfy.safetensors
```
用 Comfy Desktop 時（先 `call configs\profile.cmd`）：
```
"%PY_H3%" <repo>\tools\dmad_lora_convert.py "%COMFY_MODELS_DIR%\loras\dmad_raw\dmad_minimax_h3_4step_lora_critic.safetensors" "%COMFY_MODELS_DIR%\loras\dmad_h3_4step_lora_critic_comfy.safetensors"
```
（只需要 `lora_critic` 這一顆；`full_critic` 實測構圖會漂，不用。）

## 4. 啟動與自我驗證

在**同一個 cmd 視窗**依序執行（`profile.cmd` 設定的環境變數只在這個視窗有效）：
```
set PYTHONUTF8=1
call <repo>\configs\profile.cmd
<repo>\tools\start_comfy.cmd
"%PY_H3%" <repo>\setup\smoke_test.py
```
（`PY_H3` 由 `profile.cmd` 設定：Comfy Desktop 的 `.venv`，或自己裝的 `C:\AI\H3\venv\Scripts\python.exe`。）
`smoke_test.py` 會自己設計一個聲音、生一張首幀，跑完 VoxCPM2（設計聲音）→ VoxCPM2（念台詞）→ 自動挑選 →（有裝才跑：Breeze 設計 → BreezyVoice 念＋挑選）→ faster-whisper → 聲調比對 → Qwen-Image 2.1 → Music 3 → BS-RoFormer → H3 → RTX VSR → FlashVSR，最後印出每一步 OK／FAIL 和秒數。
- 全部 OK，且每步時間在 `docs/hardware.md` 列的範圍內（真實顯卡比 5090 慢是正常的），就算安裝完成。完整版 12 步；`--quick` 跳過 FlashVSR，11 步；有裝選用的 Breeze＋BreezyVoice 會多 3 步。
- 2026-10-07 全新安裝實測（上游，當時預設 BreezyVoice、smoke test 為 14 步；另一個 agent 只看本 repo、在清空的 `C:\AI` 從零安裝，RTX 5090）：完整版 14 步全部 OK，共 500 秒；第一次跑 BreezyVoice 會先下載 g2pW 注音模型，那一步多約 45 秒。
- 打開 `setup\smoke_out\h3\clip.mp4` 看：畫面清楚、嘴型有跟著台詞動。

## 5. 跑全本地示範片

```
"%PY_H3%" <repo>\pipeline\demo_local\run_demo.py
```
從零做兩個角色、4 鏡首幀、配音、H3、配樂，輸出 `pipeline\demo_local\out\cut\demo_1080p.mp4`（約 17 秒）。2026-10-07 全新安裝實測 12.8 分鐘（RTX 5090）；「16GB 顯卡＋32GB 記憶體」模擬條件下約 15 分鐘（5090 運算速度；真實 16GB 卡推估 30–40 分鐘）。看成片確認：兩個角色每鏡長得一樣、嘴型跟著台詞、字幕念的跟聲音一致。

## 6. 開始做片

讀 `docs/03_規則與踩坑.md`（規則）和 `pipeline/template_local/README.md`（做法），把 `templates/AGENTS_TEMPLATE.md` 放到使用者的專案根目錄改名 `AGENTS.md`（Claude Code 另加一行 `@AGENTS.md` 的 `CLAUDE.md` 橋接）。做新片：用 `skills/ai-drama` 寫劇本 → `python tools/new_film.py <片名>`（把 `pipeline/template_local/` 複製成 `films/<片名>/`） → 把角色、場景、鏡表填進 `film.json` → `make_film.py` 分段跑，三個人工關卡（首幀總覽、每鏡抽格、成片）都要給使用者看。

## 常見問題

| 症狀 | 處理 |
|---|---|
| `ComfyUI not reachable` | 先 `call configs\profile.cmd`，再 `<repo>\tools\start_comfy.cmd` |
| 跑 H3 時整台電腦卡住 | 關掉瀏覽器等大程式；確認沒有兩個 GPU 工作同時跑 |
| 「分頁檔太小」（Windows error 1455） | 請使用者把分頁檔改回「系統管理」或設 64GB 以上 |
| VAE 解碼時當掉 | `configs\profile.cmd` 的 `COMFY_EXTRA_ARGS` 加 `--disable-pinned-memory --disable-async-offload` |
| faster-whisper 找不到 cuBLAS | 用 `stt.py`（它會自動把 venv 裡 nvidia 的 DLL 加進路徑） |
| 裝套件時某個大檔（例如 `nvidia-cudnn-cu12` 700MB）下載只有幾百 kB/s、卡很久 | 確認用的是 `uv pip install`；還是卡住就先用瀏覽器或多連線下載工具把那個 wheel 抓下來，`uv pip install --python <venv> --no-deps <wheel檔>` 先裝它，再重跑整份清單 |
| 指令輸出的中文變亂碼 | 先 `set PYTHONUTF8=1`（或在 Git Bash 用 `export PYTHONUTF8=1`）；不影響結果，只影響顯示 |
| 下載清單印出 `failed` | 再跑一次同一份清單（會續傳）；一直失敗就檢查網路能不能連 huggingface.co |
