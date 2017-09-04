'''
Created on Aug 30, 2017

@author: Coder_J
'''
from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
import sqlite3
import os
from StockBarDiff.settings import BASE_DIR
from .forms import AddForm

rate_range = [
        '0.00',
        '0.0001',
        '0.0002',
        '0.0005',
        '0.001',
        '0.002',
        '0.005',
        '0.01',
        '0.02',
        '0.05',
        '0.10',
        '0.20',
        '0.50',
        '1.00',
        '2.00',
        '5.00',
        '10.0',
        '20.0',
        '50.0'
    ]

rate_title_range = [
        'rate_open',
        'rate_high',
        'rate_low',
        'rate_close',
        'rate_vol',
        'rate_adj_open',
        'rate_adj_high',
        'rate_adj_low',
        'rate_adj_close',
        'rate_adj_vol'
    ]

def stock(request, code):
    '''  All of the information query of individual stocks  '''
    sqlite_conn= sqlite3.connect(os.path.join(BASE_DIR, 'db.sqlite3'))
    sqlite_cursor = sqlite_conn.cursor()
    
    try:
        rate = request.GET['rate']
        if rate not in rate_range:
            rate = 0.0
    except:
        rate = 0.0
    top_rate = rate
    rate = round(float(rate), 4)
        
    price_rate = {}
    for rate_title in rate_title_range:
        try:
            p_rate = request.GET[rate_title]
            if p_rate not in rate_range:
                p_rate = 0.0
        except:
            p_rate = 0.0
        price_rate[rate_title] = p_rate

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
        u_stock_bar_data.local_adj_vol \
    FROM \
        u_stock_bar_data \
    WHERE \
        u_stock_bar_data.stock_code = '%s' " %(code)

    sqlite_cursor.execute(sql)
    result = sqlite_cursor.fetchall()
    
    result = calc_rate(result)
    
#     result = 
    calc_view_bit(result, price_rate)

    args = {
        'code':code,
        'rate':rate,
        'top_rate':top_rate,
        'rate_range':rate_range,
        'rate_title_range':rate_title_range,
        'price_rate':price_rate,
        'result':result
        }
    return render(request, 'stock.html',args)

def calc_view_bit(original_value, price_rate):
    start = 22
    offset = 10
    result = []
    
    price_rate = price_rate.values()
    price_rate = list(price_rate)

    for date in original_value:
        view_flag = 1
        for step in range(offset):
            table_rate = round(float(date[start + step][1]), 4)
            select_rate = round(float(price_rate[step]), 4)
            
            if table_rate < select_rate :
                view_flag = 0
                break
        date.append(view_flag)
#         if date[32] == 1 :
#             print(date[1], 'view=', date[32])
#             print('date  ', date)
    result.append(date)

    return result
            

def calc_rate(original_value):
    start = 2
    offset = 10
    result = []
    
    for date in original_value:
        for step in range(10):
            date = list(date)
            diff_price = float(date[start + step]) - float(date[start + step + offset])
            diff_price = round( abs( diff_price), 4)
            rate = 0.0
            if diff_price != 0:
                rate = diff_price / float(date[start + step])
                rate = rate * 100
                rate = round(abs(rate), 4)
            date.append([diff_price, rate])
            
#             if rate > 5000:
#                 print(float(date[start + step]), " - ", float(date[start + step + offset]), " = ", diff_price)
            
        result.append(date)
    return result
