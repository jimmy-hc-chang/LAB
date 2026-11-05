# download picked PDFs and extract per-page text
import json,os,subprocess,sys,concurrent.futures as cf
B=sys.argv[1]; picks=json.load(open(B+'/picks.json'))
os.makedirs(B+'/pdf',exist_ok=True)
def run(item):
    code,kind,u=item
    out=f'{B}/pdf/{code}_{kind}.pdf'; tx=f'{B}/pdf/{code}_{kind}.txt'
    if os.path.exists(tx) and os.path.getsize(tx)>0: return
    if not os.path.exists(out) or os.path.getsize(out)<1000:
        subprocess.run(['curl','-sSL','-m','240','--max-filesize','150000000','-o',out,u],capture_output=True)
    r=subprocess.run(['file','-b',out],capture_output=True,text=True)
    if 'PDF' not in r.stdout:
        open(tx,'w').write(''); return
    subprocess.run(['pdftotext','-enc','UTF-8',out,tx],capture_output=True,timeout=300)
items=[]
for code,v in picks.items():
    for k in ('annual','esg'):
        if v.get(k): items.append((code,k,v[k][2]))
with cf.ThreadPoolExecutor(12) as ex: list(ex.map(run,items))
print('done',len(items))
