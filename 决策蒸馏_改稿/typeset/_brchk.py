
import zipfile, re, sys
sys.stdout.reconfigure(encoding="utf-8")
for nm in ["六-1_宠物主粮的价格带与品类结构（成稿）.docx","六-2_宠物食品网络投诉的类型分布与处理结果（成稿）.docx","七-6_宠物活体运输福利问题（统一结构成稿）.docx"]:
    z = zipfile.ZipFile(r"C:\Users\Administrator\Desktop\丙酮酰化\\"+nm)
    xml = z.read("word/document.xml").decode("utf-8")
    print(nm, "w:br count =", xml.count("<w:br"))
