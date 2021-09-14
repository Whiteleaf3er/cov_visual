import pymysql
import requests
import json
import time
import traceback  #追踪异常
from selenium.webdriver import Chrome,ChromeOptions

def get_webhot():   #热搜函数
    url ="https://s.weibo.com/top/summary"  # 微博的地址

    res = requests.get(url)
    #这个就是再后台上面运行那个浏览器，不在表面上占用你的
    option = ChromeOptions()
    option.add_argument('--headless')
    option.add_argument("--no-sandbox")
    #这里也要输入
    browser = Chrome(options=option,executable_path="E://Program Files//program//Anaconda//envs//flask_0811//Scripts//chromedriver.exe")
    browser.get(url)
    #解析那个web热搜前，按住ctrl+f会在下面出现一个框框，然后改就完事
    c = browser.find_elements_by_xpath('//*[@id="pl_top_realtimehot"]/table/tbody/tr/td[2]/a')
    #这个都看得懂，就一个文本输出
    context = [i.text for i in c]
    print(context)
    #返回
    return context

def get_baidu_hot():
    """
    :return: 返回百度疫情热搜
    """
    # option = ChromeOptions()  # 创建谷歌浏览器实例
    # option.add_argument("--headless")  # 隐藏浏览器
    # option.add_argument('--no-sandbox')

    url = "https://voice.baidu.com/act/virussearch/virussearch?from=osari_map&tab=0&infomore=1"
    browser = Chrome(executable_path="E://Program Files//program//Anaconda//envs//flask_0811//Scripts//chromedriver.exe")
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

def update_hotsearch():
    """
    将疫情热搜插入数据库
    :return:
    """
    cursor = None
    conn = None
    try:
        context = get_webhot()
        # context = ["四川","宜宾","武汉","cov","delta","印度","疫苗接种"]
        print(time.asctime() + "开始更新热搜数据")
        conn, cursor = get_conn()
        sql = "insert into hotsearch(dt,content) values(%s,%s)"
        ts = time.strftime("%Y-%m-%d %X")
        for i in context:
            cursor.execute(sql, (ts, i))  # 插入数据
        conn.commit()  # 提交事务保存数据
        # print(f"{time.asctime()}数据更新完毕")
        print(time.asctime() + "更新最新数据完毕")
    except:
        traceback.print_exc()
    finally:
        close_conn(conn, cursor)

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

def get_conn():
    """
    :return: 连接，游标
    """
    # 创建连接
    conn = pymysql.connect(host="121.36.92.44",
                           user="nanhua",
                           password="123456",
                           db="cov",
                           port=3306,
                           charset="utf8")
    # 创建游标
    cursor = conn.cursor()  # 执行完毕返回的结果集默认以元组显示
    return conn, cursor


def close_conn(conn, cursor):
    if cursor:
        cursor.close()
    if conn:
        conn.close()

def update_details():
    """
    更新 details 表
    :return:
    """
    cursor = None
    conn = None
    try:
        li = get_tencent_data()[1]  #  0 是历史数据字典,1 最新详细数据列表
        conn, cursor = get_conn()
        sql = "insert into details(update_time,province,city,confirm,confirm_add,heal,dead) values(%s,%s,%s,%s,%s,%s,%s)"
        sql_query = 'select %s=(select update_time from details order by id desc limit 1)' #对比当前最大时间戳
        #最后一条记录的最后更新时间
        cursor.execute(sql_query,li[0][0]) #如果一致说明不必更新
        sql_result = cursor.fetchone()
        if not sql_result[0]:
            # print(f"{time.asctime()}开始更新最新数据")
            print(time.asctime()+"开始更新最新数据")
            for item in li:
                cursor.execute(sql, item)
            conn.commit()  # 提交事务 update delete insert操作
            # print(f"{time.asctime()}更新最新数据完毕")
            print(time.asctime() + "更新最新数据完毕")
        else:
            # print(f"{time.asctime()}已是最新数据！")
            print(time.asctime() + "已是最新数据！")
    except:
        traceback.print_exc()
    finally:
        close_conn(conn, cursor)

def insert_history():
    """
        插入历史数据
    :return:
    """
    cursor = None
    conn = None
    try:
        dic = get_tencent_data()[0]  # 0 是历史数据字典,1 最新详细数据列表
        # print(f"{time.asctime()}开始插入历史数据")
        print(time.asctime() + "开始插入历史数据")
        conn, cursor = get_conn()
        sql = "insert into history values(%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        for k, v in dic.items():
            # item 格式 {'2020-01-13': {'confirm': 41, 'suspect': 0, 'heal': 0, 'dead': 1}
            cursor.execute(sql, [k, v.get("confirm"), v.get("confirm_add"), v.get("suspect"),
                                 v.get("suspect_add"), v.get("heal"), v.get("heal_add"),
                                 v.get("dead"), v.get("dead_add")])
        conn.commit()  # 提交事务 update delete insert操作
        # print(f"{time.asctime()}插入历史数据完毕")
        print(time.asctime() + "插入历史数据完毕")
    except:
        traceback.print_exc()
    finally:
        close_conn(conn, cursor)
def update_history():
    """
    更新历史数据
    :return:
    """
    cursor = None
    conn = None
    try:
        dic = get_tencent_data()[0]  #  0 是历史数据字典,1 最新详细数据列表
        # print(f"{time.asctime()}开始更新历史数据")
        print(time.asctime() + "开始更新历史数据")
        conn, cursor = get_conn()
        sql = "insert into history values(%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        sql_query = "select confirm from history where ds=%s"
        for k, v in dic.items():
            # item 格式 {'2020-01-13': {'confirm': 41, 'suspect': 0, 'heal': 0, 'dead': 1}
            if not cursor.execute(sql_query, k):
                cursor.execute(sql, [k, v.get("confirm"), v.get("confirm_add"), v.get("suspect"),
                                     v.get("suspect_add"), v.get("heal"), v.get("heal_add"),
                                     v.get("dead"), v.get("dead_add")])
        conn.commit()  # 提交事务 update delete insert操作
        # print(f"{time.asctime()}历史数据更新完毕")
        print(time.asctime() + "历史数据更新完毕")
    except:
        traceback.print_exc()
    finally:
        close_conn(conn, cursor)
# insert_history()
update_details()
# update_history()
# update_hotsearch()
'''
总结一下：正则表达式、flask、前端返回基本结构元素、mysql操作
'''