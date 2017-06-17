from utilities.fileWorker import FileWorker


class Settings:
    """
    Үндсэн тохиргооны файлаас тохиргоог унших get функцуудыг агуулсан
    """

    isLoaded = False
    SETTINGS = None

    @staticmethod
    def read_settings():
        """
        Үндсэн тохиргооны файлыг унших
        :return:
        """
        if Settings.isLoaded is False:
            Settings.SETTINGS = FileWorker.get_settings('main.json')
            Settings.isLoaded = True

    @staticmethod
    def get_corpus_source_type():
        """
        :return: Сургалтын корпусыг ямар эх сурвалжаас уншихийг авах
        """
        Settings.read_settings()
        if Settings.SETTINGS['corpus_source']['file_or_database'] is True:
            return 'DATABASE'
        else:
            return 'FILE'

    @staticmethod
    def get_db_engine():
        """
        :return: Ямар DBMS унших эсэх
        """
        Settings.read_settings()
        return Settings.SETTINGS['corpus_source']['database']['engine']

    @staticmethod
    def get_db_host():
        """
        :return: Өгөгдлийн сантай холбогдох хаяг
        """
        Settings.read_settings()
        return Settings.SETTINGS['corpus_source']['database']['host']

    @staticmethod
    def get_db_port():
        """
        :return: Өгөгдлийн сантай холбогдох порт
        """
        Settings.read_settings()
        return Settings.SETTINGS['corpus_source']['database']['port']

    @staticmethod
    def get_db_name():
        """
        :return:
        """
        Settings.read_settings()
        return Settings.SETTINGS['corpus_source']['database']['dbname']

    @staticmethod
    def get_file_meta():
        """
        :return: Сургалтын корпусын харгалзах ангилал унших файлын нэр
        """
        Settings.read_settings()
        return Settings.SETTINGS['corpus_source']['file']['meta_location']

    @staticmethod
    def get_file_data():
        """
        :return: Сургалтын корпусыг унших файлын нэр
        """
        Settings.read_settings()
        return Settings.SETTINGS['corpus_source']['file']['data_location']

    @staticmethod
    def get_model_file():
        """
        :return: Сургалтын моделийг хадгалах/унших файлын нэр
        """
        Settings.read_settings()
        return Settings.SETTINGS['learning']['model_filename']

    @staticmethod
    def get_reciever_method():
        """
        :return: Чат хүлээн авах method : GET/POST
        """
        Settings.read_settings()
        return Settings.SETTINGS['receiver']['method']

    @staticmethod
    def get_reciever_format():
        """
        :return: Чат хүлээн авах формат
        """
        Settings.read_settings()
        return Settings.SETTINGS['receiver']['format']

    @staticmethod
    def get_reciever_url():
        """
        :return: Чат хүлээн авах хаяг
        """
        Settings.read_settings()
        return Settings.SETTINGS['receiver']['url']
