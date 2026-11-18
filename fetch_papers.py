# -*- coding: utf-8 -*-
"""
批量按 DOI 抓取文献 PDF —— 多镜像轮询 + 验证页识别
用法:
    python fetch_papers.py              # 全部 9 篇
    python fetch_papers.py 4 6          # 只抓第 4、6 篇
    python fetch_papers.py 10.1021/jasms.4c00366
镜像顺序可自己在 MIRRORS 里改；下载落盘到 ./pdfs/
"""
import os, re, sys, time, json, urllib.parse
import urllib.request, urllib.error

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "pdfs")
os.makedirs(OUT, exist_ok=True)

# ---- 待抓文献：编号, DOI, 简称 ----
PAPERS = [
    ("01_Sitosari_BBRC_2023",  "10.1016/j.bbrc.2023.01.033"),
    ("02_Liang_VetMicro_2026", "10.1016/j.vetmic.2026.110871"),
    ("03_Xu_CancerLett_2026",  "10.1016/j.canlet.2026.218650"),
    ("04_Bao_JASMS_2024",      "10.1021/jasms.4c00366"),
    ("05_Zhao_ChemResTox_2024","10.1021/acs.chemrestox.3c00298"),
    ("06_Yuan_JPR_2026",       "10.1021/acs.jproteome.5c01243"),
    ("07_Chai_MolNeurobiol_2024","10.1007/s12035-024-03995-y"),
    ("08_Demir_AminoAcids_2023","10.1007/s00726-023-03266-5"),
    ("09_Wei_Oncogene_2025",   "10.1038/s41388-025-03450-9"),
]

# ---- 镜像池：可用性会漂，坏的自动跳过 ----
MIRRORS = [
    "https://sci-hub.st",
    "https://sci-hub.ee",
    "https://sci-hub.ru",
    "https://sci-hub.ee",
    "https://www.sci-hub.ren",
    "https://sci-hub.usualwant.com",
    "https://sci-hub.al",
    "https://sci-hub.box",
    "https://sci-hub.hkvisa.net",
    "https://sci.bban.top",
    "https://sci-hub.org.cn",
]

BLOCK_PAT = re.compile(r"(Verification|turnstile|cf-challenge|Just a moment|DDoS-Guard|captcha|验证码)", re.I)

def get(url, timeout=12, referer=None):
    req = urllib.request.Request(url, headers={
        "User-Agent": UA,
        "Accept": "text/html,application/pdf,*/*",
        "Accept-Language": "en-US,en;q=0.9",
    })
    if referer:
        req.add_header("Referer", referer)
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.status, r.headers.get("Content-Type", ""), r.read()

def extract_pdf_url(html, base):
    """从渲染页里挖 PDF 地址：embed/iframe src、location.href、save button"""
    pats = [
        r'<embed[^>]+src\s*=\s*["\']([^"\']+)["\']',
        r'<iframe[^>]+src\s*=\s*["\']([^"\']+)["\']',
        r'location\.href\s*=\s*["\']([^"\']+)["\']',
        r'(?:src|href)\s*=\s*["\']([^"\']*\.pdf[^"\']*)["\']',
        r'<a[^>]+href\s*=\s*["\'](/downloads/[^"\']+)["\']',
    ]
    for p in pats:
        m = re.search(p, html, re.I)
        if not m:
            continue
        u = m.group(1).strip()
        if u.startswith("//"):
            u = "https:" + u
        elif u.startswith("/"):
            u = urllib.parse.urljoin(base + "/", u)
        elif not u.startswith("http"):
            u = urllib.parse.urljoin(base + "/", u)
        return u
    return None

def try_mirror(mirror, doi, dest):
    url = f"{mirror}/{doi}"
    try:
        status, ctype, body = get(url)
    except Exception as e:
        return None, f"unreachable({type(e).__name__})"
    if "pdf" in ctype.lower() and body[:4] == b"%PDF":
        open(dest, "wb").write(body)
        return dest, "direct-pdf"
    html = body.decode("utf-8", "ignore")
    if BLOCK_PAT.search(html[:6000]):
        return None, "blocked(CF/验证页,需浏览器过验证)"
    if re.search(r"(article not found|文章未找到|not found in the database)", html, re.I):
        return None, "not-in-db"
    pdf_url = extract_pdf_url(html, mirror)
    if not pdf_url:
        return None, "no-pdf-link"
    for attempt in (pdf_url, pdf_url.replace("http://", "https://")):
        try:
            s2, ct2, b2 = get(attempt, referer=url)
        except Exception as e:
            continue
        if b2[:4] == b"%PDF":
            open(dest, "wb").write(b2)
            return dest, "pdf-via-embed"
    return None, "pdf-link-dead"

def main(argv):
    todo = PAPERS
    if len(argv) > 1:
        sel = []
        for a in argv[1:]:
            for name, doi in PAPERS:
                if a == doi or (a.isdigit() and PAPERS[int(a)-1][1] == doi):
                    sel.append((name, doi))
        todo = sel or PAPERS

    report = []
    for name, doi in todo:
        dest = os.path.join(OUT, name + ".pdf")
        row = {"paper": name, "doi": doi, "ok": False, "how": "", "log": []}
        if os.path.exists(dest) and os.path.getsize(dest) > 20000:
            row.update(ok=True, how="cached")
            report.append(row); print(f"[=] {name} 已存在"); continue
        for m in MIRRORS:
            r, how = try_mirror(m, doi, dest)
            row["log"].append(f"{m} -> {how}")
            print(f"[{name}] {m} -> {how}")
            if r:
                row.update(ok=True, how=f"{m} / {how}")
                break
            time.sleep(1.2)
        report.append(row)

    print("\n==== 汇总 ====")
    for row in report:
        print(("OK   " if row["ok"] else "MISS "), row["paper"], row["doi"], row["how"])
    with open(os.path.join(OUT, "report.json"), "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=1)
    print("\n报告: ", os.path.join(OUT, "report.json"))

if __name__ == "__main__":
    main(sys.argv)
