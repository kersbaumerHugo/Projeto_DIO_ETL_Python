from requests import request
from pandas import DataFrame,to_datetime,
from pandas import to_datetime
data_final = to_datetime("01/01/2026")
data_inicial = to_datetime("01/01/2026")
CODIGO_SERIE = 11
response = request(url=f'https://api.bcb.gov.br/dados/serie/bcdata.sgs.{CODIGO_SERIE}/dados?formato=json&dataInicial={dataInicial}&dataFinal={dataFinal}')

print(response)