#!/usr/bin/python
# -*- coding: utf-8 -*-

import jieba
import sys
import jieba.posseg as pseg
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
reload(sys)
sys.setdefaultencoding("utf-8")


class TextProgress(object):
    """docstring for TextProgress"""

    def __init__(self, className):
        super(TextProgress, self).__init__()
        self.className = className
        self.classPath = '/home/hadoop/mooc/data/' + className
        self.stopwordsPath = '/home/hadoop/mooc/data/stopwords.data'

    def segment(self):
        inputPath = self.classPath + '/data.data'
        outputPath = self.classPath + '/segment.data'
        stopwords = [line.rstrip().lstrip()
                     for line in open(self.stopwordsPath)]
        cixing = ["o", "t", "v", "rz", "eng", "f", "d", ""]
        try:
            fread = open(inputPath, 'r')
        except Exception, e:
            raise e
            return False
        lines = fread.readlines()
        try:
            fread.close()
        except Exception, e:
            raise e
            return False

        try:
            fwrite = open(outputPath, 'w')
        except Exception, e:
            raise e
            return False

        for line in lines:
            line = line.rstrip()
            label = line[-1]
            line = line[:-1]
            line = line.replace(' ', '')
            # print line
            words = pseg.cut(line)
            result = []
            for w in words:
                # print w.word.encode('utf-8'), w.flag.encode('utf-8')
                if w.word.encode('utf-8') not in stopwords and w.flag.encode('utf-8') not in cixing:
                    result.append(w.word.encode('utf-8'))
            result.append(label)
            post = ' '.join(result)
            # print result, len(result)
            if len(result) > 1:
                fwrite.writelines(post)
                fwrite.writelines('\n')
        try:
            fwrite.close()
        except Exception, e:
            raise e
            return False

        return True

    def makeMatrix(self):
        inputPath = self.classPath + '/segment.data'
        try:
            fread = open(inputPath, 'r')
        except Exception, e:
            raise e
            return False, False
        lines = fread.readlines()
        corpus = []
        y = []
        for line in lines:
            lineList = line.rstrip().split(' ')
            y.append(int(lineList.pop()))
            post = ' '.join(lineList)
            corpus.append(post)
        try:
            fread.close()
        except Exception, e:
            raise e
            return False, False
        return corpus, y

    def featureExtraction(self, corpus):
        bigram_vectorizer = CountVectorizer(ngram_range=(1, 2), min_df=1)
        arr = bigram_vectorizer.fit_transform(corpus).toarray()
        # print arr
        featurename = bigram_vectorizer.get_feature_names()
        # for name in featurename:
        # 	print name
        transformer = TfidfTransformer()
        tfidf = transformer.fit_transform(arr)
        tfidfArr = tfidf.toarray()
        # for x in tfidfArr:
        # print x
        print tfidfArr
        return tfidfArr

if __name__ == '__main__':
    t = TextProgress('test')
    x, y = t.makeMatrix()
    if x and y:
        t.featureExtraction(x)
