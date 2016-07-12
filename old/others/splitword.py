#!/usr/bin/python 
# -*- coding: utf-8 -*-
import jieba  
import sys 
import jieba.posseg as pseg 

stopwordsPath = '/home/hadoop/mooc/data/stopwords.data'
dataPath = '/home/hadoop/mooc/data/'

def splitword(classname):
	stopwords = [ line.rstrip() for line in open(stopwordsPath) ]
	cixing = ["x", "m", "o", "t", "v", "rz", "eng", "f", "d", ""]
	paths = [dataPath + classname + path for path in ['/confusion.data', '/explain.data', '/neutral.data']]
	i = 0
	for path in paths:
		try:
			fread = open(path, 'r')
		except Exception, e:
			print 'splitword(): read open error, ', e
			return False
		data = fread.readlines()
		fread.close()

		pathList = path.split('/')
		suffixList = pathList[6].split('.')
		suffixList[0] = 'split' + suffixList[0]
		pathList[6] = '.'.join(suffixList)
		writePath = '/'.join(pathList)
		try:
			fwrite = open(writePath, 'w')
		except Exception, e:
			print 'splitword(): write open error, ', e
			return False
		 
		for line in data:
			words = pseg.cut(line)
			result = ''
			for w in words:
				if w.word.encode('utf-8') not in stopwords and w.flag.encode('utf-8') not in cixing:
					result += w.word + ' '

			if len(result):
				fwrite.writelines(result.encode('utf-8'))
				fwrite.writelines('\n')
		fwrite.close()
	return True
			

if __name__ == '__main__':
	splitword('test')
