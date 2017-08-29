'''
Created on Aug 22, 2017

@author: Coder_J
'''

class beta_url(object):
    '''
    classdocs
    '''
    _base_url = 'http://121.43.168.179:8087/quote/'
    _symbols_url =  _base_url + 'symbols'
    _symbol_type = '6'
    
    _price_daily = _base_url + 'prices/daily'
    _symbols = '600000'
    _period = '1'
    _endTime = 'last'
#     _adjustd = '1'
    
    _token = '6fab4b8e8bd63ccd37d1a5130a32659e'

    def __init__(self, symbols='600000', endtime='last', period='1'):
        self._symbols = symbols
        self._endTime = endtime
        self._period = period
    
    def get_symbol_url(self, symbol_type = '6'):
        return 'http://121.43.168.179:8087/quote/symbols/nyseandnasdaq'
    
    def get_price_url(self):
        return self._price_daily + '?&symbols=' + self._symbols + '&period=' + self._period
