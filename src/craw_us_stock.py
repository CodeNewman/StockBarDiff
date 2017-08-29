'''
Created on Aug 29, 2017

@author: Coder_J
'''
from stockbar_10jqka.line.stock_bar_crawler import *
from stockbar_10jqka.line.stock_bar_query import *
from stockbar_beta.beta_bar_query_lib import *
from stockbar_beta.beta_url_lib import *
from resource_urls import *
import sqlite3

crawler = stock_bar_crawler()
crawler.craw_stocks(STOCK_SYMBOL_FILE)