'''
Created on Aug 22, 2017

@author: Coder_J
'''
import requests
import json
from stockbar_beta.beta_url_lib import beta_url

class beta_bar_query(object):
    '''    '''
    _symbols = []

    def __init__(self):
        '''    '''
        pass
        
    def query_stock_symbols(self):
        '''    '''
        url = beta_url().get_symbol_url() 
        print(url)
        requests_symbols = requests.get(url, verify=False) 

        if  requests_symbols.status_code == 200:
            self._symbols = json.loads(requests_symbols.text)['data']['symbols']
            return self._symbols
        else:
            return []
        
    def query_stock_bar(self, symbols, date, period='1'):
        '''    '''
        url = beta_url(symbols=symbols, endtime=date, period=period).get_price_url()       
        requests_symbols = requests.get(url, verify=False) 
        
        if  requests_symbols.status_code == 200:
            return json.loads(requests_symbols.text)['data']['prices']
        else:
            return []
        
        
        
        
        