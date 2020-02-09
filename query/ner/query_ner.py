# -*- coding:utf-8 -*-
"""
identify entity from question
-----------------
use jieba to partition question

"""

import jieba
import jieba.posseg as pseg

class Word(object):
    def __init__(self, token, pos):
        self.token = token
        self.pos = pos

class QueryNER:
    def __init__(self, path_list):
        """
        initial and load dict
        :param dict_paths:
        """
        for p in path_list:
            jieba.load_userdict(p)

        # adjust jieba frequency for incorrect partition
        jieba.suggest_freq('其他名字', True)
        jieba.suggest_freq('其他名称', True)
        jieba.suggest_freq('上映地区', True)
        jieba.suggest_freq('上映国家', True)
        jieba.suggest_freq('上映时间', True)
        jieba.suggest_freq('上映语言', True)
        jieba.suggest_freq('评分人数', True)
        jieba.suggest_freq('详细介绍', True)
        jieba.suggest_freq('时长', True)
        jieba.suggest_freq('出生时间', True)

        jieba.suggest_freq('国土面积', True)
        jieba.suggest_freq('国民生产总值', True)
        jieba.suggest_freq('arearank', True)
        jieba.suggest_freq('最大城市', True)
        jieba.suggest_freq('foundingdate', True)
        jieba.suggest_freq('musicalArtist', True)

    def get_ner_objects(self, question):
        """
        based on the question, get the entity对问题进行实体识别
        :param question:·
        :return:
        """
        return [Word(word, tag) for word, tag in pseg.cut(question)]


if __name__ == '__main__':
    question_ner = QueryNER(['book_and_movie_name.txt', 'person_name.txt'])
    question = '郭帆导演的《流浪地球》好看吗?'
    ner_object = question_ner.get_ner_objects(question)
    for value in ner_object:
        print(value.token, value.pos)
