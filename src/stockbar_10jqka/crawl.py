'''
Created on Sep 1, 2017

@author: Coder_J
'''
import requests
import json
from requests.models import Response

class crawl(object):
    '''
    classdocs
    '''

    def craw_string(self, url):
        result = ''
        r= Response() 
        try:
            r = requests.get(url)
        except:
            pass

        index = 0
        while r.status_code != 200:
            try:
                r = requests.get(url)
            except:
                pass
                
            if index >= 5:
                break
            index += 1
            
        if r.status_code == 200:
            result = str(r.text)
            
        return result
            
    def craw_json(self, url):
        result = ''
        text = self.craw_string(url)
        
        index = text.find("(");
        title = text[0:index]
        text = text[index + 1:-1]
        if len(text) != 0:
            json_value = json.loads(text)
            json_value['title'] = title
            result = json_value
        
        return result
    
    def craw_data(self, url):
        data = []
        try:
            for d in str(self.craw_json(url)['data']).split(';'):
                data.append(d)
        except:
            pass
        return data
    
            