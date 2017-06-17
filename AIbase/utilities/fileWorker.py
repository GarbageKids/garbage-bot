import json
class FileWorker:

    def corpus_extract_line(filename):
        return [line.rstrip('\n')
            for line in open("corpus/{0}".format(filename), encoding="utf-8")]

    def get_settings(filename):
        with open("settings/{0}".format(filename)) as json_data:
            settings = json.load(json_data)
            return settings