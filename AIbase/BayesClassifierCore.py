#!/usr/bin/python3
# -*- coding: utf-8 -*-
import random
import nltk
import time
from nltk.tokenize import word_tokenize
import pickle
from utilities.fileWorker import FileWorker
from utilities.settings import Settings

class BayesClassifierCore:
    documents = None  # Сургалтын өгөгдлүүд
    classifier = None  # Bayes ангилагч обьект
    vocabulary = set()  # Үгсийн сан
    counter = 0

    all = 0
    pos = 0
    neg = 0

    def save_core(file_name):
        '''
        Сургалтын моделийг файлд хадгалах
        @:param file_name: файлын нэр
        :return:
        '''
        f = open(file_name+'.pickle', 'wb')
        pickle.dump(BayesClassifierCore.classifier, f)
        f.close()

    def load_core(file_name):
        '''
        Сургалтын моделийг файлаас унших
        @:param file_name: файлын нэр
        :return:
        '''
        f = open(file_name+'.pickle', 'rb')
        BayesClassifierCore.classifier = pickle.load(f)
        f.close()


    def extract_vocubulary(line):
        '''
        Өгүүлбэрээс үгсийг ялгаж үгсийн санд утга давхардахгүй хуулах
        @:param line: Өгүүлбэр
        :return:
        '''
        line = line.lower()
        for s in line.split():
            temp = s.lower()
            BayesClassifierCore.vocabulary.add(temp)

    def merge_meta_file(document, metafile):
        '''
        Файлаас унших үед текст өгөгдлийг харгалзах ангилалтай нь нэгтгэх
        :param metafile:
        :return:
        '''
        temp = []
        dt = FileWorker.corpus_extract_line(metafile)
        i = 0
        for doc in document:
            temp.append((doc[0], dt[i]))
            i += 1

        return temp

    @staticmethod
    def process():
        start_time = time.time()
        BayesClassifierCore.documents = []

        if Settings.get_corpus_source_type() == 'FILE':
            for line in FileWorker.corpus_extract_line(Settings.get_file_data()):
                BayesClassifierCore.documents.append((line, 0))
                BayesClassifierCore.extract_vocubulary(line)

            BayesClassifierCore.documents = BayesClassifierCore.merge_meta_file(BayesClassifierCore.documents,
                                                                                    Settings.get_file_meta())
        print("****************************")
        print(BayesClassifierCore.documents)
        print("****************************")
        featuresets = [({i: (i in word_tokenize(sentence.lower()))
                        for i in BayesClassifierCore.vocabulary}, tag) for sentence, tag in BayesClassifierCore.documents]

        size = int(len(featuresets))

        train_set = featuresets[:size]
        print("Сургалтын олонлог: ", size)
        test_set = featuresets[:size]
        print("Шалгах олонлог: ", size)
        BayesClassifierCore.classifier = nltk.NaiveBayesClassifier.train(train_set)
        print("------------------------------------------------------------")
        for content, category in test_set:
            result = BayesClassifierCore.classifier.classify(content)
            if result == category:
                BayesClassifierCore.pos += 1
            else:
                BayesClassifierCore.neg += 1
        print("\n---Нарийвчлал---")
        print("Алдаагүй: " + str(BayesClassifierCore.pos) + ", Алдаатай: " + str(BayesClassifierCore.neg))
        print("Оновчлол: " + str(nltk.classify.accuracy(BayesClassifierCore.classifier, test_set)))
        print("-Нарийвчлал-end-\n")
        end_time = time.time()
        print("Хугацаа: " + str(end_time - start_time) + "\n")
        return BayesClassifierCore.classifier.show_most_informative_features(25)
        # print(NaiveBayesImp.show_most_informative_features(feature))


    def classify_detail(text):
        '''
        Текстийг ангилах - Дэлгэрэгүй: Ангилал бүрийн магадлал
        :return:
        '''
        feature_test = {i: (i in word_tokenize(text.lower())) for i in BayesClassifierCore.vocabulary}
        dist = BayesClassifierCore.classifier.prob_classify(feature_test)
        print("BASE", dist.prob("BASE"))
        print("SCM", dist.prob("SCM"))
        print("CONTRACT", dist.prob("CONTRACT"))
        print("CRM", dist.prob("CRM"))



BayesClassifierCore.process()
test = str('бүртгэх боломжтой ажилладаг')
BayesClassifierCore.classify_detail(test)