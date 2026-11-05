import json,glob,re,sys,os,collections
from openpyxl import Workbook
from openpyxl.styles import Font,Alignment,PatternFill
from openpyxl.utils import get_column_letter
B=sys.argv[1]; OUT=sys.argv[2]
cs=json.load(open(B+'/companies.json')); h=json.load(open(B+'/hits.json')); picks=json.load(open(B+'/picks.json'))
tried=json.load(open(B+'/tried.json')) if os.path.exists(B+'/tried.json') else {}
cls={}
OV=json.load(open(B+'/overrides.json')) if os.path.exists(B+'/overrides.json') else {}
for f in sorted(glob.glob(B+'/cls_*.json')):
    try: cls.update(json.load(open(f)))
    except Exception as e: print('bad',f,e)
def norm(s): return re.sub(r'\s+','',s or '')
drop=collections.Counter()
def verify(code,q):
    if not q or not q.get('text'): return False
    p=B+f'/packets/{code}.txt'
    if not os.path.exists(p): return False
    ok=norm(q['text']) in norm(open(p).read())
    if not ok: drop[code]+=1
    return ok
rows=[];nodata=[]
for c in cs:
    k=c['code']; v=h[k]; pk=picks.get(k,{})
    a=v['annual'];e=v['esg'];s=v['site']
    pa=pk.get('annual'); pe=pk.get('esg')
    na=a['n_ai'] if a else None; ne=e['n_ai'] if e else None; ns=s['n'] if s else 0
    r=dict(code=k,abbr=c['abbr'],name=c['name'],market=c['market'],sub=c.get('sub',''),web=c['web'],icai=c.get('ic_ai',''))
    r['a_url']=pa[2] if (pa and a) else ''; r['a_lab']=pa[3] if (pa and a) else ''; r['a_n']=na; r['a_pg']=a['pages'] if a else None
    r['e_url']=pe[2] if (pe and e) else ''; r['e_lab']=pe[3] if (pe and e) else ''; r['e_n']=ne; r['e_pg']=e['pages'] if e else None
    r['s_n']=ns; r['s_pages']=len(json.load(open(f'{B}/sites/{k}/done.json'))['pages']) if os.path.exists(f'{B}/sites/{k}/done.json') else 0
    cl=cls.get(k)
    if cl and k in OV: cl=dict(cl,**OV[k])
    r['quotes']=[];r['ri_topics']='';r['ri_q']=None;r['basis']=''
    if cl:
        r['level']=cl.get('level','')
        r['quotes']=[q for q in cl.get('quotes',[]) if verify(k,q) and len(norm(q['text']))<=90][:3]
        r['basis']=cl.get('basis','')
        rq=cl.get('ri_quote')
        if rq and verify(k,rq): r['ri_q']=rq; r['ri_topics']=cl.get('ri_topics','')
        elif cl.get('ri_topics') and not rq: r['ri_topics']=''
        if r['level'] in ('已實施','規劃中','只是談論') and not r['quotes']:
            r['basis']=(r['basis']+'（引文核對未通過，層級改列待人工判讀）').strip(); r['level_raw']=r['level']; r['level']='引文未通過核對'
    else:
        if (a or e) and (na or 0)+(ne or 0)==0 and ns==0:
            r['level']='無'; r['basis']='已讀取之年報／永續報告書與官網頁面均未出現 AI 相關詞'
        elif not a and not e and ns==0:
            r['level']='查無資料'
        else:
            r['level']='未判定'
    if r['level']=='查無資料':
        src=[f"公司官網（{c['web']}，爬取 {r['s_pages']} 頁，未出現 AI 強詞，未找到年報／永續報告書 PDF）"]
        pass
        for kk,lab in (('annual','年報'),('esg','永續報告書')):
            if pk.get(kk) and not v[kk]:
                pf=f'{B}/pdf/{k}_{kk}.pdf'
                head=open(pf,'rb').read(400) if os.path.exists(pf) else b''
                why='伺服器拒絕下載（403/406/防機器人頁）' if re.search(rb'403|406|Forbidden|Just a moment|Not Acceptable',head) else ('連結失效（404）' if b'404' in head or b'Not Found' in head else ('非文字型 PDF 或下載失敗' if head[:4]==b'%PDF' or not head else '連結非 PDF 檔'))
                src.append(f'{lab}連結 {pk[kk][2]}：{why}')
        if k in tried: src.append('網路搜尋／官網查找：'+tried[k])
        nodata.append((c,'；'.join(src)))
    rows.append(r)
