# -*- coding:utf-8 -*-

"""
rule based query generation
------------
movie person
"""

from refo import Star, Any
from inference.basic_inference import W, Rule, KeywordRule
from inference.basic_inference import SPARQL_PREFIX, SPARQL_ASK_TEM, SPARQL_COUNT_TEM, SPARQL_SELECT_TEM, SPARQL_SELECT_TEM_FD,SPARQL_COUNT_TEM_FD
from inference.basic_inference import pos_person, pos_book_or_movie, pos_number, person_entity, book_or_movie_entity, number_entity
from inference.basic_inference import MoviePropertyValueSet
import re

"""
movie information category
"""
movie = (W('movie')|W('movies')|W('film')|W('films')|W("电影") | W("影片") | W("片子") | W("片") | W("剧"))
director = (W('direct')|W('director')|W('directs')|W('directed')|W('导演') | W('指导'))
writer = (W('write')|W('wrote')|W('written')|W('writer')|W('编剧') | W('写作') | W('写了'))
actor = (W('act')|W('actor')|W('acts')|W('acted')|W('star')|W("演了") | W("出演") | W('主演'))
gender = (W('sex')|W('gender')|W('性别'))
birthday = (W('when') + W('born')|W('birthday')|W('出生日期') | W("出生时间") | W('生日') | W('时间') + W('出生'))
birthplace = (W('where') + W('born')|W('birthplace')|W('出生地') | W('地点') + W('出生'))
profession = (W('occupation')|W('profession')|W('职业') | W('工作'))
introduction = (W('introduction') | W('abstract') |W('简介') | W('个人简介') | W('自我介绍'))
movie_person_info = (gender | birthday | birthplace | profession | introduction)
category = (W("category") |W("类型") | W("种类"))
several = (W("several") | W("many")|W("多少") | W("几部"))
higher = (W("higher") |W("大于") | W("高于"))
lower = (W("lower")|W("小于") | W("低于"))
compare = (higher | lower)
when = (W("when")|W("何时") | W("时候"))
where = (W("where")|W("哪里") | W("哪儿") | W("何地") | W("何处") | W("在") + W("哪"))


