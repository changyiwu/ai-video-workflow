# 硬體說明：RTX Spark 筆電（Windows on Arm＋64GB 統一記憶體）

> **狀態：尚未在 RTX Spark 實機上驗證（2026-10-11）。** 本文件是依上游 16GB 版的實測數據、NVIDIA 公開資訊與 PyPI 套件掃描推出來的計畫；拿到筆電後照「第一次上機」逐步驗證，結果回填本文件。
> 本專案的其他內容（流程、規則、腳本）不變；這份只處理「同一套工作流怎麼在 RTX Spark 上跑」。

## 跟桌機版差在哪

| 項目 | 桌機（本專案主設定） | RTX Spark 筆電 |
|---|---|---|
| CPU 架構 | x64 | **ARM64**（Windows 11 on Arm） |
| 記憶體 | 16GB 顯存＋64GB 系統記憶體（各自獨立，共 80GB） | **64GB 統一記憶體，CPU 與 GPU 共用** |
| GPU | RTX 50 系列，正式版 CUDA 驅動 | N1X 內建 Blackwell GPU（5120 或 6144 CUDA 核心） |
| CUDA／PyTorch | 正式版（cu130 wheel） | **開發者預覽版**（CUDA 13.4 preview、NVIDIA nightly PyTorch） |
| 設定檔 | `configs\profile.cmd` | `configs\profile_rtxspark.cmd` |

## 三個主要風險

1. **軟體生態還在預覽階段**：NVIDIA 的 Windows on Arm CUDA 工具包是 Developer Preview，官方說不適合正式使用，已知問題包括某些 PyTorch 工作流程會造成 GPU 逾時或系統重開。PyTorch 要從 NVIDIA 的 nightly 索引裝，不是 PyTorch 官方索引。
2. **部分套件沒有 Windows ARM64 版**（2026-10-11 用 `setup/spark_check.py --wheels` 掃描 PyPI 的結果）：

   | 環境 | 可直接裝 | 主要問題 | 對策 |
   |---|---|---|---|
   | `C:\AI\H3`（ComfyUI、H3、Qwen、Music 3） | 98／109 | torch 家族要換來源；`triton-windows`、`nvidia-vfx`（RTX VSR）只有 x64 | 用 `setup/env/arm64/requirements_h3_venv_arm64.txt`；放大改 `UPSCALE=lanczos` 或 FlashVSR |
   | `C:\AI\Voice`（VoxCPM2、faster-whisper、分軌） | 127／146 | **`ctranslate2`（faster-whisper 核心）沒有 Windows ARM64 版**；CUDA 12 函式庫只有 x64；VoxCPM2 需要的 `soxr`、`torchcodec` 沒有 ARM64 wheel（見下方〈語音〉） | 聽寫校對改在 Colab 跑，或之後改用 openai-whisper；VoxCPM2 先試本機 |
   | `C:\AI\BreezeTTS` | 83／88 | 少數套件要現場編譯 | 用 arm64 清單試裝 |
   | `C:\AI\BreezyVoice`（Python 3.10） | 116／136 | **numpy 1.26、scipy、pandas、scikit-learn 等在 Python 3.10 沒有 ARM64 wheel**，要自己編譯，很可能失敗 | 台詞配音預設送 Colab（`cloud/colab_h3.py full-setup`） |

3. **記憶體是共用的**：桌機的做法是「顯存放不下的模型先放系統記憶體」，在統一記憶體上這等於同一池子放兩份。上游 16GB 顯存＋32GB 記憶體版實測 H3 一共約用掉 45–50GB 仍可跑，所以 64GB 統一記憶體**理論上夠**，但 Windows 與桌面程式也從同一池子拿，生成時一定要關掉其他大程式。

## 設定（`configs\profile_rtxspark.cmd`）

| 項目 | 值 | 理由 |
|---|---|---|
| 模型 | 跟 16GB 版完全一樣（H3 剪枝 int8、Heretic int8 文字編碼器、fp16 影片 VAE、DMAD 4 步） | 上游驗證過的組合，結果可對照 |
| ComfyUI 參數 | `--reserve-vram 6 --disable-pinned-memory --disable-async-offload` | 統一記憶體不需要釘選記憶體與非同步搬移（只會重複佔用）；保留 6GB 給 Windows |
| 放大 | `UPSCALE=lanczos`（或 `flashvsr`） | RTX VSR 沒有 ARM64 版 |
| 單鏡長度 | ≤12 秒 | 同主設定 |
| 一次一件 GPU 工作 | 必須 | 同主設定，而且 CPU 程式也在搶同一池記憶體 |

