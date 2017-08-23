'''
Created on Aug 22, 2017

@author: Coder_J
'''
import re
import sqlite3
from numpy import int64
from stockbar_10jqka.line.stock_bar_crawler import *
from stockbar_10jqka.line.stock_bar_query import *
from stockbar_beta.beta_bar_query_lib import *
from stockbar_beta.beta_url_lib import *
from resource_urls import *


class diff(object):
    '''    '''
    _stock_symbols = []
    _dbconn = sqlite3.Connection
    _sqlite_cursor = sqlite3.Cursor
    
    def __init__(self):
        '''    '''
        query = beta_bar_query()
        self._stock_symbols = query.query_stock_symbols('6')
        self._dbconn = sqlite3.connect(DB_SQLITE_PATH)
        self._sqlite_cursor = self._dbconn.cursor()

    def __del__(self):
        self._dbconn.close()

    def check_bar(self):
        '''    '''
        for symbol  in self._stock_symbols :
            print('checking   ' + symbol)
            self.compare_bars(symbol)
            
    def compare_bars(self, symbol):
        '''    '''
        try:
            local_bars = stock_bar_query().query(str(symbol),year='2017')
            beta_bars = beta_bar_query().query_stock_bar(symbols=str(symbol), date='last', period='260')[str(symbol)]
            beta_bars = self.filtrate(beta_bars)
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
            print('founded and compare day  ', local_keys[local_index])
            self.compare_bar( stock_code, local_bars, beta_bars, local_keys, beta_keys, local_index, beta_index)
            self.correspond_date( stock_code, local_bars, beta_bars, local_keys, beta_keys, local_index + 1, beta_index + 1)
        elif re.search(local_keys[local_index] , beta_keys[beta_index]) :
            print('Local less a day ', local_keys[local_index] , beta_keys[beta_index])
            self.correspond_date( stock_code, local_bars, beta_bars, local_keys, beta_keys, local_index + 1, beta_index)
        else:
            print('Beta less a day ', local_keys[local_index] , beta_keys[beta_index])
            self.correspond_date( stock_code, local_bars, beta_bars, local_keys, beta_keys, local_index, beta_index + 1)
        
    def compare_bar(self, stock_code, local_bars, beta_bars, local_keys, beta_keys, local_index, beta_index):
        '''    '''
        key = str(local_keys[local_index])
        print('comparing ... ... ', stock_code, ' date ', key)
        
        try:
            db_stock_code = stock_code
            db_date           = key
            db_open           = float( beta_bars[key]['topen'] )          - float( local_bars[key]['open'] )
            db_high            = float( beta_bars[key]['thigh'] )          - float( local_bars[key]['high'] )
            db_low             = float( beta_bars[key]['tlow'] )            - float( local_bars[key]['low'] )
            db_close           = float( beta_bars[key]['tclose'] )         - float( local_bars[key]['close'] )
            db_vol              = int( beta_bars[key]['vol'] )              - int( local_bars[key]['volume'] )
            db_adj_open     = float( beta_bars[key]['adj_topen'] )   - float( local_bars[key]['adj_open'] )
            db_adj_high      = float( beta_bars[key]['adj_thigh'] )   - float( local_bars[key]['adj_high'] )
            db_adj_low       = float( beta_bars[key]['adj_tlow'] )     - float( local_bars[key]['adj_low'] )
            db_adj_close     = float( beta_bars[key]['adj_tclose'] )  - float( local_bars[key]['adj_close'] )
            db_adj_vol        = float( beta_bars[key]['adj_vol'] )     - float( local_bars[key]['adj_volume'] )
        
            sql = 'INSERT INTO "compare_data" ("stock_code", "date", "open", "high", "low", "close", "vol", "adj_open", "adj_high", "adj_low", "adj_close", "adj_vol") VALUES (\'%s\', \'%s\', \'%s\', \'%s\', \'%s\', \'%s\', \'%s\', \'%s\', \'%s\', \'%s\', \'%s\', \'%s\');'
            sql = sql %(db_stock_code, db_date, db_open, db_high, db_low, db_close, db_vol, db_adj_open, db_adj_high, db_adj_low, db_adj_close, db_adj_vol)
            self._sqlite_cursor.execute(sql)
            self._dbconn.commit()
            print('Completed !')
        except:
#             self._dbconn.close()
            print('stock code ', stock_code, ' date ', key, ' has an error occurred while the data was compared.')
        
    def filtrate(self, array):
        '''    '''
        result = {}
        for val in array:
            if  val['tradedate'][0:4] == '2017' :
                result[str(val['tradedate'])] = val
            else:
                pass
        return result
                
def main():
    '''    '''
    d = diff()
    d.check_bar()
    print('Completion of all tasks.')

if __name__ == '__main__':
    main()