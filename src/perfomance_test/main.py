from search_test import SearchTest, SearchTestElastic


if __name__ == "__main__":

    test = SearchTestElastic("ES1", "localhost:9200")
    # test.search_substrings_or(['Colorado', 'USA', 'President', 'Washington', 'December',
    #                           'Book', 'Ford', 'million', 'Apple', 'Official',
    #                           'year', 'Bank', 'Study', 'University', 'blood'],
    #                          )
    test.size_of_object('news')
    # test.search_substrings_or(['MTV', 'London'],
    #                           )

    # test.show_results()