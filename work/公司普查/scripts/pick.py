import json,re,glob,urllib.parse,sys
S=sys.argv[1]
def txt(u,a): return (a+' '+urllib.parse.unquote(u)).replace('\xa0',' ')
def is_en(s): return bool(re.search(r'(_|-|\b)EN(_|\b|\.)|英文|English|_E\.pdf|-E_',s,re.I)) and not re.search(r'中文|_CH|CH\.pdf',s)
def fy_annual(s):
    if not re.search(r'年報|annual.?report|Annual',s,re.I): return None
    if re.search(r'前十大|相互間|議事|手冊|開會通知|董事會績效|Evaluation|財務報告|財報',s,re.I): return None
    m=re.search(r'(1[01]\d)\s*年?\s*(度)?\s*股東',s)
    if m: return 1911+int(m.group(1))-1
    m=re.search(r'(1[01]\d)\s*年?度?',s)
    cand=[]
    for m in re.finditer(r'(?<!\d)(1[01]\d)(?!\d)',s): cand.append(1911+int(m.group(1)))
    for m in re.finditer(r'(?<!\d)(20[12]\d)(?!\d)',s): cand.append(int(m.group(1)))
    # uploaded path year like /2026/05/ -> report FY = upload-1
    up=re.search(r'/(20[12]\d)/(0[1-9]|1[0-2])/',s)
    if cand:
        y=max(c for c in cand)
        if re.search(r'115',s) and not re.search(r'114',s) and y==2026: return 2025
        if y>=2026 and up: return int(up.group(1))-1
        return y if y<=2025 else 2025
    if up: return int(up.group(1))-1
    return None
def fy_esg(s):
    if not re.search(r'永續報告|永續發展報告|ESG.?Report|CSR.?Report|Sustainability.?Report|社會責任報告|ESG|CSR|永續',s,re.I): return None
    if re.search(r'守則|辦法|政策|Principles|推動|執行情形|策略|Vision|信|手冊|policy|評估|evaluation',s,re.I) and not re.search(r'報告書',s): return None
    cand=[int(m.group(1)) for m in re.finditer(r'(?<!\d)(20[12]\d)(?!\d)',s)]+[1911+int(m.group(1)) for m in re.finditer(r'(?<!\d)(1[01]\d)(?!\d)',s)]
    up=re.search(r'/(20[12]\d)/(0[1-9]|1[0-2])/',s)
    cand=[c for c in cand if 2015<=c<=2026]
    if cand:
        y=max(cand); return min(y,2025)
    if up: return int(up.group(1))-1
    return None
res={}
for f in glob.glob(S+'/*/done.json'):
    code=f.split('/')[-2]; d=json.load(open(f))
    A=[];E=[]
    for u,a in d['pdfs'].items():
        s=txt(u,a)
        y=fy_annual(s)
        if y and y>=2023: A.append((y,0 if is_en(s) else 1,u,a))
        y2=fy_esg(s)
        if y2 and y2>=2023 and not fy_annual(s): E.append((y2,0 if is_en(s) else 1,u,a))
    A.sort(reverse=True);E.sort(reverse=True)
    res[code]={'annual':A[0] if A else None,'esg':E[0] if E else None}
json.dump(res,open(S+'/../picks.json','w'),ensure_ascii=False,indent=1)
print(sum(1 for v in res.values() if v['annual']),sum(1 for v in res.values() if v['esg']),len(res))
