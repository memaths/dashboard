import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
import re
import plotly.express as px
import plotly.graph_objs as go
import plotly.figure_factory as ff

df=pd.read_csv("netflix_titles.csv")
df.head()

df.isnull().sum().sort_values(ascending=False)
round(df.isnull().sum()/df.shape[0]*100,2).sort_values(ascending=False)

netflix_shows=df[df['type']=='TV Show']
print(netflix_shows)

netflix_movies=df[df['type']=='Movie']
print(netflix_movies)



# Criar a figura Plotly Pie com tamanho ajustado
colors = ['#1f78b4', '#33a02c']
fig = go.Figure(data=[go.Pie(labels=df['type'].value_counts().index, 
                             values=df['type'].value_counts().values,
                             hole=0.5,
                             title='Filmes vs Séries',
                             marker=dict(colors=colors))])


sns.set(style="darkgrid")

# Criar o gráfico de contagem com tamanho ajustado
plt.figure(figsize=(16, 12))
ax = sns.countplot(x="rating", data=netflix_movies, palette="Set1", order=netflix_movies['rating'].value_counts().index[0:15])

# Adicionar título ao gráfico
ax.set_title('Distribuição de Ratings de Filmes no Netflix', fontsize=16)
plt.xlabel("Classificação")
plt.ylabel("contador")
# Ajustar o espaçamento entre os gráficos
st.set_page_config(layout="wide")
# Criar duas colunas no Streamlit com espaçamento aumentado
col1, col2 = st.columns(2)
# Plotar o primeiro gráfico (Plotly Pie) com tamanho ajustado
with col1:
    st.plotly_chart(fig, use_container_width=True)
# Adicionar espaçamento entre os gráficos
st.write("")
# Plotar o segundo gráfico (Seaborn Countplot) com tamanho ajustado
with col2:
    st.pyplot(plt)


imdb_ratings=pd.read_csv('IMDb ratings.csv',usecols=['weighted_average_vote'])
imdb_titles=pd.read_csv('IMDb movies.csv', usecols=['title','year','genre'])
ratings = pd.DataFrame({'Title':imdb_titles.title,
                    'Release Year':imdb_titles.year,
                    'Rating': imdb_ratings.weighted_average_vote,
                    'Genre':imdb_titles.genre})
ratings.drop_duplicates(subset=['Title','Release Year','Rating'], inplace=True)
ratings.shape   
ratings.dropna()
joint_data=ratings.merge(df,left_on='Title',right_on='title',how='inner')
joint_data=joint_data.sort_values(by='Rating', ascending=False)
top_rated=joint_data[0:10]



import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import mplcursors

# Supondo que 'top_rated' e 'df' sejam seus DataFrames com os dados

# Criar um gráfico de dispersão
plt.figure(figsize=(16, 12))
figb, ax_scatter = plt.subplots(figsize=(10, 6))
scatter = ax_scatter.scatter(top_rated['Title'], top_rated['Rating'], color='orange', marker='o')
ax_scatter.plot(top_rated['Title'], top_rated['Rating'], linestyle='-', color='blue', marker='o', markersize=8)
ax_scatter.set_xlabel('Filme')
ax_scatter.set_ylabel('Nota')
ax_scatter.set_title('Notas dos Filmes')
ax_scatter.set_xticklabels(top_rated['Title'], rotation=45, ha='right')  # Rotacionar os nomes dos filmes para melhor visualização

# Adicionar anotações interativas ao passar o mouse sobre os pontos
cursor = mplcursors.cursor(scatter, hover=True)
cursor.connect("add", lambda sel: sel.annotation.set_text(f"Nota: {sel.artist.get_offsets()[sel.target.index, 1]}"))


# Exibir o gráfico de dispersão
plt.tight_layout()

# Calcular os top 10 países que mais produzem filmes
top_countries = df['country'].value_counts().head(10)

# Criar um gráfico de barras
plt.figure(figsize=(16, 12))
toppaises, ax_bar = plt.subplots(figsize=(10, 6))
top_countries.plot(kind='bar', color='skyblue', ax=ax_bar)
ax_bar.set_xlabel('País')
ax_bar.set_ylabel('quantidade')
ax_bar.set_title('Top 10 Países que Mais Produzem conteudo')
ax_bar.set_xticklabels(top_countries.index, rotation=45, ha='right')  # Rotacionar os nomes dos países para melhor visualização
plt.tight_layout()

# Exibir os gráficos lado a lado no Streamlit
col1, col2 = st.columns(2)
col1.pyplot(figb)
col2.pyplot(toppaises)


