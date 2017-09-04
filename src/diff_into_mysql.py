'''
Created on Aug 22, 2017

@author: Coder_J
'''

from sql_helper.mysql_helper_lib import mysql_helper
from tools.code_tool import code_tool
import multiprocessing

db = mysql_helper()
tool = code_tool()

class diff(object):
    '''    '''
    
    def diff_usa(self, codes):
        '''    '''
        db_table_original = 'view_usa_all_bar'
        db_table_result = 'diff_usa_bar'
        
        for code in codes:    
            print('--------------------doing--------------------\t', code,)
            self.diff_queto(code, db_table_original, db_table_result)
    
    def diff_hs(self, codes):
        '''    '''
        db_table_original = 'view_hs_all_bar'
        db_table_result = 'diff_hs_bar'
        
        for code in codes:    
            print('--------------------doing--------------------\t', code,)
            self.diff_queto(code, db_table_original, db_table_result)
    
    def diff_queto(self, code, original, result):
        '''    '''
        sql = 'SELECT `code`, date, qu_open, qu_high, qu_low, qu_close, qu_vol, qu_adj_open, qu_adj_high, qu_adj_low, qu_adj_close, qu_adj_vol, \
            jq_open, jq_high, jq_low, jq_close, jq_vol, jq_adj_open, jq_adj_high, jq_adj_low, jq_adj_close, jq_adj_vol FROM ' + original + ' \
            WHERE  `code` = %s ;'
        
        data_all = db.fetchall(sql, (code,))
        
        for row_data in data_all:
            self.diff_one_row(row_data, result)
            
    def diff_one_row(self, data, result_loc):
        sql = 'INSERT INTO ' + result_loc + ' VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);'
#         print('data  ', data)
        try:
            db_code            = data['code']
#             print(db_code)
            db_date             = str(data['date'])
#             print(db_date)
            diff_open           = round( abs(float( data['qu_open'] )          - float( data['jq_open'] )           ) ,4)
#             print('diff_open', diff_open)
            diff_high            = round( abs(float( data['qu_high'] )          - float( data['jq_high'] )            ) ,4)
#             print('diff_high', diff_high)
            diff_low             = round( abs(float( data['qu_low'] )            - float( data['jq_low'] )             ) ,4)
#             print('diff_low', diff_low)
            diff_close           = round( abs(float( data['qu_close'] )         - float( data['jq_close'] )          ) ,4)
#             print('diff_close', diff_close)
            diff_vol              = round( abs(int( data['qu_vol'] )               - int( data['jq_vol'] )                 ) ,4)
#             print('diff_vol', diff_vol)
            diff_adj_open     = round( abs(float( data['qu_adj_open'] )   - float( data['jq_adj_open'] )    ) ,4)
#             print('diff_adj_open', diff_adj_open)
            diff_adj_high      = round( abs(float( data['qu_adj_high'] )   - float( data['jq_adj_high'] )     ) ,4)
#             print('diff_adj_high', diff_adj_high)
            diff_adj_low       = round( abs(float( data['qu_adj_low'] )     - float( data['jq_adj_low'] )      ) ,4)
#             print('diff_adj_low', diff_adj_low)
            diff_adj_close     = round( abs(float( data['qu_adj_close'] )  - float( data['jq_adj_close'] )   ) ,4)
#             print('diff_adj_close', diff_adj_close)
            diff_adj_vol        = round( abs(float( data['qu_adj_vol'] )     - float( data['jq_adj_vol'] )       ) ,4)
#             print('diff_adj_vol', diff_adj_vol)
         
            element = (
                db_code, db_date, 
                diff_open, diff_high, diff_low, diff_close, diff_vol, 
                diff_adj_open, diff_adj_high, diff_adj_low, diff_adj_close, diff_adj_vol
                )
            
#             print('element  ', element)
     
            tool.update_value_to_db(sql, element, db_code)
        except : 
            pass
        
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

differ = diff()

def worker_usa(codes, name):
    differ.diff_usa(codes)
    print('\t\t\t\t\t', name, ' is completed !-------------------------------------------------!')

def worker_hs(codes, name):
    differ.diff_hs(codes)
    print('\t\t\t\t\t', name, ' is completed !-------------------------------------------------!')

def main():
    '''    '''
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
    
    print('Started all tasks.')

def test():
    worker_usa('AAPC', 'AAPC')

if __name__ == '__main__':
    main()
#     test()
