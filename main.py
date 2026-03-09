from requests import request
from pandas import DataFrame,to_datetime
from pandas import to_datetime
class RequestError(Exception):
    def __init__(self, *args,response = None):
        super().__init__(*args)
        self.code = response.status_code
        self.message = f"The requisition failed with code {self.code}"
        #self.

    pass
def fetch_CDI_data(data_inicial="01/01/2026",data_final="05/03/2026"):
    CODIGO_SERIE = 100
    response = request(url=f'https://api.bcb.gov.br/dados/serie/bcdata.sgs.{CODIGO_SERIE}/dados?formato=json&dataInicial={data_inicial}&dataFinal={data_final}',method="GET")
    return response
response = fetch_CDI_data()
try:
    if response.status_code != 200:
        raise RequestError
    df_CDI = DataFrame(response.json())
except ConnectionError as erro:
    print("A url requisitada não foi encontrada")
except RequestError as erro:
    print(erro.message)
print(df_CDI)