# -*- coding: utf-8 -*-
from pymongo import MongoClient
from utilities.settings import Settings
from utilities.stringWorker import StringWorker


class DatabaseWorker:
    """
    Өгөгдлийн сантай харьцах класс
    """

    db = None
    isConnected = False

    corpus_collection = {
        'COL_BASE': 'bases',
        'COL_CONTRACT': 'contracts',
        'COL_CRM': 'crms',
        'COL_FINANCE': 'finances',
        'COL_HRM': 'hrms',
        'COL_SCM': 'scms'
    }

    @staticmethod
    def make_connection():
        """
        DBMS тэй холболт үүсгэх
        :return:
        """
        if DatabaseWorker.isConnected is False:
            if Settings.get_db_engine() == 'mongodb':
                DatabaseWorker.db = MongoClient(Settings.get_db_host(), Settings.get_db_port())[Settings.get_db_name()]
                DatabaseWorker.isConnected = True

    @staticmethod
    def select_all(table_name, row_id, type):
        """
        Өгөгдлийн сангийн нэгжээс бүх өгөгдлийг дуудах
        :param table_name: Нэгжийн нэр
        :param type: Q/A Асуулт эсвэл Хариулт унших
        :return: list утга буцаана
        """
        DatabaseWorker.make_connection()
        data = []
        for row in DatabaseWorker.db[table_name].find():
            if type == 'Q':
                data.append((StringWorker.replacer(row[row_id]), table_name[:-1].upper()))
            elif type == 'A':
                data.append(row[row_id])
        return data

    @staticmethod
    def select_all_table():
        temp = []
        for i in DatabaseWorker.corpus_collection:
            temp.extend(DatabaseWorker.select_all((DatabaseWorker.corpus_collection[i]), 'q', 'Q'))
        return temp

    @staticmethod
    def insert_vocabulary(text):
        DatabaseWorker.make_connection()
        result = DatabaseWorker.db.vocubularys.insert_one(
            {
                "word": text
            }
        )
        return result

    @staticmethod
    def get_vocabulary():
        DatabaseWorker.make_connection()
        return DatabaseWorker.select_all('vocubularys', 'word', 'A')

    @staticmethod
    def set_empty_vocabuary():
        DatabaseWorker.db.vocubularys.remove({})
        return