wb=Workbook(); ws0=wb.active; ws0.title='摘要'
ws=wb.create_sheet('公司明細'); wn=wb.create_sheet('查無資料')
H=['股票代號','公司簡稱','公司名稱','市場別','細分類（櫃買中心產業價值鏈）','官網','AI層級','判定依據',
   '引文1','引文1來源','引文1網址','引文1頁碼','引文2','引文2來源','引文2網址','引文2頁碼','引文3','引文3來源','引文3網址','引文3頁碼',
   '年報網址','年報網頁標示','年報PDF頁數','年報AI相關詞次數','年報每百頁次數',
   '永續報告書網址','永續報告書網頁標示','永續報告書PDF頁數','永續報告書AI相關詞次數','永續報告書每百頁次數',
   '官網爬取頁數','官網AI段落數','負責任創新議題','負責任創新引文','負責任創新引文來源','負責任創新引文網址','負責任創新引文頁碼','櫃買中心「人工智慧」產業鏈收錄','備註']
ws.append(H)
def per100(n,p): return round(n*100/p,1) if (n is not None and p) else None
for r in rows:
    q=r['quotes']+[None]*3; L=[r['code'],r['abbr'],r['name'],r['market'],r['sub'],r['web'],r['level'],r['basis']]
    for x in q[:3]: L+= [x['text'],x.get('src',''),x.get('url',''),x.get('page','')] if x else ['','','','']
    L+=[r['a_url'],r['a_lab'],r['a_pg'],r['a_n'],per100(r['a_n'],r['a_pg']),r['e_url'],r['e_lab'],r['e_pg'],r['e_n'],per100(r['e_n'],r['e_pg']),r['s_pages'],r['s_n'] if r['s_pages'] else None,r['ri_topics']]
    rq=r['ri_q']; L+= [rq['text'],rq.get('src',''),rq.get('url',''),rq.get('page','')] if rq else ['','','','']
    L+=[r['icai'],'AI 僅用於內部辦公或資安工具' if re.search(r'僅內部|內部辦公|內部資安|IT工具',r['basis']) else '']
    ws.append(L)
wn.append(['股票代號','公司簡稱','公司名稱','市場別','官網','試過的來源'])
for c,src in nodata: wn.append([c['code'],c['abbr'],c['name'],c['market'],c['web'],src])
# summary
LV=['已實施','規劃中','只是談論','無','查無資料','未判定','引文未通過核對']
mk=['上市','上櫃','興櫃']
cnt=collections.Counter((r['market'],r['level']) for r in rows)
ws0.append(['生技醫療上市櫃公司 AI 實際使用與負責任創新篩選'])
ws0.append(['資料日期','2026-11-05（公司名單：證交所／櫃買中心 OpenAPI 公司基本資料，出表日期 115/11/04）'])
ws0.append([])
ws0.append(['一、家數']); ws0.append(['市場別','家數','讀到年報','讀到永續報告書','兩者皆有','官網有爬到頁面'])
for m in mk+['合計']:
    rr=[r for r in rows if m=='合計' or r['market']==m]
    ws0.append([m,len(rr),sum(1 for r in rr if r['a_pg']),sum(1 for r in rr if r['e_pg']),sum(1 for r in rr if r['a_pg'] and r['e_pg']),sum(1 for r in rr if r['s_pages'])])
ws0.append([])
ws0.append(['二、AI 層級家數']); ws0.append(['AI層級']+mk+['上市＋上櫃','合計（含興櫃）'])
for l in LV:
    a=[cnt[(m,l)] for m in mk]
    if sum(a)==0: continue
    ws0.append([l]+a+[a[0]+a[1],sum(a)])
