# extract AI and RI keyword contexts from pdf texts and site html
import json,re,glob,os,sys,html
B=sys.argv[1]
AI=re.compile(r'(?<![A-Za-z])(AI|A\.I\.|AIoT|GenAI|LLM|ChatGPT|Copilot)(?![A-Za-z])|人工智慧|人工智能|機器學習|深度學習|神經網路|大型語言模型|生成式|電腦視覺|影像辨識|智慧醫療|演算法|Artificial Intelligence|Machine Learning|Deep Learning|大數據',re.I)
AISTRONG=re.compile(r'(?<![A-Za-z])(AI|AIoT|GenAI|LLM|ChatGPT|Copilot)(?![A-Za-z])|人工智慧|人工智能|機器學習|深度學習|神經網路|大型語言模型|生成式AI|Artificial Intelligence|Machine Learning|Deep Learning',re.I)
RI=re.compile(r'病患參與|病友|患者參與|倫理|隱私|個資|個人資料|資料保護|資訊安全|人體試驗委員會|IRB|知情同意|受試者|利害關係人溝通|動物福利|責任創新|負責任')
def clean(s): return re.sub(r'\s+','',s) if False else re.sub(r'[ \t]+',' ',s.replace('\n',''))
def ctx(text,m,w=70):
    a=max(0,m.start()-w); b=min(len(text),m.end()+w)
    return text[a:b]
res={}
comps=json.load(open(B+'/companies.json'))
for c in comps:
    code=c['code']; r={'annual':None,'esg':None,'site':None}
    for k in ('annual','esg'):
        f=f'{B}/pdf/{code}_{k}.txt'
        if not os.path.exists(f) or os.path.getsize(f)<500: continue
        pages=open(f,encoding='utf-8',errors='ignore').read().split('\f')
        pages=[re.sub(r'\s*\n\s*','',p) for p in pages]  # join CJK lines
        tot=sum(len(p) for p in pages)
        hits=[];strong=0;ri=[]
        for i,p in enumerate(pages,1):
            for m in AI.finditer(p):
                if AISTRONG.fullmatch(m.group(0)) or AISTRONG.match(m.group(0)): strong+=1
                hits.append((i,m.group(0),ctx(p,m)))
            for m in RI.finditer(p): ri.append((i,m.group(0),ctx(p,m,60)))
        r[k]={'pages':len(pages),'chars':tot,'n_ai':len(hits),'n_strong':strong,'hits':hits,'ri':ri}
    # site
    sh=[]
    for f in sorted(glob.glob(f'{B}/sites/{code}/p*.html')):
        t=open(f,encoding='utf-8',errors='ignore').read(); url,t=t.split('\n',1)
        t=re.sub(r'(?is)<(script|style|noscript)[^>]*>.*?</\1>',' ',t)
        t=html.unescape(re.sub(r'<[^>]+>',' ',t)); t=re.sub(r'\s+',' ',t)
        for m in AISTRONG.finditer(t): sh.append((url,m.group(0),ctx(t,m,60)))
    # dedupe site contexts
    seen=set(); sh2=[]
    for x in sh:
        if x[2] in seen: continue
        seen.add(x[2]); sh2.append(x)
    r['site']={'n':len(sh2),'hits':sh2[:40]}
    res[code]=r
json.dump(res,open(B+'/hits.json','w'),ensure_ascii=False)
print(len(res))
