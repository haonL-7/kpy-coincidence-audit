# -*- coding: utf-8 -*-
import sys, re, io
sys.path.insert(0,'.')
from _fetch import fetch, totext

urls = [
 'https://news.zhuwang.com.cn/xinwen/20260828/650294.html',
 'http://mp.weixin.qq.com/s?__biz=MzkyMjY0MDQ4NA==&mid=2247609654&idx=1&sn=bc2e0a6194f04631500d311f0e963bb6',
 'https://www.ntv.cn/content/1/392/991392652.html',
]
out=[]
for u in urls:
    try:
        b=fetch(u); t=totext(b)
    except Exception as e:
        out.append('ERR %s %s'%(u,e)); continue
    out.append('===== %s LEN=%d'%(u,len(t)))
    hits=list(re.finditer('规模化率|规模化养殖', t))
    out.append('hits=%d'%len(hits))
    for m in hits[:6]:
        out.append('  ...'+t[max(0,m.start()-160):m.start()+160])
io.open('_web.txt','w',encoding='utf-8').write('\n'.join(out))
print('ok')
