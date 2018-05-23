# -*- coding:utf-8 -*- 
import sys

if '..' not in sys.path:
    sys.path.append('..')
from future_mysql.dbBase import DB_BASE

from sqlalchemy import Column, Integer, String, DateTime, Numeric, Index, Float, NVARCHAR, BigInteger
from sqlalchemy import Table
import os
import pandas as pd

trans = lambda x: x.encode('utf8') if isinstance(x,unicode) else x

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

    def __init__(self, db_name='check', table_name=None):#db_name=指定数据库
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
        return [ trans(i) for i in self.get_column_names(self.table_struct)]
    
    def get_col_length(self):
        return len(self.get_column_names(self.table_struct))
    
    def get_col_sizes(self):
        return self.col_sizes

class reserve_trade_all(CiticBank):
    
    def __init__(self, db_name='check', table_name='reserve_trade_all'):
        super(reserve_trade_all, self).__init__(db_name)
        self.table_struct = None
        if table_name is not None:
            self.table_name = table_name
            self.table_struct = Table(
                table_name, self.meta,
                #
                Column('index',Integer,primary_key = True,autoincrement=True),
                Column('citic_custom_id',Integer),
                Column('origin_account_number', String(32),index = True),
                Column('origin_account_name', String(128)),
                Column('trade_id',Integer),
                Column('date', String(32)),
                Column('timestamp', String(40)),
                #
                Column('operation_id',String(32)),
                Column('direction',String(6)),
                Column('turnover',Float),
                Column('residual',Float),
                Column('opponent_account_number', String(32),index = True),
                Column('opponent_account_name', String(64)),
                Column('opponent_bank_name', String(128)),
                Column('abstract',String(128)),
            )

def import_core(infile,table_name,encoding = 'utf8',if_exists='append',multi_sheet = None): #导入文件的封装函数
    if infile.endswith('.csv') or infile.endswith('.txt')or infile.endswith('.CSV'):
        df = pd.read_csv(infile,encoding = encoding,index_col = None)
    else:
        if not multi_sheet:
            df = pd.read_excel(infile,encoding = encoding,index_col = None)
        else:
            dfs = pd.read_excel(infile, encoding=encoding, index_col=None,sheetname = multi_sheet)
            df = pd.concat(dfs.values())
    # print df.head()
    df.columns = [ i.strip() for i in df.columns]
    # print df.columns
    db_obj = CiticBank()
    dtypedict = mapping_df_types(df)#改变TEXT为VARCHAR类型
    df.to_sql(table_name,db_obj.engine,chunksize = 10240,if_exists=if_exists,dtype=dtypedict)
    print 'finished'

def import_reserve_trade_all():    #导入多个文件结尾是txt
    root_path = r'C:\\Users\\gyfea\\Desktop\\oh'   #选择路径
    csvs = [ i for i in os.listdir(root_path) if i.endswith('.txt') ]
    print csvs
    dbapi = reserve_trade_all()
    dbapi.create_table()
    cols = dbapi.get_col_names()
    for infile in csvs:
        print infile
        df = pd.read_csv(os.path.join(root_path,infile),encoding = 'cp936',index_col = None)
        df.columns = cols[1:]
        df.to_sql(dbapi.table_name,dbapi.engine,if_exists='append',chunksize=10240,index = False) 
        

 
def import_cross_validation_2():   #导入单个文件，格式不限
    table_name = r'wholesale_account'#写数据库表格名字
    infile = r'C:\Users\gyfea\Desktop\wholesale_account.xls' #默认文件存放位置
    import_core(infile,table_name,encoding = 'cp936') #multi_sheet=range(3))  用于多表读取cp936,utf8

if __name__ == '__main__':
    import_cross_validation_2()
    
    