# -*- coding:utf-8 -*-

"""
rule based query generation
------------
river
"""
from refo import Star, Any
from query.inference.basic_inference import W, Rule, KeywordRule
from query.inference.basic_inference import SPARQL_PREFIX, SPARQL_SELECT_TEM_FD
from query.inference.basic_inference import river_entity, pos_river
from query.inference.basic_inference import RiverPropertyValueSet
import re

"""
river information
"""

summary = (W('introduction') | W('abstract') | W('介绍') | W('简介'))
country = W('country')
river = W('river')
source = (W('source') | W('start'))
river_info = (summary | country | river | source)

"""
SPARQL Template
"""


class QuestionSet:
    def __init__(self):
        pass

    @staticmethod
    def has_country(word_objects):
        """
        source country of a river
        :param word_objects:
        :return:
        """

        select = u"?x"
        sparql = None
        for w in word_objects:
            if w.pos == pos_river:
                e_douban = u"?c rdfs:label '{river}'@en.\n" \
                           u"?c dbo:sourceCountry ?l.\n" \
                           u"?l foaf:name ?x".format(river=w.token)

                e_db = u"?c rdfs:label '{river}'@en.\n" \
                       u"?c dbo:sourceCountry ?l.\n" \
                       u"?l foaf:name ?x".format(river=re.sub(r"(\w)([A-Z])", r"\1 \2", w.token))

                sparql = SPARQL_SELECT_TEM_FD.format(prefix=SPARQL_PREFIX,
                                                     select=select,
                                                     expression_douban=e_douban,
                                                     expression_db=e_db)

                break

        return sparql

    @staticmethod
    def has_river(word_objects):
        """
        source river
        :param word_objects:
        :return:
        """

        select = u"?x"
        sparql = None
        for w in word_objects:
            if w.pos == pos_river:
                e_douban = u"?c rdfs:label '{river}'@en.\n" \
                           u"?c dbo:river ?l.\n" \
                           u"?l foaf:name ?x".format(river=w.token)

                e_db = u"?c rdfs:label '{river}'@en.\n" \
                       u"?c dbo:river ?l.\n" \
                       u"?l foaf:name ?x".format(river=re.sub(r"(\w)([A-Z])", r"\1 \2", w.token))

                sparql = SPARQL_SELECT_TEM_FD.format(prefix=SPARQL_PREFIX,
                                                     select=select,
                                                     expression_douban=e_douban,
                                                     expression_db=e_db)

                break

        return sparql

    @staticmethod
    def has_source(word_objects):
        """
        source of river
        :param word_objects:
        :return:
        """

        select = u"?x"
        sparql = None
        for w in word_objects:
            if w.pos == pos_river:
                e_douban = u"?c rdfs:label '{river}'@en.\n" \
                           u"?c dbo:source ?l.\n" \
                           u"?l foaf:name ?x".format(river=w.token)

                e_db = u"?c rdfs:label '{river}'@en.\n" \
                       u"?c dbo:source ?l.\n" \
                       u"?l foaf:name ?x".format(river=re.sub(r"(\w)([A-Z])", r"\1 \2", w.token))

                sparql = SPARQL_SELECT_TEM_FD.format(prefix=SPARQL_PREFIX,
                                                     select=select,
                                                     expression_douban=e_douban,
                                                     expression_db=e_db)

                break

        return sparql


river_info_rules_fd = [
    Rule(condition_num=12,
         condition=(river_entity + Star(Any(), greedy=False) + country + Star(Any(), greedy=False)) | (
                 country + Star(Any(), greedy=False) + river_entity + Star(Any(), greedy=False)),
         action=QuestionSet.has_country),
    Rule(condition_num=12,
         condition=(river_entity + Star(Any(), greedy=False) + river + Star(Any(), greedy=False)) | (
                 river + Star(Any(), greedy=False) + river_entity + Star(Any(), greedy=False)),
         action=QuestionSet.has_river),
    Rule(condition_num=12,
         condition=(river_entity + Star(Any(), greedy=False) + source + Star(Any(), greedy=False)) | (
                 source + Star(Any(), greedy=False) + river_entity + Star(Any(), greedy=False)),
         action=QuestionSet.has_source),
]

basic_country_info_fd = [
    KeywordRule(condition=river_entity + Star(Any(), greedy=False) + country + Star(Any(), greedy=False),
                action=RiverPropertyValueSet.return_river_info_sourcecountry_FD),
    KeywordRule(condition=river_entity + Star(Any(), greedy=False) + river + Star(Any(), greedy=False),
                action=RiverPropertyValueSet.return_river_info_rivername_FD),
    KeywordRule(condition=river_entity + Star(Any(), greedy=False) + summary + Star(Any(), greedy=False),
                action=RiverPropertyValueSet.return_river_info_summary_FD),
    KeywordRule(condition=river_entity + Star(Any(), greedy=False) + source + Star(Any(), greedy=False),
                action=RiverPropertyValueSet.return_river_info_sourcename_FD),
]
