from pandas import read_csv
from pandas import DataFrame
from pandas import concat
import csv

def concat_files_with_pandas_concat(number_repeats, result_file, *args):
    """
    Combine files using the pandas library concatenation function.
    (The problem is the lack of RAM to load the resulting file.)

    :param numeber_repeats: number of repeats concatenations
    :param args: csv-files
    :param result_file: file for write concatenations
    """

    result = read_csv(result_file)
    for i in range(number_repeats):
        list_of_dataframe = []
        list_of_dataframe.append(result)
        for csv in args:
            file_for_concat = read_csv(csv)
            list_of_dataframe.append(file_for_concat)
            result = concat(list_of_dataframe, ignore_index=True)

    # write DataFrame to CSV-file
    result.to_csv(result_file, index=False)


def concat_files_with_adding_rows(number_repeats, result_file, *args):

    j = 0
    with open(result_file, 'w', newline='', encoding='utf-8') as csv_result:
        result = csv.writer(csv_result, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        for i in range(number_repeats):
            for csv_for_concat in args:
                with open(csv_for_concat, newline='', encoding='utf-8') as csv_to_write:
                    reader = csv.reader(csv_to_write, delimiter=',', quotechar='|')
                    for row in reader:
                        result.writerow(row)
                        print(j)
                        j += 1

if __name__ == "__main__":
    # concat_files_with_pandas_concat(3, r'Z:/roman.baldaev@econophysica.com/ElasticTestResults/result2.csv', r'../articles1.csv',
    #              r'../articles2.csv', r'../articles3.csv')
    concat_files_with_adding_rows(20, r'Z:/roman.baldaev@econophysica.com/ElasticTestResults'\
                                     '/results_with_adding_rows.csv',
                                    '../articles1.csv', r'../articles2.csv', r'../articles3.csv')