H3 還是記憶體不足時，依序試：`--reserve-vram` 調到 8–10 → 加 `--lowvram` → 換 NVFP4 文字編碼器（N1X 是 Blackwell，原生支援 FP4；上游實測畫面會跟 int8 不同但品質相當）→ `H3_BACKEND=colab`。

## 語音：筆電上先試 VoxCPM2

Breeze TTS 2（官方只支援 Linux）與 BreezyVoice（安裝與相依套件以 Linux 為準，Python 3.10 套件沒有 ARM64 wheel）在筆電上都很難裝。**VoxCPM2 是語音元件裡最有機會在筆電本機跑的**（2026-10-11 查資料與掃 PyPI，尚未實機驗證）：

- **官方需求沒有限定平台**：Python 3.10–3.12、PyTorch ≥ 2.5、CUDA ≥ 12；裝置可選 `cpu`／`cuda`／`mps`。社群在 Windows 上有在用，上游作者在 Windows 實測顯存峰值 3.6–6.4GB，佔共用記憶體很少。
- **它一個就能接手兩件事**：
  - 取代 Breeze TTS 2 設計角色參考音（`gen_voice.py --control "聲音描述" --design`）。
  - 暫代 BreezyVoice 念台詞（`gen_voice.py --ref <參考音>`）。代價：上游後來改用 BreezyVoice 是因為台灣腔較準，VoxCPM2 念台詞的口音可能較差，定稿台詞仍建議在桌機或 Colab 用 BreezyVoice。

ARM64 套件狀況：

| 套件 | Windows ARM64 | 影響與對策 |
|---|---|---|
| `voxcpm` 本體 | ✅ 純 Python | — |
| numpy、scipy、numba、llvmlite、sentencepiece | ✅ 有 win_arm64 wheel | — |
| torch／torchaudio | ⚠️ 只能用 NVIDIA 預覽版 | 同 H3 環境 |
| `soxr` 1.1.0（重新取樣，librosa 會 import） | ❌ 只有原始碼，要在 ARM64 上編 C 程式（需 Visual Studio ARM64 建置工具、CMake） | 編不起來 librosa 就無法 import → 送 Colab 或桌機 |
| `torchcodec` | ❌ 沒有 ARM64 wheel（上游語音環境本來也沒裝） | 新版 torchaudio 讀音檔要靠它；官方 issue #119 有人附參考音克隆時報 `Could not load libtorchcodec`。**附參考音克隆這條路要實測**；純聲音設計（`--design`，不讀參考音）較不受影響 |

