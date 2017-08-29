#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: zhongliang.jiang
# @Date:   2017-08-16 14:57:39
# @Last Modified time: 2017-08-17 23:34:49
import requests
import json
import os
from resource_urls import DATA_LINE_URL, WEB_URL

class stock_bar_crawler(object):
    """
        stock bar information crawler
    """

    # stock year
    _year = 'last'
    # local file save path
    _save_data_path = DATA_LINE_URL
    # flag stock code
    _stock_code = '600000'

    def __init__(self):
        pass

    def craw_stocks(self, stock_symbol_file_name, year='last'):
        """
            start crawling the data. Storage mode, the front of the right data (adj data).
        :arg year: stock year egg: '2017' ; 'last'
        :arg stock_symbol_file_name
            stock symbol file
        """
        self._year = year
        file_path = self._save_data_path + '\\' + self._year
        print(file_path)
        if not os.path.exists(file_path):
            os.makedirs(file_path)

#         for line in open(stock_symbol_file_name):
#             line = line.strip("\n")
#             line = line.split(':')
#             id_str = str(line[1])
        file = open(stock_symbol_file_name, 'r')
        id_str = json.load(file)['data']['symbols']
        print(id_str)
        
        for id_str in id_str:
            print('climbing stock number : ' + id_str + ', year : ' + self._year)
            self.craw(id_str)

        print('Crawl data completion!')

    def craw(self, stock_id):
        """
            crawl individual stock
        :type stock_id
            stock number
        """

        url_00 = WEB_URL % (stock_id, '00', self._year)
        url_01 = WEB_URL % (stock_id, '01', self._year)
        
        index = 0
        while True:
            r_00 = requests.get(url_00)
            r_01 = requests.get(url_01)
            if r_00.status_code == 200 and r_01.status_code == 200:
                break
            if index >= 5:
                print(stock_id, ' not found !!!')
                break
            index += 1

        if r_00.status_code == 200 and r_01.status_code == 200:
            index_00 = r_00.text.find("(");
            index_01 = r_01.text.find("(");

            if index_00 > 0 and index_01 > 0:
                web_data_00 = r_00.text[index_00 + 1:-1]
                web_data_01 = r_01.text[index_01 + 1:-1]

                web_data_json_00 = json.loads(web_data_00)
                web_data_json_01 = json.loads(web_data_01)

                self.save_to_file(stock_id, str(web_data_json_00['data']).split(';'),
                                  str(web_data_json_01['data']).split(';'))
            else:
                print('The vlid data location of th returned result is not found!')
        else:
            print('There is an exception to the page response!')

    def save_to_file(self, t_id, t_stock_data_00, t_stock_data_01):
        """
        Save th data sheet file.
        """
        length = len(t_stock_data_00)

        if len(t_stock_data_00) == len(t_stock_data_01) and length > 5:
            contents = []
            for data_row_00, data_row_01 in zip(t_stock_data_00, t_stock_data_01):
                data_row_arr_00 = data_row_00.split(',')
                data_row_arr_01 = data_row_01.split(',')

                data_row = self.assembly_data(t_id, data_row_arr_00, data_row_arr_01)

                contents.append(data_row)

            contents = "\n".join(contents)

            file_name = self._save_data_path + '\\' + self._year + '/%s.txt' % (t_id)
            file_object = open(file_name, 'w+')
            try:
                file_object.write(contents)
                file_object.flush()
            finally:
                """"""
                file_object.close()


        else:
            """
            Output exception message
            """
            print("An exception to the array length.")
            print(t_stock_data_00)
            print(t_stock_data_01)

    def assembly_data(self, t_id, t_data_row_arr_00, t_data_row_arr_01):
        """
        assembly row data
        :arg t_id
            stock number
        :arg t_data_row_arr_00
            data that no longer has power
        :arg t_data_row_arr_01
            the data of the previout powers
        :return:
            data
        """

        space_mark = ','

        save_data_str = \
            str(t_id) + space_mark + \
            str(t_data_row_arr_01[0]) + space_mark + \
            str(t_data_row_arr_01[1]) + space_mark + \
            str(t_data_row_arr_01[2]) + space_mark + \
            str(t_data_row_arr_01[3]) + space_mark + \
            str(t_data_row_arr_01[4]) + space_mark + \
            str(t_data_row_arr_01[5]) + space_mark + \
            str(t_data_row_arr_00[1]) + space_mark + \
            str(t_data_row_arr_00[2]) + space_mark + \
            str(t_data_row_arr_00[3]) + space_mark + \
            str(t_data_row_arr_00[4]) + space_mark + \
            str(t_data_row_arr_00[5])
        return save_data_str

