#!/usr/bin/python 
# -*- coding: utf-8 -*-

import jieba  
import sys 
import jieba.posseg as pseg 
reload(sys)
sys.setdefaultencoding( "utf-8" )

path = '/home/hadoop/mooc/data/test/data.data'
f = open(path, 'r')
lines = f.readlines()
for line in lines:
	line = line.rstrip()
	print line[-1]

