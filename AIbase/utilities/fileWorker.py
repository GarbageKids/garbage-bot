import json
class FileWorker:

    def corpus_extract_line(filename):
        """
        :return: Файл корпусаас мөр мөрөөр унших
        """
        return [line.rstrip('\n')
            for line in open("corpus/{0}".format(filename), encoding="utf-8")]

    def get_settings(filename):
        """
        :return: Тохиргооны файлыг унших
        """
        with open("settings/{0}".format(filename)) as json_data:
            return json.load(json_data)