import requests
import json
import pymysql
from time import sleep

# 需要的数据(死循环获取) _李爽
def getId(head):
    i = 0                 # 初始值为0
    while True:
        print(i)
        sleep(10)
        # 请求地址,拼接地址参数
        try:
                    # 地址参数,模拟请求
            url = "https://fx1.service.kugou.com/IndexWebPlat/IndexWebService/IndexWebService/getLiveRoomListByType/%d-0-0-1-0/" %i
            r = requests.get(url, headers=head)
            r.raise_for_status()
            print(r.status_code)
            r.encoding = r.apparent_encoding    # 得到页面信息数据
        except:
            print("获取失败")
    # 获取id
        result = json.loads(r.text)         # 转换格式
        result =result["data"]
        result = result["list"]
        print(result)
        if len(result) == 0:                # if 结果长度为0时,  本次循环结束,可以从新赋值,继续获取新上线的主播
            print("空")
            i = 0
            continue
        else:                               # else 结果长度不为0时,循环次数+1(参数+1)
            i += 1
        for j in result:                    # 遍历数据,储存数据库
            rid = j["roomId"]
            print(rid)
            saveDB(rid)


def saveDB(rid):
    conn = pymysql.connect(host='localhost', port=3306, db='python_db', user='root', password='ok', charset='utf8')
    #print(conn)
    cur = conn.cursor()
    try:
        sql1 = "select * FROM kugou WHERE rid = %s"     # 用获取到的id匹配数据库,结果>0 : return
        result = cur.execute(sql1, rid)
        if result > 0:
            return "存在"
        sql2 = "insert into `kugou` values (null,%s)"   # 执行插入sql
        cur.execute(sql2, rid)
        conn.commit()
    except Exception as e:
        print("异常:", e)
        conn.rollback()
        conn.close()
    print("储存数据库完成")


def main():
    head = {
        'Accept': '*/*',
        'Accept-Encoding': 'gzip,deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'User-Agent':
        'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:56.0) Gecko/20100101 Firefox/56.0',
    }
    getId(head)
    print("ok")
main()