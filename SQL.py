#!/usr/bin/env python
# -*- coding:utf-8 -*- 
#@Time :2018/6/6 14:09
#!@Author ： gyfeather
#!@File :.py
#连接mysql进行基本的查询

#1.创建数据库
def create_schema(schema_name):
    import pymysql
    db = pymysql.connect(host='127.0.0.1', user='gaoyu', password='123456', port=3306)
    cursor = db.cursor()
    cursor.execute('SELECT VERSION()')
    data = cursor.fetchone()     #获得第一条数据，也就得到了版本号
    print('Database version:', data)
    cursor.execute("CREATE DATABASE %s DEFAULT CHARACTER SET utf8"%schema_name) #创建数据库
    db.close()

#2.创建数据表
def create_table(db_name,table_name):
    import pymysql
    db = pymysql.connect(host='127.0.0.1', user='gaoyu', password='123456', port=3306, db=db_name)
    cursor = db.cursor()
    sql = 'CREATE TABLE IF NOT EXISTS %s(id VARCHAR(255) NOT NULL, name VARCHAR(255) NOT NULL, ' \
          'age INT NOT NULL, PRIMARY KEY (id))'%table_name
    cursor.execute(sql)
    db.close()

#5.插入数据
def insert_single_data():
    import pymysql
    data = {                #插入的数据内容
        'id': '20120001',
        'name': 'Bob',
        'age': 20
    }
    db = pymysql.connect(host='127.0.0.1', user='gaoyu', password='123456', port=3306, db="spider")
    cursor = db.cursor()
    table = "student"
    keys = ', '.join(data.keys())
    values = ', '.join(['%s'] * len(data))
    sql = 'INSERT INTO {table}({keys}) VALUES ({values})'.format(table=table, keys=keys, values=values)
    try:
        if cursor.execute(sql, tuple(data.values())):
            print('Successful')
            db.commit()
    except:
        print('Failed')
        db.rollback()
    db.close()
#3.导入单个表格（有标题）
def import_single_table(infile,table_name,schema_name="spider",multi_sheet=None,encoding='utf8',if_exists='append'):
    import pandas as pd
    from sqlalchemy import Column, String, create_engine

    if infile.endswith('.csv') or infile.endswith('.txt') or infile.endswith('.CSV'):
        df = pd.read_csv(infile, encoding=encoding, index_col=None)
    else:
        if not multi_sheet:
            df = pd.read_excel(infile, encoding=encoding, index_col=None)
        else:
            dfs = pd.read_excel(infile, encoding=encoding, index_col=None, sheetname=multi_sheet)
            df = pd.concat(dfs.values())

    # 将数据写入指定数据库
    engine = create_engine(r"mysql+pymysql://gaoyu:123456@127.0.0.1:3306/{0}?charset=utf8".format(schema_name))
    df.to_sql(table_name, engine, if_exists=if_exists)
    print("老板，表格已经导入成功！")
#4.导入单个表格（无标题）
def import_single_table2(infile,table_name,schema_name="spider",list=[],multi_sheet=None,encoding='utf8',if_exists='append'):
    import pandas as pd
    from sqlalchemy import Column, String, create_engine
    if infile.endswith('.csv') or infile.endswith('.txt') or infile.endswith('.CSV'):
        df = pd.read_csv(infile, encoding=encoding, index_col=None,names=list)
    else:
        if not multi_sheet:
            df = pd.read_excel(infile, encoding=encoding, index_col=None,names=list)
        else:
            dfs = pd.read_excel(infile, encoding=encoding, index_col=None, sheetname=multi_sheet,names=list)
            df =  pd.concat(dfs.values())

    #将数据写入指定数据库
    engine = create_engine(r"mysql+pymysql://gaoyu:123456@127.0.0.1:3306/{0}?charset=utf8".format(schema_name))
    df.to_sql(table_name,engine,if_exists=if_exists)
    print("老板，表格已经导入成功！")


#6.查询并将结果导出
def sql_to_write_excel(sql=None,):
    import pandas as pd
    from db_table import CiticBank
    import os,sys
    if sys.getdefaultencoding() != 'utf-8':
        reload(sys)
        sys.setdefaultencoding('utf-8')
    infile = r"C:/Users/gyfea/Desktop/test1.xlsx"    #查询的关键字段
    df = pd.read_excel(infile,header = None)
    dbapi = CiticBank()
    count1=0

     #循环读入列表数据并进行模糊查询
    for index,row in df.iterrows():
        sub1 = row.iloc[0].encode("utf-8")    #结果为byte格式
        #***输入需要查询的SQL
        sql = u"SELECT * FROM `check`.merchant_center WHERE merchant_center.机构名称 LIKE '%s'" %(sub1.decode())
        #***
        df2 = pd.read_sql_query(sql,dbapi.engine)

        # print(sub1+'查询到：'+ str(df2.iloc[:,0].size) + '条数据！')   #打印查询结果的行数d
        count1=df2.iloc[:,0].size+count1
        # print('当前合计查询到：'+str(count1)+ '条数据！')

        df2.to_csv(r"C:/Users/gyfea/Desktop/gaoyu163.csv",mode='a',encoding="cp936",float_format='%s')

if __name__ == '__main__':
    # create_schema("spider") #1.建库

    # create_table("spider","student")  #2.建表

    # import_single_table(infile=r"C:\Users\gyfea\Desktop\bin.xlsx",table_name="hello world",schema_name="spider")
    #
    # import_single_table2(infile=r"C:\Users\gyfea\Desktop\bin.xlsx",table_name="hello world",schema_name="spider",   list=["BIN","BANK_NAME"]) #3.导表（不含标题行）,LIST为设定标题行，除INDEX列以外

    # insert_single_data()   #4.录入一行数据

    sql_to_write_excel()   #5.查询数据并导出









