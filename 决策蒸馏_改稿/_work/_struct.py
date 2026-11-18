# -*- coding: utf-8 -*-
import io, re
a=io.open('draft.orig.md',encoding='utf-8').read()
b=io.open('draft.md',encoding='utf-8').read()
def struct(t):
    heads=[l for l in t.split('\n') if l.startswith('#')]
    paras=[p for p in t.split('\n\n') if p.strip()]
    return heads, len(paras)
ha,na=struct(a); hb,nb=struct(b)
print('headings identical:', ha==hb, len(ha))
print('paras:', na, nb)
def cites(t):
    body=t.split('## 参考文献')[0]
    return re.findall(r'\[[0-9][0-9,\-]*\]', body)
ca, cb = cites(a), cites(b)
print('citation tokens identical:', ca==cb, len(ca))
if ca!=cb:
    import difflib
    for x in difflib.unified_diff(ca,cb,lineterm=''): print(x)
# figure caption
print('caption A:', [l for l in a.split('\n') if l.startswith('图1')])
print('caption B:', [l for l in b.split('\n') if l.startswith('图1')])
print('refs count A/B:', len([l for l in a.split('\n') if re.match(r'^\[1?[0-9]\] ',l)]), len([l for l in b.split('\n') if re.match(r'^\[1?[0-9]\] ',l)]))
