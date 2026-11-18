# -*- coding: utf-8 -*-
import sys, re, io
sys.path.insert(0,'.')
from _fetch import fetch, totext
out=[]
tests = [
 ('stcn','https://www.stcn.com/article/detail/1463240.html'),
 ('nfncb','https://epaper.nfncb.cn/nfnc/content/20241224/Articel10001MT.htm'),
]
for name,u in tests:
    try:
        b=fetch(u); t=totext(b)
    except Exception as e:
        out.append('ERR %s %s'%(u,e)); continue
    out.append('===== %s %s LEN=%d'%(name,u,len(t)))
    for m in list(re.finditer('规模化率', t))[:3]:
        out.append('   ...'+t[max(0,m.start()-260):m.start()+120])
io.open('_web3.txt','w',encoding='utf-8').write('\n'.join(out))
print('ok')
