# -*- coding: utf-8 -*-
import re, sys, io, json

def load(path):
    return io.open(path, encoding='utf-8').read()

def body_only(txt):
    # cut references section
    lines = txt.split('\n')
    out=[]
    for ln in lines:
        s = ln.strip()
        if re.match(r'^#*\s*参考文献\s*$', s):
            break
        out.append(ln)
    return '\n'.join(out)

def strip_md(txt):
    txt = re.sub(r'^#+\s*', '', txt, flags=re.M)
    txt = re.sub(r'!\[[^\]]*\]\([^)]*\)', '', txt)
    txt = re.sub(r'^\|.*$', '', txt, flags=re.M)
    return txt

def report(path, name):
    raw = load(path)
    b = strip_md(body_only(raw))
    # remove reference-ish bracket numbers? keep them; count only CJK
    cjk = re.findall(r'[\u4e00-\u9fff]', b)
    n_cjk = len(cjk)
    # sentences: split on 。！？ keep 
    sents = [s for s in re.split(r'[。！？]', b)]
    sents = [s.strip() for s in sents if re.search(r'[\u4e00-\u9fff]', s)]
    # sentence lengths in cjk chars
    lens = [len(re.findall(r'[\u4e00-\u9fff]', s)) for s in sents]
    n_sent = len(sents)
    avg = n_cjk/ n_sent if n_sent else 0
    long60 = sum(1 for x in lens if x > 60)
    semis = b.count('；')
    semi_per_k = semis / n_cjk * 1000
    benwen = len(re.findall(r'本文', b))
    zheyi = len(re.findall(r'这一[\u4e00-\u9fff]', b))
    dash = b.count('——')
    straight = b.count('"') + b.count("'")
    curly = b.count('“')
    return dict(file=name, cjk=n_cjk, sents=n_sent, avg=round(avg,1), long60=long60,
                semis=semis, semi_per_k=round(semi_per_k,2), benwen=benwen,
                zheyi=zheyi, dash=dash, straight_quotes=straight, curly_open=curly)

for p in sys.argv[1:]:
    print(json.dumps(report(p, p), ensure_ascii=False))
