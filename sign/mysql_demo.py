#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: WangLX
# datetime: 2019/6/2 1:05
# software: PyCharm
from pymysql import cursors, connect

# 链接数据库
conn = connect(host='127.0.0.1',
               user='root',
               password='19920113',
               db='guest',
               charset='utf8mb4',
               cursorclass=cursors.DictCursor)
try:
    with conn.cursor() as cursor:
        # 创建嘉宾数据
        sql = 'INSERT INTO sign_guest (realname, phone, email, sign, event_id, create_time) ' \
              'VALUES ("tom", 18800110022,"tom@example.com", 0, 1, NOW());'
        cursor.execute(sql)
        # 提交事务
    conn.commit()

    with conn.cursor() as cursor:
        # 查询嘉宾
        sql = 'SELECT realname,phone,email,sign FROM sign_guest WHERE phone=%s'
        cursor.execute(sql, ('18800110022',))
        result = cursor.fetchone()
        print(result)
finally:
    conn.close()


