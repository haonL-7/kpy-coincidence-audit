
import zipfile, re, sys
sys.stdout.reconfigure(encoding="utf-8")
z = zipfile.ZipFile(r"C:\Users\Administrator\Desktop\丙酮酰化\六-1_宠物主粮的价格带与品类结构（成稿）.docx")
xml = z.read("word/document.xml").decode("utf-8")
for m in re.finditer(r"<w:br[^/]*/>", xml):
    i = m.start()
    s = max(xml.rfind("<w:p ", 0, i), xml.rfind("<w:p>", 0, i))
    e = xml.find("</w:p>", i)
    seg = re.sub(r'<w:rPr>.*?</w:rPr>', '', xml[s:e], flags=re.S)
    seg = re.sub(r'<w:pPr>.*?</w:pPr>', '[[pPr]]', seg, flags=re.S)
    print("at", i, "para:", re.sub(r'<w:drawing>.*?</w:drawing>','[DRAW]',seg,flags=re.S)[:400])
    print("---")
