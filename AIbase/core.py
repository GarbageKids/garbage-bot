#!/usr/bin/python3
# -*- coding: utf-8 -*-
import random
import nltk
import time
# import NaiveBayesImp
import codecs
from nltk.probability import FreqDist
from nltk.classify import NaiveBayesClassifier
from itertools import chain
from nltk.tokenize import word_tokenize
import sys
import pickle

class Core:
    #units = None
    #def __init__(self, label_probdist, feature_probdist):
    #   super().__init__(self, label_probdist, feature_probdist)
    documents = None
    classifier = None
    vocabulary = set()
    counter = 0

    all = 0
    pos = 0
    neg = 0

    def save_core(self):
        f = open('gogo_classifier.pickle', 'wb')
        pickle.dump(Core.classifier, f)
        f.close()

    def load_core(self):
        f = open('gogo_classifier.pickle', 'rb')
        Core.classifier = pickle.load(f)
        f.close()

    def extract_line(filename):
        return [line.rstrip('\n')
            for line in open("corpus/{0}".format(filename),encoding="utf-8")]


    def extract_word_lower(line):
        lowers = []
        for s in line.split():
            temp = s.lower()
            Core.vocabulary.add(temp)
            lowers.append(temp)
            Core.counter += 1
        return lowers

    def filter_words(document):
        words = []
        for content in document:
            for word in content[0]:
                words.append(word)
        return words

    def filter_document(document):
        for i in range(0,5):
            document.pop(0)
        return document

    def merge_meta(document, meta):
        md = Core.filter_document(Core.extract_line(meta))
        index = 0
        for m in md:
            document[index] = tuple(m if i==1 else x
                                    for i, x in enumerate(document[index]))
            index += 1

        Core.all = index
        del index
        return document

    def merge_class(document, metafile):
        temp = []
        dt = Core.extract_line(metafile)
        i = 0
        for doc in document:
            temp.append((doc[0], dt[i]))
            i += 1

        return temp

    def document_features(document, units):
        document_words = set(document)
        features = {}
        for word in units:
            features['contains({})'.format(word)] = (word in document_words)
        return features

    @staticmethod
    def process2():
        start = time.time()

        Core.documents = []
        for line in Core.extract_line('case.data'):
            Core.documents.append((line, 0))
            Core.extract_word_lower(line)

        # Core.documents = [(list(Core.extract_word_lower(line)), 0)
        #                   for line in Core.extract_line('case.data')]

        Core.documents = Core.merge_class(Core.filter_document(Core.documents), 'case.meta')
        # print(Core.documents)
        featuresets = [({i: (i in word_tokenize(sentence.lower())) for i in Core.vocabulary}, tag) for sentence, tag in
                       Core.documents]

        size = int(len(featuresets))

        train_set = featuresets[:size]
        print("Сургалтын олонлог: " + str(size))
        test_set = featuresets[:size]
        print("Шалгах олонлог: " + str(len(featuresets) - size))
        Core.classifier = nltk.NaiveBayesClassifier.train(train_set)
        print("------------------------------------------------------------")
        for content, category in test_set:
            result = Core.classifier.classify(content)
            if result == category:
                # print("Corrent")
                Core.pos += 1
            else:
                # print("Wrong")
                Core.neg += 1
        print("\n---Нарийвчлал---")
        print("Алдаагүй: " + str(Core.pos) + ", Алдаатай: " + str(Core.neg))
        print("Оновчлол: " + str(nltk.classify.accuracy(Core.classifier, test_set)))
        # print("-Нарийвчлал-end-\n")
        end = time.time()
        print("Хугацаа: " + str(end - start) + "\n")
        return Core.classifier.show_most_informative_features(25)
        # print(NaiveBayesImp.show_most_informative_features(feature))

    @staticmethod
    def process(train = 20, feature = 25, info = False):
        start = time.time()
        Core.documents = [(list(Core.extract_word_lower(line)),0)
                     for line in Core.extract_line('case.data')]

        print(Core.documents)
        print("****************************************************************")
        Core.documents = Core.merge_meta(Core.filter_document(Core.documents), 'case.meta')
        print(Core.documents)
        # print (Core.documents)
        #Core.vocabulary = set(chain(*[word_tokenize(i[0].lower()) for i in Core.documents]))
        # random.shuffle(Core.documents)

        units = nltk.FreqDist(w for w in Core.filter_words(Core.documents))

        featuresets = [(Core.document_features(d,units),c) for (d,c) in Core.documents]

        size = int(len(featuresets))
        train_set = featuresets[:size]
        print("Сургалтын олонлог: "+str(size))
        test_set = featuresets[:size]
        print("Шалгах олонлог: "+str(len(featuresets)-size))
        Core.classifier = nltk.NaiveBayesClassifier.train(train_set)
        # print(train_set)
        print("------------------------------------------------------------")
        for content,category in test_set:
            result = Core.classifier.classify(content)
            if result == category:
                #print("Corrent")
                Core.pos += 1
            else:
                #print("Wrong")
                Core.neg += 1

        print("\n---Нарийвчлал---")
        print("Алдаагүй: "+str(Core.pos)+", Алдаатай: "+str(Core.neg))
        print("Оновчлол: "+str(nltk.classify.accuracy(Core.classifier,test_set)))
        #print("-Нарийвчлал-end-\n")
        end = time.time()
        print("Хугацаа: "+str(end - start)+"\n")
        if info:
            return Core.classifier.show_most_informative_features(feature)
            #print(NaiveBayesImp.show_most_informative_features(feature))

    @staticmethod
    def validator(param):
        test = False
        if Core.classifier == None:
            Core.process(20,25,False)
        else:
            if test:
                for content,category in param:
                    result = Core.classifier.classify(content)
                    if result == category:
                        result = 1
                    else:
                        result = 0
            else:
                result = Core.classifier.classify(param)
        return result

#Core.process(98,10,True)
Core.process2()
test = str('бүртгэх боломжтой ажилладаг')
feature_test = {i:(i in word_tokenize(test.lower())) for i in Core.vocabulary}
print("matching ----------------------")
for i,a in feature_test.items():
    if(a):
        print(i)
print("matching ----------------------")
dist = Core.classifier.prob_classify(feature_test)
print("BASE",dist.prob("BASE"))
print("SCM",dist.prob("SCM"))
print("CONTRACT",dist.prob("CONTRACT"))
print("CRM",dist.prob("CRM"))


# for line in dump:
#     print(line)
