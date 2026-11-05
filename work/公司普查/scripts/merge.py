import json,glob,sys,re
B=sys.argv[1]
picks=json.load(open(B+'/picks.json'))
tried=json.load(open(B+'/tried.json')) if glob.glob(B+'/tried.json') else {}
n=0
for f in sorted(glob.glob(B+'/found_*.json')):
    try: d=json.load(open(f))
    except Exception as e: print('bad',f,e); continue
    for code,v in d.items():
        if not isinstance(v,dict): continue
        if v.get('tried'): tried[code]=v['tried']
        for k in ('annual','esg'):
            x=v.get(k)
            if x and x.get('url') and not picks.get(code,{}).get(k):
                u=x['url']
                if re.search(r'twse\.com\.tw',u): continue
                picks.setdefault(code,{'annual':None,'esg':None})[k]=[None,1,u,x.get('label','')]
                n+=1
json.dump(picks,open(B+'/picks.json','w'),ensure_ascii=False,indent=1)
json.dump(tried,open(B+'/tried.json','w'),ensure_ascii=False,indent=1)
print('merged',n)
