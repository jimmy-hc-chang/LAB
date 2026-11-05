import json, re, sys, os, subprocess, urllib.parse, concurrent.futures as cf, html
W=sys.argv[1]; OUT=sys.argv[2]
comps=json.load(open(W+'/companies.json'))
KEYLINK=re.compile(r'投資人|股東|年報|永續|ESG|CSR|社會責任|investor|annual|sustainab|report|財務|產品|product|solution|服務|技術|technology|研發|R&D|AI|智慧',re.I)
DOCKEY=re.compile(r'年報|annual|永續|ESG|CSR|社會責任|sustainab',re.I)
def get(url,path=None,maxt=25):
    try:
        cmd=['curl','-sSL','-m',str(maxt),'--max-filesize','80000000','-w','\n__CT__%{content_type}']
        if path: cmd+=['-o',path]
        r=subprocess.run(cmd+[url],capture_output=True,timeout=maxt+10)
        out=r.stdout
        ct=out.rsplit(b'__CT__',1)[-1].decode('latin1') if b'__CT__' in out else ''
        body=out.rsplit(b'\n__CT__',1)[0] if not path else b''
        return ct,body
    except Exception as e:
        return '',b''
def dec(b):
    for enc in ('utf-8','big5','cp950'):
        try: return b.decode(enc)
        except: pass
    return b.decode('utf-8','ignore')
def norm(u):
    u=u.strip()
    if not u.startswith('http'): u='http://'+u
    return u
def crawl(c):
    code=c['code']; d=f'{OUT}/{code}'; os.makedirs(d,exist_ok=True)
    if os.path.exists(d+'/done.json'): return
    start=norm(c['web']); host=urllib.parse.urlparse(start).netloc.replace('www.','')
    seen=set(); queue=[(start,0,'home')]; pages=[]; pdfs={}
    while queue and len(seen)<45:
        url,depth,anchor=queue.pop(0)
        if url in seen: continue
        seen.add(url)
        ct,b=get(url)
        if not b: continue
        if 'pdf' in ct.lower(): continue
        t=dec(b); pages.append({'url':url,'anchor':anchor,'len':len(t)})
        with open(f'{d}/p{len(pages):02d}.html','w') as f: f.write(url+'\n'+t)
        if depth>=2: continue
        for m in re.finditer(r'<a\s[^>]*href\s*=\s*["\']([^"\'#]+)["\'][^>]*>(.*?)</a>',t,re.I|re.S):
            href=html.unescape(m.group(1)); a=re.sub(r'<[^>]+>','',m.group(2)); a=html.unescape(re.sub(r'\s+',' ',a)).strip()[:80]
            if href.startswith(('javascript','mailto','tel')): continue
            u=urllib.parse.urljoin(url,href)
            h=urllib.parse.urlparse(u).netloc.replace('www.','')
            if u.lower().split('?')[0].endswith('.pdf'):
                if DOCKEY.search(a+' '+urllib.parse.unquote(u)): pdfs[u]=a
                continue
            if h!=host: continue
            if KEYLINK.search(a+' '+urllib.parse.unquote(u)) and u not in seen:
                queue.append((u,depth+1,a))
    json.dump({'pages':pages,'pdfs':pdfs},open(d+'/done.json','w'),ensure_ascii=False,indent=0)
with cf.ThreadPoolExecutor(20) as ex:
    list(ex.map(crawl,comps))
print('ok')
