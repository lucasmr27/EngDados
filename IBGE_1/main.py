import pandas as pd

PATH = r"IBGE_1\Tabela1.1(UF).ods"
df = pd.read_excel(PATH, engine="odf")
df = df.drop([0, 1, 2, 36, 37, 38])
df = df.drop(['Unnamed: 2', 'Unnamed: 4', 'Unnamed: 6', 'Unnamed: 8', 'Unnamed: 10'], axis=1)
df = df.reset_index(drop=True)
df = df.rename(columns=dict(zip(df.columns, ['Região','Total', 'Branca', 'Preta', 'Parda', "Amarela ou indígena"])))
print(df.head())
df.to_json(r"IBGE_1\tabela.json")