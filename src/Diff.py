'''
Created on Aug 22, 2017

@author: Coder_J
'''
import re
import sqlite3
from numpy import int64
import threading
from time import ctime,sleep
from stockbar_10jqka.line.stock_bar_crawler import *
from stockbar_10jqka.line.stock_bar_query import *
from stockbar_beta.beta_bar_query_lib import *
from stockbar_beta.beta_url_lib import *
from resource_urls import *
from blaze.tests.test_sql import sql


class diff(object):
    '''    '''
    _stock_symbols = []
    _dbconn = sqlite3.Connection
    _sqlite_cursor = sqlite3.Cursor
    
    def __init__(self):
        '''    '''
        query = beta_bar_query()
        self._stock_symbols = query.query_stock_symbols()
        self._dbconn = sqlite3.connect(DB_SQLITE_PATH)
        self._sqlite_cursor = self._dbconn.cursor()

    def __del__(self):
        '''    '''
        self._dbconn.close()

    def check_bar(self, flag_month):
        '''    '''
        for symbol  in self._stock_symbols :
            print('checking   ' + symbol)
            self.compare_bars(symbol, flag_month)
            
    def compare_bars(self, symbol, flag_month):
        '''    '''
        try:
            local_bars = stock_bar_query().query(str(symbol),year='2017')
            beta_bars = beta_bar_query().query_stock_bar(symbols=str(symbol), date='last', period='260')[str(symbol)]
            beta_bars = self.filtrate(beta_bars, flag_month)
        except KeyError:
            print(symbol, " has KeyError exception")
            return
        
        del local_bars['stock_code']
        local_keys = tuple(local_bars.keys())
        beta_keys = tuple(beta_bars.keys())
        local_index = 0
        beta_index = 0
        self.correspond_date(symbol,local_bars, beta_bars, local_keys, beta_keys, local_index, beta_index)
        
    def correspond_date(self, stock_code, local_bars, beta_bars, local_keys, beta_keys, local_index, beta_index):
        '''  correspond date, then compare  '''
        if  local_index >= len(local_keys) or beta_index >= len(beta_keys):
            return
        
        if local_keys[local_index] == beta_keys[beta_index]:
