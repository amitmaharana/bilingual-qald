# -*- coding:utf-8 -*-

"""
The piple of query generation
"""
from ner.query_ner import QueryNER
from inference.query2sparql import Query2Sparql
from fuseki.sparql_query import SparqlQuery
from optimize.result import OptimizeResult


class Query:
    def __init__(self):
        """
        Initial
        """

        # Initial Jena Fuseki server
        self.sparql_query = SparqlQuery()

        # NER initial and load keywords
        self.query_ner = QueryNER(
            ['ner/book_and_movie_name.txt', 'ner/person_name.txt', 'ner/country_name.txt', 'ner/river.txt',
             'ner/singer.txt'])

        # initial load reference model
        self.query2sparql = Query2Sparql()

        # Optimize return results
        self.optimize_result = OptimizeResult()
        print("Query Initialization Complete/Query初始化完成...")
        print("This is your bilingual assistant FACX, please ask me a question/我是你的双语虚拟助手FACX ")
        print("If you don't know questions, please type 'template'/输入问答查看问题模板/type 'mix' to see bilingual template")

    def parse(self, question):
        """
        main parse process
        :return:
        """
        if "问答" in str(question, encoding='utf-8'):
            result = "你好, 你可以问我关于电影、书籍领域的问题. 比如:\n" \
                     "1. 江湖的主演/导演/编剧/上映地区/上映时间/时长/简介是什么？\n" \
                     "2. 李连杰的性别/生日/出生地/职业/介绍/是什么?\n" \
                     "3. 吴京主演/导演/的电影有哪些？\n" \
                     "4. 追风筝的人的出版社/出版日期/页数/简介/目录是什么?\n" \
                     "5. 杨绛的性别/生日/出生地/介绍/是什么?\n" \
                     "6. 杨绛写作/翻译的书籍有哪些?\n" \
                     "...等等其他类型书籍、电影问题"
            return result
        if "template" in str(question, encoding='utf-8'):
            result = "Hi, you can ask me question about movie and book, like:\n" \
                     "1. What is  BrettGipson birthday/birthplace？\n" \
                     "2. What movie does GaylenRoss star in？\n" \
                     "3. Which movies TomHanks act?\n" \
                     "4. What movies does TerranceDicks write?\n" \
                     "5. In movie CastAway, what are actors?\n" \
                     "6. Show me movie CastAway duration?\n" \
                     "7. What is CatchMeIfYouCan cast look like?\n" \
                     "...etc"
            return result
        if "mix" in str(question, encoding='utf-8'):
            result = "Hi, you can ask me question about movie and book, like:\n" \
                     "1. What is 吴京 birthday？\n" \
                     "2. What is 吴京 birthplace？\n" \
                     "3. CastAway 有哪些演员？\n" \
                     "4. TerranceDicks的生日是什么？\n" \
                     "...etc"
            return result

        # Indentify entity
        question_label = self.query_ner.get_ner_objects(question)

        # Sparql template generate
        sparql_list = self.query2sparql.parse(question_label)
        for sparql in sparql_list:
            print(sparql[0])
            print('=' * 20)
            print(sparql[1])
            print('=' * 40)

        # Apache Jena query
        candidate_list = []
        for sparql_q in sparql_list:
            sparql_result = self.sparql_query.get_sparql_result(sparql_q[1])
            sparql_result_value = self.sparql_query.get_sparql_result_value(sparql_result)
            candidate_list.append((sparql_q[0], sparql_result_value))
        print(candidate_list)

        # optimize result
        result = self.optimize_result.parse(candidate_list)
        return result


if __name__ == '__main__':
    query = Query()
    question = 'Which movies TomHanks act?'
    while True:
        question = input('question/问题: ').encode('utf-8')
        ans = query.parse(question)
        print(ans)
