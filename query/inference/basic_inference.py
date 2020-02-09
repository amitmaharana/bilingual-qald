# -*- coding:utf-8 -*-

"""
rule based deduction
------------
common blocks
"""
from refo import finditer, Predicate
import re


class W(Predicate):
    def __init__(self, token=".*", pos=".*"):
        self.token = re.compile(token + "$")
        self.pos = re.compile(pos + "$")
        super(W, self).__init__(self.match)

    def match(self, word):
        m1 = self.token.match(word.token)
        m2 = self.pos.match(word.pos)
        return m1 and m2


class Rule(object):
    def __init__(self, condition_num, condition=None, action=None):
        assert condition and action
        self.condition_num = condition_num
        self.condition = condition
        self.action = action

    def apply(self, sentence):
        # print("rule apply")
        # print(sentence)
        matches = []
        for m in finditer(self.condition, sentence):
            i, j = m.span()
            matches.extend(sentence[i:j])
        return self.action(matches), self.condition_num


class KeywordRule(object):
    def __init__(self, condition=None, action=None):
        assert condition and action
        self.condition = condition
        self.action = action

    def apply(self, sentence):
        matches = []
        for m in finditer(self.condition, sentence):
            i, j = m.span()
            matches.extend(sentence[i:j])
        if len(matches) == 0:
            return None
        else:
            return self.action()


"""
Prefix and Template
"""
SPARQL_PREFIX = u"""PREFIX : <http://www.douban_kgqa.com#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX dbo: <http://dbpedia.org/ontology/>
PREFIX dbp: <http://dbpedia.org/property/>
PREFIX dct: <http://purl.org/dc/terms/>
PREFIX res: <http://dbpedia.org/resource/>
PREFIX yago: <http://dbpedia.org/class/yago/>
PREFIX foaf: <http://xmlns.com/foaf/0.1/>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
"""
SPARQL_SELECT_TEM_FD = u"{prefix}\n" + \
                       u"SELECT DISTINCT {select} WHERE {{\n" + \
                       u"{{\n" + \
                       u"SERVICE <http://localhost:3030/douban_kgqa>{{\n" + \
                       u"{expression_douban}\n" + \
                       u"}}\n" + \
                       u"}}\n" + \
                       u"UNION {{\n" + \
                       u"SERVICE <http://dbpedia.org/sparql>{{\n" + \
                       u"{expression_db}\n" + \
                       u"}}\n" + \
                       u"}}\n" + \
                       u"}}\n"

SPARQL_COUNT_TEM_FD = u"{prefix}\n" + \
                      u"SELECT COUNT({select}) WHERE {{\n" + \
                      u"{{\n" + \
                      u"SERVICE <http://localhost:3030/douban_kgqa>{{\n" + \
                      u"{expression_douban}\n" + \
                      u"}}\n" + \
                      u"}}\n" + \
                      u"UNION {{\n" + \
                      u"SERVICE <http://dbpedia.org/sparql>{{\n" + \
                      u"{expression_db}\n" + \
                      u"}}\n" + \
                      u"}}\n" + \
                      u"}}\n"

SPARQL_SELECT_TEM = u"{prefix}\n" + \
                    u"SELECT DISTINCT {select} WHERE {{\n" + \
                    u"{expression}\n" + \
                    u"}}\n"

SPARQL_COUNT_TEM = u"{prefix}\n" + \
                   u"SELECT COUNT({select}) WHERE {{\n" + \
                   u"{expression}\n" + \
                   u"}}\n"

SPARQL_ASK_TEM = u"{prefix}\n" + \
                 u"ASK {{\n" + \
                 u"{expression}\n" + \
                 u"}}\n"

"""
keyword
"""
pos_person = "nr"
pos_book_or_movie = "nz"
pos_number = "m"
pos_country = "nc"
pos_river = "nw"
# singer
pos_singer = "ns"

country_entity = (W(pos=pos_country))
person_entity = (W(pos=pos_person))
book_or_movie_entity = (W(pos=pos_book_or_movie))
number_entity = (W(pos=pos_number))
river_entity = (W(pos=pos_river))

# singer entity
singer_entity = (W(pos=pos_singer))
s_entity = (W(pos=pos_singer))


