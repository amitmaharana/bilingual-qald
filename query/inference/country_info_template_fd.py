# -*- coding:utf-8 -*-

"""
rule based query generation
------------
country
"""
from refo import Star, Any
from inference.basic_inference import W, Rule, KeywordRule
from inference.basic_inference import SPARQL_PREFIX, SPARQL_ASK_TEM, SPARQL_COUNT_TEM, SPARQL_SELECT_TEM,SPARQL_SELECT_TEM_FD
from inference.basic_inference import pos_person, pos_book_or_movie, pos_number, person_entity, book_or_movie_entity, number_entity, pos_country, country_entity
from inference.basic_inference import CountryPropertyValueSet
import re

"""
country information
"""
population = (W('population')|W('人口') )
areatotal = (W('size')|W('how')+W('large')|W('多大')|W('面积')|W('国土面积'))
foundingdate = (W('foundingdate')|W('建国日'))
longname = (W('longname')|W('全称'))
summary = (W('introduction') | W('abstract') |W('介绍') | W('简介'))
currency =(W('currency')|W('货币'))
language = (W('language')|W('语言'))
capital = (W('capital')|W('首都') | W('行政中心'))
leader = (W('leader')|W('leaders')|W('领导人'))
largestcity = (W('最大城市'))
largest = W('largest')
city = W('city')
country_info = (foundingdate | population | areatotal | longname | summary | currency)

"""
SPARQL Template
"""
class QuestionSet:
    def __init__(self):
        pass

    @staticmethod
    def has_country_info(word_objects):
        """
        The basic information about a country
        :param word_objects:
        :return:
        """
        keyword = None
        for r in basic_country_info_fd:
            keyword = r.apply(word_objects)
            if keyword is not None:
                keyword_split = re.split("( )+", keyword)
                keyword_db = keyword_split.pop()
                keyword_split.pop()
                keyword_douban = keyword_split.pop()
                break

        select = u"?x"
        sparql = None
        for w in word_objects:
            if w.pos == pos_country:
                e_douban = u"?c rdfs:label '{country}'@en." \
                    u"?c {keyword} ?x.".format(country=w.token, keyword=keyword_douban)
                e_db = u"?c rdfs:label '{country}'@en.\n" \
                       u"?c {keyword} ?x".format(country=re.sub(r"(\w)([A-Z])", r"\1 \2", w.token), keyword=keyword_db)
                sparql = SPARQL_SELECT_TEM_FD.format(prefix=SPARQL_PREFIX,
                                                     select=select,
                                                     expression_douban=e_douban,
                                                     expression_db=e_db)

                break

        return sparql

    @staticmethod
    def has_largestcity(word_objects):
        """
        largestcity of a country
        :param word_objects:
        :return:
        """

        select = u"?x"
        sparql = None
        for w in word_objects:
            if w.pos == pos_country:
                e_douban = u"?c rdfs:label '{country}'@en.\n" \
                       u"?c dbo:largestCity ?l.\n" \
                       u"?l foaf:name ?x".format(country=w.token)
                e_db = u"?c rdfs:label '{country}'@en.\n" \
                       u"?c dbo:largestCity ?l.\n" \
                       u"?l foaf:name ?x".format(country=re.sub(r"(\w)([A-Z])", r"\1 \2", w.token))
                sparql = SPARQL_SELECT_TEM_FD.format(prefix=SPARQL_PREFIX,
                                                     select=select,
                                                     expression_douban=e_douban,
                                                     expression_db=e_db)

                break

        return sparql

    @staticmethod
    def has_capital(word_objects):
        """
        largestcity of a country
        :param word_objects:
        :return:
        """
        select = u"?x"
        sparql = None
        for w in word_objects:
            if w.pos == pos_country:
                e_douban = u"?c rdfs:label '{country}'@en.\n" \
                       u"?c dbo:capital ?l.\n" \
                       u"?l foaf:name ?x".format(country=w.token)
                e_db = u"?c rdfs:label '{country}'@en.\n" \
                       u"?c dbo:capital ?l.\n" \
                       u"?l foaf:name ?x".format(country=re.sub(r"(\w)([A-Z])", r"\1 \2", w.token))
                sparql = SPARQL_SELECT_TEM_FD.format(prefix=SPARQL_PREFIX,
                                                     select=select,
                                                     expression_douban=e_douban,
                                                     expression_db=e_db)

                break

        return sparql

    @staticmethod
    def has_language(word_objects):
        """
        largestcity of a country
        :param word_objects:
        :return:
        """
        select = u"?x"
        sparql = None
        for w in word_objects:
            if w.pos == pos_country:

                e_douban = u"?c rdfs:label '{country}'@en.\n" \
                       u"?c dbo:language ?l.\n" \
                       u"?l foaf:name ?x".format(country=w.token)
                e_db = u"?c rdfs:label '{country}'@en.\n" \
                       u"?c dbo:language ?l.\n" \
                       u"?l foaf:name ?x".format(country=re.sub(r"(\w)([A-Z])", r"\1 \2", w.token))
                sparql = SPARQL_SELECT_TEM_FD.format(prefix=SPARQL_PREFIX,
                                                     select=select,
                                                     expression_douban=e_douban,
                                                     expression_db=e_db)

                break

        return sparql

    @staticmethod
    def has_leader(word_objects):
        """
        largestcity of a country
        :param word_objects:
        :return:
        """
        select = u"?x"
        sparql = None
        for w in word_objects:
            if w.pos == pos_country:
                e_douban = u"?c rdfs:label '{country}'@en.\n" \
                       u"?c dbo:leader ?l.\n" \
                       u"?l foaf:name ?x".format(country=w.token)
                e_db = u"?c rdfs:label '{country}'@en.\n" \
                       u"?c dbo:leader ?l.\n" \
                       u"?l foaf:name ?x".format(country=re.sub(r"(\w)([A-Z])", r"\1 \2", w.token))
                sparql = SPARQL_SELECT_TEM_FD.format(prefix=SPARQL_PREFIX,
                                                     select=select,
                                                     expression_douban=e_douban,
                                                     expression_db=e_db)

                break

        return sparql


