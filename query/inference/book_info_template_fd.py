# -*- coding:utf-8 -*-
"""
rule based query generation
------------
book
"""
from refo import Star, Any
from inference.basic_inference import W, Rule, KeywordRule
from inference.basic_inference import SPARQL_PREFIX, SPARQL_ASK_TEM, SPARQL_COUNT_TEM, SPARQL_SELECT_TEM, SPARQL_SELECT_TEM_FD
from inference.basic_inference import pos_person, pos_book_or_movie, pos_number, person_entity, book_or_movie_entity, number_entity
from inference.basic_inference import BookPropertyValueSet
import re


plot = (W('剧情') | W('剧情片') | W('plot'))
disaster = (W('灾难') | W('灾难片')|W('disaster'))
music = (W('音乐') | W('音乐片')|W('music'))
absurd = (W('荒诞') | W('荒诞片'))
motion = (W('运动') | W('运动片')|W('motion'))
west = (W('西部') | W('西部片'))
opera = (W('戏曲') | W('戏曲片')|W('opera'))
science = (W('科幻') | W('科幻片')|W('sci-fi'))
history = (W('历史') | W('历史片')|W('history'))
martial_arts = (W('武侠') | W('武侠片'))
adventure = (W('冒险') | W('冒险片')|W('adventure'))
biography = (W('传记') | W('传记片')|W('biography'))
musical = (W('歌舞') | W('歌舞片'))
fantasy = (W('奇幻') | W('奇幻片')|W('fantasy'))
crime = (W('犯罪') | W('犯罪片')|W('crime'))
action = (W('动作') | W('动作片')|W('action'))
costume = (W('古装') | W('古装片'))
horror = (W('恐怖') | W('恐怖片')|W('horror'))
love = (W('爱情') | W('爱情片')|W('love'))
short = (W('短片'))
ghosts = (W('鬼怪') | W('鬼怪片') | W('鬼神') | W('鬼神片'))
suspense = (W('悬念') | W('悬念片'))
child = (W('儿童') | W('儿童片'))
mystery = (W("悬疑") | W("悬疑片"))
war = (W('战争') | W('战争片'))
thriller = (W('惊悚') | W('惊悚片'))
comedy = (W('喜剧') | W('喜剧片'))
erotic = (W('情色') | W('情色片'))
gay = (W('同性') | W('同性片'))
family = (W('家庭') | W('家庭片'))
animation = (W('动画') | W('动画片'))
reality_show = (W('真人秀'))
documentary = (W('纪录') | W('纪录片'))
talk_show = (W('脱口秀'))
stagecraft = (W('舞台艺术'))
film_noir = (W('黑色电影'))
genre = (plot | disaster | music | absurd | motion | west | opera | science
         | history | martial_arts | adventure | biography | musical | fantasy
         | crime | action | costume | horror | love | short | ghosts | suspense
         | child | mystery | war | thriller | comedy | erotic | gay | family
         | animation | reality_show | documentary | talk_show | stagecraft | film_noir)
book = (W('book')|W('书籍') | W('书') | W('图书'))
category = (W("类型") | W("种类") | W('类别')| W('genre')|W('category'))
author = (W('write')|W('wrote')|W('writes')|W('写作') | W('写了') | W('写过')|W('author'))
translator = (W('translate')|W('translates')|W('翻译')|W('translator'))
image_url = (W('image')|W('poster')|W('picture')|W('cover')|W('海报') | W('图片') | W('封面'))
press = (W('出版社')|W('publisher'))  # 出版社
publish_year = (W('出版日期') | W('出版') | W('发布时间')|W('publish') + W('date'))
page_num = (W('页') | W('页数')|W('page') + W('number'))
price = (W('价格') | W('价钱') | W('多少钱')|W('price'))
content_abstract = (W('内容') | W('简介') | W('内容简介') | W('主要内容')|W('introduction'))
catalog = (W('目录') | W('大纲')|W('catalog'))
rating = (W('评分') | W('分') | W('分数')|W('rating'))
review_count = (W('评分人数') | W('人数'))
detail_information = (W('详细信息') | W('详细介绍')|W('detail'))
rating_basic = (rating | review_count)
book_info = (image_url | press | publish_year | page_num | price | content_abstract | catalog | rating | review_count)
higher = (W("大于") | W("高于"))
lower = (W("小于") | W("低于"))
compare = (higher | lower)
when = (W("何时") | W("时候"))
where = (W("哪里") | W("哪儿") | W("何地") | W("何处") | W("在") + W("哪"))

