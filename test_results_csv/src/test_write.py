from pandas import read_csv
from pandas import DataFrame
from pandas import concat


if __name__ == "__main__":
    """
    Test for save results
    """
    d = ['index', 'size(MB)', 'query', 'time']
    data = ['index', 100, 'Washington | Russia', 0.234]
    source = read_csv('ElasticResults.csv')

    wr = DataFrame([data], columns=d)

    # adding data to end of DataFrame
    _sum = concat([source, wr], ignore_index=True)

    # write DataFrame to CSV-file
    _sum.to_csv('ElasticResults.csv', index=False)