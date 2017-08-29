from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
import sqlite3
import os
from StockBarDiff.settings import BASE_DIR

def stock(request, code):
    sqlite_conn= sqlite3.connect(os.path.join(BASE_DIR, 'db.sqlite3'))
    sqlite_cursor = sqlite_conn.cursor()

    sql = "SELECT \
        u_stock_bar_data.stock_code, \
        u_stock_bar_data.date, \
        u_stock_bar_data.beta_open, \
        u_stock_bar_data.beta_high, \
        u_stock_bar_data.beta_low, \
        u_stock_bar_data.beta_close, \
        u_stock_bar_data.beta_vol, \
        u_stock_bar_data.beta_adj_open, \
        u_stock_bar_data.beta_adj_high, \
        u_stock_bar_data.beta_adj_low, \
        u_stock_bar_data.beta_adj_close, \
        u_stock_bar_data.beta_adj_vol, \
        u_stock_bar_data.local_open, \
        u_stock_bar_data.local_high, \
        u_stock_bar_data.local_low, \
        u_stock_bar_data.local_close, \
        u_stock_bar_data.local_vol, \
        u_stock_bar_data.local_adj_open, \
        u_stock_bar_data.local_adj_high, \
        u_stock_bar_data.local_adj_low, \
        u_stock_bar_data.local_adj_close, \
        u_stock_bar_data.local_adj_vol, \
        u_stock_bar_data.diff_open, \
        u_stock_bar_data.diff_high, \
        u_stock_bar_data.diff_low, \
        u_stock_bar_data.diff_close, \
        u_stock_bar_data.diff_vol, \
        u_stock_bar_data.diff_adj_open, \
        u_stock_bar_data.diff_adj_high, \
        u_stock_bar_data.diff_adj_low, \
        u_stock_bar_data.diff_adj_close, \
        u_stock_bar_data.diff_adj_vol \
    FROM \
        u_stock_bar_data \
    WHERE \
        u_stock_bar_data.stock_code = '%s' " %(code)

    sqlite_cursor.execute(sql)
    result = sqlite_cursor.fetchall()
    index = 1

    args = {
        'index':index,
        'code':code,
        'result':result
        }
    return render(request, 'stock.html',args)

def index(request):
    # return HttpResponse(u"Server Running ...")
    sqlite_conn= sqlite3.connect(os.path.join(BASE_DIR, 'db.sqlite3'))
    sqlite_cursor = sqlite_conn.cursor()
     
    threshold='> 0.0'
    base_sql = 'SELECT u_stock_bar_data.stock_code, count(u_stock_bar_data.%s) FROM u_stock_bar_data WHERE abs(u_stock_bar_data.%s) %s GROUP BY u_stock_bar_data.stock_code '
    
    sql = base_sql%('diff_open', 'diff_open', threshold)
    sqlite_cursor.execute(sql)
    result_open = sqlite_cursor.fetchall()
    result_open = format_tuple_to_dict(result_open)
    
    sql = base_sql%('diff_high', 'diff_high', threshold)
    sqlite_cursor.execute(sql)
    result_high = sqlite_cursor.fetchall()
    result_high = format_tuple_to_dict(result_high)
    
    sql = base_sql%('diff_low', 'diff_low', threshold)
    sqlite_cursor.execute(sql)
    result_low = sqlite_cursor.fetchall()
    result_low = format_tuple_to_dict(result_low)  ##
        
    sql = base_sql%('diff_close', 'diff_close', threshold)
    sqlite_cursor.execute(sql)
    result_close = sqlite_cursor.fetchall()
    result_close = format_tuple_to_dict(result_close)  ##
    
    sql = base_sql%('diff_vol', 'diff_vol', threshold)
    sqlite_cursor.execute(sql)
    result_vol = sqlite_cursor.fetchall()
    result_vol = format_tuple_to_dict(result_vol)  ##
    
    sql = base_sql%('diff_adj_open', 'diff_adj_open', threshold)
    sqlite_cursor.execute(sql)
    result_adj_open = sqlite_cursor.fetchall()
    result_adj_open = format_tuple_to_dict(result_adj_open)  ##
#     print('result_adj_open  ', result_adj_open)
    
    sql = base_sql%('diff_adj_high', 'diff_adj_high', threshold)
    sqlite_cursor.execute(sql)
    result_adj_high = sqlite_cursor.fetchall()
    result_adj_high = format_tuple_to_dict(result_adj_high)  ##
#     print('result_adj_high  ', result_adj_high)
    
    sql = base_sql%('diff_adj_low', 'diff_adj_low', threshold)
    sqlite_cursor.execute(sql)
    result_adj_low = sqlite_cursor.fetchall()
    result_adj_low = format_tuple_to_dict(result_adj_low)  ##
#     print('result_adj_low  ', result_adj_low)
    
    sql = base_sql%('diff_adj_close', 'diff_adj_close', threshold)
    sqlite_cursor.execute(sql)
    result_adj_close = sqlite_cursor.fetchall()
    result_adj_close = format_tuple_to_dict(result_adj_close)  ##
#     print('result_adj_close  ', result_adj_close)
    
    sql = base_sql%('diff_adj_vol', 'diff_adj_vol', threshold)
    sqlite_cursor.execute(sql)
    result_adj_vol = sqlite_cursor.fetchall()
    result_adj_vol = format_tuple_to_dict(result_adj_vol)  ##
#     print('result_adj_vol  ', result_adj_vol)
    
    sql = 'SELECT DISTINCT u_stock_bar_data.stock_code FROM u_stock_bar_data'
    sqlite_cursor.execute(sql)
    codes = sqlite_cursor.fetchall()
    
    result = []
    i = 1
    for code in codes:
        code = code[0]
        litem = [i]
        i += 1
        litem.append(code)
        
        litem = add_item(code, litem, result_open)
        litem = add_item(code, litem, result_high)
        litem = add_item(code, litem, result_low)
        litem = add_item(code, litem, result_close)
        litem = add_item(code, litem, result_vol)
        litem = add_item(code, litem, result_adj_open)
        litem = add_item(code, litem, result_adj_high)
        litem = add_item(code, litem, result_adj_low)
        litem = add_item(code, litem, result_adj_close)
        litem = add_item(code, litem, result_adj_vol)
        result.append(litem)
    
    return render(request, 'index.html', {'result': result})

def add_item(code, litem, dicto):
    try:
        litem.append(dicto[code])
    except:
        litem.append(0)
    
    return litem
    
def format_tuple_to_dict(list_tuple):
    result = {}
    for t in list_tuple:
        result[t[0]] = t[1]
    return result
    
    