"""
SPARQL template
"""
class QuestionSet:
    def __init__(self):
        pass

    @staticmethod
    def has_book_info(word_objects):
        """
        Basic information of book
        :param word_objects:
        :return:
        """
        for r in basic_book_info_fd:
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
                e_douban = u"?b :book_info_name '{book}'." \
                    u"?b {keyword} ?x.".format(book=w.token, keyword=keyword_douban)
                e_db = u"?m rdfs:label '{book}'@en.\n" \
                       u"?m dbo:author ?p.\n" \
                       u"?m {keyword} ?x".format(book=re.sub(r"(\w)([A-Z])", r"\1 \2", w.token), keyword=keyword_db)
                sparql = SPARQL_SELECT_TEM_FD.format(prefix=SPARQL_PREFIX,
                                                     select=select,
                                                     expression_douban=e_douban,
                                                     expression_db=e_db)

                break

        return sparql

    @staticmethod
    def has_book_genre(word_objects):
        """
        what is the genre of a book
        :param word_objects:
        :return:
        """
        select = u"?x"
        sparql = None
        for w in word_objects:
            if w.pos == pos_book_or_movie:
                e_douban = u"?b :book_info_name '{book}'." \
                            u"?b :has_book_genre ?g."\
                            u"?g :book_genre_name ?x".format(book=w.token)
                e_db = u"?m rdfs:label '{book}'@en.\n" \
                       u"?m dbo:literaryGenre ?p.\n" \
                       u"?p foaf:name ?x".format(book=re.sub(r"(\w)([A-Z])", r"\1 \2", w.token))
                sparql = SPARQL_SELECT_TEM_FD.format(prefix=SPARQL_PREFIX,
                                                     select=select,
                                                     expression_douban=e_douban,
                                                     expression_db=e_db)
                break

        return sparql

    @staticmethod
    def has_author(word_objects):
        """
        what are the author of books
        :param word_objects:
        :return:
        """
        select = u"?x"
        sparql = None
        for w in word_objects:
            if w.pos == pos_book_or_movie:
                e_douban = u"?b :book_info_name '{book}'." \
                    u"?b :has_author ?a." \
                    u"?a :book_person_name ?x".format(book=w.token)
                e_db = u"?m rdfs:label '{book}'@en.\n" \
                       u"?m dbo:author ?p.\n" \
                       u"?p foaf:name ?x".format(book=re.sub(r"(\w)([A-Z])", r"\1 \2", w.token))
                sparql = SPARQL_SELECT_TEM_FD.format(prefix=SPARQL_PREFIX,
                                                     select=select,
                                                     expression_douban=e_douban,
                                                     expression_db=e_db)
                break
        return sparql

    @staticmethod
    def has_translator(word_objects):
        """
        what are the translator of book?
        :param word_objects:
        :return:
        """
        select = u"?x"
        sparql = None
        for w in word_objects:
            if w.pos == pos_book_or_movie:
                e_douban = u"?b :book_info_name '{book}'." \
                    u"?b :has_translator ?a." \
                    u"?a :book_person_name ?x".format(book=w.token)
                e_db = u"?m rdfs:label '{book}'@en.\n" \
                       u"?m dbo:translator ?p.\n" \
                       u"?p foaf:name ?x".format(book=re.sub(r"(\w)([A-Z])", r"\1 \2", w.token))
                sparql = SPARQL_SELECT_TEM_FD.format(prefix=SPARQL_PREFIX,
                                                     select=select,
                                                     expression_douban=e_douban,
                                                     expression_db=e_db)
                break
        return sparql


book_info_rules_fd = [
    Rule(condition_num=3, condition=book_or_movie_entity + Star(Any(), greedy=False) + book_info + Star(Any(), greedy=False), action=QuestionSet.has_book_info),
    Rule(condition_num=3, condition=book_or_movie_entity + Star(Any(), greedy=False) + category + Star(Any(), greedy=False), action=QuestionSet.has_book_genre),
    Rule(condition_num=3, condition=book_or_movie_entity + Star(Any(), greedy=False) + author + Star(Any(), greedy=False), action=QuestionSet.has_author),
    Rule(condition_num=3, condition=book_or_movie_entity + Star(Any(), greedy=False) + translator + Star(Any(), greedy=False), action=QuestionSet.has_translator)
]

basic_book_info_fd = [
    KeywordRule(condition=book_or_movie_entity + Star(Any(), greedy=False) + press + Star(Any(), greedy=False),action=BookPropertyValueSet.return_book_info_press_value_FD),
    KeywordRule(condition=book_or_movie_entity + Star(Any(), greedy=False) + publish_year + Star(Any(), greedy=False),action=BookPropertyValueSet.return_book_info_publish_year_value),
    KeywordRule(condition=book_or_movie_entity + Star(Any(), greedy=False) + page_num + Star(Any(), greedy=False),action=BookPropertyValueSet.return_book_info_page_num_value),
    KeywordRule(condition=book_or_movie_entity + Star(Any(), greedy=False) + price + Star(Any(), greedy=False),action=BookPropertyValueSet.return_book_info_price_value),
    KeywordRule(condition=book_or_movie_entity + Star(Any(), greedy=False) + content_abstract + Star(Any(), greedy=False),action=BookPropertyValueSet.return_book_info_content_abstract_value_FD),
    KeywordRule(condition=book_or_movie_entity + Star(Any(), greedy=False) + catalog + Star(Any(), greedy=False),action=BookPropertyValueSet.return_book_info_catalog_value),
    KeywordRule(condition=book_or_movie_entity + Star(Any(), greedy=False) + rating + Star(Any(), greedy=False),action=BookPropertyValueSet.return_book_info_rating_value),
    KeywordRule(condition=book_or_movie_entity + Star(Any(), greedy=False) + review_count + Star(Any(), greedy=False),action=BookPropertyValueSet.return_book_info_review_count_value)
]