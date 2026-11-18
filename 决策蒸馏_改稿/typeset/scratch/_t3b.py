
import zipfile, io
z = zipfile.ZipFile(r"C:\Users\Administrator\Desktop\丙酮酰化\六-1_宠物主粮的价格带与品类结构（成稿）.docx")
xml = z.read("word/document.xml").decode("utf-8")
i = xml.find('<wp:extent cx="5219700"')
s = max(xml.rfind("<w:p ", 0, i), xml.rfind("<w:p>", 0, i))
e = xml.find("</w:p>", i)
im = xml[s:e+6]
# drop the drawing body for brevity
k = im.find("<w:drawing>"); k2 = im.find("</w:drawing>")+len("</w:drawing>")
imshort = im[:k] + "[[DRAWING]]" + im[k2:]
e2 = xml.find("</w:p>", e+6); p2 = xml[e+6:e2+6]
e3 = xml.find("</w:p>", e2+6); p3 = xml[e2+6:e3+6]
e4 = xml.find("</w:p>", e3+6); p4 = xml[e3+6:e4+6]
out = "IMG:\n"+imshort+"\n\nP2:\n"+p2+"\n\nP3:\n"+p3+"\n\nP4:\n"+p4
open(r"C:\Users\Administrator\Desktop\丙酮酰化\决策蒸馏_改稿\_t3u.txt","w",encoding="utf-8").write(out)
print("ok")
