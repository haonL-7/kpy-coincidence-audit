# -*- coding: utf-8 -*-
import io, re
a=io.open('draft_v2.md',encoding='utf-8').read().split('## 参考文献')[0]
b=io.open('draft_final.md',encoding='utf-8').read().split('## 参考文献')[0]
TOK=re.compile(r'\[\d+(?:[-,]\d+)*\]')
sa, sb = TOK.sub('[N]',a), TOK.sub('[N]',b)
print('BODY identical after normalizing citation tokens:', sa==sb)
if sa!=sb:
    import difflib
    for x in list(difflib.unified_diff(sa.split('\n'),sb.split('\n'),lineterm=''))[:10]: print(x[:160])
# token-level ledger
pa=[m.group(0) for m in TOK.finditer(a)]
pb=[m.group(0) for m in TOK.finditer(b)]
print('tokens:',len(pa),len(pb))
pairs=[(x,y) for x,y in zip(pa,pb) if x!=y]
print('changed tokens:', pairs)
print('BODY cjk equal:', len(re.findall(r'[\u4e00-\u9fff]',a))==len(re.findall(r'[\u4e00-\u9fff]',b)))
