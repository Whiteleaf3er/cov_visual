from bs4 import BeautifulSoup
import requests

url = "http://wsjkw.sc.gov.cn/scwsjkw/gzbd/fyzt.shtml"
res = requests.get(url)
res.encoding = "utf-8"
html = res.text

soup = BeautifulSoup(html,'html.parser')

a = soup.find("a")
url_day = "http://wsjkw.sc.gov.cn" + a.attrs["href"]
res = requests.get(url_day)
res.encoding = "utf-8"
html = res.text
soup = BeautifulSoup(html,'html.parser')
content = soup.find_all("p")[1]
content_text = content.text
print(content_text)
patten="全省累计报告新型冠状病毒肺炎确诊病例([0-9]+).*?累计治愈出院(\d+).*?死亡(\d+)例"
import re
res = re.search(patten,content_text)
print(res.groups())
print(res.group(0))

url_tencent = "https://view.inews.qq.com/g2/getOnsInfo?name=disease_h5"
res_tencent = requests.get(url_tencent)
# res_tencent.encoding = "utf-8"
html_tecent = res_tencent.text
import json
dict_tecent = json.loads(html_tecent)

data_all = json.loads(dict_tecent['data'])
print(data_all.keys())
update_time = data_all["lastUpdateTime"]
total_1 = data_all["chinaTotal"]
add_1 = data_all["chinaAdd"]
print(update_time)
print(total_1)
print(add_1)

