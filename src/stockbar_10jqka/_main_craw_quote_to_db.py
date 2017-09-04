'''
Created on Aug 31, 2017

@author: Coder_J
'''
from sql_helper.mysql_helper_lib import mysql_helper as db
from stockbar_10jqka.url_lib import jurl
from stockbar_10jqka.crawl import crawl
import multiprocessing
import pymysql
import sys

db = db()
jurl = jurl()
crawl = crawl()

def craw_quote_hs_2017(codes):
    '''
    http://d.10jqka.com.cn/v2/line/hs_600000/01/last.js
    '''
    type = 'line'  # @ReservedAssignment
    area = 'hs'
    flag = '01'
    year = '2017'
    db_name = '10jqka_hs_01_bar'
    
    for code in codes:    
        print('--------------------doing--------------------\t', code,)
        craw_10jqka(type, area, code, flag, year, db_name)

def craw_quote_usa_2017(codes):
    '''
    http://d.10jqka.com.cn/v2/line/usa_AAPL/01/last.js
    '''
    type = 'line'  # @ReservedAssignment
    area = 'usa'
    flag = '01'
    year = '2017'
    db_name = '10jqka_usa_01_bar'
    
    for code in codes:    
        print('--------------------doing--------------------\t', code,)
        craw_10jqka(type, area, code, flag, year, db_name)

def craw_10jqka(type, area, code, flag, year, db_name):  # @ReservedAssignment
    
    sql = 'INSERT INTO `%s` (`code`, `date`, `type`, `open`, `high`, `low`, `close`, `vol`, `val_01`, `val_02`) VALUES (##, ##, ##, ##, ##, ##, ##, ##, ##, ##);' % (db_name)
    sql = sql.replace('##', '%s')
    
    url = jurl.get(type, area, code, flag, year)
    datas = crawl.craw_data(url)
    
    if datas == []:
        return
    
    for row in datas:
        row = str(row).split(',')
        date = row[0]
        date = date[0:4] + '-' + date[4:6] + '-' + date[6:8]
        
        element = (
            code,
            date,
            flag,
            row[1],
            row[2],
            row[3],
            row[4],
            row[5],
            row[6],
            row[7],
            )
        
        insert_value_to_db(sql, element, code)

def insert_value_to_db(sql, element, code):
    try:
        db.insert(sql, element)
        print('code \t', code, '\t :Inserted')
        
    except pymysql.err.IntegrityError:
        print('code \t', code, '\t', code, '\t :already has')
        pass
    except pymysql.err.ProgrammingError as err:
        print('code \t', code, '\t', code, '\t :ProgrammingError')
        print(repr(err))
        print(element)
        pass
    except pymysql.err.InternalError as err:
        print('code \t', code, '\t\t :InternalError')
        print(repr(err))
        print(element)
        pass
    except KeyError:
        print('code \t', code, '\t\t :KeyError')
        print(element)
        pass
    except TimeoutError as err:
        print('code \t', code, '\t\t :TimeoutError')
        print(repr(err))
        print(element)
        pass
    except pymysql.err.DataError as err:
        print('code \t', code, '\t\t :pymysql.err.DataError')
        print(repr(err))
        print(element)
        pass
    except:
        print('\t\t', code, '\t\t :OtherError')
        print(sys.exc_info()[0])
        print(element)
        pass

def get_codes(area):
    codes = []
    sql = 'SELECT `code` FROM `code` WHERE `code`.type = %s ;'
    try:
        codes = db.fetchall_one_column(sql, (area), column='code')
    except:
        print("There was an error in the query the stock code!" )
    return codes

def filt_codes(codes, start):
    result = []
    for code in codes:
        if str(code).startswith(start):
            result.append(code)
    
    return result

def worker_usa(codes, name):
    craw_quote_usa_2017(codes)
    print('\t\t\t\t\t', name, ' is completed !-------------------------------------------------!')

def worker_hs(codes, name):
    craw_quote_hs_2017(codes)
    print('\t\t\t\t\t', name, ' is completed !-------------------------------------------------!')

def main():
    codes_usa = get_codes("usa")
    codes_hs = get_codes("hs")
    
    for x in [chr(i) for i in range(65,91)]:
        p = multiprocessing.Process(target = worker_usa, args = (filt_codes(codes_usa, x), x, ))
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
        p = multiprocessing.Process(target = worker_hs, args = (filt_codes(codes_hs, x), x, ))
        p.start()

if __name__ == '__main__':
    main()