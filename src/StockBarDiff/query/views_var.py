'''
Created on Aug 29, 2017

@author: Coder_J
'''
from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
import sqlite3
import os
import math
from StockBarDiff.settings import BASE_DIR

db_stock_col_grade = [
        'diff_open', 'diff_high', 'diff_low', 'diff_close', 'diff_vol', \
        'diff_adj_open', 'diff_adj_high', 'diff_adj_low', 'diff_adj_close', 'diff_adj_vol'
    ]

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
    '''  To obtain a line of stock data  '''
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
    '''  Find the maximum value of migration rate  '''
    sql = 'SELECT MAX(u_stock_bar_data.%s) FROM u_stock_bar_data WHERE u_stock_bar_data.stock_code = \'%s\'' %(col_head, str(code))
    mmax = db_value_format(cur, sql)[0]
    sql = 'SELECT MIN(u_stock_bar_data.%s) FROM u_stock_bar_data WHERE u_stock_bar_data.stock_code = \'%s\'' %(col_head, str(code))
    mmin = db_value_format(cur, sql)[0]
    
    try:
        max_rate = round(((mmax - average) / average), 4)
        min_rate =  round(((average - mmin) / average), 4)
    except ZeroDivisionError:
        max_rate = 0
        min_rate = 0
     
    if max_rate > min_rate :
        return [mmax, max_rate]
    else:
        return [mmin, min_rate]

def db_stock_code (cur):
    '''  锟斤拷取锟斤拷锟捷匡拷锟斤拷锟斤拷锟叫的癸拷票锟斤拷锟斤拷  '''
    sql = 'SELECT DISTINCT u_stock_bar_data.stock_code FROM u_stock_bar_data'
    result = []
    cur.execute(sql)
    db_result = cur.fetchall()
    for item in db_result:
        result.append(item[0])
    return result

def db_grades(cur, stock_code, col_head):
    '''  锟斤拷取锟斤拷锟捷匡拷锟叫ｏ拷锟斤拷锟桔革拷锟斤拷锟斤拷  '''
    sql = 'SELECT u_stock_bar_data.%s FROM u_stock_bar_data WHERE u_stock_bar_data.stock_code = \'%s\'' %(col_head, str(stock_code))
    return db_value_format(cur, sql)

def db_value_format(cur, sql):
    '''  Query and format data  '''
    result = []
    cur.execute(sql)
    db_result = cur.fetchall()
    for item in db_result:
        result.append(float(item[0]))
    return result

def grades_sum(grades):
    '''  sum  '''
    total = 0
    for grade in grades:
        total += grade
    return total

def grades_average(grades):
    '''  averaging  '''
    sum_of_grades = grades_sum(grades)
    average = sum_of_grades / float(len(grades))
    return average

def grades_variance(scores, average=None):
    '''  Strives for the variance  '''
    if average == None:
        average=grades_average(scores)
    variance=0
    for score in scores:
        variance+=(average-score)**2
    var=variance/len(scores)
    return math.sqrt(var)