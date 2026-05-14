# Progress — Interactive Reading

進度時間軸。每完成一個小段落（spec 對齊、wave 啟動、wave 完工等）就 append 一筆。

---

## 2026-05-12 — 專案啟動

- 確定方向：把 20 篇英文短文改成互動式閱讀（B 方向：中等版 template）
- 確定使用情境：課中老師帶 + 學生自學
- 確定分級：低 / 中 / 高三級，首篇 pilot 用「低」級的 *Go to the zoo*
- 確定提案受眾：主管 + 合作夥伴
- 確定 working directory：獨立資料夾 `~/Desktop/ing/interactive-reading/`（未來工程實作再整合進 jutor-mvp）
- 建立 `docs/` 三件套（progress / decisions / meetings）
- 互動 5 階段骨架已 draft：暖身 → 聽力 → 詞彙 → 理解 → 口說

## 2026-05-13 — Unit 1 POC v1 完成

- 鎖定來源教材：`reading_2.pdf`（Boyo Reading – intermediate），首篇 Unit 1 *Go to the zoo*
- POC 範圍對齊：4 階段（跳過口說），目的是給主管/夥伴看互動長相
- TTS 路徑決議：Gemini TTS（model `gemini-2.5-flash-preview-tts`、voice `Aoede`），用 `.env` 既有 GEMINI_API_KEY
- 產出檔：
  - `index.html`（332 KB，雙擊即開，self-contained，base64 嵌 5 段 mp3）
  - `assets/generate_tts.py`（重新生 mp3 用）
  - `assets/build.py`（重新組裝 HTML 用）
  - `assets/template.html`（HTML 主體，audio 用 placeholder）
  - `assets/*.mp3`（passage + 4 個生字朗讀）
- 4 階段互動規格已實作：
  - 暖身：兩題快問快答（無對錯，prime 情境）
  - 聽力：播放全文 + 1 題大意題
  - 詞彙：4 字翻卡（含中文/例句/朗讀）→ 4 組配對
  - 理解：全文（生字 hover tip）+ 2 題選擇題（原書題目），答對 highlight 課文依據句
- 待 user 驗收：UI、音檔、互動流暢度。觀察點：難度是不是「低」級（本書其實標 intermediate，可能要回頭修 decisions.md）

## 2026-05-14 — Unit 1 POC v2（大改造）

依 v1 驗收 feedback 重做：
- Stage 2 加課文 + karaoke 句子高亮（用 ffmpeg silencedetect 自動抓 6 句切換時點：0 / 2.66 / 4.46 / 6.89 / 9.63 / 12.94 秒）
- Stage 3 配對改為「課文克漏字」（4 個生字回填課文 4 個空格，銜接 Stage 4 閱讀）
- 加吉祥物 Toro 🐯，每個 stage 換對話泡泡引導；答對 cheer 動畫、答錯 sad 動畫
- 計分系統（0–100）+ 4 顆星徽章 + 完成慶祝（confetti 飄落）
- Web Audio API 合成音效（答對上行琶音、答錯下行、翻卡 click、星星收集 chord）
- 配色加暖色點綴（橘 #f59e0b 與藍漸層）+ 浮動裝飾（☁️☀️🌳⭐ 隨機飄）
- 翻卡 3D flip 動畫、選項 hover 微動、stage 切換 fade+slide

產出檔：`index.html`（348 KB，仍為 self-contained 單檔）

## 2026-05-14 — Unit 1 POC v2.1（題目集中到 Stage 4）

User feedback：v2 中 Stage 2（1 題）vs Stage 4（2 題）的不對稱沒有清楚的教學意圖。決定**所有題目集中到 Stage 4**：
- Stage 2 改純聽讀（karaoke），移除 MCQ；用「我聽完了 →」手動過關按鈕（學生可以多聽幾次）
- Stage 4 變 4 題，分兩區：
  - 📘 細節題（句中直接找）：Q1 Who with → Family；Q2 Sister likes → Bears and monkeys
  - 🧩 推理題（綜合全文）：Q3 Weather → nice；Q4 Which NOT true → C
- 過關條件：Stage 2 點「我聽完了」、Stage 4 四題全答完
- 教學意圖明確：聽力 = 輸入暴露（無評量壓力），理解 = 整合輸出（完整評量）

## 2026-05-14 — 上架 GitHub + 開放 Pages

- Repo：`chingchinglin/interactive-reading`（個人帳號）
- Demo URL：https://chingchinglin.github.io/interactive-reading/
- 可見性：**Public**（free 方案 Pages 限制只能 public）
- 上架前清理：
  - 移除 `assets/generate_tts.py` 的 hardcoded API key fallback
  - `.gitignore` 排除 `reading_2.pdf`（版權教材，不上傳）、`.env`、`*.pdf`
- 待觀察的版權邊界：4 句 zoo 短文 + 4 個生字翻譯來自 Boyo Reading，量少但已隨 repo public。若主管/版權單位有疑慮可再評估

## 2026-05-14 — 計分規則修正

User 在驗收時問「計分怎麼算」，查 code 後發現原本是「行為分 + 答題分」混用：

- 暖身完成 +10、聽完按鈕 +10、翻完 4 卡 +10、克漏字每格 +5、理解每題 +20
- 理論最大值 130，被 Math.min cap 在 100，看不出「全對」和「跑流程不答對」的差別
- 學生光跑流程不答題就能拿 50 分（無評量意義）

改成「只答對才加分，總分 100」：
- 克漏字每格 +10（4×10 = 40）
- 理解題每題 +15（4×15 = 60）
- 行為觸發（暖身、聽完、翻卡）不再加分；星星徽章仍標記 stage 完成（與分數脫鉤）

意圖：分數反映「真實理解程度」，學生答錯就拿不到分。
