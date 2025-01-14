# combinação dos scripts de extração e visualização
import os
import time
import json
from random import random
import csv
from sys import argv
from datetime import datetime

import pandas as pd
import seaborn as sns
import requests

URL = 'https://api.bcb.gov.br/dados/serie/bcdata.sgs.4392/dados'
# Criando a variável data e hora

try:
    # faz a requisição usando request
    response = requests.get(url=URL)
    # verifica se a resposta foi mais de 200
    response.raise_for_status()
except requests.HTTPError as exc:
    print("Dado não encontrado, continuando.")
    cdi = None
except Exception as exc:
    print("Erro, parando a execução.")
    raise exc
else:
    # se a requisição deu certo, transforma o response em um dicionario
    # pega o ultimo elemento e a chave 'valor' dele
    dado = json.loads(response.text)[-1]['valor']

for _ in range(0, 10):
    data_e_hora = datetime.now()
    data = datetime.strftime(data_e_hora, '%Y/%m/%d')
    hora = datetime.strftime(data_e_hora, '%H:%M:%S')
    # Captando a taxa CDI do site da B3

    cdi = float(dado) + (random() - 0.5)

  # Verificando se o arquivo "taxa-cdi.csv" existe, se false ele cria o arquivo
if os.path.exists('./taxa-cdi.csv') == False:
    with open(file='./taxa-cdi.csv', mode='w', encoding='utf8') as fp:
        fp.write('data,hora,taxa\n')
    # Salvando dados no arquivo "taxa-cdi.csv"
with open(file='./taxa-cdi.csv', mode='a', encoding='utf8') as fp:
    fp.write(f'{data},{hora},{cdi}\n')
    time.sleep(1)
print("Sucesso")


# extraindo colunas hora e taxa
df = pd.read_csv('./taxa-cdi.csv')

# salvando no grafico, usando os dados de df
grafico = sns.lineplot(x=df['hora'], y=df['taxa'])
_ = grafico.set_xticklabels(labels=df['hora'], rotation=90)
grafico.get_figure().savefig(f'{argv[1]}.png')
