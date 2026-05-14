# Interactive Reading — POC

把 20 篇英文短文做成互動式閱讀的 POC。首篇 pilot：**Unit 1 — Go to the zoo**。

對象：均一 Jutor K–9 英文學習產品線。

---

## 怎麼看 Demo

雙擊 `index.html` 即可在瀏覽器開啟。無需安裝、無需網路。

GitHub Pages 連結（若已啟用）：見 repo 設定 → Pages。

## 4 階段互動

| Stage | 內容 |
|---|---|
| 1. 暖身 Warm-up | 兩題快問快答，激活背景知識 |
| 2. 聽力 Listening | 全文 TTS 朗讀 + karaoke 句子高亮（純輸入，無題目） |
| 3. 詞彙 Vocabulary | 4 張字卡翻面學習 → 課文克漏字回填 |
| 4. 理解 Comprehension | 4 題評量：細節 2 題 + 推理 2 題 |

加分元素：吉祥物 Toro 🐯、計分系統、4 顆星徽章、CSS 動畫、Web Audio 音效、完成 confetti。

## 檔案結構

```
.
├── index.html                # 最終交付 self-contained 單檔（base64 嵌音檔）
├── assets/
│   ├── template.html         # HTML 模板（audio 用 placeholder）
│   ├── build.py              # 把 mp3 base64 嵌入 template → index.html
│   ├── generate_tts.py       # 用 Gemini TTS 生成所有 mp3
│   └── *.mp3                 # TTS 音檔（passage + 4 個生字）
└── docs/
    ├── progress.md           # 專案進度
    ├── decisions.md          # 決策紀錄
    └── meetings/             # 會議紀錄
```

## 重新生成內容

```bash
# 1) 重新生成 TTS 音檔（需 Gemini API key）
export GEMINI_API_KEY=your_key_here
python3 assets/generate_tts.py

# 2) 改完 template.html 後重新組裝 index.html
python3 assets/build.py
```

## 技術棒

- 單一 HTML 檔，雙擊即開
- TTS：Gemini 2.5 Flash TTS（voice: Aoede）→ ffmpeg 轉 mp3 → base64 嵌入
- Karaoke timing：ffmpeg `silencedetect` 自動抓句子切換點
- 音效：Web Audio API 即時合成（無外部音檔）

## 進度與決策

詳見 `docs/progress.md` 與 `docs/decisions.md`。

## 內容來源 / Attribution

本 POC 所使用的閱讀短文（*Go to the zoo*）與生字翻譯來自 **博幼基金會（Boyo Foundation）** 的 *Boyo Reading – intermediate* 教材 Unit 1。

**僅作為教學示範用途**，無商業使用、不對外散布。若有版權疑慮請聯繫專案負責人。
