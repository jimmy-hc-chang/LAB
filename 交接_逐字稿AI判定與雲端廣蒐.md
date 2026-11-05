# 【最新・桌機版 11/5 15:05 更新：下載全部完成】先讀這一段

桌機版工作階段已經用使用者電腦連上公開資訊觀測站，下載「查無資料」公司的股東會年報（doc.twse.com.tw，mtype=F，檔案代碼 F04；先抓 year=115，沒有再抓 114）。

已完成並合併進 `work/公司普查/`：
- `pdf_F/{代號}_annual.txt`：年報全文文字（pdftotext）。6657、6539 文字層亂碼，無法判讀。
- `picks.json`、`hits.json`：這幾家的 annual 欄已更新為觀測站年報（來源網址是觀測站查詢頁＋檔名）。
- `packets/{代號}.txt`：已改成含年報證據的新證據包（原官網段落保留在後面）。
- 101 家中 97 家取得年報（7422、7686、7920、7924 觀測站查無股東會年報，已記入 tried.json）。
- 試跑 build.py：**未判定 69**（待雲端判定）、無 61、已實施 43、只是談論 42、規劃中 28、查無資料 9。

**雲端這次只要做任務 C 的判定（最優先，接手就做）：**
1. 找出 build.py 結果為「未判定」的公司（`python3 -I scripts/build.py work/公司普查 /tmp/x.xlsx` 後看公司明細分頁，或直接比對 cls_*.json 沒有的代號且 hits.json annual.n_ai>0）。
2. 照 `rules.md` 逐家讀 `packets/{代號}.txt` 判定，寫入 `work/公司普查/cls_F.json`（可平行開子代理分批）。
3. 重建 Excel：`python3 -I work/公司普查/scripts/build.py work/公司普查 生技醫療上市櫃_AI與負責任創新篩選_20261105.xlsx`，確認 dropped quotes 為 0，commit 並 push 到本分支。
4. 下載已全部完成，不會再有新檔。

**任務 A、B（訪談逐字稿）不要做，也不要把任何逐字稿內容放進這個 repo：這個 repo 是公開的。** 訪談判定改在桌機版處理。

---

# 交接：訪談逐字稿 AI 判定 ＋ 雲端廣蒐（給用學校帳號重開的新工作階段）

使用者：張弘佶（陽明交大科管所博士生），指導教授陳詩欣老師（簡稱「老師」）。全程用中文回報。
新工作階段的 Google Drive 連接器應已改連學校帳號 **chang.hung-chi.mg11@nycu.edu.tw**。先用 `search_files` 查 `owner = 'me'` 確認是哪個帳號，再開始。

## 一、前一個工作階段已完成（不用重做）

公司普查已完成並存在這個 repo：

- `生技醫療上市櫃_AI與負責任創新篩選_20261105.xlsx`（分頁：摘要／公司明細／查無資料）。252 家（上市 62、上櫃 98、興櫃 92）。目前判定：已實施 43、規劃中 28、只是談論 42、無 38、查無資料 101。
- `work/公司普查/`：可重建 Excel 的全部中間檔。
  - `rules.md`：AI 四層級判定規則與引文規則（**逐字稿判定請用同一套**）。
  - `scripts/build.py`：重建 Excel（用法 `python3 -I scripts/build.py <work目錄> <輸出xlsx>`；會自動把檔案屬性設成張弘佶、去掉 openpyxl 字樣）。
  - `cls_*.json`：各批判定結果；`overrides.json`：人工覆寫；`packets/`：每家證據包；`hits.json`：關鍵詞命中；`picks.json`／`found_*.json`／`tried.json`：年報與永續報告書網址及嘗試紀錄。
- 公開資訊觀測站（doc.twse.com.tw／mops）在雲端環境**下載不到**，年報全部改從公司官網取得；這點摘要分頁已寫明。

## 二、這次要做的事

### 任務 A（最優先）：訪談逐字稿的 AI 判定，附原文證據

使用者的要求（原話）：「要像我的那份 Excel 檔一樣，分析逐字稿所有內容，哪些有關 AI 的，把它分類成 AI 相關，但要有證據，你是看到哪句判斷有 AI 應用的。」

1. 先讀使用者的訪談 Excel：
   `https://docs.google.com/spreadsheets/d/1AmF0os6aP5COm3LhYQSY9nBeYI6O0U-f/edit?gid=1414040422`
   （file id `1AmF0os6aP5COm3LhYQSY9nBeYI6O0U-f`，是上傳到 Drive 的 .xlsx）。裡面有 37 位受訪者與每份逐字稿的連結。以它的名單為準。
2. 逐字稿所在資料夾（使用者提供）：
   - https://drive.google.com/drive/folders/1qm0sAWWCU16JDY33Qp_c858E5AweuXOD
   - https://drive.google.com/drive/folders/1i0alk_oUG7JcDl1FDKKPZHd6G15HtP_E
   - https://drive.google.com/drive/folders/1eXUkZok6ltw25ymKuZ8a1oQGvqBlhTKW
   - https://drive.google.com/drive/folders/1Aozxv8El74QGIk7X5xNIWLvyR9eaoVXU
   - https://drive.google.com/drive/folders/1hG7Ha_zR10k17hbFCTCYOYN63pBt-bfA
   用 `search_files` 的 `parentId = '<id>'` 列出內容；找不到的再用 `fullText contains '<受訪者姓名>'` 或 `title contains` 廣蒐整個雲端（使用者明確說：「我的雲端妳應該可以自己搜尋」）。
