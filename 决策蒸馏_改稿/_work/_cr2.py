# -*- coding: utf-8 -*-
import sys, json, subprocess, re, io, urllib.parse
UA='Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
def get(url):
    p=subprocess.run(['curl','-sL','--compressed','-A',UA,'--max-time','40','-H','Accept: application/json',url],capture_output=True)
    return p.stdout
def q(title, extra=''):
    url='https://api.crossref.org/works?rows=3&query.bibliographic='+urllib.parse.quote(title)+extra
    try:
        j=json.loads(get(url).decode('utf-8','ignore'))
    except Exception as e:
        return 'FAIL'
    res=[]
    for m in j['message']['items']:
        res.append(dict(doi=m.get('DOI'), title=(m.get('title') or [''])[0],
            container=(m.get('container-title') or [''])[0], vol=m.get('volume'), issue=m.get('issue'),
            page=m.get('page'), year=(m.get('issued',{}).get('date-parts') or [[None]])[0][0],
            authors=[a.get('family','') for a in m.get('author',[])][:3]))
    return res
qs = {
 '11':'The wisdom of select crowds Mannes Soll Larrick',
 '17':'How social influence can undermine the wisdom of crowd effect Lorenz Rauhut Schweitzer',
 '2':'Economic and environmental benefits of digital agricultural technological solutions in livestock farming a review',
 '3':'Modernizing livestock operations smart feedlot technologies and their impact',
 '9':'Agent-in-the-loop to distill expert knowledge into artificial intelligence models a survey',
}
out=[]
for k,v in qs.items():
    out.append('===== [%s] %s'%(k,v))
    out.append(json.dumps(q(v),ensure_ascii=False,indent=1))
io.open('_crossref2.txt','w',encoding='utf-8').write('\n'.join(out))
print('ok')
