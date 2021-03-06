#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: zhongliang.jiang
# @Date:   2017-08-21 18:36:54
# @Last Modified time: 2017-08-21 18:37:56
from stockbar_10jqka.line.stock_bar_crawler import *
from stockbar_10jqka.line.stock_bar_query import *
from stockbar_beta.beta_bar_query_lib import *
from stockbar_beta.beta_url_lib import *
import sqlite3

# crawler = stock_bar_crawler()
# crawler.craw_stocks("./data/stock_code.txt", '2015')

# query = stock_bar_query()
# val = query.query('600000', 'last')
# print(val)
# val = query.query('600000', date = 20160104)
# val = query.query('601000',year='last')
# print(val)

# uurl = beta_url()
# print(uurl.get_symbol_url())
# print(uurl.get_price_url())

# query = beta_bar_query()
# val = query.query_stock_symbols()
# # print(val)
# val = query.query_stock_bar(symbols='601000', date='last', period='260')
# print(val)

sqlite_conn= sqlite3.connect("./db.sqlite3")
sqlite_cursor = sqlite_conn.cursor()

flag='open'
sql = 'SELECT compare_data.stock_code, count(compare_data.%s) as diff_%s FROM compare_data WHERE abs(compare_data.%s) %s GROUP BY compare_data.stock_code '
sql = sql%(flag, flag, flag, '= 0.0')

print(sql)
sqlite_cursor.execute(sql)
result = sqlite_cursor.fetchall()

print(type(result))
print(result)