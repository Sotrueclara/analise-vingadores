import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Leitura do arquivo CSV
avengers_df = pd.read_csv('data/avengers.csv', encoding='ISO-8859-1')

# Preenchimento de valores nulos em 'Return1' e conversão de colunas para valores binários
avengers_df['Return1'] = avengers_df['Return1'].fillna('NO')
avengers_df['Death1'] = avengers_df['Death1'].map({'YES': 1, 'NO': 0})
avengers_df['Return1'] = avengers_df['Return1'].map({'YES': 1, 'NO': 0})

# Distribuição de gênero
print(avengers_df['Name/Alias'].nunique())
print(avengers_df['Gender'].value_counts())

gender_counts = avengers_df['Gender'].value_counts()
plt.figure(figsize=(6, 6))
plt.pie(gender_counts, labels=gender_counts.index, autopct='%.1f%%', startangle=140, colors=['#66b3ff', '#ff9999'])
plt.title('Distribuição de Gênero dos Vingadores')
plt.savefig('images/distribuicao_genero.png')
plt.show()

# Média de aparições
media_aparicoes = avengers_df['Appearances'].mean()
print(round(media_aparicoes, 2))

plt.hist(avengers_df['Appearances'].dropna(), bins=30, color='#66b3ff', edgecolor='black')
plt.title('Distribuição de Aparições dos Personagens')
plt.xlabel('Número de Aparições')
plt.ylabel('Quantidade de Personagens')
plt.savefig('images/aparicoes_histograma.png')
plt.show()

# Comparação de aparições por gênero
male_df = avengers_df[avengers_df['Gender'] == 'MALE']
female_df = avengers_df[avengers_df['Gender'] == 'FEMALE']

plt.hist(female_df['Appearances'], bins=20, alpha=0.5, label='Feminino')
plt.xlabel('Número de Aparições')
plt.ylabel('Número de Personagens')
plt.legend()
plt.savefig('images/aparicoes_feminino.png')
plt.show()

# Evolução do número de personagens por ano
personagens_por_ano = avengers_df.groupby('Year').size()
plt.figure(figsize=(6, 6))
plt.plot(personagens_por_ano.index, personagens_por_ano.values)
plt.title('Número de Personagens por Ano')
plt.xlabel('Ano')
plt.ylabel('Quantidade de Personagens')
plt.savefig('images/personagens_por_ano.png')
plt.show()

# Evolução a partir de 1939
avengers_df_filtrado = avengers_df[avengers_df['Year'] >= 1939]
personagens_filtrados = avengers_df_filtrado.groupby('Year').size()
personagens_filtrados.plot(marker='o')
plt.title('Número de Personagens por Ano (a partir de 1939)')
plt.xlabel('Ano')
plt.ylabel('Número de Personagens')
plt.savefig('images/personagens_desde_1939.png')
plt.show()

# Distribuição por década e gênero
avengers_df['decada'] = avengers_df['Year'] // 10 * 10
decada_genero = avengers_df.groupby(['decada', 'Gender']).size().unstack()

decada_genero.plot(kind='bar', color=['lightcoral', 'seagreen'])
plt.title('Distribuição de Gênero por Década')
plt.xlabel('Década')
plt.ylabel('Número de Personagens')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('images/genero_por_decada.png')
plt.show()

# Afiliação por gênero
frequencia_afil = pd.crosstab(avengers_df['Gender'], avengers_df['Honorary'])
frequencia_afil.plot(kind='bar', stacked=False)
plt.title('Distribuição de Afiliação por Gênero (Frequência Bruta)')
plt.xlabel('Gênero')
plt.ylabel('Número de Personagens')
plt.legend(title='Honorary')
plt.tight_layout()
plt.savefig('images/afiliacao_bruta_genero.png')
plt.show()

