# -*- coding: utf-8 -*-
"""Sci-Hub ALTCHA 验证绕过 + 按 DOI 下载 PDF"""
import hashlib, json, base64, os, re, sys, time, urllib.request, http.cookiejar, urllib.parse

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "pdfs")
os.makedirs(OUT, exist_ok=True)

class Client:
    def __init__(self):
        self.cj = http.cookiejar.CookieJar()
        self.op = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(self.cj))
        self.base = None
    def get(self, url, tries=6, want=None, bytes_=False):
        last = None
        for i in range(tries):
            try:
                r = self.op.open(urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "*/*"}), timeout=25)
                data = r.read()
                ct = r.headers.get("Content-Type", "")
                if bytes_:
                    return data, ct
                body = data.decode("utf-8", "ignore")
                if want == "altcha" and "altcha" not in body.lower():
                    last = f"len={len(body)}"; time.sleep(2); continue
                if want == "article" and ("altcha" in body.lower() or "ddg" in body.lower()[:1500]):
                    last = f"len={len(body)}"; time.sleep(2); continue
                return body, ct
            except Exception as e:
                last = type(e).__name__; time.sleep(2)
        raise RuntimeError(f"get failed: {url} ({last})")

    def post_json(self, url, obj):
        data = json.dumps(obj).encode()
        req = urllib.request.Request(url, data=data, headers={"User-Agent": UA, "Content-Type": "application/json"})
        with self.op.open(req, timeout=25) as r:
            return r.status, r.read().decode("utf-8", "ignore")

CHECK = re.compile(r'challengeurl\s*=\s*"(/captcha/challenge/(\d+))"')
SOL = re.compile(r"fetch\('(/captcha/solution/(\d+))'")

def solve_altcha(cli, html, page_url):
    m, s = CHECK.search(html), SOL.search(html)
    if not m or not s:
        return False
    chal_url = urllib.parse.urljoin(page_url, m.group(1))
    sol_url = urllib.parse.urljoin(page_url, s.group(1))
    body, _ = cli.get(chal_url)
    ch = json.loads(body)
    salt, target = ch["salt"], ch["challenge"]
    algo = ch.get("algorithm", "SHA-256").replace("-", "").lower()
    maxnum = int(ch.get("maxnumber") or 1000000)
    h = hashlib.new(algo)
    number = None
    for n in range(maxnum + 1):
        h2 = hashlib.new(algo, (salt + str(n)).encode()).hexdigest()
        if h2 == target:
            number = n
            break
    if number is None:
        return False
    payload = base64.b64encode(json.dumps({
        "algorithm": ch.get("algorithm", "SHA-256"),
        "challenge": target, "number": number, "salt": salt,
        "signature": ch.get("signature", ""),
    }).encode()).decode()
    st, resp = cli.post_json(sol_url, {"captcha": payload})
    return st == 200 and '"success":true' in resp.replace(" ", "")

def find_pdf(html, base):
    for pat in [r'<embed[^>]+src\s*=\s*["\']([^"\']+)', r'<iframe[^>]+src\s*=\s*["\']([^"\']+)',
                r'location\.href\s*=\s*["\']([^"\']+)', r'href\s*=\s*["\']([^"\']*/downloads/[^"\']+)']:
        mm = re.search(pat, html, re.I)
        if mm:
            u = mm.group(1).replace("\\/", "/")
            if u.startswith("//"): return "https:" + u
            if u.startswith("http"): return u
            return urllib.parse.urljoin(base + "/", u)
    return None

def grab(host, doi, dest):
    cli = Client()
    page = f"{host}/{doi}"
    html, _ = cli.get(page, tries=10)
    if "altcha" in html.lower():
        ok = solve_altcha(cli, html, page)
        print(f"  altcha solved: {ok}")
        if ok:
            html, _ = cli.get(page, tries=10, want="article")
    if "altcha" in html.lower():
        return None, "captcha-unresolved"
    if re.search(r"(article not found|not found in the database|未找到)", html, re.I):
        return None, "not-in-db"
    u = find_pdf(html, host)
    if not u:
        return None, "no-pdf-link"
    data, ct = cli.get(u, bytes_=True)
    if data[:4] != b"%PDF":
        return None, f"not-pdf({ct})"
    open(dest, "wb").write(data)
    return dest, "ok"

if __name__ == "__main__":
    jobs = [("01_Sitosari_BBRC_2023", "10.1016/j.bbrc.2023.01.033"),
            ("05_Zhao_ChemResTox_2024", "10.1021/acs.chemrestox.3c00298")]
    for name, doi in jobs:
        dest = os.path.join(OUT, name + ".pdf")
        for host in ["https://sci-hub.st", "https://sci-hub.ru", "https://sci-hub.ee"]:
            try:
                r, how = grab(host, doi, dest)
            except Exception as e:
                r, how = None, f"{type(e).__name__}:{str(e)[:60]}"
            print(f"[{name}] {host} -> {how}")
            if r:
                print("   saved", dest, os.path.getsize(dest))
                break
