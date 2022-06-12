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

# TODO 1: Média de gastos de pessoas com ingresso pista
resposta_1 = f"R${round(df_final[df_final['tipo'] == 'Pista']['gastos'].mean(), 2)}"
print('\n1) A média de gastos por pessoas com o ingresso tipo pista foi de:')
print(resposta_1)
# Salvando resposta
with open('Desafio/questao_1.txt', 'w') as q1:
    q1.write(resposta_1)

# TODO 2: Pessoas que não compareceram aos shows
compraram = set(tabela_ingressos[tabela_ingressos['status'] == 'Concluido']['nome'])
compareceram = set(df_final[df_final['status'] == 'Concluido']['nome'])
resposta_2 = ''
print('\n2) Pessoas que não compareceram aos shows:')
for pessoa in sorted(list(compraram - compareceram)):
    print(pessoa)
    resposta_2 += pessoa + '\n'
# Salvando resposta
with open('Desafio/questao_2.txt', 'w') as q2:
    q2.write(resposta_2)

# TODO 3: Pessoas que compraram ingressos com os concorrentes
concorrencia = sorted(list(set(df_final[df_final['status'] != 'Concluido']['nome'])))
resposta_3 = ''
print('\n3) Lista de pessoas que compraram pelo menos um ingresso na concorrência:')
for pessoa in concorrencia:
    print(pessoa)
    resposta_3 += pessoa + '\n'
# Salvando resposta
with open('Desafio/questao_3.txt', 'w') as q3:
    q3.write(resposta_3)


# TODO 4: Dia com maior gasto
total_compras_dia = df_final.groupby('data')['gastos'].sum().reset_index()
indice = total_compras_dia[total_compras_dia['gastos'] == total_compras_dia['gastos'].max()].index[0]
dia_maior_gasto = total_compras_dia.at[indice, 'data']
resposta_4 = '{:0=2d}/{:0=2d}/{}'.format(dia_maior_gasto.day, dia_maior_gasto.month, dia_maior_gasto.year)
print('\n4) O dia com maior gasto foi:')
print(resposta_4)
# Salvando resposta
with open('Desafio/questao_4.txt', 'w') as q4:
    q4.write(resposta_4)

# TODO 5: Listar os clientes que desistiram de comprar o ingresso com a AT
# Criação do data frame dos desistentes
tabela_ingressos = tabela_ingressos.sort_values('status')
df_desistentes = tabela_ingressos.groupby(['nome', 'show'])['status'].sum().reset_index()
df_desistentes = df_desistentes[df_desistentes['status'].apply(lambda x: x[0]) != 'C']
df_desistentes = df_desistentes.drop(['status'], axis=1)
df_desistentes = df_desistentes.merge(tabela_compras, how='left')
df_desistentes.fillna(0)
desistentes = []
resposta_5 = '['

# Formatação das informações dos desistentes
for pessoa in sorted(list(set(df_desistentes['nome']))):
    nome = pessoa
    gastos = df_desistentes[df_desistentes['nome'] == pessoa]['gastos'].sum()
    shows = df_desistentes[df_desistentes["nome"] == pessoa]["show"].to_list()
    desistentes += [{'nome': pessoa,
                    'gastos': round(gastos, 2),
                    'shows': shows
                    }]
    resposta_5 += ('{\n'
            f'    "nome": "{pessoa}",\n'
            f'    "gastos": {round(gastos, 2)},\n'
            f'    "shows": {shows}\n'
            '},\n')
print("\n5) Lista com os clientes que desistiram de comprar o ingresso com a AT.")
resposta_5 = resposta_5[:-2] + "]"
resposta_5 = resposta_5.translate(str.maketrans("'",'"'))
print(resposta_5)
# Salvando em arquivo os resultados da questão 5
with open('Desafio/questao_5.json', 'w') as q5:
    q5.write(resposta_5)
# tabela = pd.DataFrame(data=desistentes)
# tabela.to_json('Desafio/questao_5.json', orient="records")