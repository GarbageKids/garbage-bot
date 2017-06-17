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
        Сургалтын корпусыг хаанаас уншихийг авах
        :return:
        """
        Settings.read_settings()
        if Settings.SETTINGS['corpus_source']['file_or_database'] is True:
            return 'DATABASE'
        else:
            return 'FILE'

    @staticmethod
    def get_file_meta():
        """
        Мета файл буюу ангилалуудыг унших
        :return:
        """
        Settings.read_settings()
        return Settings.SETTINGS['corpus_source']['file']['meta_location']

    @staticmethod
    def get_file_data():
        """
        Сургалтын файлыг унших
        :return:
        """
        Settings.read_settings()
        return Settings.SETTINGS['corpus_source']['file']['data_location']

    @staticmethod
    def get_learn_location():
        """
        Сургасан моделоо хадгалахах газарыг авах
        :return:
        """
        Settings.read_settings()
        return Settings.SETTINGS['learning_schedule']['location']

    @staticmethod
    def get_learn_freq():
        """
        Сургалтын моделийг даних сургах давтамжийг авах
        :return:
        """
        Settings.read_settings()
        if Settings.SETTINGS['learning_schedule']['frequency']['daily'] is True:
            return 'DAILY'
        if Settings.SETTINGS['learning_schedule']['frequency']['weekly'] is True:
            return 'WEEKLY'
        if Settings.SETTINGS['learning_schedule']['frequency']['monthly'] is True:
            return 'MONTHLY'

    @staticmethod
    def get_learn_time():
        """
        Сургалтын моделийг дахин сургах хугацааг авах
        :return:
        """
        Settings.read_settings()
        return Settings.SETTINGS['learning_schedule']['frequency']['time']
