# build per-company evidence packets for classification
import json,sys,os,re
B=sys.argv[1]; codes=sys.argv[2].split(',') if len(sys.argv)>2 and sys.argv[2] else None
h=json.load(open(B+'/hits.json')); picks=json.load(open(B+'/picks.json'))
comps={c['code']:c for c in json.load(open(B+'/companies.json'))}
STRONG=re.compile(r'(?<![A-Za-z])(AI|AIoT|GenAI|LLM|ChatGPT|Copilot)(?![A-Za-z])|人工智慧|人工智能|機器學習|深度學習|神經網路|大型語言模型|生成式|Artificial Intelligence|Machine Learning|Deep Learning',re.I)
os.makedirs(B+'/packets',exist_ok=True)
for code,v in h.items():
    if codes and code not in codes: continue
    c=comps[code]; L=[f"### {code} {c['abbr']}（{c['name']}，{c['market']}）細分類：{c.get('sub','')}"]
    for k,lab in (('annual','年報'),('esg','永續報告書')):
        p=picks.get(code,{}).get(k)
        if v[k] and p:
            L.append(f"[{lab}] 來源網址：{p[2]}｜網頁標示：{p[3]}｜共{v[k]['pages']}頁(PDF頁)｜AI相關詞出現{v[k]['n_ai']}次(強詞{v[k]['n_strong']}次)")
            hs=sorted(v[k]['hits'],key=lambda x:(0 if STRONG.search(x[1]) else 1))
            seen=set();n=0
            for pg,kw,cx in hs:
                key=cx[20:60]
                if key in seen: continue
                seen.add(key); n+=1
                if n>25: break
                L.append(f"  - PDF第{pg}頁｜{kw}｜{cx}")
            seen=set();n=0
            for pg,kw,cx in v[k]['ri']:
                if kw in seen and n>3: continue
                seen.add(kw); n+=1
                if n>10: break
                L.append(f"  * RI PDF第{pg}頁｜{kw}｜{cx}")
    s=v['site']
    if s and s['n']:
        L.append(f"[官網] AI強詞段落{s['n']}處")
        for url,kw,cx in s['hits'][:15]: L.append(f"  - {url}｜{kw}｜{cx}")
    open(f'{B}/packets/{code}.txt','w').write('\n'.join(L)+'\n')
print('ok')
