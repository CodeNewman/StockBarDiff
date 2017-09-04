'''
Created on Sep 1, 2017

@author: Coder_J
'''
from sql_helper.mysql_helper_lib import mysql_helper
import pymysql
import sys

db = mysql_helper()

class code_tool(object):
    '''
    classdocs
    '''
    
    def get_codes(self, area):
        codes = []
        sql = 'SELECT `code` FROM `code` WHERE `code`.type = %s ;'
        try:
            codes = db.fetchall_one_column(sql, (area), column='code')
        except:
            print("There was an error in the query the stock code!" )
        return codes

    def filt_codes(self, codes, start):
        result = []
        for code in codes:
            if str(code).startswith(start):
                result.append(code)
        
        return result
    
    def insert_value_to_db(self, sql, element, code):
        self.update_value_to_db(sql, element, code)
    
    def update_value_to_db(self, sql, element, code):
        try:
            db.update(sql, element)
#             print('code \t', code, '\t :Updated')
            
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
        except ValueError as err:
            print('code \t', code, '\t\t :ValueError')
            print(repr(err))
            print(element)
            pass
        except TypeError as err:
            print('code \t', code, '\t\t :TypeError')
            print(repr(err))
            print(element)
            pass
        except:
            print('\t\t', code, '\t\t :OtherError')
            print(sys.exc_info()[0])
            print(element)
            pass
        