# -*- coding:utf-8 -*-

from inference.river_info_template_fd import river_info_rules_fd
from inference.book_info_template_fd import book_info_rules_fd
from inference.book_person_template_fd import book_person_rules_fd
from inference.movie_info_template_fd import movie_info_rules_fd
from inference.movie_person_template_fd import movie_person_rules_fd
from inference.country_info_template_fd import country_info_rules_fd
from inference.singer_person_template_fd import singer_info_rules_fd


class Query2Sparql:
    def __init__(self):
        self.book_info_rules_fd = book_info_rules_fd
        self.book_person_rules_fd = book_person_rules_fd
        self.movie_person_rules_fd = movie_person_rules_fd
        self.movie_info_rules_fd = movie_info_rules_fd
        self.country_info_rules_fd = country_info_rules_fd
        self.river_info_rules_fd = river_info_rules_fd
        self.singer_info_rules_fd = singer_info_rules_fd

    def parse(self, question_label):
        """
        parse question type
        :return:
        """
        sparql_list = []

        for rule in self.movie_info_rules_fd:
            sparql, num = rule.apply(question_label)
            if isinstance(sparql, list) and sparql:
                for temp_sparql in sparql:
                    sparql_list.append((num, temp_sparql))
                continue
            if sparql:
                sparql_list.append((num, sparql))
                continue

        for rule in self.movie_person_rules_fd:
            sparql, num = rule.apply(question_label)
            if isinstance(sparql, list) and sparql:
                for temp_sparql in sparql:
                    sparql_list.append((num, temp_sparql))
                continue
            if sparql:
                sparql_list.append((num, sparql))
                continue

        for rule in self.book_info_rules_fd:
            sparql, num = rule.apply(question_label)
            if isinstance(sparql, list) and sparql:
                for temp_sparql in sparql:
                    sparql_list.append((num, temp_sparql))
                continue
            if sparql:
                sparql_list.append((num, sparql))

        for rule in self.book_person_rules_fd:
            sparql, num = rule.apply(question_label)
            if isinstance(sparql, list) and sparql:
                for temp_sparql in sparql:
                    sparql_list.append((num, temp_sparql))
                continue
            if sparql:
                sparql_list.append((num, sparql))

        for rule in self.country_info_rules_fd:
            sparql, num = rule.apply(question_label)
            if isinstance(sparql, list) and sparql:
                for temp_sparql in sparql:
                    sparql_list.append((num, temp_sparql))
                continue
            if sparql:
                sparql_list.append((num, sparql))

        for rule in self.river_info_rules_fd:
            sparql, num = rule.apply(question_label)
            if isinstance(sparql, list) and sparql:
                for temp_sparql in sparql:
                    sparql_list.append((num, temp_sparql))
                continue
            if sparql:
                sparql_list.append((num, sparql))

        for rule in self.singer_info_rules_fd:
            sparql, num = rule.apply(question_label)
            if isinstance(sparql, list) and sparql:
                for temp_sparql in sparql:
                    sparql_list.append((num, temp_sparql))
                continue
            if sparql:
                sparql_list.append((num, sparql))

        return sparql_list
