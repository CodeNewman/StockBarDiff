'''
Created on Sep 1, 2017

@author: Coder_J
'''

class jurl(object):
    '''
    classdocs
    '''
    _base_url = 'http://d.10jqka.com.cn/v2/'
    '''
    http://d.10jqka.com.cn/v2/line/hs_600000/01/2017.js
    '''
    
    def get(self, type, area, code, flag, year):  # @ReservedAssignment
        return self._base_url + type + '/' \
            + area + '_' + code + '/' + flag + '/' + year + '.js'
