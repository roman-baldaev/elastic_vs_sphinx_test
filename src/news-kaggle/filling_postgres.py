import psycopg2
from abc import ABC, abstractmethod

class PostgresData:

    def __init__(self, _dbname, _user, _password, _host, **kwargs):
        """

        :param _dbname: database name, parameter for connect
        :param _user:  user name, parameter for connect
        :param _password: password, parameter for connect
        :param _host: host, default "localhost", parameter for connect

        :param kwargs: a dictionary of conformity between the rows of the database table and the names of the data
                categories for the record. For example, if a CSV-file is written to the database,
                the data category name is the name of the column of CSV-file.
                Format: kwarg[table_name.row_name] = data_category_name
        """
        self.connect = psycopg2.connect(database=_dbname, user=_user, password=_password, host=_host)
        self.conformity = kwargs

        # calculate the number of tables
        tables = set()
        for key in kwargs.iteritems():
            tables.add(key.split(".")[0])

        self.number_of_tables = len(tables)