3. 已知讀不到、要特別找的四份：
   - 汪彥佑（承鋆生醫）
   - 柯屹又（財團法人生物技術開發中心 智慧生醫組）
   - 周維宜（永昕生醫）
   - 鄭宗達（工研院 TIBIC）**2025 年**校對稿（舊帳號只有 2022-09-20 那場，Google Doc id `19GiaEam0UdjH16ekskz9RO2InWgJvUO3iBIP7SE57yk`；2025 版要另外找）
4. 每位受訪者讀**全文**（`read_file_content`；docx／pdf／Google Doc 都可以讀），然後：
   - 判定 AI 層級，四選一，標準同 `work/公司普查/rules.md`：
     - 已實施：受訪者所屬機構自己已在使用、販售或部署 AI 產品／流程。
     - 規劃中：有具體計畫、試辦、研發中。
     - 只是談論：願景、趨勢、投資 AI 新創（創投、加速器投資 AI 新創一律算這級）、教育訓練。
     - 無：全文沒有與該機構自身相關的 AI 內容。
     - 讀不到：檔案找不到或打不開（寫明試過哪些搜尋）。
   - **智慧照護、資訊系統、數位轉型、大數據、遠距、物聯網本身不算 AI**；要原文明說 AI／人工智慧／機器學習／深度學習／演算法模型才算。前一次使用者自己判的 20 位「已實施」裡有不少其實是智慧照護或資訊系統，這次要用證據把它們分開。
   - 每位附 1–3 句**逐字原文**（≤80 字，不可改寫、不可加省略號），註明檔名與段落位置（例如「第 12 段，受訪者發言」）。程式逐字比對：把引文與全文都去掉空白後做子字串比對，不符的刪掉。
   - 另記一欄：逐字稿裡有沒有談到負責任創新相關議題（病患參與、倫理、資料隱私、法規、利害關係人溝通），有就附一句原文。
5. 產出 Excel：`訪談逐字稿_AI與負責任創新判定_YYYYMMDD.xlsx`，分頁：摘要（各層級人數、與使用者原判定的對照表：原判定 vs 本次判定、差異說明）／受訪者明細（每人一列：編號、姓名、單位、職稱、檔名、Drive 連結、AI 層級、判定依據、引文 1–3 與位置、負責任創新議題與引文）／讀不到（試過的來源）。檔案屬性作者與最後修改者設成「張弘佶」，不要留 python／openpyxl 字樣（`work/公司普查/scripts/build.py` 最後一段有做法）。
6. 做完用傳檔功能把 Excel 傳給使用者，並 commit 到 repo 分支 `claude/biotech-ai-screening`。

使用者原本的 37 位判定（來自 11/5 的 Excel，供對照用）：已實施 20、規劃中 3、只是談論 10、無 1、讀不到 3。

### 任務 B：雲端廣蒐

使用者說「我還需要妳去廣蒐我的雲端」。目前已知要找的：上面四份逐字稿、訪談 Excel；另外請順手把學校帳號雲端裡所有「智慧生醫／生技訪談」相關的逐字稿、訪談清單、錄音轉譯檔列成一張清單（檔名、Drive 連結、修改日期、對應受訪者），放進 Excel 的「雲端檔案清單」分頁，讓使用者知道還有哪些檔沒進名單。

### 任務 C（有時間才做）：公司普查的查無資料 101 家

主要卡在官網沒放 PDF、下載被擋（403）、PDF 文字層亂碼（6539 麗彤、6704、6574、4120、3205）。如果使用者能從公開資訊觀測站手動下載年報放到 Drive 或 repo，就用 `work/公司普查/` 的流程續做：`pdftotext` → `scripts/hits.py` → `scripts/mkinput.py` → 判定寫 `cls_F.json` → `scripts/build.py`。

## 三、規則（使用者固定要求，一定要遵守）

- 不准寄任何信，不准在任何網站送出表單。
- 雲端硬碟一律唯讀：不要建立、修改、移動、分享或刪除任何檔案。
- 報告裡不要提學生個人的貢獻或論文。
- 機構名稱不要自行翻譯，沒有官方中文名就保留原文。
- 只寫有來源的事：沒有來源就留空，不要寫「待補」「待確認」，不要用猜的。
- 邊做邊存：每完成約 10 位受訪者就更新一次 Excel 並 commit。
- 引文必須是原文，程式逐字核對後才能進 Excel。

## 四、研究脈絡（老師 11/3、11/4 交代）

老師要寫「台灣智慧生醫的負責任創新」，目標期刊 Journal of Responsible Innovation。做法：先用全部上市櫃生技醫療公司的年報、永續報告書普查，再用訪談稿收斂；「AI 篩選要比 Google News 更精準」，新聞只能當線索不能當證據。公司側與訪談側要用同一套判定標準，兩邊才能對照。
