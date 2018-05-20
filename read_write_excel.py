#!/usr/bin/env python
# -*- coding:utf-8 -*- 
#@Time :2018/5/11 22:34
#!@Author ： gyfeather
#!@File :.py

import pandas as pd
from db_table import CiticBank
import sys

def read_write_excel:

    if sys.getdefaultencoding() != 'utf-8':
        reload(sys)
        sys.setdefaultencoding('utf-8')
    infile = r"C:/Users/gyfea/Desktop/test1.xlsx"
    df = pd.read_excel(infile,header = None)
    dbapi = CiticBank()
    count1=0

    for index,row in df.iterrows():
        sub1 = row.iloc[0].encode("utf-8")
        # sql = u"SELECT * FROM `check`.channel6"
        sql = u"SELECT * FROM `check`.merchant_center WHERE merchant_center.机构名称 LIKE '%s'" %(sub1)
        df2 = pd.read_sql_query(sql,dbapi.engine)

        print sub1+'查询到：'+ str(df2.iloc[:,0].size) + '条数据！'   #打印查询结果的行数
        count1=df2.iloc[:,0].size+count1
        print '当前合计查询到：'+str(count1)+ '条数据！'
        # break
        df2.to_csv(ur"C:/Users/gyfea/Desktop/gaoyu163.csv",mode='a') #追加模式将查询结果写入指定EXCEL
if __name__ == '__main__':

    read_write_excel()