# Configurar o estilo do Seaborn
sns.set(style="darkgrid")

# Criar o gráfico de contagem
ano, ax = plt.subplots(figsize=(12, 10))
sns.countplot(y="release_year", data=df, order=df['release_year'].value_counts().index[0:15], palette="viridis", ax=ax)

# Adicionar números do contador à direita de cada barra
for p in ax.patches:
    ax.annotate(f'{int(p.get_width())}', (p.get_width() + 0.1, p.get_y() + p.get_height() / 2.), va='center', fontsize=9, color='black')

# Adicionar título ao gráfico
ax.set_title('Contagem de Filmes por Ano de Lançamento (Top 15)', fontsize=16)
ax.set_ylabel("Ano de Estreia")
ax.set_xlabel("Contador")



# Remover eixo esquerdo (background)


# Remover bordas


df.director.value_counts().head(10)
df.listed_in.value_counts().head(10)

# Configurar o estilo do Seaborn
sns.set(style="whitegrid", rc={"axes.facecolor": (0, 0, 0, 0)})

# Criar o gráfico de contagem
cont, ax = plt.subplots(figsize=(12, 10))
sns.countplot(y="listed_in", data=df, order=df['listed_in'].value_counts().index[0:15], palette="Set2", ax=ax)

# Adicionar números do contador à direita de cada barra
for p in ax.patches:
    ax.annotate(f'{int(p.get_width())}', (p.get_width() + 0.1, p.get_y() + p.get_height() / 2.), va='center', fontsize=9, color='black')

# Adicionar título ao gráfico
ax.set_title('Contagem de Filmes por Categoria (Top 15)', fontsize=16)
ax.set_ylabel("Gênero")
ax.set_xlabel("Contador")


# Remover bordas

col1, col2 = st.columns(2)
col1.pyplot(ano)
col2.pyplot(cont)

# Contar o número de filmes por diretor
top_directors = df['director'].value_counts().head(10)

# Configurar o estilo do Seaborn
sns.set(style="whitegrid", rc={"axes.facecolor": (0, 0, 0, 0)})

# Criar um gráfico de barras
direct, ax = plt.subplots(figsize=(12, 6))
bar_plot = sns.barplot(x=top_directors.index, y=top_directors.values, palette="viridis", ax=ax)
plt.title('Top 10 Diretores com Mais Filmes')
plt.xlabel('Diretores')

# Rotacionar os rótulos do eixo x para melhor visualização
plt.xticks(rotation=45, ha='right')
sns.despine(left=True, right=True, top=True, bottom=True, ax=ax)

# Adicionar rótulos com a quantidade exata de filmes ao lado das barras
for index, value in enumerate(top_directors.values):
    ax.text(index, value + 0.1, str(value), ha='center', va='bottom', fontsize=9)

# Adicionar nomes dos diretores no eixo x
ax.set_xticklabels(top_directors.index)
ax.set_ylabel('Quantidade de conteudo produzido')
# Remover rótulos no eixo y
ax.set_yticks([])

plt.show()

# Obtenha a lista de todos os atores
all_actors = [actor for sublist in df['cast'].dropna().str.split(', ') for actor in sublist]

# Crie uma tabela dinâmica para contar a frequência de cada ator
top_actors = pd.Series(all_actors).value_counts().head(10)

# Configurar o estilo do Seaborn
sns.set(style="whitegrid", rc={"axes.facecolor": (0, 0, 0, 0)})

# Criar um gráfico de barras
actor, ax = plt.subplots(figsize=(12, 6))
bar_plot = sns.barplot(x=top_actors.index, y=top_actors.values, palette="colorblind", ax=ax)
plt.title('Top 10 Atores Mais Frequentes na Netflix')
plt.xlabel('Atores')

# Rotacionar os rótulos do eixo x para melhor visualização
plt.xticks(rotation=45, ha='right')

# Adicionar rótulos com a quantidade exata de filmes ao lado das barras
for index, value in enumerate(top_actors.values):
    ax.text(index, value + 0.1, str(value), ha='center', va='bottom', fontsize=9)

# Remover fundo e manter linhas de grade
sns.despine(left=True, right=True, top=True, bottom=True, ax=ax)
ax.set_facecolor("none")  # Define a cor de fundo como transparente
ax.set_ylabel('Quantidade de conteudo produzido')
# Remover rótulos no eixo y
ax.set_yticks([])

# Exibir o gráfico no Streamlit
col1, col2 = st.columns(2)
col1.pyplot(direct)
col2.pyplot(actor)


