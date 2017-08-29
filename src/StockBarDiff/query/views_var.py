'''
Created on Aug 29, 2017

@author: Coder_J
'''
from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
import sqlite3
import os
from StockBarDiff.settings import BASE_DIR

db_stock_col_grade = [
    'beta_open', 'beta_high', 'beta_low', 'beta_close', 'beta_vol', \
    'beta_adj_open', 'beta_adj_high', 'beta_adj_low', 'beta_adj_close', 'beta_adj_vol', \
    'local_open', 'local_high', 'local_low', 'local_close', 'local_vol', \
    'local_adj_open', 'local_adj_high', 'local_adj_low', 'local_adj_close', 'local_adj_vol' ]

def do_work(request):
    result = []
    sqlite_conn= sqlite3.connect(os.path.join(BASE_DIR, 'db.sqlite3'))
    sqlite_cursor = sqlite_conn.cursor()
    stock_codes = db_stock_code(sqlite_cursor)
    index = 1
    for code in stock_codes:
        lop = stock_row_format(index, sqlite_cursor, code, db_stock_col_grade)
        index += 1
        result.append(lop)
    
    args = {
        'result':result
        }
    return render(request, 'var.html',args)

def stock_row_format(index, cursor, code, col_grade):
    # '''  循环计算各列的值  '''
    result = []
    for col_head in col_grade:
        p_grades = db_grades(cursor, code, col_head)        
        p_average = grades_average(p_grades)
        p_average = round(p_average, 4)
        p_variance = grades_variance(p_grades, p_average)
        p_variance = round(p_variance, 4)
        p_range = db_abs_range(cursor, code, p_average, col_head)

        lop = []
        lop.append(index)
        lop.append(code)
        lop.append(p_variance)
        lop.append(p_range)
        result.append(lop)
    return result
        

def db_abs_range(cur, code, average, col_head):
    # '''  取最大差值  '''
    sql = 'SELECT MAX(u_stock_bar_data.%s) FROM u_stock_bar_data WHERE u_stock_bar_data.stock_code = \'%s\'' %(col_head, str(code))
    mmax = db_value_format(cur, sql)[0]
    max_rate = round((abs(mmax - average) / average), 4)
    sql = 'SELECT MIN(u_stock_bar_data.%s) FROM u_stock_bar_data WHERE u_stock_bar_data.stock_code = \'%s\'' %(col_head, str(code))
    mmin = db_value_format(cur, sql)[0]
    min_rate = round((abs(mmin - average) / average), 4)
    if max_rate > min_rate :
        return [mmax, max_rate]
    else:
        return [mmin, min_rate]

def db_stock_code (cur):
    # '''  获取数据库中所有的股票号码  '''
    sql = 'SELECT DISTINCT u_stock_bar_data.stock_code FROM u_stock_bar_data'
    result = []
    cur.execute(sql)
    db_result = cur.fetchall()
    for item in db_result:
        result.append(item[0])
    return result

def db_grades(cur, stock_code, col_head):
    # '''  获取数据库中，“价格”数组  '''
    sql = 'SELECT u_stock_bar_data.%s FROM u_stock_bar_data WHERE u_stock_bar_data.stock_code = \'%s\'' %(col_head, str(stock_code))
    return db_value_format(cur, sql)

def db_value_format(cur, sql):
    result = []
    cur.execute(sql)
    db_result = cur.fetchall()
    for item in db_result:
        result.append(float(item[0]))
    return result

def grades_sum(grades):
    # '''  定义求和函数  '''
    total = 0
    for grade in grades:
        total += grade
    return total

def grades_average(grades):
    # '''  定义求平均值函数  '''
    sum_of_grades = grades_sum(grades)
    average = sum_of_grades / float(len(grades))
    return average

def grades_variance(scores, average=None):
    # '''  定义求方差函数  '''
    if average == None:
        average=grades_average(scores)
    variance=0
    for score in scores:
        variance+=(average-score)**2
    return variance/len(scores)