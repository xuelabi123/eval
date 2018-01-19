# -*- coding: utf-8 -*-
# author panyox
# 2017-10-23 21:42
import sys
import re
import codecs
import time

reload(sys)
sys.setdefaultencoding('utf-8')
f= codecs.open('q2.txt','w','utf-8')

print '正在匹配答案...'
for question in open('q.txt'):
	f.write(question)
	for answer in open('a.txt'):
		num,ans = answer.split('．',1)
		if re.match(num+'．', question):
			f.write('答案：'+ans)
			break
f.close()
print '匹配完成.'
