#!/usr/bin/env python
# -*- coding:utf-8 -*- 
#@Time :2018/6/6 21:30
#!@Author ： gyfeather
#!@File :.py

# -*- coding:utf-8 -*-
import sys
if '..' not in sys.path:
    sys.path.append('..')
from dbBase import DB_BASE

from sqlalchemy import Column, Integer, String, Float
from sqlalchemy import Table
import os
import pandas as pd

trans = lambda x: x.encode('utf8') if isinstance(x, unicode) else x


def mapping_df_types(df):
    dtypedict = {}
    for i, j in zip(df.columns, df.dtypes):
        if i == u'账户':
            # dtypedict.update({i: NVARCHAR(length=32)})
            pass
    #         if "object" in str(j):
    #             dtypedict.update({i: NVARCHAR(length=255)})
    #         if "float" in str(j):
    #             dtypedict.update({i: Float(precision=2, asdecimal=True)})
    #         if "int" in str(j):
    #             dtypedict.update({i: Integer()})
    return dtypedict


class CiticBank(DB_BASE):

    def __init__(self, db_name='check', table_name=None):  # db_name=指定数据库
        super(CiticBank, self).__init__(db_name)
        self.table_struct = None
        self.col_sizes = []

    def create_table(self):
        if self.table_struct is not None:
            self.table_struct = self.quick_map(self.table_struct)

    def check_table_exist(self):
        if self.table_struct is not None:
            return self.table_struct.exists()
        else:
            raise Exception("no table specified")

    def get_row_counts(self):
        session = self.get_session()
        n = session.query(self.table_struct).count()
        session.close()
        return n

    def get_col_names(self):
        return [trans(i) for i in self.get_column_names(self.table_struct)]

    def get_col_length(self):
        return len(self.get_column_names(self.table_struct))

    def get_col_sizes(self):
        return self.col_sizes


def import_core(infile, table_name, encoding='utf8', if_exists='append', multi_sheet=None):  # 导入文件的封装函数
    if infile.endswith('.csv') or infile.endswith('.txt') or infile.endswith('.CSV'):
        df = pd.read_csv(infile, encoding=encoding, index_col=None)
    else:
        if not multi_sheet:
            df = pd.read_excel(infile, encoding=encoding, index_col=None)
        else:
            dfs = pd.read_excel(infile, encoding=encoding, index_col=None, sheetname=multi_sheet)
            df = pd.concat(dfs.values())
    # print df.head()
    df.columns = [i.strip() for i in df.columns]
    # print df.columns
    db_obj = CiticBank()
    dtypedict = mapping_df_types(df)  # 改变TEXT为VARCHAR类型
    df.to_sql(table_name, db_obj.engine, chunksize=10240, if_exists=if_exists, dtype=dtypedict)
    # print 'finished'