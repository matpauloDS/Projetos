import pandas as pd

dfs = []
for year in range(2014, 2023):
    filename = f"{year}_LoL_esports_match_data_from_OraclesElixir.csv"
    df = pd.read_csv("C:/Users/Mat/Projetos/Dia Projeto CBLOL/dados/drive-download-20230703T090232Z-001/" + filename, low_memory=False)
    dfs.append(df)

merged_df = pd.concat(dfs)

# Filtrar as linhas com base nas condições desejadas
filtered_df = merged_df[(merged_df['league'] == 'CBLOL') & (merged_df['position'] == 'team') & (merged_df['year'] == 2022)]

# Salvar o dataframe filtrado em um novo arquivo CSV
filtered_df.to_csv('alltimecblol.csv', index=False)
