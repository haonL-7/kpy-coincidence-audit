
import zipfile, re
z = zipfile.ZipFile(r"C:\Users\Administrator\Desktop\丙酮酰化\六-1_宠物主粮的价格带与品类结构（成稿）.docx")
xml = z.read("word/document.xml").decode("utf-8")
print("drawings:", xml.count("<w:drawing>"))
for m in re.finditer(r'<wp:extent cx="(\d+)" cy="(\d+)"/>', xml):
    print("extent", m.group(1), m.group(2), "cm=%.2f x %.2f" % (int(m.group(1))/360000, int(m.group(2))/360000), "at", m.start())
