from bs4 import BeautifulSoup
import requests
import json
import time

def get_tencent_data():
    """
    :return: 返回历史数据和当日详细数据
    """
    url = 'https://view.inews.qq.com/g2/getOnsInfo?name=disease_h5'
    url_histort = "https://view.inews.qq.com/g2/getOnsInfo?name=disease_other"
    url2='&name=disease_h5'
    headers = {
        'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Mobile Safari/537.36',
        'Referer':' https://news.qq.com/zt2020/page/feiyan.htm'
    }
    r = requests.get(url, headers)
    res = json.loads(r.text)  # json字符串转字典
    data_all = json.loads(res['data'])
    r_history = requests.get(url_histort)
    res_history = json.loads(r_history.text)
    data_history_all = json.loads(res_history['data'])

    history = {}  # 历史数据h5
    for i in data_history_all["chinaDayList"]:
        ds = "2020." + i["date"]
        tup = time.strptime(ds, "%Y.%m.%d")
        ds = time.strftime("%Y-%m-%d", tup)  # 改变时间格式,不然插入数据库会报错，数据库是datetime类型
        confirm = i["confirm"]
        suspect = i["suspect"]
        heal = i["heal"]
        dead = i["dead"]
        history[ds] = {"confirm": confirm, "suspect": suspect, "heal": heal, "dead": dead}
    for i in data_history_all["chinaDayAddList"]:
        ds = "2020." + i["date"]
        tup = time.strptime(ds, "%Y.%m.%d")
        ds = time.strftime("%Y-%m-%d", tup)
        confirm = i["confirm"]
        suspect = i["suspect"]
        heal = i["heal"]
        dead = i["dead"]
        history[ds].update({"confirm_add": confirm, "suspect_add": suspect, "heal_add": heal, "dead_add": dead})

    details = []  # 当日详细数据
    update_time = data_all["lastUpdateTime"]
    data_country = data_all["areaTree"]  # list 25个国家
    data_province = data_country[0]["children"]  # 中国各省
    for pro_infos in data_province:
        province = pro_infos["name"]  # 省名
        for city_infos in pro_infos["children"]:
            city = city_infos["name"]
            confirm = city_infos["total"]["confirm"]
            confirm_add = city_infos["today"]["confirm"]
            heal = city_infos["total"]["heal"]
            dead = city_infos["total"]["dead"]
            details.append([update_time, province, city, confirm, confirm_add, heal, dead])
    return history, details

def get_baidu_hot():
    """
    :return: 返回百度疫情热搜
    """
    option = ChromeOptions()  # 创建谷歌浏览器实例
    option.add_argument("--headless")  # 隐藏浏览器
    option.add_argument('--no-sandbox')

    url = "https://voice.baidu.com/act/virussearch/virussearch?from=osari_map&tab=0&infomore=1"
    browser = Chrome(options=option,executable_path=".C:\\Program Files (x86)\\Google\Chrome\\Application/chromedriver.exe")
    browser.get(url)
    # 找到展开按钮
    dl = browser.find_element_by_xpath('//*[@id="main"]/div/div/section/div[2]/div/div[2]/section/div')
    dl.click()
    time.sleep(1)
    # 找到热搜标签
    c = browser.find_elements_by_xpath('//*[@id="main"]/div/div/section/div[2]/div/div[2]/section/a/div/span[2]')
    context = [i.text for i in c]  # 获取标签内容
    print(context)
    return context


his_1,details1_1 = get_tencent_data()
print(his_1)
print(details1_1)

