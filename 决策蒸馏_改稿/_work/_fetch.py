# -*- coding: utf-8 -*-
import sys, re, subprocess, os
UA='Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
def fetch(url):
    p=subprocess.run(['curl','-sL','--compressed','-A',UA,'--max-time','40',url],capture_output=True)
    return p.stdout
def totext(b):
    for enc in ('utf-8','gb18030','gbk'):
        try:
            s=b.decode(enc); break
        except Exception: continue
    else:
        s=b.decode('utf-8','ignore')
    s=re.sub(r'<script.*?</script>','',s,flags=re.S|re.I)
    s=re.sub(r'<style.*?</style>','',s,flags=re.S|re.I)
    s=re.sub(r'<[^>]+>',' ',s)
    s=re.sub(r'&nbsp;',' ',s)
    s=re.sub(r'&[a-z]+;',' ',s)
    s=re.sub(r'\s+',' ',s)
    return s
if __name__=='__main__':
    url=sys.argv[1]; pats=sys.argv[2:]
    b=fetch(url); t=totext(b)
    print('LEN',len(t))
    for p in pats:
        hits=list(re.finditer(p,t))
        print('PAT',p,'hits',len(hits))
        for m in hits[:4]:
            print('   ...',t[max(0,m.start()-150):m.start()+150])
