# -*- coding:utf-8 -*-
"""
rule based query generation
------------
book person
"""
from refo import Star, Any
from inference.basic_inference import W, Rule, KeywordRule
from inference.basic_inference import SPARQL_PREFIX, SPARQL_ASK_TEM, SPARQL_COUNT_TEM, SPARQL_SELECT_TEM, SPARQL_SELECT_TEM_FD, SPARQL_COUNT_TEM_FD
from inference.basic_inference import pos_person, pos_book_or_movie, pos_number, person_entity, book_or_movie_entity, number_entity
from inference.basic_inference import BookPropertyValueSet
import re


book = (W('book')|W('书籍') | W('书') | W('图书'))
author = (W('write')|W('wrote')|W('writes')|W('写作') | W('写了') | W('写过')|W('author'))
translator = (W('translate')|W('translates')|W('翻译')|W('translator'))
image_url = (W('image')|W('poster')|W('picture')|W('cover')|W('海报') | W('图片') | W('封面'))
gender = (W('sex')|W('gender')|W('性别'))
birthday = (W('when') + W('born')|W('birthday')|W('birth') + W('date')|W('出生日期') | W("出生时间") | W('生日') | W('时间') + W('出生'))
birthplace = (W('birthplace')|W('where') + W('born')|W('出生地') | W('地点') + W('出生'))
other_name = (W('alternate')|W('other') + W('name')|W('nickname')|W('Chinese') + W('name')|W('English') + W('name')|W('其他名字') | W('其他名称') | W('别名') | W('中文名') | W('英文名'))
introduction = (W('introduction')|W('who')|W('简介') | W('自我介绍') | W('介绍') | W("是") + W("谁"))
detail_information = (W('detail') + W('information')|W('详细信息') | W('详细介绍'))
book_person_info = (gender | birthday | birthplace | introduction)
category = (W("category") |W("genre") |W("类型") | W("种类"))
several = (W("several") |W("how") + W("many") |("多少") | W("几部"))
higher = (W("higher") |W("大于") | W("高于"))
lower = (W("lower")|W("小于") | W("低于"))
compare = (higher | lower)

