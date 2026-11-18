# -*- coding: utf-8 -*-
import io
t=io.open('draft.md',encoding='utf-8').read()
blocks=[b for b in t.split('\n\n') if b.strip()]
out=[]
for i,b in enumerate(blocks):
    out.append('%02d | %s' % (i, b[:46].replace('\n',' ')))
io.open('_work/_blocks.txt','w',encoding='utf-8').write('\n'.join(out))
print(len(blocks))
