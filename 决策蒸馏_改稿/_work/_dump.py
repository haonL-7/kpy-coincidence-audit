
import zipfile, re, io
from xml.etree import ElementTree as ET
src=r'C:/Users/Administrator/Documents/xwechat_files/wxid_h72ol1ylw9hv22_d04f/msg/file/2026-10/决策蒸馏——宏集智能体与养殖场数字化管理系统管控（修订版）.docx'
z=zipfile.ZipFile(src)
xml=z.read('word/document.xml').decode('utf-8')
NS='{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'
root=ET.fromstring(xml)
body=root.find(NS+'body')
paras=[]
for p in body:
    if not p.tag.endswith('}p'): continue
    buf=[]
    has_draw=False
    for r in p.iter(NS+'r'):
        if r.find(NS+'drawing') is not None or r.find(NS+'pict') is not None:
            has_draw=True
        for node in r:
            if node.tag==NS+'t': buf.append(node.text or '')
            elif node.tag==NS+'tab': buf.append('\t')
            elif node.tag==NS+'br': buf.append('\n')
    txt=''.join(buf)
    paras.append((txt, has_draw))
with io.open('_paras.txt','w',encoding='utf-8') as f:
    for i,(t,d) in enumerate(paras):
        f.write('[%02d]%s %s\n' % (i, 'DRAW' if d else '', t))
print('paras', len(paras))
