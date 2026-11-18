# -*- coding: utf-8 -*-
import io, re
t=io.open('draft_v2.md',encoding='utf-8').read()
o=io.open('draft.md',encoding='utf-8').read()
lines=[]
for pat in ['前述','上文','前文','如前','上述','第三章','本节','下文','第一层','该层','这一步']:
    for m in re.finditer(pat, t):
        lines.append('%-6s | %s' % (pat, t[max(0,m.start()-30):m.start()+34].replace('\n',' ')))
io.open('_work/_refs.txt','w',encoding='utf-8').write('\n'.join(lines))
print(len(lines))
