# -*- coding: utf-8 -*-
import sys, re, io
sys.path.insert(0,'.')
from _fetch import fetch, totext
urls = [
 'https://npecrr.agri.cn/snxwfbjj/fbjj2026/202601/t20260122_469381.htm',
 'https://m.yangzhu360.com/guonei/20260123/897434.html',
 'https://www.meat360.cn/news/detail/808605.html',
 'https://www.cpcti.com/dongtai/157335.html',
]
out=[]
for u in urls:
    try:
        b=fetch(u); t=totext(b)
    except Exception as e:
        out.append('ERR %s %s'%(u,e)); continue
    out.append('===== %s LEN=%d'%(u,len(t)))
    for p in ['规模化率','规模化养殖占比','规模化水平','年出栏500头']:
        hits=list(re.finditer(p,t))
        if hits:
            out.append(' PAT %s hits=%d'%(p,len(hits)))
            for m in hits[:3]:
                out.append('   ...'+t[max(0,m.start()-180):m.start()+180])
io.open('_web2.txt','w',encoding='utf-8').write('\n'.join(out))
print('done')
