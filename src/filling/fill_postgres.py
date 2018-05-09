import psycopg2
from abc import ABC, abstractmethod

class PostgresData(ABC):
    """"
    Abstract class for filling PostgresDB
    """
    def __init__(self, _dbname, _user, _password, _host):
        """

        :param _dbname: database name, parameter for connect
        :param _user:  user name, parameter for connect
        :param _password: password, parameter for connect
        :param _host: host, default "localhost", parameter for connect

        """
        self.connect = psycopg2.connect(database=_dbname, user=_user, password=_password, host=_host)

    @abstractmethod
    def fill_data(self, source, table_name):
        ...


class PostgresDataCsv(PostgresData):
    """
    Class for filling PostgresDB from CSV-file
    """
    def fill_data(self, source, table_name):

        cursor = self.connect.cursor()
        cursor.execute(
            "COPY {} "
            "FROM '{}' DELIMITER ',' CSV HEADER".format(table_name, source)
        )
        self.connect.commit()


if __name__ == "__main__":
    articles1 = PostgresDataCsv('news1gb', 'roman', 'admin', 'localhost')
    articles1.fill_data('/home/roman/Projects/ElasticMongoTest/src/news-kaggle/datasets/articles1.csv',
                        'news')
    # articles1.select_all()