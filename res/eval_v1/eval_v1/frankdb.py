# -*- coding:utf-8 -*-

import MySQLdb
from MySQLdb.cursors import DictCursor
from DBUtils.PooledDB import PooledDB
import config

class Frankdb(object):
    
    _dbpool = None
    
    def __init__(self):
        self.conn = Frankdb.getConn()
        self.cursor = self.conn.cursor()
        
    @staticmethod
    def getConn():
        #获取数据库连接
        if Frankdb._dbpool is None:
            _dbpool = PooledDB(creator=MySQLdb,mincached=1,maxcached=20,
            host=config.Mysql['host'],user=config.Mysql['user'],passwd=config.Mysql['password'],db=config.Mysql['database'],
            use_unicode='false',charset='utf8',cursorclass=DictCursor)
        
        return _dbpool.connection()
            
    def getAll(self, sql, param=None):
        if param is None:
            self.cursor.execute(sql)
        else:
            self.cursor.execute(sql, param)
        
        return self.cursor.fetchall()
    
    def getOne(self, sql, param=None):
        if param is None:
            self.cursor.execute(sql)
        else:
            self.cursor.execute(sql, param)
        
        return self.cursor.fetchone()
 
    def insertOne(self, sql, value=None):
        if value is None:
            self.cursor.execute(sql)
        else:
            self.cursor.execute(sql, value)
        return self._lastId()
    
    def insertMany(self, sql, values=None):
        if values is None:
            res = self.cursor.execute(sql)
        else:
            res = self.cursor.execute(sql,values)
        return res
    
    def update(self, sql, param=None):
        self._exe(sql, param)
        
    def delete(self,sql, param=None):
        self._exe(sql, param)
        
    def _exe(self, sql, param=None):
        if param is None:
            count = self.cursor.execute(sql)
        else:
            count = self.cursor.execute(sql, param)
        return count
    
    #当前连接最后一条插入的ID
    def _lastId(self):
        self.cursor.execute("SELECT @@IDENTITY AS id")  
        result = self.cursor.fetchall()  
        return result[0]['id']
    #开始事物
    def begin(self):
        self.conn.autocommit(0)
        
    def commit(self):
        self.conn.commit()
    #事物回滚
    def rollback(self):
        self.conn.rollback()
    #释放连接
    def close(self,save=1):
        if save==1:
            self.commit()
        else:
            self.rollback()
        self.cursor.close()
        self.conn.close()