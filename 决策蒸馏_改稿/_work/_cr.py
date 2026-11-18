# -*- coding: utf-8 -*-
import sys, json, subprocess, re, io, urllib.parse
UA='Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
def get(url, extra=None):
    cmd=['curl','-sL','--compressed','-A',UA,'--max-time','40']
    if extra: cmd+=extra
    cmd.append(url)
    p=subprocess.run(cmd,capture_output=True)
    return p.stdout

out=[]
def cr(doi):
    b=get('https://api.crossref.org/works/'+urllib.parse.quote(doi),['-H','Accept: application/json'])
    try:
        j=json.loads(b.decode('utf-8','ignore'))
    except Exception:
        return 'FAIL '+b[:120].decode('utf-8','ignore')
    m=j['message']
    return dict(title=(m.get('title') or [''])[0],
                container=(m.get('container-title') or [''])[0],
                vol=m.get('volume'), issue=m.get('issue'), page=m.get('page'),
                year=(m.get('issued',{}).get('date-parts') or [[None]])[0][0],
                authors=[a.get('family','') for a in m.get('author',[])][:3],
                type=m.get('type'))

dois = {
 '11':'10.1037/a0037511',
 '12':'10.1016/j.compag.2018.12.007',
 '16':'10.1287/orsc.2.1.71',
 '17':'10.1073/pnas.1105562108',
 '18':'10.1371/journal.pone.0224725',
}
for k,d in dois.items():
    out.append('[%s] %s -> %s'%(k,d,json.dumps(cr(d),ensure_ascii=False)))
io.open('_crossref.txt','w',encoding='utf-8').write('\n'.join(out))
print('ok')
