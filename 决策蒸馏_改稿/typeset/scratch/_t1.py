
import zipfile, re, sys
z = zipfile.ZipFile(r"C:\Users\Administrator\Desktop\丙酮酰化\六-1_宠物主粮的价格带与品类结构（成稿）.docx")
xml = z.read("word/document.xml").decode("utf-8")
i = xml.find("<w:drawing>")
print("drawing idx", i, "len", len(xml))
s = xml.rfind("<w:p ", 0, i)
e = xml.find("</w:p>", i)
print("=== IMAGE PARA ===")
print(xml[s-200:e+6])
print("=== NEXT PARAS ===")
print(xml[e+6:e+3000])
