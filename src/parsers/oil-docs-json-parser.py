import json
from pprint import pprint
from copy import copy
import os


class ChangeClusterAndIndex:

    def __init__(self, path_to_folder_old_docs, path_to_folder_new_docs, path_to_stop_words_file = None):
        self.path_to_folder_old_docs = path_to_folder_old_docs
        self.path_to_folder_new_docs = path_to_folder_new_docs
        self.file_list = None
        self.set_of_pronouns = set()
        self.stop_words = self.get_stop_words(path_to_stop_words_file)

    def get_paths_to_json_files(self):
        paths = []
        for (dirpath, dirnames, filenames) in os.walk(self.path_to_folder_old_docs):
            paths.extend(filenames)
        self.file_list = paths

    def get_stop_words(self, path):
        with open(path) as stop_words:
            s_words =  stop_words.readlines()
        stop_words = []

        # delete \n
        for word in s_words:
            stop_words.append(word[:-1])

        return stop_words


    @staticmethod
    def json_reader(json_path):
        with open(json_path) as f:
            data = json.load(f)

        return data

    @staticmethod
    def json_writter(json_path, data):
        with open(json_path, 'w', encoding='utf-8') as outfile:
            json.dump(data, outfile, ensure_ascii=False)

    def change_json(self, file_name):

        path_data = os.path.join(self.path_to_folder_old_docs, file_name)
        path_out = os.path.join(self.path_to_folder_new_docs, file_name)

        data = self.json_reader(path_data)
        text = data['text']
        coreferences = data['coreferences']

        cluster_dict = {}
        for cluster in coreferences:
            start = cluster['index_1']
            finish = cluster['index_2']
            name = text[start:finish]
            number = cluster['cluster_number']
            if number not in cluster_dict.keys():
                cluster_dict[number] = []
            cluster_dict[number].append(name)

        max_cluster_dict = copy(cluster_dict)

        for item in max_cluster_dict.keys():
            keywords_without_pronouns = set(cluster_dict[item]) - set(self.stop_words)
            if len(keywords_without_pronouns) == 0:
                max_cluster_dict[item] = max(cluster_dict[item], key=len)
            else:
                max_cluster_dict[item] = max(keywords_without_pronouns, key=len)

        new_coreferences = []

        for key in cluster_dict.keys():
            for keyword in cluster_dict[key]:
                new_coreferences.append({'keyword': keyword,
                                         'cluster_name': max_cluster_dict[key]})
        data['coreferences'] = new_coreferences

        self.json_writter(path_out, data)

    def change_all_in_directory(self):

        if self.file_list is None:
            self.get_paths_to_json_files()

        for file in self.file_list:
            self.change_json(file)

    def get_set_of_pronouns(self):

        if self.file_list is None:
            self.get_paths_to_json_files()

        for file in self.file_list:

            path_data = os.path.join(self.path_to_folder_old_docs, file)

            data = self.json_reader(path_data)
            text = data['text']
            coreferences = data['coreferences']

            for cluster in coreferences:
                start = cluster['index_1']
                finish = cluster['index_2']
                name = text[start:finish].lower()
                if len(name) <= 6 or name[:5] == "котор":
                    self.set_of_pronouns.add(name)

        self.set_of_pronouns = sorted(self.set_of_pronouns, key=len)

    def write_pronouns_to_txt(self, directory_path, file_name):
        path = os.path.join(directory_path, file_name)
        with open(path, 'w', encoding='utf-8') as outfile:
            for word in self.set_of_pronouns:
                outfile.write(word)
                outfile.write("\n")

if __name__ == "__main__":

    A = ChangeClusterAndIndex(path_to_folder_old_docs="/home/roman/Projects/ElasticMongoTest/datasets/"
                                                      "neftyanoe_coreferent",
                              path_to_folder_new_docs="/home/roman/Projects/ElasticMongoTest/datasets/"
                                                      "new_neftyanoe_coreferent",
                              path_to_stop_words_file="/home/roman/Projects/ElasticMongoTest/datasets/"
                                                      "pronouns/pronouns.txt")
    A.change_all_in_directory()