class QuestionSet:
    def __init__(self):
        pass

    @staticmethod
    def has_movie_person_info(word_objects):
        """
        someone's basic information
        :param word_objects:
        :return:
        """
        keyword = None
        for r in basic_movie_person_fd:
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
                e_douban = u"?p :movie_person_name '{person}'.\n" \
                    u"?p {keyword} ?x.".format(person=w.token, keyword=keyword_douban)
                e_db = u"?p rdfs:label '{person}'@en.\n" \
                       u"?m dbo:starring ?p.\n" \
                       u"?p {keyword} ?x".format(person=re.sub(r"(\w)([A-Z])", r"\1 \2", w.token),keyword=keyword_db)
                sparql = SPARQL_SELECT_TEM_FD.format(prefix=SPARQL_PREFIX,
                                                     select=select,
                                                     expression_douban=e_douban,
                                                     expression_db=e_db)
                break

        return sparql

    @staticmethod
    def has_acted_in(word_objects):
        """
        what movies does someone act in?
        :param word_objects:
        :return:
        """
        select = u"?x"
        sparql = None
        for w in word_objects:
            if w.pos == pos_person:
                e_db = u"?p rdfs:label '{person}'@en.\n" \
                    u"?m dbo:starring ?p.\n" \
                    u"?m foaf:name ?x".format(person=re.sub(r"(\w)([A-Z])", r"\1 \2", w.token))
                e_douban = u"?p :movie_person_name '{person}'.\n" \
                    u"?p :has_acted_in ?m.\n" \
                    u"?m :movie_info_name ?x".format(person=w.token)
                sparql = SPARQL_SELECT_TEM_FD.format(prefix=SPARQL_PREFIX,
                                                     select=select,
                                                     expression_douban=e_douban,
                                                     expression_db=e_db)


                break

        return sparql

    @staticmethod
    def has_writed_in(word_objects):
        """
        what movies does someone write?
        :param word_objects:
        :return:
        """
        select = u"?x"
        sparql = None
        for w in word_objects:
            if w.pos == pos_person:
                e_douban = u"?p :movie_person_name '{person}'.\n" \
                    u"?p :has_writed_in ?m.\n" \
                    u"?m :movie_info_name ?x".format(person=w.token)
                e_db = u"?p rdfs:label '{person}'@en.\n" \
                    u"?m dbo:writer ?p.\n" \
                    u"?m foaf:name ?x".format(person=re.sub(r"(\w)([A-Z])", r"\1 \2", w.token))
                sparql = SPARQL_SELECT_TEM_FD.format(prefix=SPARQL_PREFIX,
                                                     select=select,
                                                     expression_douban=e_douban,
                                                     expression_db=e_db)
                break

        return sparql

    @staticmethod
    def has_directed_in(word_objects):
        """
        Which movies does a director direct?某人导演了哪些电影
        :param word_objects:
        :return:
        """
        select = u"?x"
        sparql = None
        for w in word_objects:
            if w.pos == pos_person:
                e_douban = u"?p :movie_person_name '{person}'.\n" \
                    u"?p :has_directed_in ?m.\n" \
                    u"?m :movie_info_name ?x".format(person=w.token)
                e_db = u"?p rdfs:label '{person}'@en.\n" \
                    u"?m dbo:director ?p.\n" \
                    u"?m foaf:name ?x".format(person=re.sub(r"(\w)([A-Z])", r"\1 \2", w.token))
                sparql = SPARQL_SELECT_TEM_FD.format(prefix=SPARQL_PREFIX,
                                                     select=select,
                                                     expression_douban=e_douban,
                                                     expression_db=e_db)
                break

        return sparql

    @staticmethod
    def has_act_quantity_movie(word_objects):
        """
        How many movies does an actor star in/某演员演了多少部电影
        :param word_objects:
        :return:
        """
        select = u"?x"
        sparql = None
        for w in word_objects:
            if w.pos == pos_person:
                e_db = u"?p rdfs:label '{person}'@en.\n" \
                       u"?m dbo:starring ?p.\n" \
                       u"?m foaf:name ?x".format(person=re.sub(r"(\w)([A-Z])", r"\1 \2", w.token))
                e_douban = u"?p :movie_person_name '{person}'.\n" \
                           u"?p :has_acted_in ?m.\n" \
                           u"?m :movie_info_name ?x".format(person=w.token)
                sparql = SPARQL_COUNT_TEM_FD.format(prefix=SPARQL_PREFIX,
                                                     select=select,
                                                     expression_douban=e_douban,
                                                     expression_db=e_db)
                break
        print(sparql)
        return sparql


movie_person_rules_fd = [
    Rule(condition_num=6, condition=several + Star(Any(), greedy=False)+person_entity + Star(Any(), greedy=False) + actor + Star(Any(), greedy=False), action=QuestionSet.has_act_quantity_movie),
    Rule(condition_num=6, condition=person_entity + Star(Any(), greedy=False) + movie_person_info + Star(Any(), greedy=False), action=QuestionSet.has_movie_person_info),
    Rule(condition_num=6, condition=person_entity + Star(Any(), greedy=False) + director + Star(Any(), greedy=False), action=QuestionSet.has_directed_in),
    Rule(condition_num=6, condition=person_entity + Star(Any(), greedy=False) + writer + Star(Any(), greedy=False), action=QuestionSet.has_writed_in),
    Rule(condition_num=6, condition=person_entity + Star(Any(), greedy=False) + actor + Star(Any(), greedy=False), action=QuestionSet.has_acted_in),
]

basic_movie_person_fd = [
    KeywordRule(condition=person_entity + Star(Any(), greedy=False) + gender + Star(Any(), greedy=False), action=MoviePropertyValueSet.return_movie_person_gender_value_FD),
    KeywordRule(condition=person_entity + Star(Any(), greedy=False) + birthday + Star(Any(), greedy=False), action=MoviePropertyValueSet.return_movie_person_birthday_value_FD),
    KeywordRule(condition=person_entity + Star(Any(), greedy=False) + birthplace + Star(Any(), greedy=False), action=MoviePropertyValueSet.return_movie_person_birthplace_value_FD),
    KeywordRule(condition=person_entity + Star(Any(), greedy=False) + profession + Star(Any(), greedy=False), action=MoviePropertyValueSet.return_movie_person_profession_value_FD),
    KeywordRule(condition=person_entity + Star(Any(), greedy=False) + introduction + Star(Any(), greedy=False), action=MoviePropertyValueSet.return_movie_person_introduction_value_FD)
]