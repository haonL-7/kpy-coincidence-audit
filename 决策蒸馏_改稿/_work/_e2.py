# -*- coding: utf-8 -*-
import io
p='draft.md'
t=io.open(p,encoding='utf-8').read()
edits=[
 ("仅用于对照说明现有实践与上述机制设计之间的差距。","仅用于对照说明现有实践与机制设计之间的差距。"),
 ("其服务的 25 万头母猪体系客户综合成本比原体系低 0.4 元/斤，\u201c母猪养殖在线\u201d使企业管理效率提升 30% 以上，中小规模场部分案例每头母猪年增收超 4000 元[15]。",
  "其服务的 25 万头母猪体系客户综合成本比原体系低 0.4 元/斤。\u201c母猪养殖在线\u201d使企业管理效率提升 30% 以上，中小规模场部分案例每头母猪年增收超 4000 元[15]。"),
]
for a,b in edits:
    assert t.count(a)==1,(a[:20],t.count(a))
    t=t.replace(a,b)
io.open(p,'w',encoding='utf-8').write(t)
print('ok')