ws0.append([])
lst=[r for r in rows if r['market']!='興櫃']
ws0.append(['三、與 TEJ 初步數字對照'])
ws0.append(['項目','TEJ 初步','本表','說明'])
ws0.append(['生技醫療公司家數',201,len(lst),'本表＝證交所產業別代碼 22（上市）＋櫃買中心產業別代碼 22（上櫃）；興櫃另有 %d 家未計入'%sum(1 for r in rows if r['market']=='興櫃')])
ws0.append(['有永續報告書家數',124,sum(1 for r in lst if r['e_pg']),'本表數字為「本次實際下載並讀到永續報告書」的上市櫃家數，非「有發行」家數'])
ws0.append([])
ws0.append(['四、方法說明'])
M=['1. 名單：證交所 OpenAPI t187ap03_L（上市公司基本資料）與櫃買中心 OpenAPI mopsfin_t187ap03_O／_R（上櫃／興櫃公司基本資料），篩選產業別代碼 22（生技醫療業）。',
 '2. 細分類：櫃買中心產業價值鏈資訊平台（ic.tpex.org.tw）製藥（C100）、醫療器材（C200）、食品生技（C300）、再生醫療（C400）各子產業的公司清單；一家公司可同時列於多個子產業。',
 '3. 文件來源：年報與永續報告書 PDF 先由各公司官網（投資人專區、股東會、企業永續頁面）取得；官網找不到的公司，年報改從公開資訊觀測站（doc.twse.com.tw，股東會年報）下載，來源以「年報網址」與「年報網頁標示」欄為準。優先取 2025 年度年報（115 年股東會年報）與最新一期永續報告書；官網只有較早版本時取最新可得版本，版本以「網頁標示」欄為準；部分公司官網僅有 2024 年度或英文版年報。',
 '4. AI 相關詞：AI、AIoT、GenAI、LLM、ChatGPT、Copilot、人工智慧、人工智能、機器學習、深度學習、神經網路、大型語言模型、生成式、電腦視覺、影像辨識、智慧醫療、演算法、大數據及英文全名。「AI相關詞次數」為全文出現次數，「每百頁次數」＝次數÷PDF頁數×100。',
 '5. AI 層級判定標準與訪談稿相同：已實施（公司自己使用、販售或部署 AI 產品或流程）、規劃中（具體計畫、試辦、研發中）、只是談論（願景、趨勢、投資 AI 公司、教育訓練）、無（文件中無與公司自身相關之 AI 內容）。智慧醫療、資訊系統、數位轉型、大數據本身不視為 AI。',
 '6. 引文：皆為 PDF 文字層或官網頁面之原文連續片段（PDF 換行已合併），每句經程式逐字比對證據文字；未通過比對的引文已刪除。頁碼為 PDF 檔案頁序（PDF第N頁），可能與印刷頁碼不同。',
 '7. 負責任創新欄：以永續報告書（無則年報）中病患參與、倫理、隱私／個資、資訊安全、受試者保護、IRB、利害關係人溝通等段落判定，附一句原文。',
 '8. 「無」＝有讀到文件或官網但未出現 AI 相關內容；「查無資料」＝未取得年報、永續報告書，且官網未出現 AI 強詞，試過的來源列於「查無資料」分頁。外部新聞媒體報導未作為證據；「官網」來源之引文包含公司官網自行發布的產品頁與新聞稿頁面。']
for m in M: ws0.append([m])
# formatting
for w in (ws,wn):
    for cell in w[1]: cell.font=Font(bold=True); cell.fill=PatternFill('solid',fgColor='DDEBF7')
    w.freeze_panes='C2'
widths={1:9,2:12,3:24,4:7,5:28,6:24,7:12,8:40,9:50,13:50,17:50,34:50}
for i in range(1,len(H)+1): ws.column_dimensions[get_column_letter(i)].width=widths.get(i,14)
for row in ws.iter_rows(min_row=2):
    for cell in row: cell.alignment=Alignment(wrap_text=cell.column in (8,9,13,17,34),vertical='top')
wn.column_dimensions['C'].width=28; wn.column_dimensions['E'].width=30; wn.column_dimensions['F'].width=100
ws0.column_dimensions['A'].width=22; ws0.column_dimensions['D'].width=60
ws0['A1'].font=Font(bold=True,size=14)
ws.auto_filter.ref=ws.dimensions
wb.properties.creator='張弘佶'; wb.properties.lastModifiedBy='張弘佶'; wb.properties.title='生技醫療上市櫃 AI 與負責任創新篩選'
wb.save(OUT)
print('saved',OUT,collections.Counter(r['level'] for r in rows),'dropped quotes',sum(drop.values()),dict(drop))
# strip openpyxl from app.xml
import zipfile,shutil
tmp=OUT+'.tmp'
with zipfile.ZipFile(OUT) as zi, zipfile.ZipFile(tmp,'w',zipfile.ZIP_DEFLATED) as zo:
    for it in zi.infolist():
        d=zi.read(it.filename)
        if it.filename=='docProps/app.xml':
            d=re.sub(rb'<Application>.*?</Application>',b'<Application>Microsoft Excel</Application>',d)
            d=re.sub(rb'<AppVersion>.*?</AppVersion>',b'<AppVersion>16.0300</AppVersion>',d)
        zo.writestr(it,d)
shutil.move(tmp,OUT)
