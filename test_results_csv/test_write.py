from pandas import read_csv
from pandas import DataFrame
from pandas import concat

d = ['index', 'size(MB)', 'query', 'time', 'date', 'percent']
data = ['index', 100, 'Washington | Russia', '0.234', '26.23', '52%']
source = read_csv('ElasticResults.csv')

wr = DataFrame([data], columns=d)

print(type(source))
print(type(wr))
_sum = concat([source, wr], ignore_index=True)

_sum.to_csv('ElasticResults.csv', index=False)