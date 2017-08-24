#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: zhongliang.jiang
# @Date:   2017-08-17 10:04:09
# @Last Modified time: 2017-08-17 10:31:52
from resource_urls import DATA_LINE_URL

class stock_bar_query(object):
    """
        stock bar information query
    """
    _stock_code = ''
    _save_flie_path = DATA_LINE_URL

    def __init__(self):
        pass

    # 提供一个查询的方式，给你一个symbol，快速的查询数据
    def query(self, stock_code, year=None, date=None):
        """
            query stock bar data
        :arg stock_code
            stock number , six bit. egg: 600000
        :arg year
            stock year egg: 2017
        :arg date
            stock date egg: xxxx-xx-xx 2017-01-01
        :return
            stock bar data, a data dictionary
        """
        if  year is None:
            self._year = str(date)[0:4]
        else:
            self._year = year

            
        self._stock_code = stock_code
        self._save_flie_path = self._save_flie_path + '\\'  + str(self._year)  + '\\'

        stock_data = self.init_stock_data()
        if date is None:
            return stock_data
        else:
            return stock_data[str(date)]

    def init_stock_data(self):
        """
            open file and init stock data
        """
        stock_data = {}
        stock_data['stock_code'] = self._stock_code
        stock_symbol_file_name = self._save_flie_path + '%s.txt' % (str(self._stock_code))
        try:
            for line in open(stock_symbol_file_name):
                line = line.strip("\n")
                line = line.split(',')
                quary_data = self.assembly_quary_data(line)
                stock_data[str(line[1])] = quary_data
        finally:
            return stock_data
        

    def assembly_quary_data(self, t_line):
        """"""
        result = {}

        result["adj_open"] = t_line[2]
        result["adj_high"] = t_line[3]
        result["adj_low"] = t_line[4]
        result["adj_close"] = t_line[5]
        result["adj_volume"] = t_line[6]

        result["open"] = t_line[7]
        result["high"] = t_line[8]
        result["low"] = t_line[9]
        result["close"] = t_line[10]
        result["volume"] = t_line[11]

        return result
