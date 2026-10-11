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
- 其餘程式邏輯、模型下載清單、音效（Freesound CC0）與圖片素材未修改。
