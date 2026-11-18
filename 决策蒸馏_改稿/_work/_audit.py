# -*- coding: utf-8 -*-
import io, re
t=io.open('draft.md',encoding='utf-8').read()
o=io.open('draft.orig.md',encoding='utf-8').read()
lines=[]
def cnt(txt,pat): return len(re.findall(pat,txt))
for pat in ['这一[\u4e00-\u9fff]','本文','——','综上所述','随着','值得注意的是','赋能','抓手','闭环','不是[^。]{0,20}而是','并非','不仅']:
    lines.append('### %s  draft=%d  orig=%d'%(pat,cnt(t,pat),cnt(o,pat)))
    for m in list(re.finditer(pat,t))[:10]:
        lines.append('    '+t[max(0,m.start()-30):m.start()+35].replace('\n',' '))
io.open('_audit.txt','w',encoding='utf-8').write('\n'.join(lines))
print('ok')
