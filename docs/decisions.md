# Decisions — Interactive Reading

決策紀錄。格式：日期、結論、理由、（必要時）替代方案。

---

## 2026-05-12 — 互動深度走 B（中等版 template）

**結論**：採用「一套互動 template × 20 份內容素材」模式。每篇含 5 階段：暖身 → 聽力 → 詞彙 → 理解 → 口說。

**理由**：
- 20 篇要規模化，第一篇定下的框架決定後面 19 篇的製作成本
- A（輕量版）跟看 PDF 差別不大，學生黏著度低
- C（AI 互動版）價值高但前期投入大、風險高
- B 是規模化的甜蜜點：一次設計好 template，剩下填內容即可

**替代方案**：
- A 輕量版：每篇 1–2 小時，但互動弱
- C AI 互動版：建議未來挑 2–3 篇加碼，不在 MVP 範圍

---

## 2026-05-12 — 使用情境：課中老師帶 + 學生自學

**結論**：兩個場景共用同一份內容，前端模式不同（老師有控制台、學生有自動引導）。

**理由**：使用者（PM）目前無意先排他單一場景；兩場景同步設計可避免後期重做。

---

## 2026-05-12 — 分級邏輯：低 / 中 / 高

**結論**：互動 template 不變，調整各階段「難度旋鈕」。

- 低：60–80 字、4–5 生字、過去式主動句
- 中：100–150 字、8–10 生字、混合時態 + 因果連接詞
- 高：150–200 字、12–15 生字、含轉折 / 比較 / 關係子句

**理由**：避免每級重做 UI，內容素材分級即可。

**待驗證**：Wave 2 做中、高各 1 篇時，確認 template 撐得住。

---

## 2026-05-12 — Working directory：獨立資料夾（A 方案）

**結論**：放 `~/Desktop/ing/interactive-reading/`，不放 jutor-mvp 內。

**理由**：
- 目前是溝通階段（提案、規格、會議紀錄），主要產出是文件不是 code
- 給合作夥伴分享時整個資料夾打包即可
- Claude context 乾淨，不被 jutor-mvp 工程脈絡干擾
- 未來進工程階段，spec 搬一份到 jutor-mvp，code 進 jutor-mvp

**替代方案**：
- B：放 jutor-mvp 內 → 工程接續無縫，但提案階段過早載入工程 context
- C Hybrid：提案階段 A，工程階段切 B（= 本案的長期路徑）

---

## 2026-05-13 — TTS 路徑：Gemini TTS（model `gemini-2.5-flash-preview-tts`、voice `Aoede`）

**結論**：用 Gemini 2.5 Flash TTS 預先生成 mp3、ffmpeg 轉檔後 base64 嵌進 HTML。voice 用 `Aoede`（清晰女聲）。

**理由**：
- 既有 `.env` 已有 `GEMINI_API_KEY`，零額外設定
- POC 預先生成（非執行時呼叫），mp3 嵌 HTML 後不依賴網路或 API，demo 穩定
- 單篇成本 < $0.001 USD，可忽略

**替代方案考慮過但未採用**：
- 公司既有 Azure TTS（token endpoint 在 Cloud Run）：token endpoint 有 origin 限制，從 `file://` 拿不到 token；要繞需要架設前端代理，POC 不划算
- OpenAI TTS：穩定但需 user 新建 API key，多一步設定
- 瀏覽器內建 Web Speech API：零成本但音質一般，demo 視覺加分弱

**Karaoke timing 怎麼來**：用 `ffmpeg silencedetect` 自動抓句子停頓邊界（不是手算詞數比例）— 6 句切換時點 0 / 2.66 / 4.46 / 6.89 / 9.63 / 12.94 秒。

---

## 2026-05-14 — 題目集中到 Stage 4（聽力純輸入、理解作評量）

**結論**：所有 MCQ 評量都放最後階段。Stage 2 純聽讀（karaoke + 「我聽完了」按鈕），Stage 4 出 4 題（2 細節 + 2 推理）。

**理由**：
- V2 中 Stage 2（1 題）vs Stage 4（2 題）的不對稱沒有清楚的教學意圖，user 在驗收時直接 challenge
- 拆分為「輸入階段（聽力、詞彙）= 暴露 + 學習」、「輸出階段（理解）= 整合 + 評量」，職能比題數平均化更重要
- 細節題（句中直接找）+ 推理題（綜合全文）分區呈現，讓「評量」這個 stage 有重量感

**替代方案**：
- 維持 1+2：有職能區隔但 user 看不出設計意圖
- 對稱 2+2：題數均衡但聽力階段就要評量，干擾「純輸入暴露」的設計
- 重新分工但保留 stage 2 細節題：方向對但 user 想更乾淨

---

## 2026-05-14 — 計分模型：只「答對」才加分，總分 100

**結論**：克漏字每格 +10（4×10 = 40）、理解題每題答對 +15（4×15 = 60）。行為觸發（暖身完成、聽完按鈕、翻卡）不再加分。

**理由**：
- 原本「行為分 + 答題分」混用：跑流程不答題能拿 50 分；理論最大 130 被 cap 100，分數無法區分「全對」和「半對 + 流程跑完」
- 分數要反映「真實理解程度」，否則星星和分數兩個指標形同重複
- 星星徽章保留作 stage 完成標記（與分數脫鉤）：星星 = 走完流程、分數 = 答對程度

**替代方案**：
- 保留行為分：簡單但失去評量意義
- 答錯阻擋進度：教學嚴格但 demo 流暢度差，挫折感重

---

## 2026-05-14 — GitHub 上架：個人 repo + Public + Pages

**結論**：`chingchinglin/interactive-reading`（個人帳號）、**Public**、啟用 GitHub Pages。Demo URL：https://chingchinglin.github.io/interactive-reading/

**理由**：
- 個人帳號合 working dir decision（POC/提案階段個人 sandbox）；未來進工程才搬 org/jutor-mvp
- Public 是被迫的：GitHub Free 方案的 Pages 只支援 public repo
- Demo URL 一條丟給主管/夥伴最低摩擦，比下載 zip 直觀

**上架前必做**（避免 secret 洩漏 + 版權問題）：
- 拿掉 `generate_tts.py` 的 hardcoded API key fallback（改成沒 env 就報錯）
- `.gitignore` 排除 `reading_2.pdf`（版權教材）、`.env`、`*.pdf`

**替代方案考慮過但未採用**：
- Private + Cloudflare Pages 接：保留私密但多一層設定，POC 不值得
- Private + GitHub Pro（~$4/月）：簡單但要花錢
- Private + 寄 index.html：簡單但失去「丟網址」的低摩擦

---

## 2026-05-14 — 版權標示：博幼基金會、僅作教學示範用途

**結論**：README + 頁面 footer 各一份標示「短文與生字翻譯來源：博幼基金會（Boyo Foundation）· Boyo Reading – intermediate Unit 1 · 僅作教學示範用途」。

**理由**：
- 4 句課文 + 4 個生字翻譯隨 public repo 公開，需明確標示來源做合理引用
- README 給 repo 訪客看；footer 給 demo 訪客看 — 兩個入口都要

**Follow-up**：若主管或博幼方面有版權疑慮，再回頭評估（移除內容、改授權、或申請正式授權）。
