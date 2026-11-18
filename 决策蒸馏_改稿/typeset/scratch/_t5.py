
import zipfile, re
COVER = r"C:\\Users\\Administrator\\Documents\\xwechat_files\\wxid_h72ol1ylw9hv22_d04f\\msg\\file\\2026-11\\五-11_本轮生猪产能调控政策的成效评估与养殖场经营风险分.docx"
z = zipfile.ZipFile(COVER)
print("=== core.xml ==="); print(z.read("docProps/core.xml").decode("utf-8"))
print("=== app.xml ==="); print(z.read("docProps/app.xml").decode("utf-8")[:1500])
print("=== footer1 ==="); print(z.read("word/footer1.xml").decode("utf-8")[:1200])
print("=== rels ==="); print(z.read("word/_rels/document.xml.rels").decode("utf-8"))
print("=== six-1 sectPr ===")
z2 = zipfile.ZipFile(r"C:\Users\Administrator\Desktop\丙酮酰化\六-1_宠物主粮的价格带与品类结构（成稿）.docx")
x2 = z2.read("word/document.xml").decode("utf-8")
for m in re.finditer(r"<w:sectPr[^>]*>.*?</w:sectPr>", x2, re.S):
    s = re.sub(r' xmlns(:w+)?="[^"]*"', "", m.group(0))
    print(s[:900]); print("---")
print("=== six-1 core ==="); print(z2.read("docProps/core.xml").decode("utf-8"))
print("parts six-1:", [n for n in z2.namelist() if "footer" in n or "media" in n])
