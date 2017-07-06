import os

import lxml.etree as ET
import time
import regex
import time
import codecs
import sys

#from tqdm import tqdm_notebook as tqdm
from tqdm import tqdm
import utils

"""
Class used to parse a xml file containing list of publication

"""


class Xml_parser(object):
    def __init__(self):
        """

        :param parameters: parameter file contining input and output path
        :type parameters: dict
        """
        self.author_to_publications = dict()
        self.author_to_authorID = dict()
        self.authorID_to_publications = dict()

    def __add_publication(self, authors, publication):
        """
        Add a new entry if the author doesn't exist yet otherwise it
        add a new publication to the existing list. or
        :param author: author
        :type author: str
        :param publication: publication title
        type: str
        """
        for author in authors:

            if author not in self.author_to_publications:
                self.author_to_publications[author] = set()
            self.author_to_publications[author].add(publication)

    def __add_author(self, key_name, others_names, personal_information):
        """
        add all the nickname of one author in the mapping
        :param key_name: id of the author
        :type key_name:  str
        :param others_names: list of nickname
        :type others_names:  list of str
        :param personal_information: indicate if the www balise containt more than jsute
         a name and title (url or note for example)
        :type personal_information: bool

        """
        for name in others_names:
            self.author_to_authorID[name] = (key_name, personal_information)


    def collect_data(self, data_folder):
        """
        iterate over the xml file using regex (faster than iterparse) and collect the author publication couple
        and also all the nickame use to represent one author
        """
        print("Start collecting")
        input_file_path = os.path.join(data_folder, "dblp.xml")
        with codecs.open(input_file_path, "r", encoding="iso-8859-1") as file:
            start = time.time()
            tmp = start

            title = ""
            key_prefix = ""
            authors = []
            personal_information = False
            publications_type = ["article", "inproceedings", "proceedings", "book",
                                 "incollection", "phdthesis", "mastersthesis"]
            start_publication_regex = r"<([^\/]*?) (.*)>"  # </article><article mdate="2017-05-28" key="journals/acta/Simon83">
            end_publication_regex = r"<\/(.*?)>"  # </article><article mdate="2017-05-28" key="journals/acta/Simon83">
            author_regex = r"<author>(.*)</author>"  # <author>Katsuyuki Tateishi</author>
            title_regex = r"<title>(.*)</title>"  # <title>A quadratic speedup theorem ...</title>
            start_person_regex = r'<www.*key="(.*)">'  #<www mdate="2009-06-10" key="homepages/32/3977">
            end_person_regex = r"<\/www>"
            note_url_regex = r"<note.*?>|<url.*?>"
            inside_publication = False
            inside_person = False
            for i, line in tqdm(enumerate(file)):
                # Test end of publication, if true add publication
                result = regex.search(end_publication_regex, line)
                if result:
                    if result.group(1) in publications_type:
                        if inside_publication and authors and title:
                            # This a a publication, lets add it to the dictionnay author -> title
                            self.__add_publication(authors, title)
                        title = ""
                        authors = []
                        inside_publication = False
                        personal_information = False
                        key_prefix = ""

                #Test beginning of a publication
                result = regex.search(start_publication_regex, line)
                if result and result.group(1) in publications_type:
                    inside_publication = True
                    title = ""
                    authors = []
                    personal_information = False
                    key_prefix = ""

                #Check if author
                result = regex.search(author_regex, line)
                if result and (inside_publication or inside_person):
                    authors.append(result.group(1))
                #Check if title
                result = regex.search(title_regex, line)
                if result and (inside_publication or inside_person):
                    title = result.group(1)
                #Check if containt url or note
                result = regex.search(note_url_regex, line)
                if result:
                #if inside_person and ("<note" in line or "<url" in line):
                    personal_information = True
                # Check if end of person, if true add author
                result = regex.search(end_person_regex, line)
                if result and inside_person:
                    if authors and "homepages/" in key_prefix and title == "Home Page":
                        self.__add_author(key_prefix, authors, personal_information)
                    key_prefix = ""
                    authors = []
                    inside_person = False
                    personal_information = False
                    title = ""
                #Check start person
                result = regex.search(start_person_regex, line)
                if result:
                    inside_person = True
                    key_prefix = result.group(1)


        self.__save_everything(data_folder)
        self.__merge_data()
        self.__save_everything(data_folder)

        











    def __save_everything(self, data_folder):
        author_publication_path = os.path.join(data_folder, "authorName_publication.p")
        utils.pickle_data(self.author_to_publications, author_publication_path)
        print("Saving author_publication in ", author_publication_path)
        author_to_authorID_path = os.path.join(data_folder, "authorName_to_authorID.p")
        utils.pickle_data(self.author_to_authorID, author_to_authorID_path)
        print("Saving author_to_authorID in ", author_to_authorID_path)
        authorID_to_publications_path = os.path.join(data_folder, "authorID_to_publications.p")
        utils.pickle_data(self.authorID_to_publications, authorID_to_publications_path)
        print("Saving authorID_to_publications in ", authorID_to_publications_path)

    def __merge_data(self):
        print("merge authorID and publication")
        for author, titles in tqdm(self.author_to_publications.items()):
            if  author in self.author_to_authorID:
                author_id, personal_info = self.author_to_authorID[author]
            else:
                author_id = author
                personal_info = False

            if author_id in self.authorID_to_publications:
                self.authorID_to_publications[author_id]['titles'].union(titles)
            else:
                self.authorID_to_publications[author_id] = {"titles":titles, "info":personal_info}



