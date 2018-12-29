import requests
import json
import pymysql
import random
from time import sleep

# 需要的数据
def getId(head, url):
    while True:
        i = random.randint(1, 10)
        sleep(60)
        print(i)
        try:
            url = url + "%d" %i             # 请求地址,参数变化
            r = requests.get(url, headers=head)
            r.raise_for_status()
            r.encoding = "utf-8"
        except:
            print("获取异常")
        result1 = json.loads(r.text)        # 格式转换
        result2 = result1["result"]
        result = result2["data"]
        for j in result:                    # 循环获取id
            roomId = j["explicit_uid"]
            print(roomId)
            saveDB(roomId)




# 存储数据库
def saveDB(roomId):
    conn = pymysql.connect(host='localhost', port=3306, db='python_db', user='root', password='ok', charset='utf8')
    cur = conn.cursor()
    try:
        sql1 = "select * FROM `now` WHERE rid = %s"     # 用获取到的id匹配数据库,有:return
        result = cur.execute(sql1, roomId)
        if result > 0:                          # if 返回值>0(存在) return
            return "存在"
        sql2 = "insert into `now` values (null,%s)"   # else 执行插入sql
        cur.execute(sql2, roomId)
        conn.commit()
    except Exception as e:
        print("数据库异常:", e)
        conn.rollback()
        conn.close()
    print("储存数据库完成")



# 主方法
def main ():
    url = "https://now.qq.com/cgi-bin/now/web/user/get_personal_live_rcmd_read?num=150&tab_id="
    head = {
        'Accept': '*/*',
        'Accept-Encoding': 'gzip,deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'User-Agent':
        'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1',
    }
    getId(head, url)
    print("OK")

main()