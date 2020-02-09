# -*- coding:utf-8 -*-

"""
rule based query generation
------------
singer
"""
from refo import Star, Any
from inference.basic_inference import W, Rule, KeywordRule
from inference.basic_inference import SPARQL_PREFIX, SPARQL_ASK_TEM, SPARQL_COUNT_TEM, SPARQL_SELECT_TEM,SPARQL_SELECT_TEM_FD
from inference.basic_inference import pos_person, pos_book_or_movie, pos_number, person_entity, book_or_movie_entity, number_entity, pos_country, country_entity, singer_entity, pos_singer,s_entity
from inference.basic_inference import SingerPropertyValueSet
import re
"""
singer information
"""
abstract = (W('abstract')|W('简介') )
birthDate = (W('birthday')|W('birthDate')|W('生日'))
birthName = (W('birthname')|W('birthName')|W('出生姓名')|W('本名'))
birthPlace = (W('birthplace')|W('birthPlace')|W('出生地') )
residence = (W('residence')|W('居住地') )
musicalArtist = (W('musicalArtist')|W('songs')|W('作品')|W('创作了'))

"""
SPARQL Template
"""
class QuestionSet:
    def __init__(self):
        pass

    @staticmethod
    def has_birthDate(word_objects):
        """
        what are the birth date of a singer
        :param word_objects:
        :return:
        """
        select = u"?x"
        sparql = None

        for w in word_objects:
            if w.pos == pos_singer:
                e_douban = u"?c rdfs:label '{singer}'@en.\n" \
                       u"?c dbo:birthDate ?l.\n" \
                       u"?l foaf:name ?x".format(singer=w.token)
                e_db = u"?c rdfs:label '{singer}'@en.\n" \
                       u"?c dbo:birthDate ?x.".format(singer=re.sub(r"(\w)([A-Z])", r"\1 \2", w.token))
                sparql = SPARQL_SELECT_TEM_FD.format(prefix=SPARQL_PREFIX,
                                                     select=select,
                                                     expression_douban=e_douban,
                                                     expression_db=e_db)

                break

        return sparql

    @staticmethod
    def has_musicalArtist(word_objects):
        """
        what are the musical arts of a singer
        """
        select = u"?l"
        sparql = None

        for w in word_objects:

            if w.pos == pos_singer:

                e_douban = u"?c rdfs:label '{singer}'@en.\n" \
                       u"?c dbo:musicalArtist ?l.\n" \
                       u"?l foaf:name ?x".format(singer=w.token)
                e_db = u"?c rdfs:label '{singer}'@en.\n" \
                       u"?x dbo:musicalArtist ?c.\n" \
                       u"?x dbp:title ?l".format(singer=re.sub(r"(\w)([A-Z])", r"\1 \2", w.token))
                sparql = SPARQL_SELECT_TEM_FD.format(prefix=SPARQL_PREFIX,
                                                     select=select,
                                                     expression_douban=e_douban,
                                                     expression_db=e_db)

                break

        return sparql


    @staticmethod
    def has_abstract(word_objects):
        """
        what are the abstract of a singer
        :param word_objects:
        :return:
        """
        select = u"?x"
        sparql = None

        for w in word_objects:
            if w.pos == pos_singer:
                e_douban = u"?c rdfs:label '{singer}'@en.\n" \
                       u"?c dbo:abstract ?l.\n" \
                       u"?l foaf:name ?x".format(singer=w.token)
                e_db = u"?c rdfs:label '{singer}'@en.\n" \
                       u"?c dbo:abstract ?x.".format(singer=re.sub(r"(\w)([A-Z])", r"\1 \2", w.token))
                sparql = SPARQL_SELECT_TEM_FD.format(prefix=SPARQL_PREFIX,
                                                     select=select,
                                                     expression_douban=e_douban,
                                                     expression_db=e_db)

                break

        return sparql

    @staticmethod
    def has_birthName(word_objects):
        """
        what are the birth name of a singer
        :param word_objects:
        :return:
        """
        select = u"?x"
        sparql = None

        for w in word_objects:
            if w.pos == pos_singer:
                e_douban = u"?c rdfs:label '{singer}'@en.\n" \
                       u"?c dbo:birthName ?l.\n" \
                       u"?l foaf:name ?x".format(singer=w.token)
                e_db = u"?c rdfs:label '{singer}'@en.\n" \
                       u"?c dbo:birthName ?x.".format(singer=re.sub(r"(\w)([A-Z])", r"\1 \2", w.token))
                sparql = SPARQL_SELECT_TEM_FD.format(prefix=SPARQL_PREFIX,
                                                     select=select,
                                                     expression_douban=e_douban,
                                                     expression_db=e_db)

                break

        return sparql



    @staticmethod
    def has_birthPlace(word_objects):
        """
        what are the birth place of a singer
        :param word_objects:
        :return:
        """
        select = u"?x"
        sparql = None

        for w in word_objects:
            if w.pos == pos_singer:
                e_douban = u"?c rdfs:label '{singer}'@en.\n" \
                       u"?c dbo:birthPlace ?l.\n" \
                       u"?l foaf:name ?x".format(singer=w.token)
                e_db = u"?c rdfs:label '{singer}'@en.\n" \
                       u"?c dbo:birthPlace ?a.\n" \
                       u"?a foaf:name ?x".format(singer=re.sub(r"(\w)([A-Z])", r"\1 \2", w.token))
                sparql = SPARQL_SELECT_TEM_FD.format(prefix=SPARQL_PREFIX,
                                                     select=select,
                                                     expression_douban=e_douban,
                                                     expression_db=e_db)

                break

        return sparql



    @staticmethod
    def has_residence(word_objects):
        """
        what are the residence of a singer
        :param word_objects:
        :return:
        """
        select = u"?x"
        sparql = None

        for w in word_objects:
            if w.pos == pos_singer:
                e_douban = u"?c rdfs:label '{singer}'@en.\n" \
                       u"?c dbo:residence ?l.\n" \
                       u"?l foaf:name ?x".format(singer=w.token)
                e_db = u"?c rdfs:label '{singer}'@en.\n" \
                       u"?c dbo:residence ?a.\n" \
                       u"?a foaf:name ?x".format(singer=re.sub(r"(\w)([A-Z])", r"\1 \2", w.token))
                sparql = SPARQL_SELECT_TEM_FD.format(prefix=SPARQL_PREFIX,
                                                     select=select,
                                                     expression_douban=e_douban,
                                                     expression_db=e_db)

                break

        return sparql





singer_info_rules_fd = [
    Rule(condition_num=13,
         condition=s_entity+Star(Any(), greedy=False) + birthDate + Star(Any(), greedy=False),
         action=QuestionSet.has_birthDate),
    Rule(condition_num=13,
         condition=s_entity + Star(Any(), greedy=False) + musicalArtist + Star(Any(), greedy=False),
         action=QuestionSet.has_musicalArtist),
    Rule(condition_num=13,
         condition=s_entity + Star(Any(), greedy=False) + abstract + Star(Any(), greedy=False),
         action=QuestionSet.has_abstract),
    Rule(condition_num=13,
         condition=s_entity + Star(Any(), greedy=False) + birthName + Star(Any(), greedy=False),
         action=QuestionSet.has_birthName),
    Rule(condition_num=13,
         condition=s_entity + Star(Any(), greedy=False) + birthPlace + Star(Any(), greedy=False),
         action=QuestionSet.has_birthPlace),
    Rule(condition_num=13,
         condition=s_entity + Star(Any(), greedy=False) + residence + Star(Any(), greedy=False),
         action=QuestionSet.has_residence),

]
