# -*- coding: utf-8 -*-
"""对漏抓的 5 篇做多轮重试（CF 验证页是随机的，重试常能过）"""
import os, re, time, urllib.parse, urllib.request
UA="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"
OUT=os.path.join(os.path.dirname(os.path.abspath(__file__)),"pdfs"); os.makedirs(OUT,exist_ok=True)
TODO=[("01_Sitosari_BBRC_2023","10.1016/j.bbrc.2023.01.033"),
      ("02_Liang_VetMicro_2026","10.1016/j.vetmic.2026.110871"),
      ("03_Xu_CancerLett_2026","10.1016/j.canlet.2026.218650"),
      ("05_Zhao_ChemResTox_2024","10.1021/acs.chemrestox.3c00298"),
      ("06_Yuan_JPR_2026","10.1021/acs.jproteome.5c01243")]
MIR=["https://sci-hub.st","https://sci-hub.ru","https://sci-hub.ee","https://www.sci-hub.ren","https://sci-hub.usualwant.com","https://sci-hub.al"]
BLOCK=re.compile(r"(Verification|turnstile|cf-challenge|Just a moment|DDoS-Guard|captcha)",re.I)
def get(u,ref=None,t=15):
    q=urllib.request.Request(u,headers={"User-Agent":UA,"Accept":"text/html,application/pdf,*/*","Accept-Language":"en-US,en;q=0.9"})
    if ref:q.add_header("Referer",ref)
    with urllib.request.urlopen(q,timeout=t) as r: return r.headers.get("Content-Type",""),r.read()
def pdfurl(h,base):
    for p in [r'<embed[^>]+src=["\']([^"\']+)',r'<iframe[^>]+src=["\']([^"\']+)',r'location\.href\s*=\s*["\']([^"\']+)']:
        m=re.search(p,h,re.I)
        if m:
            u=m.group(1)
            return ("https:"+u) if u.startswith("//") else (urllib.parse.urljoin(base+"/",u) if not u.startswith("http") else u)
    return None
for name,doi in TODO:
    dest=os.path.join(OUT,name+".pdf")
    if os.path.exists(dest) and os.path.getsize(dest)>20000: print("[=]",name,"已有"); continue
    done=False
    for rnd in range(3):
        for m in MIR:
            try: ct,bdy=get(f"{m}/{doi}")
            except Exception as e: continue
            if bdy[:4]==b"%PDF": open(dest,"wb").write(bdy); print("[OK]",name,"direct",m); done=True; break
            h=bdy.decode("utf-8","ignore")
            if BLOCK.search(h[:6000]): continue
            u=pdfurl(h,m)
            if not u: continue
            try: ct2,b2=get(u,ref=f"{m}/{doi}")
            except Exception: continue
            if b2[:4]==b"%PDF": open(dest,"wb").write(b2); print("[OK]",name,m,u[:70]); done=True; break
        if done: break
        time.sleep(3)
    if not done: print("[MISS]",name,doi)
print("done")
