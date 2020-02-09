# -*- coding:utf-8 -*-

"""
rule based query generation
------------
movie
"""
from refo import Star, Any
from inference.basic_inference import W, Rule, KeywordRule
from inference.basic_inference import SPARQL_PREFIX, SPARQL_ASK_TEM, SPARQL_COUNT_TEM, SPARQL_SELECT_TEM,SPARQL_SELECT_TEM_FD
from inference.basic_inference import pos_person, pos_book_or_movie, pos_number, person_entity, book_or_movie_entity, number_entity
from inference.basic_inference import MoviePropertyValueSet
import re
"""
movie information
"""

movie = (W('movie')|W('movies')|W('film')|W('films')|W("电影") | W("影片") | W("片子") | W("片") | W("剧"))
actor = (W('cast')|W('act')|W('actor')|W('acts')|W('acted')|W('star')|W("演了") | W("出演") | W('主演'))
writer = (W('write')|W('wrote')|W('written')|W('writer')|W('编剧') | W('写作') | W('写了'))
director = (W('direct')|W('director')|W('directs')|W('directed')|W('导演') | W('指导'))
country = (W('country')|W('area')  |W('上映地区') | W('上映国家'))
language = (W('language')|W('语言') | W('上映语言'))
duration = (W('duration')|W('多长时间') | W('时长'))  # 时长
summary = (W('introduction') | W('abstract') |W('介绍') | W('简介'))  # 简介
movie_info = ( country | language  | duration | summary )
higher = (W("大于") | W("高于"))
lower = (W("小于") | W("低于"))
compare = (higher | lower)
when = (W("何时") | W("时候"))
where = (W("哪里") | W("哪儿") | W("何地") | W("何处") | W("在") + W("哪"))

"""
SPARQL Template
"""
class QuestionSet:
    def __init__(self):
        pass

    @staticmethod
    def has_movie_info(word_objects):
        """
        The basic information about a moive某电影的基本信息
        :param word_objects:
        :return:
        """
        keyword = None
        for r in basic_movie_info_fd:
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
            if w.pos == pos_book_or_movie:
                e_douban = u"?s :movie_info_name '{movie}'." \
                    u"?s {keyword} ?x.".format(movie=w.token, keyword=keyword_douban)
                e_db = u"?m rdfs:label '{movie}'@en.\n" \
                       u"?m dbo:starring ?p.\n" \
                       u"?m {keyword} ?x".format(movie=re.sub(r"(\w)([A-Z])", r"\1 \2", w.token), keyword=keyword_db)
                sparql = SPARQL_SELECT_TEM_FD.format(prefix=SPARQL_PREFIX,
                                                     select=select,
                                                     expression_douban=e_douban,
                                                     expression_db=e_db)

                break

        return sparql

    @staticmethod
    def has_actor(word_objects):
        """
        What are actors in a movie某电影有哪些演员
        :param word_objects:
        :return:
        """
        select = u"?x"
        sparql = None
        for w in word_objects:
            if w.pos == pos_book_or_movie:
                e_douban = u"?m :movie_info_name '{movie}'." \
                    u"?m :has_actor ?a." \
                    u"?a :movie_person_name ?x".format(movie=w.token)
                e_db = u"?m rdfs:label '{movie}'@en.\n" \
                       u"?m dbo:starring ?p.\n" \
                       u"?p foaf:name ?x".format(movie=re.sub(r"(\w)([A-Z])", r"\1 \2", w.token))
                sparql = SPARQL_SELECT_TEM_FD.format(prefix=SPARQL_PREFIX,
                                                     select=select,
                                                     expression_douban=e_douban,
                                                     expression_db=e_db)
                break

        return sparql

    @staticmethod
    def has_writer(word_objects):
        """
        What are writers in a movie某电影有哪些编剧
        :param word_objects:
        :return:
        """
        select = u"?x"
        sparql = None
        for w in word_objects:
            if w.pos == pos_book_or_movie:
                e_douban = u"?m :movie_info_name '{movie}'." \
                    u"?m :has_writer ?a." \
                    u"?a :movie_person_name ?x".format(movie=w.token)
                e_db = u"?m rdfs:label '{movie}'@en.\n" \
                       u"?m dbo:writer ?p.\n" \
                       u"?p foaf:name ?x".format(movie=re.sub(r"(\w)([A-Z])", r"\1 \2", w.token))
                sparql = SPARQL_SELECT_TEM_FD.format(prefix=SPARQL_PREFIX,
                                                     select=select,
                                                     expression_douban=e_douban,
                                                     expression_db=e_db)
                break

        return sparql

    @staticmethod
    def has_director(word_objects):
        """
        What a director in a moive某电影有哪些导演
        :param word_objects:
        :return:
        """
        select = u"?x"
        sparql = None
        for w in word_objects:
            if w.pos == pos_book_or_movie:
                e_douban = u"?m :movie_info_name '{movie}'.\n" \
                    u"?m :has_director ?a.\n" \
                    u"?a :movie_person_name ?x".format(movie=w.token)
                e_db = u"?m rdfs:label '{movie}'@en.\n" \
                       u"?m dbo:director ?p.\n" \
                       u"?p foaf:name ?x".format(movie=re.sub(r"(\w)([A-Z])", r"\1 \2", w.token))
                sparql = SPARQL_SELECT_TEM_FD.format(prefix=SPARQL_PREFIX,
                                                     select=select,
                                                     expression_douban=e_douban,
                                                     expression_db=e_db)
                break

        return sparql


