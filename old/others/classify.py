#!/usr/bin/python 
# -*- coding: utf-8 -*-

import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )

dataPath = '/home/hadoop/mooc/data/test/test.data'
confusionPath = '/home/hadoop/mooc/data/test/confusion.data'
explainPath = '/home/hadoop/mooc/data/test/explain.data'
neutralPath = '/home/hadoop/mooc/data/test/neutral.data'

def classify():
	try:
		dataFile = open(dataPath, 'r+')
		confusionFile = open(confusionPath, 'w')
		neutralFile = open(neutralPath, 'w')
		explainFile = open(explainPath, 'w')
		data = dataFile.readlines()
	except Exception, e:
		print 'classify():open or read error, ', e
		return False

	for line in data:
		print line[-1]
		if int(line[-1]) == 1:
			confusionFile.write(line[:-1])
			confusionFile.write('\n')
		elif int(line[-1]) == 0:
			neutralFile.write(line[:-1])
			neutralFile.write('\n')
		else:
			explainFile.write(line[:-1])
			explainFile.write('\n')
	dataFile.close()
	confusionFile.close()
	neutralFile.close()
	explainFile.close()
	return True


	# def classify(self):
	# 	dataPath = self.classPath + '/data.data'
	# 	confusionPath = self.classPath + '/confusion.data'
	# 	neutralPath = self.classPath + '/neutral.data'
	# 	explainPath = self.classPath + '/explain.data'
	# 	try:
	# 		dataFile = open(dataPath, 'r+')
	# 		confusionFile = open(confusionPath, 'w')
	# 		neutralFile = open(neutralPath, 'w')
	# 		explainFile = open(explainPath, 'w')
	# 		data = dataFile.readlines()
	# 	except Exception, e:
	# 		raise e
	# 		return False
	# 	for line in data:
	# 		print line[1]
	# 		if int(line[-2]) == 1:
	# 			confusionFile.write(line[:-2])
	# 			confusionFile.write('\n')
	# 		elif int(line[-2]) == 0:
	# 			neutralFile.write(line[:-2])
	# 			neutralFile.write('\n')
	# 		else:
	# 			explainFile.write(line[:-2])
	# 			explainFile.write('\n')
	# 	try:
	# 		dataFile.close()
	# 		confusionFile.close()
	# 		neutralFile.close()
	# 		explainFile.close()
	# 	except Exception, e:
	# 		raise e
	# 	return True

		
if __name__ == '__main__':
	if classify():
		print 'ok'