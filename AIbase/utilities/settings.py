from utilities.fileWorker import FileWorker



class Settings:

    isLoaded = False
    SETTINGS = None

    @staticmethod
    def read_settings():
        if Settings.isLoaded is False:
            Settings.SETTINGS = FileWorker.get_settings('main.json')
            Settings.isLoaded = True

    @staticmethod
    def get_corpus_source_type():
        Settings.read_settings()
        if Settings.SETTINGS['corpus_source']['file_or_database'] is True:
            return 'DATABASE'
        else:
            return 'FILE'

    @staticmethod
    def get_file_meta():
        Settings.read_settings()
        return Settings.SETTINGS['corpus_source']['file']['meta_location']

    @staticmethod
    def get_file_data():
        Settings.read_settings()
        return Settings.SETTINGS['corpus_source']['file']['data_location']

    @staticmethod
    def get_learn_location():
        Settings.read_settings()
        return Settings.SETTINGS['learning_schedule']['location']

    @staticmethod
    def get_learn_freq():
        Settings.read_settings()
        if Settings.SETTINGS['learning_schedule']['frequency']['daily'] is True:
            return 'DAILY'
        if Settings.SETTINGS['learning_schedule']['frequency']['weekly'] is True:
            return 'WEEKLY'
        if Settings.SETTINGS['learning_schedule']['frequency']['monthly'] is True:
            return 'MONTHLY'

    @staticmethod
    def get_learn_time():
        Settings.read_settings()
        return Settings.SETTINGS['learning_schedule']['frequency']['time']
