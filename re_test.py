import re
string1 = "google runoob taobao"
patten = "oog*"
res = re.search(patten,string1)
print(res.group(0))