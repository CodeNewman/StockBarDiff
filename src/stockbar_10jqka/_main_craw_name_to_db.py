'''
Created on Sep 1, 2017

@author: Coder_J
'''
from sql_helper.mysql_helper_lib import mysql_helper
from stockbar_10jqka.url_lib import jurl
from stockbar_10jqka.crawl import crawl
from tools.code_tool import code_tool
import multiprocessing

db = mysql_helper()
jurl = jurl()
crawl = crawl()
tool = code_tool()

def craw_name_hs(codes):
    '''
    http://d.10jqka.com.cn/v2/line/hs_600000/01/last.js
    '''
    type = 'line'  # @ReservedAssignment
    area = 'hs'
    flag = '00'
    year = 'last'
    
    for code in codes:    
        print('--------------------doing--------------------\t', code,)
        craw_10jqka(type, area, code, flag, year)

def craw_name_usa(codes):
    '''
    http://d.10jqka.com.cn/v2/line/usa_AAPL/01/last.js
    '''
    type = 'line'  # @ReservedAssignment
    area = 'usa'
    flag = '00'
    year = 'last'
    
    for code in codes:    
        print('--------------------doing--------------------\t', code,)
        craw_10jqka(type, area, code, flag, year)

def craw_10jqka(type, area, code, flag, year):  # @ReservedAssignment
    sql = 'UPDATE `stocks`.`code` SET `name`=%s, `rt`=%s, `start`=%s, `year`=%s WHERE (`code`=%s);' # 
    url = jurl.get(type, area, code, flag, year)
    data = crawl.craw_json(url)
    
    if len(data) == 0:
        return
    
    name = data['name'] # .decode("gbk").encode("utf-8")
    years = str(data['year']).encode(encoding='utf_8', errors='strict')
    
    element = (
        name,
        data['rt'],
        data['start'],
        years,
        code
        )
        
    tool.update_value_to_db(sql, element, code)

def worker_usa(codes, name):
    craw_name_usa(codes)
    print('\t\t\t\t\t', name, ' is completed !-------------------------------------------------!')

def worker_hs(codes, name):
    craw_name_hs(codes)
    print('\t\t\t\t\t', name, ' is completed !-------------------------------------------------!')

def main():
    codes_usa = tool.get_codes("usa")
    codes_hs = tool.get_codes("hs")
    
    for x in [chr(i) for i in range(65,91)]:
        p = multiprocessing.Process(target = worker_usa, args = (tool.filt_codes(codes_usa, x), x, ))
        p.start()
    
    hs_work_names = [
        '000',
        '002',
        '300',
        '600',
        '601',
        '603'
        ]
    
    for x in hs_work_names:
        p = multiprocessing.Process(target = worker_hs, args = (tool.filt_codes(codes_hs, x), x, ))
        p.start()

if __name__ == '__main__':
    main()