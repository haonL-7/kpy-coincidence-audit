# -*- coding: utf-8 -*-
import io, re
p='draft.md'
t=io.open(p,encoding='utf-8').read()
# alternate straight double quotes into curly
out=[]; open_q=True
for ch in t:
    if ch=='"':
        out.append('\u201c' if open_q else '\u201d'); open_q=not open_q
    else:
        out.append(ch)
t2=''.join(out)
io.open(p,'w',encoding='utf-8').write(t2)
print('open_q balanced at end:', open_q)
print('curly open', t2.count('\u201c'), 'close', t2.count('\u201d'), 'straight', t2.count('"'))
# contexts
for pat in ['这一[\u4e00-\u9fff]','本文','——','综上所述','随着','值得注意的是','赋能','抓手','闭环','不是..而是','而是']:
    hits=[(m.start(), t2[max(0,m.start()-25):m.start()+30].replace('\n',' ')) for m in re.finditer(pat,t2)]
    print('--- %s : %d'%(pat,len(hits)))
    for h in hits[:8]: print('   ', h[1])
