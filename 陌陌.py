import requests
import json
import pymysql
# 获取需要的数据
def getId(url, head):
    i = 0
    while True:
        print(i)
        try:
            params = {"page": "%d" % i}     # 请求参数
            r = requests.post(url, headers=head, data=params)       # post请求
            r.raise_for_status()
            r.encoding = r.apparent_encoding    # 得到页面信息
        except:
            print("获取失败")
        # 获取id
        result1 = json.loads(r.text)        # 信息转换
        result2 = result1['data']
        result = result2['r_infos']         # 获取第i次循环json中的集合数据
        h_next = result2['h_next']
        if h_next is False:                 # if    中h_next字段为False时,数据取完,重新开始循环(i=0)
            i = 0
            continue
        else:                               # else      循环次数+1(参数+1)
            i += 1
        for j in result:                    # 循环第一次集合数据得到单个id
            rid = j["stid"]
            print(rid)
            saveDB(rid)
# 储存到数据库
def saveDB(rid):
    conn = pymysql.connect(host='localhost', port=3306, db='python_db', user='root', password='ok', charset='utf8')
    cur = conn.cursor()
    try:
        sql1 = "select * FROM momo WHERE rid = %s"      # 获取的id匹配数据库
        result = cur.execute(sql1, rid)
        if result > 0:                             # if 结果>0说明已有id,直接return
            return "存在"
        sql = "insert into momo values (null,%s)"     # else 执行插入sql
        cur.execute(sql, rid)
        conn.commit()
    except Exception as e:
        print("异常:", e)
        conn.rollback()
        conn.close()
    print("储存数据库完成")
def main():
    url = "https://web.immomo.com/webmomo/api/scene/recommend/lists/"   #访问的地址
    # post请求需要缓存,添加cookie
    cookie = "MMID=caff49763e18432d2dd755c3069f618f; Hm_lvt_96a25bfd79bc4377847ba1e9d5dfbe8a=1545736521; cId=73652713649188; _uab_collina=154573656167124516014263; webmomo=nL5G3r4YJ6VUYqsBrVtNwWSGm9nEJMQ_; webmomo.sig=AGXHvfy60F4qxIQ3xNqOZCYzpWg; s_id=40bd2850a976a4f2f3d2584e80f79520; web-imi-bew=s%3A672696783.9NkLfLkV5YUMQkewcuzulhY3BaAI3R3afSyBJqVSLKo; web-imi-bew.sig=VjXHr-V4xjisr3hhu8sZOPRKGsg; Hm_lvt_c391e69b0f7798b6e990aecbd611a3d4=1545753915,1545754004,1545754900,1545785081; io=WxEjEx7FAglbMRTqAdEy; Hm_lpvt_c391e69b0f7798b6e990aecbd611a3d4=1545796450"
    head = {
        'Accept': '*/*',
        'Accept-Encoding': 'gzip,deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'User-Agent':
        'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:56.0) Gecko/20100101 Firefox/56.0',
        'Cookie': cookie
    }
    getId(url, head)
    print("ok")
main()
