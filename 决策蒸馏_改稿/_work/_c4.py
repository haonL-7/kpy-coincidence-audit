# -*- coding: utf-8 -*-
import sys, re, io
sys.path.insert(0,'.')
from _fetch import fetch, totext
out=[]
t=totext(fetch('https://www.stdaily.com/web/gdxw/2026-04/29/content_510139.html'))
out.append('[8] len=%d'%len(t))
out.append('  head: '+t[:220])
for p in ['2至3天','2—3天','提前','预警','长岭']:
    for m in list(re.finditer(p,t))[:2]:
        out.append('  %s ... %s'%(p,t[max(0,m.start()-200):m.start()+150]))
io.open('_chk4.txt','w',encoding='utf-8').write('\n'.join(out))
print('ok')
