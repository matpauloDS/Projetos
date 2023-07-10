import streamlit as st
import pandas as pd
import numpy as np
import statsmodels.api as sm
import seaborn as sns
import matplotlib.pyplot as plt

# Carregar os dados do arquivo CSV
path = "./alltimecblol.csv"
cblol_raw = pd.read_csv(path, encoding='ISO-8859-1')

# Formatar a coluna 'date'
cblol_raw['date'] = pd.to_datetime(cblol_raw['date'], format='%Y-%m-%d %H:%M:%S')
cblol_raw['date'] = cblol_raw['date'].dt.date

# Padronizar em minutos o tamanho do jogo
cblol_raw['gamelength'] = cblol_raw['gamelength'] / 60

# Calcular o winrate e somar as colunas 'towers' e 'opp_towers' por time
def calculate_winrate(df):
    total_games = len(df)
    total_wins = df['result'].sum()
    total_towers = df['towers'].sum()
    total_opp_towers = df['opp_towers'].sum()
    return pd.Series({
        'winrate': total_wins / total_games,
        'total_towers': total_towers,
        'total_opp_towers': total_opp_towers
    })

# Renomear as equipes corretamente
wr = cblol_raw.copy()
wr.loc[wr['teamname'] == 'Flamengo Esports', 'teamname'] = 'Flamengo Los Grandes'
wr.loc[wr['teamname'] == 'Miners', 'teamname'] = 'Netshoes Miners'

# Calcular winrate e Pythagoras
wr = wr.groupby('teamname').apply(calculate_winrate).reset_index()
wr['pyth'] = wr['total_towers']**2 / (wr['total_towers']**2 + wr['total_opp_towers']**2)
# Cálculo da variação para cada time
wr['variação'] = wr['winrate'] - wr['pyth']
wr['variação'] = wr['variação'].map(lambda x: f'{x*100:.2f}%')
# Modelo de regressão linear
model = sm.OLS(wr['winrate'], sm.add_constant(wr['pyth']))
results = model.fit()


# Configurar o app do Streamlit
st.title('Análise do CBLOL')

# Exibir a tabela atualizada com a variação de cada time
st.subheader('Tabela Atualizada')
st.dataframe(wr[['teamname', 'winrate', 'pyth', 'variação']])

# Exibir o gráfico de barras da tabela atualizada
st.subheader('Gráfico de Barras da Tabela Atualizada')
plt.figure(figsize=(10, 6))
sns.barplot(x='teamname', y='winrate', data=wr)
plt.xlabel('Equipe')
plt.ylabel('Winrate')
plt.title('Tabela Atualizada')
st.pyplot(plt)

# Exibir os resultados da regressão
st.subheader('Resultados da Regressão')
st.text(results.summary())

# Exibir o gráfico de regressão
st.subheader('Gráfico de Regressão')
plt.figure(figsize=(10, 6))
plt.scatter(wr['pyth'], wr['winrate'])
plt.plot(wr['pyth'], results.predict(), color='red')
plt.xlabel('Pythagoras')
plt.ylabel('Winrate')
plt.title('Regressão Linear')
st.pyplot(plt)