movie_info_rules_fd = [
    Rule(condition_num=11, condition=book_or_movie_entity + Star(Any(), greedy=False) + movie_info + Star(Any(), greedy=False), action=QuestionSet.has_movie_info),
    Rule(condition_num=11,condition=(book_or_movie_entity + Star(Any(), greedy=False) + actor + Star(Any(), greedy=False)) | (actor + Star(Any(), greedy=False) + book_or_movie_entity + Star(Any(), greedy=False)), action=QuestionSet.has_actor),
    Rule(condition_num=11,condition=(book_or_movie_entity + Star(Any(), greedy=False) + writer + Star(Any(), greedy=False)) | (writer + Star(Any(), greedy=False) + book_or_movie_entity + Star(Any(), greedy=False)), action=QuestionSet.has_writer),
    Rule(condition_num=11,condition=(book_or_movie_entity + Star(Any(), greedy=False) + director + Star(Any(), greedy=False)) | (writer + Star(Any(), greedy=False) + book_or_movie_entity) + Star(Any(), greedy=False), action=QuestionSet.has_director),
]

basic_movie_info_fd = [
    KeywordRule(condition=(book_or_movie_entity + Star(Any(), greedy=False) + country + Star(Any(), greedy=False))|( country + Star(Any(), greedy=False) + book_or_movie_entity + Star(Any(), greedy=False)), action=MoviePropertyValueSet.return_movie_info_country_value_FD),
    KeywordRule(condition=(book_or_movie_entity + Star(Any(), greedy=False) + language + Star(Any(), greedy=False))|( language + Star(Any(), greedy=False) + book_or_movie_entity + Star(Any(), greedy=False)), action=MoviePropertyValueSet.return_movie_info_language_value_FD),
    KeywordRule(condition=(book_or_movie_entity + Star(Any(), greedy=False) + duration + Star(Any(), greedy=False))|( duration + Star(Any(), greedy=False) + book_or_movie_entity + Star(Any(), greedy=False)), action=MoviePropertyValueSet.return_movie_info_duration_value_FD),
    KeywordRule(condition=(book_or_movie_entity + Star(Any(), greedy=False) + summary + Star(Any(), greedy=False))|( summary + Star(Any(), greedy=False) + book_or_movie_entity + Star(Any(), greedy=False)), action=MoviePropertyValueSet.return_movie_info_summary_value_FD),
]
