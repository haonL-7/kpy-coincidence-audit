# -*- coding: utf-8 -*-
import io, re
a=io.open('draft_v2.md',encoding='utf-8').read()
b=io.open('draft_final.md',encoding='utf-8').read()
TOK=re.compile(r'\[\d+(?:[-,]\d+)*\]')
sa=TOK.sub('[N]', a)
sb=TOK.sub('[N]', b)
print('body identical after stripping citation tokens:', sa==sb)
print('cjk v2/final:', len(re.findall(r'[\u4e00-\u9fff]', a.split('## 参考文献')[0])), len(re.findall(r'[\u4e00-\u9fff]', b.split('## 参考文献')[0])))
# show the changed lines in body
for i,(la,lb) in enumerate(zip(a.split('\n'), b.split('\n'))):
    if la!=lb and '] ' not in la[:5]:
        print('LINE',i+1)
        print('  v2  :', la[:150])
        print('  fin :', lb[:150])
