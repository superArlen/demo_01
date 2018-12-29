import requests
from bs4 import BeautifulSoup
import re
import pymysql
from time import sleep

# 需要的数据 (死循环)
def getId(head, url):
    i = 4       # 初始值
    while True:
        print(i)
        sleep(10)
        try:
            params = {"page": "%d" % i}
            #params = {"page": 4}
            r = requests.get(url, headers=head, params=params)
            r.raise_for_status()
            r.encoding = "utf-8"
        except:
            print("获取异常")
        # 获取roomId
        soup = BeautifulSoup(r.text, "html.parser")
        allTag = soup.find("div", {"class": "list_panel_bd clearfix"}).find_all("a")
        if len(allTag) == 0:            # if  获取allTag长度为0,说明网站加载的页码取完.从新赋值开始
            print("无数据,本次循环结束")
            i = 1
            continue
        else:                           # else 次数+1
            i += 1
        for j in allTag:
            rid = j.get("href")         # href中两组数字,取下标0的数字是需要id
            rid = (re.findall(r"\d+\d*", rid))[0]
            print(rid)
            saveDB(rid)                 # 储存

# 插入数据库
def saveDB(rid):
    conn = pymysql.connect(host='localhost', port=3306, db='python_db', user='root', password='ok', charset='utf8')
    cur = conn.cursor()
    try:
        sql1 = "select * FROM yingke WHERE rid = %s"     # 用获取到的id匹配数据库,有:return
        result = cur.execute(sql1, rid)
        if result > 0:                          # if 返回值>0,return
            return "存在"
        sql2 = "insert into `yingke` values (null,%s)"   # else 执行插入sql
        cur.execute(sql2, rid)
        conn.commit()
    except Exception as e:
        print("数据库异常:", e)
        conn.rollback()
        conn.close()
    print("储存数据库完成")



def main():
    url = "http://www.inke.cn/hotlive_list.html"
    head = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:56.0) Gecko/20100101 Firefox/56.0'}
    getId(head, url)
    print("OK")

main()