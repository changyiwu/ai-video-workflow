# 填 film.json（把鏡表變成製作設定）

欄位完整說明在 `<repo>/pipeline/template_local/README.md`〈film.json 欄位〉；技術規則的完整版與理由在 `<repo>/docs/03_規則與踩坑.md` §2–4。本檔只列**填寫時最常出錯、一定要照做**的事，不重抄那兩份。

## 開始前

- `films/<片名>/需求確認.md` 與 `劇本.md`（含鏡表）都已經使用者確認。
- 每個角色的 `look`、`voice_design` **照抄** `films/角色/<角色>/README.md`，不要自己改寫外觀。
- 定妝已定：把 `<角色>_turn.png`、`<角色>_expr.png`（千問備選為 `<角色>.png`）複製到 `out/chars/`，`make_film.py` 看到檔案已存在就會沿用，不會重生。
- 有做預演的話，旁邊開著 `camera_plan_v<N>.json`：`visible`、`motion` 要跟這裡一致。

## 鏡表 → shots[]

| 鏡表欄位 | `shots[]` | 注意 |
|:---|:---|:---|
| 鏡號 | `id` | |
| 秒數 | `dur` | 4–12；有台詞會自動延長到夠念完 |
| 場景／景別 | `scene` | 同場景的鏡頭都裁**同一張母版**；景別、窗戶方向跨鏡一致 |
| 畫面裡的角色 | `refs` | **只放入鏡演戲的人**。寫了沒入鏡的角色 H3 會把他叫進畫面 |
| 首幀畫面 | `frame` | 英文；景別、誰在哪、做什麼、表情、窗戶在哪一邊 |
| 動作 | `action` | 英文；見下方〈逐鏡加註〉 |
| 台詞 | `line` | 沒台詞寫 `null`（給靜音音軌，角色才不會嘟囔） |
| 運鏡 | `camera`（選填） | 不寫就用 `h3.camera`（預設靜止三腳架）；見〈運鏡〉 |
| 額外限制 | `extra_constraints`（選填） | 這一鏡才需要的限制句 |

## 誰在畫面裡（最常退件的來源）

- **單人鏡**：提示詞完全不提其他人；`refs` 只放那一人。需要時在 `extra_constraints` 加：
  `Only the <角色> is visible. The other remains outside the frame to the right. Exactly one visible person.`
- **多人同框**：寫 `Exactly N people`，並寫清楚左右：
  `Both must stay visible simultaneously, <A> LEFT and <B> RIGHT, throughout the complete shot.`
- **說話者在畫面外**：台詞照常給，`action` 寫明說話者 offscreen、畫面中的人嘴巴不動。
- 不要讓角色橫向走（H3 會跟拍、桌椅跟著滑），改原地轉身。

## 運鏡

- 預設靜止：`h3.camera` 與 `h3.constraints` 已有三腳架鎖定句（範例：`LOCKED-OFF STATIC CAMERA on a tripod`）。**靜止鏡不要在 `action` 裡寫推進、搖鏡**——自相矛盾是已記錄的踩坑。
- 只有真的要運鏡的鏡頭才在該鏡寫 `camera`；有做預演時，運鏡必須跟 `camera_plan` 的 `motion` 一致（`static`／`push`）。
- 空景、時鐘、桌面特寫：用靜圖＋慢推，不要讓 H3 自由發揮（會自己加人或切走）。

## 逐鏡加註（依實際問題加，不要每鏡都塞）

| 鏡頭類型 | 加在 `action` 或 `extra_constraints` |
|:---|:---|
| 動作要跟台詞同時發生 | 寫成「說到那個字的瞬間」做動作（例：stands up as he says …），否則慢半拍 |
| 道具不可舉起展示 | `hand quietly tucks paper below the crop, without raising or displaying it.` |
| 頭套、玩偶等實體道具 | `is a real sewn costume prop with rigid button eyes: no eyelids, no blinking or animal expressions. Only the real human face beneath it performs.` |
| 沒台詞 | `He does not speak.`（`line: null` 之外也寫進 `action`） |
| 長音 | 寫長音秒數＋「嘴維持張開到聲音結束」 |
| 畫面裡不能有字 | `frame_suffix` 已寫 No text；黑板、紙張再寫一次 blank |

## 對嘴的界線

- **配音先定稿**，H3 用同一份音訊當引導；不要事後換聲音掩蓋不同步。
- **長靜默**（說話 → 停頓 → 再說話）最容易露餡：盡量拆成兩鏡；拆不了就在 `action` 寫明靜默時段嘴巴閉上。
- 不用嘴／眼 XY 平移貼片修表演；未做逐音素量測就照實寫「未做逐音素認證」，不寫「完美對嘴」。

## 填完自查

- [ ] 每鏡 `refs` 只有入鏡演戲的人，單人鏡沒有提到其他人
- [ ] 靜止鏡的 `action` 沒有寫運鏡；有運鏡的鏡頭跟預演契約一致
- [ ] 沒台詞的鏡頭 `line: null` 且 `action` 寫明不說話
- [ ] 同場景各鏡的母版、景別、窗戶方向一致
- [ ] `look` 是照抄角色 README，不是改寫
- [ ] 片尾 `ending.cards` 的生圖工具名稱符合實際用的後端（混用 `agent-draw` 時要手動核對）
