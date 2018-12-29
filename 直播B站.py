import requests
import json
import pymysql
from time import sleep

# 需要的数据     死循环获取
def getId(head, url):
    i = 1
    while True:
        sleep(10)
        print(i)
        try:
            params = {"page": "%d" % i}         # 参数从1开始获取页面信息
            r = requests.get(url, headers=head, params=params)     # 获取页面信息
            r.raise_for_status()
            r.encoding = r.apparent_encoding
        except:
            print("获取异常")
        # 获取roomId
        result = json.loads(r.text)     # 转换
        result = result["data"]
        if len(result) == 0:            # if 获取的数据长度为0,说明本次获取结束,从新赋值i,继续循环----获取新上线的id
            print("无数据")
            i = 0
            continue
        else:                           # else 循环次数+1(page+1)
            i += 1
        for j in result:                # 保存数据库
            roomid = j["roomid"]
            print(roomid)
            saveDB(roomid)



    # 执行插入操作
def saveDB(roomId):
    conn = pymysql.connect(host='localhost', port=3306, db='python_db', user='root', password='ok', charset='utf8')
    #print(conn)
    cur = conn.cursor()
    try:
        sql1 = "select * FROM blibli WHERE rid = %s"     # 用获取到的id匹配数据库,有:return
        result = cur.execute(sql1, roomId)              # if返回值>0,return
        if result > 0:
            return "存在"
        sql2 = "insert into `blibli` values (null,%s)"   # else 执行插入sql
        cur.execute(sql2, roomId)
        conn.commit()
    except Exception as e:
        print("数据库异常:", e)
        conn.rollback()
        conn.close()
    print("储存数据库完成")




def main():
    url = "https://api.live.bilibili.com/room/v1/room/get_user_recommend"
    head = {
        'Accept': '*/*',
        'Accept-Encoding': 'gzip,deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'User-Agent':
        'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:56.0) Gecko/20100101 Firefox/56.0',
    }
    getId(head, url)

    print("OK")

main()