# movie property
class MoviePropertyValueSet:
    def __init__(self):
        pass

    @staticmethod
    def return_movie_info_country_value_FD():
        return u':movie_info_country dbp:country'

    @staticmethod
    def return_movie_info_language_value_FD():
        return u':movie_info_language dbp:language'

    @staticmethod
    def return_movie_info_duration_value_FD():
        return u':movie_info_duration dbo:runtime'

    @staticmethod
    def return_movie_info_summary_value_FD():
        return u':movie_info_summary dbo:abstract'

    @staticmethod
    def return_movie_person_gender_value_FD():
        return u":movie_person_gender foaf:gender"

    @staticmethod
    def return_movie_person_birthday_value_FD():
        return u":movie_person_birthday dbo:birthDate"

    @staticmethod
    def return_movie_person_birthplace_value_FD():
        return u":movie_person_birthplace dbo:birthPlace"

    @staticmethod
    def return_movie_person_profession_value_FD():
        return u":movie_person_profession dct:description"

    @staticmethod
    def return_movie_person_introduction_value_FD():
        return u":movie_person_introduction dbo:abstract"

    @staticmethod
    def return_higher_value():
        return u'>'

    @staticmethod
    def return_lower_value():
        return u'<'


class BookPropertyValueSet:
    def __init__(self):
        pass

    @staticmethod
    def return_book_info_image_url_value():
        return u":book_info_image_url"

    @staticmethod
    def return_book_info_press_value_FD():
        return u":book_info_press dbo:publisher"

    @staticmethod
    def return_book_info_content_abstract_value_FD():
        return u":book_info_content_abstract dbo:abstract"

    @staticmethod
    def return_book_info_publish_year_value():
        return u":book_info_publish_year"

    @staticmethod
    def return_book_info_page_num_value():
        return u":book_info_page_num"

    @staticmethod
    def return_book_info_price_value():
        return u":book_info_price"

    @staticmethod
    def return_book_info_catalog_value():
        return u":book_info_catalog"

    @staticmethod
    def return_book_info_rating_value():
        return u":book_info_rating"

    @staticmethod
    def return_book_info_review_count_value():
        return u":book_info_review_count"

    @staticmethod
    def return_book_person_image_url_value():
        return u":book_person_image_url"

    @staticmethod
    def return_book_person_gender_value_FD():
        return u":book_person_gender foaf:gender"

    @staticmethod
    def return_book_person_birthday_value_FD():
        return u":book_person_birthday dbo:birthDate"

    @staticmethod
    def return_book_person_birthplace_value_FD():
        return u":book_person_birthplace dbo:birthPlace"

    @staticmethod
    def return_book_person_introduction_value_FD():
        return u":book_person_introduction dbo:abstract"

    @staticmethod
    def return_book_person_other_name_value():
        return u":book_person_other_name"

    @staticmethod
    def return_higher_value():
        return u'>'

    @staticmethod
    def return_lower_value():
        return u'<'


# movie property
class CountryPropertyValueSet:
    def __init__(self):
        pass

    @staticmethod
    def return_country_info_foundingdate_FD():
        return u'dbo:foundingDate dbo:foundingDate'

    @staticmethod
    def return_country_info_longname_FD():
        return u'dbo:longName dbo:longName'

    @staticmethod
    def return_country_info_arearank_FD():
        return u'dbp:areaRank dbp:areaRank'

    @staticmethod
    def return_country_info_summary_FD():
        return u'dbo:abstract dbo:abstract'

    @staticmethod
    def return_country_info_currency_FD():
        return u'dbp:currencyCode dbp:currencyCode'

    @staticmethod
    def return_country_info_population_FD():
        return u'dbo:populationTotal dbo:populationTotal'

    @staticmethod
    def return_country_info_areatotal_FD():
        return u'dbo:areaTotal dbo:areaTotal'


class RiverPropertyValueSet:
    def __init__(self):
        pass

    @staticmethod
    def return_river_info_sourcecountry_FD():
        return u'dbo:sourceCountry dbo:sourceCountry'

    @staticmethod
    def return_river_info_summary_FD():
        return u'dbo:abstract dbo:abstract'

    @staticmethod
    def return_river_info_rivername_FD():
        return u'dbo:river dbo:river'

    @staticmethod
    def return_river_info_sourcename_FD():
        return u'dbo:source dbo:source'


# singer property
class SingerPropertyValueSet:
    def __init__(self):
        pass

    @staticmethod
    def return_singer_info_abstract_FD():
        return u'dbo:abstract dbo:abstract'

    @staticmethod
    def return_singer_info_birthDate_FD():
        return u'dbo:birthDate dbo:birthDate'

    @staticmethod
    def return_singer_info_birthName_FD():
        return u'dbo:birthName dbo:birthName'

    @staticmethod
    def return_singer_info_birthPlace_FD():
        return u'dbo:birthPlace dbo:birthPlace'

    @staticmethod
    def return_singer_info_residence_FD():
        return u'dbp:residence dbp:residence'

    @staticmethod
    def return_singer_info_musicalArtist_FD():
        return u'dbo:musicalArtist dbo:musicalArtist'
