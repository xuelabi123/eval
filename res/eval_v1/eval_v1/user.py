# -*- coding: utf-8 -*-

from frankdb import Frankdb
import math
import re
import jieba.analyse
import codecs
import collections
import time

class UserModel(object):

    def __init__(self):
        self.frank = Frankdb()
        self.industrys = [1,4,35,46,57,69,83,95,104,119,133,142,152,172,180,182,220,243]
    
    #提取关键词    
    def news_keywords(self,content):
        
        content1 = re.sub('<[^>]*>','', content)
        
        tags = jieba.analyse.extract_tags(content1,15)
        
        return tags
    
    
    def labels2index(self,id):
        for i in xrange(len(self.industrys)):
            if int(id)==self.industrys[i]:
                return i
        return None
    
    def doc_dict(self):
        return [0]*len(self.industrys)
    
    def user_similar(self):
        cateX1 = [0]*len(self.industrys)
        cateX2 = [0]*len(self.industrys)
        userData1 = [4,104,142,180,95,119,172,152]
        userData2 = [35,69,104,152,172]
        
        for d in userData1:
            index = self.labels2index(d)
            if d in self.industrys:
                cateX1[index]=1
            else:
                cateX1[index]=-1
        for d2 in userData2:
            index = self.labels2index(d2)
            if d2 in self.industrys:
                cateX2[index]=1
            else:
                cateX2[index]=-1
        
        fz=0
        fm1=0
        fm2=0
        x=0
        while x<len(cateX1):
            fz += cateX1[x]*cateX2[x]
            fm1 += cateX1[x]*cateX1[x]
            fm2 += cateX2[x]*cateX2[x]
            x += 1 
            
        cos = fz*1.0/(math.sqrt(fm1)*math.sqrt(fm2))
        
        print '两个用户之间的相似度是: %s' % cos
        
    def get_user_recom(self):
        '''
        根据用户浏览记录，提取关键词
        '''
        print '正在提取用户浏览记录...'
        
        sql='select a.industry_id, b.uid from zt_news a, user_analysis b where a.id=b.page_id and b.uid>0 and b.page_type=1 and a.industry_id>0'

        user_data = self.frank.getAll(sql)
        user_industry = collections.defaultdict(self.doc_dict)
        user_knbs = collections.defaultdict(list)
        user_recom = collections.defaultdict(list)
        
        print '正在计算用户之间相似度...'
        #通过计算多维度空间向量夹角余玄得到用户相似度
        for user in user_data:
            index = self.labels2index(user['industry_id'])
            if index is None:
                continue
            user_industry[user['uid']][index]+=1
        for k,v in user_industry.items():
            for k1,v1 in user_industry.items():
                if k1!=k:
                    cos = self.sv_cos(v,v1)
#                        print '%s号与%s号的相似度是: %s' % (k,k1,cos)
                    if cos>0.5:
                        user_knbs[k].append(int(k1))
            
        print '正在为用户推荐...'
        #通过协同过滤算法为用户推荐内容
        
        cur_time = time.time()
        time1 = cur_time-cur_time%(86400*2)
        
        for k,v in user_knbs.items():
            sql = "select page_id from user_analysis where uid=%s and create_time>%s"
            news_item = self.frank.getAll(sql,(int(k),time1))
            upage=set()
            for n in news_item:
                upage.add(n['page_id'])
#            print upage
            ids = str(v)
            ids = ids.strip('[')
            ids = ids.strip(']')
            sql = "select page_id from user_analysis where uid in (%s) " % ids
            sql += "and create_time>%s" % time1
            
            news_item1 = self.frank.getAll(sql)
#            print news_item1
            if news_item1 is not None:
                for page in news_item1:
                    if page['page_id'] not in upage:
                        user_recom[k].append(page)
        
        for k,v in user_recom.items():
            if len(v)>0:
                time2 = time.time()
                sql = "insert into zt_user_recom(uid, news_id, create_time) values "
                for vid in v:
                    sql += "(%s, %s, %s)," % (k,vid['page_id'],time2)
                sql = sql.strip(',')
                self.frank.insertMany(sql)  
        self.frank.commit()
        print '推荐完成'
        
    def sv_cos(self,sv1,sv2):
        fz=0
        fm1=0
        fm2=0
        x=0
        while x<len(sv1):
            fz += sv1[x]*sv2[x]
            fm1 += sv1[x]*sv1[x]
            fm2 += sv2[x]*sv2[x]
            x += 1 
            
        cos = fz*1.0/(math.sqrt(fm1)*math.sqrt(fm2))
        
        return cos
        