**Python 版本裝不起來的備案**：VoxCPM 官方推薦 [llama.cpp-omni](https://github.com/tc-mb/llama.cpp-omni)（C++、不需要 Python），載入 VoxCPM2 的 GGUF 權重，支援 CPU／CUDA／Vulkan。NVIDIA 的 Windows on Arm 頁面有列 llama.cpp 支援，但 omni 是分支，Windows ARM64 上能不能編譯沒人驗證過；最差可以純 CPU 跑（慢，但不需要 GPU 驅動）。注意它不經過 `gen_voice.py`，要另外接進流程。

## 建議分工（第一次上機前的預設）

| 工作 | 在哪跑 |
|---|---|
| 劇本、剪接、字幕、自審（CPU） | 筆電 |
| 角色與首幀 | OpenAI Image 2.5（本專案預設，雲端，不受 ARM64 影響）；備選本機 Qwen-Image |
| 配樂（Music 3） | 筆電（ComfyUI 跑得起來的話） |
| H3 影片 | 筆電先試；不行改 `set H3_BACKEND=colab` |
| 角色參考音（聲音設計） | 筆電先試 VoxCPM2（`--control … --design`）；不行改 Colab 或桌機 |
| 台詞配音 | 定稿：BreezyVoice 在 Colab 或桌機；筆電上試做可用 VoxCPM2（口音可能較差） |
| 聽寫校對（faster-whisper） | Colab（`cloud/README.md`），或在桌機跑好再同步過來 |
| 放大 | 筆電，ffmpeg lanczos |

> 專案放在 Google 雲端硬碟，桌機（RTX 5060 Ti 16GB＋64GB）和筆電看得到同一份檔案：配音這類筆電跑不了的步驟，也可以直接在桌機做。

## 第一次上機（照順序，每步結果回填本文件）

1. **硬體偵測**：`python setup\detect_hardware.py` → 應該顯示 RTX Spark 設定的建議。
2. **原生 ARM64 Python**：裝 python.org 的 Python 3.12 **ARM64** 版（或 `uv python install cpython-3.12-windows-aarch64`）。用 x64 版 Python 會走模擬，CUDA 用不了。確認：`python -c "import platform;print(platform.machine())"` → `ARM64`。
3. **驅動與 CUDA**：照 NVIDIA RTX Spark 開發者頁面裝 Windows on Arm 驅動與 CUDA 13.4 preview。確認：`nvidia-smi` 看得到 GPU。
4. **H3 環境**：
   ```
   py -V:3.12-arm64 -m venv C:\AI\H3\venv
   C:\AI\H3\venv\Scripts\python.exe -m pip install --pre --upgrade --only-binary=:all: --extra-index-url https://pypi.nvidia.com/nvtorch_oot_nightly torch torchvision torchaudio
   uv pip install --python C:\AI\H3\venv\Scripts\python.exe --no-deps -r <repo>\setup\env\arm64\requirements_h3_venv_arm64.txt --index-strategy unsafe-best-match
   ```
   ComfyUI 與自訂節點照 `AGENT_SETUP.md` 2a（`Nvidia_RTX_Nodes_ComfyUI` 先不要裝）。
5. **相容性總檢查**：`python setup\spark_check.py --torch-python C:\AI\H3\venv\Scripts\python.exe --out spark_report.json` → 看 `torch.cuda` 是否為 `true`、`gpu_total_gb` 報多少。
6. **ComfyUI 啟動**：`call configs\profile_rtxspark.cmd` 後 `C:\AI\tools\start_comfy.cmd`。
7. **語音環境（VoxCPM2）**：
   ```
   py -V:3.12-arm64 -m venv C:\AI\Voice\venv
   C:\AI\Voice\venv\Scripts\python.exe -m pip install --pre --upgrade --only-binary=:all: --extra-index-url https://pypi.nvidia.com/nvtorch_oot_nightly torch torchvision torchaudio
   uv pip install --python C:\AI\Voice\venv\Scripts\python.exe --no-deps -r <repo>\setup\env\arm64\requirements_voice_venv_arm64.txt --index-strategy unsafe-best-match
   ```
   逐項確認並回填（下面的 `gen_voice.py` 指 `C:\AI\Voice\venv\Scripts\python.exe C:\AI\tools\gen_voice.py`）：
   - `soxr` 有沒有編譯成功：`C:\AI\Voice\venv\Scripts\python.exe -c "import soxr, librosa; print('ok')"`
   - VoxCPM2 載入：`C:\AI\Voice\venv\Scripts\python.exe -c "import voxcpm; print('ok')"`
   - 純聲音設計：`gen_voice.py --control "a calm Taiwanese male teacher in his thirties" --design --text "大家好" --out design.wav`
   - 附參考音克隆（torchcodec 風險）：`gen_voice.py --ref design.wav --text "明天要考試" --out clone.wav`；報 `libtorchcodec` 錯誤就記下來，改送 Colab／桌機
   - 失敗時記下卡在哪個套件，再評估 llama.cpp-omni 備案
8. **smoke test**：`setup\smoke_test.py`；過了再跑 `pipeline\demo_local\run_demo.py`（BreezyVoice、Breeze TTS 2、faster-whisper 那幾段預期要改走 Colab）。
9. 把每一步的結果（成功／失敗、速度、記憶體峰值）寫回本文件，並更新上面的分工表。

## 重新產生 ARM64 套件清單

原清單（`setup/env/requirements_*.txt`）改過之後：
```
python setup\spark_check.py --wheels --emit
```
會重寫 `setup/env/arm64/`：torch 家族與 x64 專用套件註解掉、沒有 ARM64 wheel 的套件改釘到 PyPI 上最新的 ARM64 版本，完全沒有的標 `TODO`。**版本跳動可能造成相容問題**，裝完一定要跑 smoke test。

## 參考

- NVIDIA RTX Spark 產品頁：<https://www.nvidia.com/en-us/products/rtx-spark/>
- NVIDIA Windows on Arm 移植指引（驅動、CUDA 13.4、PyTorch 安裝指令）：<https://developer.nvidia.com/topics/ai/local-ai/port-apps>
- CUDA Toolkit for Windows on Arm 預覽版說明：<https://videocardz.com/newz/nvidia-releases-first-cuda-toolkit-preview-for-windows-on-arm-and-rtx-spark>
- VoxCPM 官方 README（需求、裝置選項、llama.cpp-omni）：<https://github.com/OpenBMB/VoxCPM>
- VoxCPM issue #119（附參考音時 `Could not load libtorchcodec`）：<https://github.com/OpenBMB/VoxCPM/issues/119>
- llama.cpp-omni（VoxCPM2 GGUF，C++ 推論）：<https://github.com/tc-mb/llama.cpp-omni>
