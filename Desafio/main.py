import pandas as pd

# Extração dos dados
URL_SHOWS = r'https://us-central1-raccoon-bi.cloudfunctions.net/psel_de_shows'
URL_INGRESSOS = r'https://us-central1-raccoon-bi.cloudfunctions.net/psel_de_ingressos'
URL_COMPRAS = r'https://us-central1-raccoon-bi.cloudfunctions.net/psel_de_compras'

# Criação dos DataFrames
df_shows = pd.read_json(URL_SHOWS)
df_ingressos = pd.read_json(URL_INGRESSOS)
df_compras = pd.read_csv(URL_COMPRAS)


def formatar_data(df):
    df = df.rename(columns={'ano': 'year', 'mes': 'month', 'dia': 'day'})
    df['data'] = pd.to_datetime(df[['year', 'month', 'day']], format='%Y%m%d')
    df = df.drop(['year', 'month', 'day'], axis=1)
    return df

# Transformações das tabelas
tabela_shows = formatar_data(df_shows.transpose())
tabela_shows = tabela_shows.reset_index()
tabela_shows = tabela_shows.rename(columns={'index': 'show'})

tabela_ingressos = formatar_data(df_ingressos)
tabela_ingressos = tabela_ingressos[['data', 'nome', 'status', 'tipo']]
tabela_ingressos = tabela_ingressos.merge(tabela_shows, how='left')

tabela_compras = df_compras.groupby(['nome', 'show'])['gastos'].sum().reset_index()

df_final = tabela_compras.merge(tabela_shows, how='left')
df_final = df_final.merge(tabela_ingressos[tabela_ingressos['status'] == 'Concluido'], how='left')
print(df_final)
#print(tabela_ingressos[tabela_ingressos.duplicated(keep = False, subset=['nome'])])
# print(df_ingressos[(df_ingressos['tipo'] == 'Pista') & (df_ingressos['status'] == 'Concluido')])
# teste = 'Miguel Ramey'
# print(df_ingressos[df_ingressos['nome'] == teste])
# print(df_compras[df_compras['nome'] == teste])
# print(df_final[df_final['nome'] == teste])



"""
for indice in tabela_ingressos[tabela_ingressos['status'] == 'Concluido'].index:
    data = tabela_ingressos['data'][indice]
    indice_show = tabela_shows[tabela_shows['data'] == data].index[0]
    show = tabela_shows.at[indice_show, 'show']
    tabela_ingressos['show'][indice] = show
"""

# print(tabela_ingressos[(tabela_ingressos['status'] == 'Concluido') & (tabela_ingressos['tipo'] == 'Pista')])
# TODO 1: Média de gastos de pessoas com ingresso pista
print('A média de gastos por pessoas com o ingresso tipo pista foi de:')
print(df_final[df_final['tipo'] == 'Pista']['gastos'].mean())

# TODO 2: Pessoas não compareceram aos shows
#print(tabela_ingressos)
#print(tabela_ingressos[(tabela_ingressos['show'] == 'Nascent Letter') & (tabela_ingressos['status'] == 'Concluido')])

# TODO 3: Pessoas que compraram ingressos com os concorrentes

# TODO 4: Dia com maior gasto

# TODO 5: no pdf
