class StringWorker:

    @staticmethod
    def min(a, b, c):
        """
        3 тооны хамгийн бага утга
        :param a:
        :param b:
        :param c:
        :return:
        """
        if a < b:
            if a < c:
                return a
            elif c < b:
                return c
        elif b < c:
            return b
        else:
            return c


    @staticmethod
    def levenshtein_distance(s1, s2):
        """
        Levenshtein алгоритм; Доороос дээш (bottom-up) динамик програмчлал
        :param s1: Текст1
        :param s2: Текст2
        :return:
        """
        s1len = len(s1) + 1
        s2len = len(s2) + 1
        dp = [[0 for x in range(s2len)] for y in range(s1len)]

        for i in range(0, s1len-1):
            dp[i][0] = i
        for i in range(0, s2len-1):
            dp[0][i] = i

        for i in range(1, s2len):
            for e in range(1, s1len):
                c = 0
                if s1[e-1] == s2[i-1]:
                    c = 0
                else:
                    c = 1
                dp[e][i] = min(dp[e-1][i]+1, dp[e][i-1]+1, dp[e-1][i-1]+c)


        return dp[s1len-2][s2len-2]

    @staticmethod
    def word_changes(s1, s2, complex):
        """
        Үгс хоорондын зөрүүг тооцох
        :param s1: Текст1
        :param s2: Текст2
        :param complex: Үгсийг шалгахдаа Levenshtein ий алгоритм ашиглах эсэх
        :return: ялгаатай үгсийн тоо
        """
        threshold = 50
        diff = 0
        s1w = s1.split()
        s2w = s2.split()
        s1len = len(s1w)
        s2len = len(s2w)

        for i in range(0, s1len):
            exist = False
            for e in range(0, s2len):
                if complex is True:
                    if StringWorker.levenshtein_distance(s1w[i], s2w[e]) < threshold:
                        exist = True
                        break
                else:
                    if s1w[i] == s2w[e]:
                        exist = True
                        break

            if exist is False:
                diff += 1

        return diff

    @staticmethod
    def str_compare(s1, s2):
        """
        Өгүүлбэрийг хооронд нь харьцуулах
        :param s1: Текст1
        :param s2: Текст2
        :return: Төстэй байх магадлалыг илгээнэ
        """
        s1len = len(s1.split())
        similarity1 = 100 - StringWorker.levenshtein_distance(s1, s2) * 100 / len(s1)
        similarity2 = 100 - StringWorker.word_changes(s1, s2, True) * 100 / s1len
        # similarity3 = 100 - ((abs(len(s1) - len(s2))) * 100) / len(s1)
        # similarity4 = 100 - ((abs(s1len - len(s2.split()))) * 100) / s1len
        # return (similarity1 + similarity2 * 2 + similarity3 + similarity4) / 5
        return (similarity1 + similarity2 * 3) / 4

    @staticmethod
    def replacer(line):
        """
        Тэмдэгтүүдийг хоосон зайгаар солих
        :param line:
        :return:
        """
        for e in range(0, len(line)):
            if line[e] == '-' or line[e] == '!' or line[e] == '?' or line[e] == '.' or line[e] == ',':
                line = line[:e] + " " + line[e+1:]
        return line

