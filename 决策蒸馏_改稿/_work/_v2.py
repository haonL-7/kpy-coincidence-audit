# -*- coding: utf-8 -*-
import io, re
t=io.open('draft.md',encoding='utf-8').read()
B=[b for b in t.split('\n\n') if b.strip()]
assert len(B)==60

T1='难点集中在三处：多位资深人员的分歧难以聚合，归因控制难以成立，激励与权责难以对齐。'
T2='另外两类难点不在系统之内。'
T3='上述三层机制能否成立，取决于上一章列出的三项条件。'

H1='## 一、问题背景（现状数据）：系统上线与成本改善之间的落差'
H3='## 三、现存难点：分歧、归因与激励'
H4='## 四、对策建议：宏集智能体的机制设计'
H5='## 五、个人判断'
SUB='### 研究局限'

order = [B[0],B[1],B[2],
         H1, B[4],B[5],B[6],B[7],
         B[8], B[9],B[10],B[11],B[12],B[13],B[14],B[15],
         H3, T1, B[26], T2, B[30],B[31],B[32],B[33],
         H4, B[17],B[18],B[19],B[20],B[21],B[22],B[23],B[24],B[25],B[27],B[28], T3,
         H5, B[35],B[36],B[37],B[38],B[39], SUB, B[40],
         B[41], B[42],B[43],B[44],B[45],B[46],B[47],B[48],B[49],B[50],B[51],B[52],B[53],B[54],B[55],B[56],B[57],B[58],B[59]]

v2='\n\n'.join(order)+'\n'
io.open('draft_v2.md','w',encoding='utf-8').write(v2)

# ---- verification: every source block appears exactly once, in full ----
low=v2
missing=[]; dup=[]
for i,b in enumerate(B):
    if b.startswith('##'):
        if i in (3,16,29,34):
            continue  # replaced headings
    c=v2.count(b)
    if c==0: missing.append(i)
    elif c>1: dup.append((i,c))
print('blocks:',len(B),'missing:',missing,'dup:',dup)
# sentence-level: multiset of sentences in source body vs new body (excluding new transitions/headings)
def sents(x):
    x=x.split('## 参考文献')[0]
    x=re.sub(r'^#+ .*$','',x,flags=re.M)
    parts=[s for s in re.split(r'(?<=[。！？])', x) if s.strip()]
    return [s.strip() for s in parts]
s_old=sents(t); s_new=sents(v2)
from collections import Counter
co, cn = Counter(s_old), Counter(s_new)
lost = [k for k in co if cn[k]<co[k]]
added= [k for k in cn if cn[k]>co[k]]
print('sentences old/new:',len(s_old),len(s_new))
print('LOST sentences:',len(lost))
for k in lost[:5]: print('  -',k[:60])
print('ADDED sentences:',len(added))
for k in added[:8]: print('  +',k[:60])
