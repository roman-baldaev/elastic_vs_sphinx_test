from pandas import DataFrame


def init_csv(file_name, _columns=('index', 'size', 'query', 'time', 'total')):
    # Create a CSV-file to save test results
    df = DataFrame(columns=list(_columns))
    df.to_csv('{}.csv'.format(file_name), index=False)


if __name__ == "__main__":
    init_csv('ElasticsearchTest')
