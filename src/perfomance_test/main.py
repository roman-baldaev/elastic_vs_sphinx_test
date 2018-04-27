from search_test import SearchTest, SearchTestElastic


if __name__ == "__main__":

    test = SearchTestElastic(timeout=50, file_for_save=
                             '/home/roman/Projects/ElasticMongoTest/test_results_csv/ElasticsearchTest.csv')
    # test.search_substrings_or(['Colorado', 'USA', 'President', 'Washington', 'December',
    #                           'Book', 'Ford', 'million', 'Apple', 'Official',
    #                           'year', 'Bank', 'Study', 'University', 'blood'],
    #                          )
    # test.search_substring(['Washington', 'Russia', 'USA', 'MTV', 'London', 'Crime', 'Science',
    #                        'good', 'kosdfsd', 'luck'], 'news100gb')

    # print(test.size_of_object('news10gb'))
    test.size_of_object('news14gb', 'message')
    print(test.size)
    # test.search_substrings_or(['MTV', 'London'],
    #                           )

    # test.show_results()
