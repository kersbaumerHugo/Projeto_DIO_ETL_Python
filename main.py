from requests import request
from pandas import DataFrame,to_datetime
from pandas import to_datetime
from matplotlib import pyplot as plt

class RequestError(Exception):
    """Classe de erro de request, tratamento de exceções da requisição"""
    def __init__(self, *args,response = None):
        super().__init__(*args)
        self.code = response.status_code
        self.message = f"The requisition failed with code {self.code}"
        #self.

    pass
def fetch_CDI_data(data_inicial="01/01/2026",data_final="05/03/2026"):
    """Função que retorna os dados do CDI do site do banco central"""
    CODIGO_SERIE = 11
    response = request(url=f'https://api.bcb.gov.br/dados/serie/bcdata.sgs.{CODIGO_SERIE}/dados?formato=json&dataInicial={data_inicial}&dataFinal={data_final}',method="GET")
    return response

#Variável de debug
#==============================================#
debug_dict = {"Extract" : True, "Transform" : False, "Load" : True}
#==============================================#
#Entrada do usuário
if not debug_dict["Extract"]:
    data_inicial = input("Digite a data de aporte inicial (ex. 01/01/2025): ")
    data_final = input("Digite a data onde será retirado o dinheiro (ex. 01/01/2025): ")
    montante_inicial = float(inicial = input("Digite o valor do aporte inicial: "))
if debug_dict["Extract"]:
    montante_inicial = 1000
#==============================================#
#Parte de extração dos dados do site do banco central via API 
# referentes à variação da Selic diária

response = fetch_CDI_data()
try:
    if response.status_code != 200:
        raise RequestError
    df_CDI = DataFrame(response.json())
except ConnectionError as erro:
    print("A url requisitada não foi encontrada")
except RequestError as erro:
    print(erro.message)
if debug_dict["Extract"]:
    print(df_CDI)
#==============================================#
#Transformação dos dados, calculando rendimento baseado em um aporte e 
# calculando os juros compostos dia a dia.
variacao_cdi = df_CDI['valor'].apply(lambda x: float(x)).to_list()
df_CDI['data'] = df_CDI['data'].apply(lambda x: x[:-5])
montante_parcial = [montante_inicial]
for variacao in variacao_cdi:
    montante_parcial.append(round(montante_parcial[-1]*(1+variacao/100),2))
    if debug_dict["Transform"]:
        print("Montante parcial: ", montante_parcial)
        print("Variação: ",variacao)
        #print(montante_parcial,variacao)
montante_parcial = montante_parcial[1:]
if debug_dict["Transform"]:
    print("Itens em montante_parcial: ",len(montante_parcial))
    print("Itens em variação_cdi: ",len(variacao_cdi))
    #print(len(montante_parcial),len(variacao_cdi))
#==============================================#
#Exportação dos dados obtidos na forma de gráfico de evolução diária de patrimônio.
#plt.style.use('_mpl_gallery')
x_dados = df_CDI["data"]
y_dados = montante_parcial
ESPACAMENTO_XTICKS = 5 #Número para a cada quantos pontos ele desenha a label do eixo x
ESPACAMENTO_LABELS = 4 #Número para a cada quantos pontos ele desenha a label no gráfico
ESPACAMENTO_POINTS = 4 #Número para a cada quantos pontos ele os pontos no gráfico
if debug_dict["Load"]:
    print(df_CDI)
fig, ax = plt.subplots()
plt.xticks(range(0, len(x_dados), ESPACAMENTO_XTICKS), x_dados[::ESPACAMENTO_XTICKS], rotation=45, ha='right')
for i in range(0, len(x_dados), ESPACAMENTO_LABELS):
    #Pega as coordenadas do ponto atual
    x_posicao = x_dados[i-5 if i-5 >=0 else i+5]
    y_posicao = y_dados[i+2 if i>2 or i<1 else i]
    # Use plt.text() to add the annotation
    # adjust the position slightly above the marker (e.g., +5 for y)
    print(y_posicao)
    plt.text(x_posicao, y_posicao -1, f'(R${y_posicao})', ha='center', fontsize=8)
ax.plot(x_dados,y_dados,linewidth=2.0)
plt.scatter(x_dados[::ESPACAMENTO_POINTS],y_dados[::ESPACAMENTO_POINTS])
plt.show()
