import requests

from selenium.webdriver import Chrome,ChromeOptions

import time
import pymysql
import traceback
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
get_webhot()