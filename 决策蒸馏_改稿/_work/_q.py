# -*- coding: utf-8 -*-
import io, re
p='draft.md'
t=io.open(p,encoding='utf-8').read()
edits = [
 ("这一环可以由一个只判不说的判定模型分担一部分。", "其中一环可以由一个只判不说的判定模型分担一部分。"),
 ("但这一步要成立，必须先补上归因控制。", "不过，离群验证要成立，还必须先补上归因控制。"),
 ("技术本身并不决定这一点。", "技术本身并不决定这件事。"),
 ("厂长们要评价的不是\u201c这个方法听起来好不好\u201d，而是\u201c在我场条件下，这个归因是否成立\u201d。",
  "厂长们要评价的是\u201c在我场条件下，这个归因是否成立\u201d，一句\u201c这个方法听起来好不好\u201d并不够。"),
 ("规范批次与栏舍编码、统一数据口径，不仅是为了数据能归集，更是为了让AI能区分\u201c方法差异\u201d与\u201c条件差异\u201d。",
  "规范批次与栏舍编码、统一数据口径，是为了数据能归集，也是为了让AI能区分\u201c方法差异\u201d与\u201c条件差异\u201d。"),
]
for a,b in edits:
    assert t.count(a)==1, ('NOT FOUND/UNIQ', a[:20], t.count(a))
    t=t.replace(a,b)
io.open(p,'w',encoding='utf-8').write(t)

o=io.open('draft.orig.md',encoding='utf-8').read()
body=t.split('## 参考文献')[0]; ob=o.split('## 参考文献')[0]
q1=re.findall('\u201c([^\u201d]{1,60})\u201d', body); q0=set(re.findall('\u201c([^\u201d]{1,60})\u201d', ob))
lines=['quoted segs draft=%d orig=%d'%(len(q1),len(q0)),'NEW quoted:']
for x in q1:
    if x not in q0: lines.append('  '+x)
lines.append('open %d close %d'%(body.count('\u201c'),body.count('\u201d')))
for i,para in enumerate(body.split('\n\n')):
    if para.count('\u201c')!=para.count('\u201d'): lines.append('UNBALANCED para %d: %s'%(i,para[:50]))
io.open('_q.txt','w',encoding='utf-8').write('\n'.join(lines))
print('ok')
