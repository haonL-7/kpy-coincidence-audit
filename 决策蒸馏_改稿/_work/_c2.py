# -*- coding: utf-8 -*-
import sys, re, io
sys.path.insert(0,'.')
from _fetch import fetch, totext
out=[]
# [6] content check
t=totext(fetch('https://m.gmw.cn/2024-01/23/content_1303640502.htm'))
out.append('[6] len=%d'%len(t))
for p in ['规模化率','68%','生猪养殖规模化']:
    for m in list(re.finditer(p,t))[:3]:
        out.append('  %s ... %s'%(p, t[max(0,m.start()-200):m.start()+150]))
# [10],[14] arxiv comments/journal-ref
for aid in ['2607.21051','2609.26550']:
    t=totext(fetch('https://arxiv.org/abs/'+aid))
    m=re.search(r'Comments?:.*?(?=Subjects|Submission history)', t, re.S)
    j=re.search(r'Journal reference:.*?(?=ACM|Subjects)', t, re.S)
    d=re.search(r'DOI:.*?(?=\s)', t)
    out.append('[%s] comments=%s | journal=%s | doi=%s'%(aid, m.group(0)[:300] if m else 'none', j.group(0)[:200] if j else 'none', d.group(0)[:120] if d else 'none'))
    out.append('  authors: '+t[t.find('Authors:'):t.find('Authors:')+300])
io.open('_chk2.txt','w',encoding='utf-8').write('\n'.join(out))
print('ok')
