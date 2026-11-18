# -*- coding: utf-8 -*-
import io, re
t=io.open('draft.md',encoding='utf-8').read()
assert t.count('显著偏低')==2, t.count('显著偏低')
t=t.replace('显著偏低','明显偏低')
io.open('draft.md','w',encoding='utf-8').write(t)

# 更新 changes.md 的 A-2.7 说明
c=io.open('changes.md',encoding='utf-8').read()
old='- 「显著偏低」2 处（三节第 7、8 段）：原文描述单一猪场的对比，不涉统计检验；此处按原文保留，未加「显著」的检验，也未削弱为「偏低」。若审稿人追问，建议改为「明显偏低」或补检验口径。'
new='- 「显著／明显偏低」2 处（三节第 7、8 段）：原为「显著偏低」，描述单一猪场的对比，文中没有统计检验。经作者确认后改为「明显偏低」（只改这两个词，其余未动）；改后不再暗示显著性检验。'
assert old in c
c=c.replace(old,new)
io.open('changes.md','w',encoding='utf-8').write(c)

# citations.md：[9] 页码说明
ci=io.open('citations.md',encoding='utf-8').read()
oldc='- 未能确认字段：页码。Crossref 记录无 page（Springer 近年以文章号著录），条目中的「1-55」无法复核。建议改为文章号或删去页码，未擅自改。'
newc='- 未能确认字段：页码。Crossref 记录无 page（Springer 近年以文章号著录），条目中的「1-55」无法复核。**页码以出版社页面为准，Crossref 无记录**；经作者决定保留原样，不改文章号（无记录不等于可以猜）。'
assert oldc in ci
ci=ci.replace(oldc,newc)
io.open('citations.md','w',encoding='utf-8').write(ci)
print('ok', t.count('明显偏低'))
