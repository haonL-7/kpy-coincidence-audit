# -*- coding: utf-8 -*-
import sys, re, io
sys.path.insert(0,'.')
from _fetch import fetch, totext
out=[]
out.append('DATE: '+__import__('subprocess').run(['date'],capture_output=True).stdout.decode('utf-8','ignore').strip())
t=totext(fetch('https://www.farmer.com.cn/2025/10/17/991002119.html'))
out.append('[15] len=%d'%len(t))
for p in ['0.4','4000','30%','数影','25万']:
    for m in list(re.finditer(p,t))[:2]:
        out.append('  %s ... %s'%(p,t[max(0,m.start()-220):m.start()+160]))
t2=totext(fetch('https://www.ntv.cn/content/1/392/991392652.html'))
out.append('[6new] len=%d'%len(t2))
m=re.search(r'(20\d\d-\d\d-\d\d[^ ]{0,10})', t2)
out.append('  date-ish: '+str(m.group(1) if m else 'none'))
out.append('  head: '+t2[:300])
io.open('_chk3.txt','w',encoding='utf-8').write('\n'.join(out))
print('ok')