"""
SPARQL template
"""
class QuestionSet:
    def __init__(self):
        pass

    @staticmethod
    def has_book_person_info(word_objects):
        """
        author's basic information
        :return:
        """
        keyword = None
        for r in basic_book_person_fd:
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
            if w.pos == pos_person:
                e_douban = u"?p :book_person_name '{person}'.\n" \
                           u"?p {keyword} ?x.".format(person=w.token, keyword=keyword_douban)
                e_db = u"?p rdfs:label '{person}'@en.\n" \
                       u"?m dbo:author ?p.\n" \
                       u"?p {keyword} ?x".format(person=re.sub(r"(\w)([A-Z])", r"\1 \2", w.token), keyword=keyword_db)
                sparql = SPARQL_SELECT_TEM_FD.format(prefix=SPARQL_PREFIX,
                                                     select=select,
                                                     expression_douban=e_douban,
                                                     expression_db=e_db)
                break

        return sparql

    @staticmethod
    def has_authored_in(word_objects):
        """
        Who writes what books (e.g. Stephen King)
        :param word_objects:
        :return:
        """
        select = u"?x"
        sparql = None
        for w in word_objects:
            if w.pos == pos_person:
                e_douban = u"?p :book_person_name '{person}'." \
                    u"?p :has_authored_in ?b." \
                    u"?b :book_info_name ?x".format(person=w.token)
                e_db = u"?p rdfs:label '{person}'@en.\n" \
                    u"?m dbo:author ?p.\n" \
                    u"?m foaf:name ?x".format(person=re.sub(r"(\w)([A-Z])", r"\1 \2", w.token))
                sparql = SPARQL_SELECT_TEM_FD.format(prefix=SPARQL_PREFIX,
                                                  select=select,
                                                  expression_douban=e_douban,
                                                  expression_db=e_db)
                break

        return sparql

    @staticmethod
    def has_translated_in(word_objects):
        """
        who translate what books (e.g. Alfred Birnbaum)
        :param word_objects:
        :return:
        """
        select = u"?x"
        sparql = None
        for w in word_objects:
            if w.pos == pos_person:
                e_douban = u"?p :book_person_name '{person}'." \
                    u"?p :has_translated_in ?b." \
                    u"?b :book_info_name ?x".format(person=w.token)
                e_db = u"?p rdfs:label '{person}'@en.\n" \
                    u"?m dbo:translator ?p.\n" \
                    u"?m foaf:name ?x".format(person=re.sub(r"(\w)([A-Z])", r"\1 \2", w.token))
                sparql = SPARQL_SELECT_TEM_FD.format(prefix=SPARQL_PREFIX,
                                                     select=select,
                                                     expression_douban=e_douban,
                                                     expression_db=e_db)
                break

        return sparql

    @staticmethod
    def has_write_quantity_book(word_objects):
        """
        How many books does an author write
        :param word_objects:
        :return:
        """
        select = u"?x"
        sparql = None
        for w in word_objects:
            if w.pos == pos_person:
                e_db = u"?p rdfs:label '{person}'@en.\n" \
                       u"?m dbo:author ?p.\n" \
                       u"?m foaf:name ?x".format(person=re.sub(r"(\w)([A-Z])", r"\1 \2", w.token))
                e_douban = u"?p :book_person_name '{person}'." \
                    u"?p :has_authored_in ?b.\n" \
                    u"?b :book_info_name ?x".format(person=w.token)
                sparql = SPARQL_COUNT_TEM_FD.format(prefix=SPARQL_PREFIX,
                                                     select=select,
                                                     expression_douban=e_douban,
                                                     expression_db=e_db)
                break

        return sparql

    @staticmethod
    def has_translate_quantity_book(word_objects):
        """
        How many books does an author translate
        :param word_objects:
        :return:
        """
        select = u"?x"
        sparql = None
        for w in word_objects:
            if w.pos == pos_person:
                e_db = u"?p rdfs:label '{person}'@en.\n" \
                       u"?m dbo:translator ?p.\n" \
                       u"?m foaf:name ?x".format(person=re.sub(r"(\w)([A-Z])", r"\1 \2", w.token))
                e_douban = u"?p :book_person_name '{person}'." \
                    u"?p :has_translated_in ?b.\n" \
                    u"?b :book_info_name ?x".format(person=w.token)
                sparql = SPARQL_COUNT_TEM_FD.format(prefix=SPARQL_PREFIX,
                                                     select=select,
                                                     expression_douban=e_douban,
                                                     expression_db=e_db)
                break

        return sparql


book_person_rules_fd = [
    Rule(condition_num=7, condition=person_entity + Star(Any(), greedy=False) + book_person_info +  Star(Any(), greedy=False), action=QuestionSet.has_book_person_info),
    Rule(condition_num=7, condition=person_entity + Star(Any(), greedy=False) + author + Star(Any(), greedy=False), action=QuestionSet.has_authored_in),
    Rule(condition_num=7, condition=person_entity + Star(Any(), greedy=False) + translator + Star(Any(), greedy=False), action=QuestionSet.has_translated_in)
]

basic_book_person_fd = [
    KeywordRule(condition=person_entity + Star(Any(), greedy=False) + gender + Star(Any(), greedy=False), action=BookPropertyValueSet.return_book_person_gender_value_FD),
    KeywordRule(condition=person_entity + Star(Any(), greedy=False) + birthday + Star(Any(), greedy=False), action=BookPropertyValueSet.return_book_person_birthday_value_FD),
    KeywordRule(condition=person_entity + Star(Any(), greedy=False) + birthplace + Star(Any(), greedy=False), action=BookPropertyValueSet.return_book_person_birthplace_value_FD),
    KeywordRule(condition=person_entity + Star(Any(), greedy=False) + introduction + Star(Any(), greedy=False), action=BookPropertyValueSet.return_book_person_introduction_value_FD)
]