# Afiliação em percentual por gênero
percentual_por_genero = pd.crosstab(avengers_df['Gender'], avengers_df['Honorary'], normalize='index')
percentual_por_genero.columns = ['Academy', 'Full', 'Honorary', 'Probationary']
percentual_por_genero.plot(kind='bar', stacked=False)
plt.title('Distribuição Percentual de Afiliação por Gênero')
plt.xlabel('Gênero')
plt.ylabel('Porcentagem (%)')
plt.legend(title='Honorary', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.savefig('images/afiliacao_percentual_genero.png')
plt.show()

# Afiliação em percentual por tipo
percentual_por_coluna = pd.crosstab(avengers_df['Gender'], avengers_df['Honorary'], normalize='columns')
percentual_por_coluna.columns = percentual_por_coluna.columns.str.strip()

fig, ax = plt.subplots(figsize=(8, 5))
percentual_por_coluna.T.plot(kind='bar', ax=ax)
ax.set_title('Distribuição Percentual por Tipo de Afiliação')
ax.set_xlabel('Tipo de Afiliação')
ax.set_ylabel('Porcentagem (%)')
ax.legend(title='Gênero', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.savefig('images/afiliacao_percentual_tipo.png')
plt.show()

# Análise de mortes e retornos
avengers_df['morreu'] = avengers_df[['Death1', 'Death2', 'Death3', 'Death4', 'Death5']].any(axis=1)
print(avengers_df.groupby('Gender')['morreu'].sum())

mortos_por_genero = {'MALE': 48, 'FEMALE': 21}
total_por_genero = {'MALE': 115, 'FEMALE': 58}
percentual_mortos = [mortos_por_genero['MALE'] / total_por_genero['MALE'] * 100,
                     mortos_por_genero['FEMALE'] / total_por_genero['FEMALE'] * 100]

plt.bar(['MALE', 'FEMALE'], percentual_mortos, color=['skyblue', 'lightcoral'])
plt.title('Percentual de Mortes por Gênero')
plt.ylabel('% de Personagens que Morreram')
plt.ylim(0, 100)
plt.grid(axis='y', linestyle='--', alpha=0.7)
for i, valor in enumerate(percentual_mortos):
    plt.text(i, valor + 2, f'{valor:.1f}%', ha='center', fontsize=10)
plt.savefig('images/mortes_por_genero.png')
plt.show()

avengers_df['retornou'] = avengers_df[['Return1', 'Return2', 'Return3', 'Return4', 'Return5']].any(axis=1)
retorno_apos_morte = avengers_df[avengers_df['morreu']].groupby('Gender')['retornou'].sum()

retorno_percentual = [62.5, 76.19]
plt.bar(['MALE', 'FEMALE'], retorno_percentual, color=['pink', 'blue'])
plt.ylabel('% de Personagens que Retornaram')
plt.xlabel('Gênero')
plt.ylim(0, 100)
plt.grid(axis='y', linestyle='--', alpha=0.7)
for i, valor in enumerate(retorno_percentual):
    plt.text(i, valor + 2, f'{valor:.1f}%', ha='center', fontsize=10)
plt.savefig('images/retorno_pos_morte.png')
plt.show()

# Análise de quartis
avengers_df['quartil'] = pd.qcut(avengers_df['Appearances'], q=4, labels=['Q1', 'Q2', 'Q3', 'Q4'])
percentual_mortes_quartil = avengers_df.groupby('quartil')['Death1'].mean()

percentual_mortes_quartil.plot(kind='bar')
plt.title('Percentual de Mortes por Quartil de Aparições')
plt.xlabel('Quartil')
plt.ylabel('Percentual de Mortes')
plt.ylim(0, 1)
plt.savefig('images/mortes_por_quartil.png')
plt.show()

# Heatmap: média de aparições por gênero e morte
media_aparicoes_heatmap = avengers_df.groupby(['Gender', 'Death1'])['Appearances'].mean().unstack().rename(columns={0: 'NO', 1: 'YES'})
print(media_aparicoes_heatmap)

sns.heatmap(media_aparicoes_heatmap, annot=True, fmt='.0f', cmap='YlGnBu')
plt.title('Média de Aparições por Gênero e Morte')
plt.xlabel('Morreu?')
plt.ylabel('Gênero')
plt.savefig('images/heatmap_aparicoes_genero_morte.png')
plt.show()
