# -*- coding: utf-8 -*-
import zipfile, re, io
from xml.etree import ElementTree as ET
src=r'C:/Users/Administrator/Documents/xwechat_files/wxid_h72ol1ylw9hv22_d04f/msg/file/2026-10/决策蒸馏——宏集智能体与养殖场数字化管理系统管控（修订版）.docx'
z=zipfile.ZipFile(src)
xml=z.read('word/document.xml').decode('utf-8')
NS='{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'
root=ET.fromstring(xml); body=root.find(NS+'body')
paras=[]
for p in body:
    if not p.tag.endswith('}p'): continue
    buf=[]; draw=False
    for r in p.iter(NS+'r'):
        if r.find(NS+'drawing') is not None or r.find(NS+'pict') is not None: draw=True
        for node in r:
            if node.tag==NS+'t': buf.append(node.text or '')
            elif node.tag==NS+'tab': buf.append('\t')
            elif node.tag==NS+'br': buf.append('\n')
    paras.append((''.join(buf), draw))

HEAD = {3,8,16,29,34}
out=[]
for i,(t,d) in enumerate(paras):
    if d:
        out.append('![](figure_1.png)')
        continue
    if i==0:
        out.append('# '+t); continue
    if i in HEAD:
        out.append('## '+t); continue
    if t.strip()=='参考文献':
        out.append('## 参考文献'); continue
    out.append(t)
txt='\n\n'.join(x for x in out if x.strip()!='') + '\n'
io.open('draft.orig.md','w',encoding='utf-8').write(txt)

# verify verbatim round trip
def norm(s):
    s=re.sub(r'^#+\s*','',s,flags=re.M)
    s=re.sub(r'!\[[^\]]*\]\([^)]*\)','',s)
    return re.sub(r'\s+','',s)
srcall=norm('\n'.join(t for t,d in paras if not d))
mdall=norm(txt)
print('roundtrip equal:', srcall==mdall, len(srcall), len(mdall))
if srcall!=mdall:
    import difflib
    for j,(a,b) in enumerate(zip(srcall,mdall)):
        if a!=b:
            print('first diff at',j, repr(srcall[j-30:j+30]), '||', repr(mdall[j-30:j+30])); break
