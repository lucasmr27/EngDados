from lib2to3.pgen2.pgen import DFAState
from re import T
import pandas as pd

# Extração dos dados
URL_SHOWS = r'https://us-central1-raccoon-bi.cloudfunctions.net/psel_de_shows'
URL_INGRESSOS = r'https://us-central1-raccoon-bi.cloudfunctions.net/psel_de_ingressos'
URL_COMPRAS = r'https://us-central1-raccoon-bi.cloudfunctions.net/psel_de_compras'

# Criação dos DataFrames
df_shows = pd.read_json(URL_SHOWS)
df_ingressos = pd.read_json(URL_INGRESSOS)
df_compras = pd.read_csv(URL_COMPRAS)

# Transformações das tabelas
tabela_shows = df_shows.T
tabela_shows = tabela_shows.rename(columns={'ano': 'year', 'mes': 'month', 'dia': 'day'})
tabela_shows['data'] = pd.to_datetime(tabela_shows, format='%Y%m%d')
tabela_shows = tabela_shows.drop(['year', 'month', 'day'], axis=1)
tabela_shows = tabela_shows.reset_index()
tabela_shows = tabela_shows.rename(columns={'index': 'show'})

print(tabela_shows)
tabela_ingressos = df_ingressos
tabela_ingressos = tabela_ingressos.rename(columns={'ano': 'year', 'mes': 'month', 'dia': 'day'})
tabela_ingressos['data'] = pd.to_datetime(tabela_ingressos[['year', 'month', 'day']], format='%Y%m%d')
tabela_ingressos = tabela_ingressos.drop(['year', 'month', 'day'], axis=1)
tabela_ingressos = tabela_ingressos[['data', 'nome', 'status', 'tipo']]

print(tabela_ingressos.head())

# Média de gastos de pessoas com ingresso pista
