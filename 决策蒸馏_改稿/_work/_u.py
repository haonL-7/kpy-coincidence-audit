# -*- coding: utf-8 -*-
import sys, re, io, subprocess, json
sys.path.insert(0,'.')
from _fetch import fetch, totext
out=[]
def head(u):
    p=subprocess.run(['curl','-sL','--compressed','-A','Mozilla/5.0 (Windows NT 10.0; Win64; x64)','-o','/dev/null','-w','%{http_code} %{url_effective}','--max-time','40',u],capture_output=True)
    return p.stdout.decode('utf-8','ignore')

urls = {
 '1':'https://www.moa.gov.cn/govpublic/FZJHS/202001/t20200120_6336316.htm',
 '6':'https://m.gmw.cn/2024-01/23/content_1303640502.htm',
 '7':'https://www.caaa.cn/html/fw/market/zhu/2026/0519/23756.html',
 '13':'https://www.zgswcn.com/news.html?aid=345926',
 '15':'https://www.farmer.com.cn/2025/10/17/991002119.html',
 '10':'https://arxiv.org/abs/2607.21051',
 '14':'https://arxiv.org/abs/2609.26550',
 '5doi':'https://doi.org/10.27409/d.cnki.gxbnu.2023.002796',
}
for k,u in urls.items():
    out.append('[%s] %s -> %s'%(k,u,head(u)))
    if k in ('6','7','10','14','15','13','1'):
        t=totext(fetch(u))
        out.append('   TITLE/TEXT: '+t[:260].replace('\n',' '))
io.open('_urls.txt','w',encoding='utf-8').write('\n'.join(out))
print('ok')