#             print('founded and compare day  ', local_keys[local_index])
            self.compare_bar( stock_code, local_bars, beta_bars, local_keys, beta_keys, local_index, beta_index)
            self.correspond_date( stock_code, local_bars, beta_bars, local_keys, beta_keys, local_index + 1, beta_index + 1)
        elif re.search(local_keys[local_index] , beta_keys[beta_index]) :
            print('Beta less a day ', local_keys[local_index] , beta_keys[beta_index])
            self.correspond_date( stock_code, local_bars, beta_bars, local_keys, beta_keys, local_index + 1, beta_index)
        else:
            print('Local less a day ', local_keys[local_index] , beta_keys[beta_index])
            self.correspond_date( stock_code, local_bars, beta_bars, local_keys, beta_keys, local_index, beta_index + 1)
        
    def compare_bar(self, stock_code, local_bars, beta_bars, local_keys, beta_keys, local_index, beta_index):
        '''    '''
        key = str(local_keys[local_index])
        print('comparing ... ... ', stock_code, ' date ', key)
        
        try:
            db_stock_code = stock_code
            db_date           = key
            diff_open           = round( float( beta_bars[key]['open'] )          - float( local_bars[key]['open'] ) ,4)
            diff_high            = round( float( beta_bars[key]['high'] )          - float( local_bars[key]['high'] )  ,4)
            diff_low             = round( float( beta_bars[key]['low'] )            - float( local_bars[key]['low'] )    ,4)
            diff_close           = round( float( beta_bars[key]['close'] )         - float( local_bars[key]['close'] ) ,4)
            diff_vol              = round( int( beta_bars[key]['volume'] )              - int( local_bars[key]['volume'] )      ,4)
            diff_adj_open     = round( float( beta_bars[key]['adj_open'] )   - float( local_bars[key]['adj_open'] )    ,4)
            diff_adj_high      = round( float( beta_bars[key]['adj_high'] )   - float( local_bars[key]['adj_high'] )     ,4)
            diff_adj_low       = round( float( beta_bars[key]['adj_low'] )     - float( local_bars[key]['adj_low'] )      ,4)
            diff_adj_close     = round( float( beta_bars[key]['adj_close'] )  - float( local_bars[key]['adj_close'] )   ,4)
            diff_adj_vol        = round( float( beta_bars[key]['adj_volume'] )     - float( local_bars[key]['adj_volume'] )   ,4)
        
            sql = 'INSERT INTO "u_stock_bar_data" ("stock_code", "date", "beta_open", "beta_high", "beta_low", '\
            '"beta_close", "beta_vol", "beta_adj_open", "beta_adj_high", "beta_adj_low", "beta_adj_close", "beta_adj_vol", '\
            '"local_open", "local_high", "local_low", "local_close", "local_vol", "local_adj_open", "local_adj_high", "local_adj_low", '\
            '"local_adj_close", "local_adj_vol", "diff_open", "diff_high", "diff_low", "diff_close", "diff_vol", "diff_adj_open", '\
            '"diff_adj_high", "diff_adj_low", "diff_adj_close", "diff_adj_vol") VALUES (\'%s\', \'%s\', \'%s\', \'%s\', \'%s\', '\
            '\'%s\', \'%s\', \'%s\', \'%s\', \'%s\', \'%s\', \'%s\', \'%s\', \'%s\', \'%s\', \'%s\', \'%s\', \'%s\', \'%s\', '\
            '\'%s\', \'%s\', \'%s\', \'%s\', \'%s\', \'%s\', \'%s\', \'%s\', \'%s\', \'%s\', \'%s\', \'%s\', \'%s\');'
    
            sql = sql %(db_stock_code, db_date, \
                        beta_bars[key]['open'] , beta_bars[key]['high'] , beta_bars[key]['low'] , beta_bars[key]['close'] , beta_bars[key]['volume'], \
                        beta_bars[key]['adj_open'] , beta_bars[key]['adj_high'] , beta_bars[key]['adj_low'] , beta_bars[key]['adj_close'] , beta_bars[key]['adj_volume'], \
                        local_bars[key]['open'] , local_bars[key]['high'] , local_bars[key]['low'] , local_bars[key]['close'] , local_bars[key]['volume'], \
                        local_bars[key]['adj_open'] , local_bars[key]['adj_high'] , local_bars[key]['adj_low'] , local_bars[key]['adj_close'] , local_bars[key]['adj_volume'], \
                        diff_open, diff_high, diff_low, diff_close, diff_vol, \
                        diff_adj_open, diff_adj_high, diff_adj_low, diff_adj_close, diff_adj_vol )
    
            self._sqlite_cursor.execute(sql)
            self._dbconn.commit()
        except : # sqlite3.OperationalError:
#                 print('sqlite3.OperationalError: database is locked')
            print('stock code ', stock_code, ' date ', key, ' has an error occurred while the data was compared.')
        
    def filtrate(self, array, flag):
        '''    '''
        result = {}
        for val in array:
            val['date'] = val['date'].replace('-','')
            if  val['date'][0:4] == '2017' :
                result[str(val['date'])] = val
            else:
                pass
        return result
                
def main():
    '''    '''
    threads = []
#     t1 = threading.Thread(target=diff('201701'))
#     threads.append(t1)
#     t2 = threading.Thread(target=diff('201702'))
#     threads.append(t2)
    d = diff()
    t1 = threading.Thread(target=d.check_bar('201701'))
    threads.append(t1)
#     t2 = threading.Thread(target=d.check_bar('201702'))
#     threads.append(t2)
#     t3 = threading.Thread(target=d.check_bar('201703'))
#     threads.append(t3)
#     t1 = threading.Thread(target=d.check_bar('201704'))
#     threads.append(t1)
#     t1 = threading.Thread(target=d.check_bar('201705'))
#     threads.append(t1)
#     t1 = threading.Thread(target=d.check_bar('201706'))
#     threads.append(t1)
#     t1 = threading.Thread(target=d.check_bar('201707'))
#     threads.append(t1)
#     t1 = threading.Thread(target=d.check_bar('201708'))
#     threads.append(t1)
#     t1 = threading.Thread(target=d.check_bar('201709'))
#     threads.append(t1)
#     t1 = threading.Thread(target=d.check_bar('201710'))
#     threads.append(t1)
#     t1 = threading.Thread(target=d.check_bar('201711'))
#     threads.append(t1)
#     t1 = threading.Thread(target=d.check_bar('201712'))
#     threads.append(t1)
#     t1 = threading.Thread(target=d.check_bar('201701'))
#     threads.append(t1)
    
    for thr in threads:
        thr.setDaemon(True)
        thr.start()
    
    print('Completion of all tasks.')

if __name__ == '__main__':
    main()
