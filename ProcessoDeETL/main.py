import pandas as pd

colspecs = [(2, 10),
            (10, 12),
            (12, 24),
            (27, 39),
            (56, 69),
            (69, 82),
            (82, 95),
            (108, 121),
            (152, 170),
            (170, 188)
            ]

names = ['data_pregao', 'codbdi', 'sigla_acao', 'nome_acao', 'preco_abertura', 'preco_maximo',
         'preco_minimo', 'preco_fechamento', 'qtd_negocios', 'volume_negocios']

# Criação do dataframe
df = pd.read_fwf(r'C:\Users\lucas\OneDrive\Documentos\Estudos\Python\Eng_Dados\ProcessoDeETL\ProcessoDeETL'
                 r'\COTAHIST_A2021.TXT', colspecs=colspecs, names=names, skiprows=1)

# TRANSFORMAÇÕES

# Filtrando pelo código bdi == 2
df = df [df['codbdi'] == 2] 
# Excluindo a coluna (1 indica que é coluna)
df = df.drop(['codbdi'], 1)

# ajuste do campo de data
df['data_pregao'] = pd.to_datetime(df['data_pregao'], format = '%Y%m%d')

# ajuste dos campos numéricos
df['preco_abertura'] = (df['preco_abertura']/100).astype(float)
df['preco_maximo'] = (df['preco_maximo']/100).astype(float)
df['preco_minimo'] = (df['preco_minimo']/100).astype(float)
df['preco_fechamento'] = (df['preco_fechamento']/100).astype(float)


print(df.head())