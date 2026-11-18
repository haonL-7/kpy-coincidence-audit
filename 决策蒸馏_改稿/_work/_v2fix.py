# -*- coding: utf-8 -*-
import io
p='draft_v2.md'
t=io.open(p,encoding='utf-8').read()
old='上述三层机制能否成立，取决于上一章列出的三项条件。'
new='该机制能否成立，取决于上一章列出的三项条件。'
assert t.count(old)==1
t=t.replace(old,new)
io.open(p,'w',encoding='utf-8').write(t)
print('ok')
