#!/usr/bin/python3
# -*- coding: utf-8 -*-
import random
import nltk
import time
from nltk.tokenize import word_tokenize
import pickle
from utilities.fileWorker import FileWorker
from utilities.databaseWorker import DatabaseWorker
from utilities.settings import Settings
from utilities.stringWorker import StringWorker


class BayesClassifierCore:
    """
    Bayes -н ангилагчийг хэрэгжүүлсэн
    """
    documents = None  # Сургалтын өгөгдлүүд
    classifier = None  # Bayes ангилагч обьект
    vocabulary = set()  # Үгсийн сан
    counter = 0

    pos = 0 # Сургалтын тестийг амжилттай давсан
    neg = 0 # Сургалтын тестийг амжилтгүй давсан

    # Feature -т тооцохгүй үгс
    filter_vocab = {
        'яаж': True,
        'вэ': True,
        'юу': True,
        'гэж': True,
        'хэрхэн': True,
        'хийх': True,
        'үү': True,
        'уу': True,
        'рүү': True,
        'руу': True,
        'нь': True,
        'нд': True,
        'н': True,
        'г': True,
        'ын': True,
        'ийн': True,
        'ний': True,
        'ны': True,
        'и': True
    }

    @staticmethod
    def save_core(file_name):
        """
        Сургалтын моделийг файлд хадгална
        Үгсийн санг өгөгдлийн санд хадгална
        @:param file_name: файлын нэр
        :return:
        """
        f = open(file_name+'.pickle', 'wb')
        pickle.dump(BayesClassifierCore.classifier, f)
        f.close()

    @staticmethod
    def load_core(file_name):
        """
        Сургалтын моделийг файлаас унших
        Үгсийн санг өгөгдлийн сангаас унших
        @:param file_name: файлын нэр
        :return:
        """
        f = open(file_name+'.pickle', 'rb')
        BayesClassifierCore.classifier = pickle.load(f)
        f.close()

    @staticmethod
    def extract_vocubulary(line):
        """
        Өгүүлбэрээс үгсийг ялгаж үгсийн санд утга давхардахгүй хуулах
        @:param line: Өгүүлбэр
        :return:
        """
        line = line.lower()
        for s in line.split():
            try:
                if BayesClassifierCore.filter_vocab[s] is True:
                    continue
            except KeyError:
                BayesClassifierCore.vocabulary.add(s)

    def merge_meta_file(document, metafile):
        """
        Файлаас унших үед текст өгөгдлийг харгалзах ангилалтай нь нэгтгэх
        :param metafile:
        :return:
        """
        temp = []
        dt = FileWorker.corpus_extract_line(metafile)
        i = 0
        for doc in document:
            temp.append((doc[0], dt[i]))
            i += 1

        return temp

    @staticmethod
    def get_document():
        if Settings.get_corpus_source_type() == 'FILE':
            for line in FileWorker.corpus_extract_line(Settings.get_file_data()):
                line = BayesClassifierCore.replacer(line)
                BayesClassifierCore.documents.append((line, 0))
                BayesClassifierCore.extract_vocubulary(line)

            BayesClassifierCore.documents = BayesClassifierCore.merge_meta_file(BayesClassifierCore.documents,
                                                                                Settings.get_file_meta())
        elif Settings.get_corpus_source_type() == 'DATABASE':
            BayesClassifierCore.documents = DatabaseWorker.select_all_table()
            for line in BayesClassifierCore.documents:
                BayesClassifierCore.extract_vocubulary(line[0])

    @staticmethod
    def process():
        """
        Үсийн хусдаг метход
        :return:
        """
        start_time = time.time()
        BayesClassifierCore.get_document()

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

    @staticmethod
    def classify_detail(text):
        """
        Текстийг ангилах - Дэлгэрэгүй: Ангилал бүрийн магадлал
        :return:
        """
        feature_test = {i: (i in word_tokenize(text.lower())) for i in BayesClassifierCore.vocabulary}
        dist = BayesClassifierCore.classifier.prob_classify(feature_test)
        print("BASE", dist.prob("BASE"))
        print("SCM", dist.prob("SCM"))
        print("CONTRACT", dist.prob("CONTRACT"))
        print("CRM", dist.prob("CRM"))

    @staticmethod
    def classify(text):
        """
        Текстийг ангилах
        :return: Харгалзах ангилалыг буцаана
        """
        feature_test = {i: (i in word_tokenize(text.lower())) for i in BayesClassifierCore.vocabulary}
        return BayesClassifierCore.classifier.classify(feature_test)

    @staticmethod
    def validateData(text):
        print("len:",len(BayesClassifierCore.vocabulary))

        for k in word_tokenize(text.lower()):
            print("|"+k+"|")
            for j in BayesClassifierCore.vocabulary:
                if k == j:
                    print("Match: ",j)

BayesClassifierCore.process()
print(BayesClassifierCore.vocabulary)
# BayesClassifierCore.load_core(Settings.get_model_file())
test = 'үйлчилгээний нөхцөл гэрээ бүртгэх'
BayesClassifierCore.validateData(test)
print(test)
BayesClassifierCore.classifier.show_most_informative_features(25)
kechi = BayesClassifierCore.classify(test)
BayesClassifierCore.classify_detail(test)
print(kechi)
# data = DatabaseWorker.select_all(kechi.lower()+'s', 'a')
#
# max = 0
# max_str = ''
#
# for i in data:
#     result = StringWorker.str_compare(test, i[0])
#     if result > 90:
#         max_str = i[0]
#         break
#     if result > max:
#         max = result
#         max_str = i[0]
#
# print('FINAL ANSWER: ',max_str)