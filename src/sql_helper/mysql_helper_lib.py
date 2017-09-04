'''
Created on Aug 31, 2017

@author: Coder_J
'''
import pymysql.cursors

class mysql_helper(object):
    '''
    classdocs
    '''
    # Connect to the database
    connection = pymysql.connect(host='192.168.75.133',
                                 user='root',
                                 password='abc123',
                                 db='stocks',
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
        
    def execute(self, sql, element):
        ''''    '''
        try:            
            with self.connection.cursor() as cursor:
                cursor.execute(sql, element)
            self.connection.commit()
        finally:
            pass
        
    def insert(self, sql, element):
        ''''    '''
        self.execute(sql, element)
        
    def update(self, sql, element):
        ''''    '''
        self.execute(sql, element)

    def fetchall(self,  sql, element):
        '''    '''
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(sql, element)
                result = cursor.fetchall()
                return(result)
        finally:
            pass

    def fetchall_one_column(self,  sql, element, column):
        '''    '''
        try:
            result = []
            with self.connection.cursor() as cursor:
                cursor.execute(sql, element)
                all = cursor.fetchall()  # @ReservedAssignment
                for item in all:
                    result.append(item[column])
                return(result)
        finally:
            pass

    def close(self):
        self.connection.close()