country_info_rules_fd = [
    Rule(condition_num=12,condition=(country_entity + Star(Any(), greedy=False) + leader + Star(Any(), greedy=False))|(leader + Star(Any(), greedy=False) + country_entity + Star(Any(), greedy=False)), action=QuestionSet.has_leader),
    Rule(condition_num=12,condition=(country_entity + Star(Any(), greedy=False) + capital + Star(Any(), greedy=False))|(capital + Star(Any(), greedy=False) + country_entity + Star(Any(), greedy=False)), action=QuestionSet.has_capital),
    Rule(condition_num=12,condition=(country_entity + Star(Any(), greedy=False) + language + Star(Any(), greedy=False))|(language + Star(Any(), greedy=False) + country_entity + Star(Any(), greedy=False)), action=QuestionSet.has_language),
    Rule(condition_num=12,condition=(country_entity + Star(Any(), greedy=False) + country_info + Star(Any(), greedy=False))|(country_info + Star(Any(), greedy=False) + country_entity + Star(Any(), greedy=False)), action=QuestionSet.has_country_info),
    Rule(condition_num=12,condition=(country_entity + Star(Any(), greedy=False) + largestcity + Star(Any(), greedy=False))|(largestcity + Star(Any(), greedy=False) + country_entity + Star(Any(), greedy=False))|(largest+ Star(Any(), greedy=False)+city + Star(Any(), greedy=False) + country_entity + Star(Any(), greedy=False)) |(country_entity + Star(Any(), greedy=False)+largest+ Star(Any(), greedy=False)+city + Star(Any(), greedy=False)), action=QuestionSet.has_largestcity),
]

basic_country_info_fd = [
    KeywordRule(condition=country_entity + Star(Any(), greedy=False) + foundingdate + Star(Any(), greedy=False), action=CountryPropertyValueSet.return_country_info_foundingdate_FD),
    KeywordRule(condition=country_entity + Star(Any(), greedy=False) + longname + Star(Any(), greedy=False), action=CountryPropertyValueSet.return_country_info_longname_FD),
    KeywordRule(condition=country_entity + Star(Any(), greedy=False) + summary + Star(Any(), greedy=False), action=CountryPropertyValueSet.return_country_info_summary_FD),
    KeywordRule(condition=country_entity + Star(Any(), greedy=False) + currency + Star(Any(), greedy=False), action=CountryPropertyValueSet.return_country_info_currency_FD),
    KeywordRule(condition=country_entity + Star(Any(), greedy=False) + population + Star(Any(), greedy=False), action=CountryPropertyValueSet.return_country_info_population_FD),
    KeywordRule(condition=country_entity + Star(Any(), greedy=False) + areatotal + Star(Any(), greedy=False), action=CountryPropertyValueSet.return_country_info_areatotal_FD),
]
