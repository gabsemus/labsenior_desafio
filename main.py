import streamlit as st
import pandas as pd
import time
from sklearn.svm import LinearSVC
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

home = "# Home page "

st.sidebar.markdown(home)
st.markdown(home)

# lê a base de dados
df = pd.read_csv('https://raw.githubusercontent.com/SeniorSA/seniorlabs-challenge/main/sms_senior.csv',
                 encoding='unicode_escape')
# df.head()

# =====================================================================================================

# Etapa 1: Listar as colunas
# Etapa 2: Definir os tipos que serão somados
# Etapa 3: Eliminar os valores de totais acumulados (Common_Words_Count, Word_Count)
# Etapa 4: Iterar sobre as colunas e validar as seguintes informações:
#          A coluna é de valor númerico?
#          A coluna é dos totais acumulados (Common_Words_Count, Word_Count)?
# Etapa 5: Calcular o total da coluna e salvar num dicionário
# Etapa 6: Organizar o dicionário em ordem decescente pelo valores
# Etapa 7: Questionar o usuário a quantidade de itens que ele deseja visualizar
# Etapa 8: Exibir o TOP-N valores com base na quantidade que o usuário solicitou

st.write("""

Avaliando a nossa base de dados, separamos as palavras mais comuns: 

""")

# 1
colunas = df.columns.values.tolist()
# 2
tipos_numericos = ['float64', 'int64']
# 3
valores_acumulados = ['Common_Word_Count', 'Word_Count']

frequencia_palavras = {}
# 4
for coluna in colunas:
    tipo = df[coluna].dtype
    if tipo in tipos_numericos and coluna not in valores_acumulados:
        # 5
        total = df[coluna].sum()
        frequencia_palavras[coluna] = total

# 6
quantidade_palavras = st.slider('Selecione a quantide de palavras:', 1, 149, 5, 1)

frequencia_palavras = dict(
    sorted(frequencia_palavras.items(),
           key=lambda item: item[1], reverse=True)
    # 7
    [:quantidade_palavras])
# 8
df_frequencia_palavras = pd.DataFrame(frequencia_palavras, index=[0])

st.bar_chart(df_frequencia_palavras)

# =====================================================================================================

# Etapa 1: Criar uma coluna 'Mês' com base na informação da coluna 'Date'
# Etapa 2: Contar os valores da coluna 'Mês' das mensagens spam e não spam
# Etapa 3: Criar função que retorna o gráfico de pizza dos valores totais e percentuais de mensagens por mês


st.write("""

### Avaliação de mensagens Spams e Não-Spams por mês: 

""")

df['mes'] = pd.DatetimeIndex(df['Date']).month

df_mes_spam = df[df['IsSpam'] == 'yes']

df_mes_nao_spam = df[df['IsSpam'] == 'no']

df_mes_spam = df_mes_spam['mes'].value_counts()

df_mes_nao_spam = df_mes_nao_spam['mes'].value_counts()

st.write("""
##### Mensagens de spam por mês: 
""")

st.bar_chart(df_mes_spam)

st.write("""
##### Mensagens não-spam por mês: 
""")

st.bar_chart(df_mes_nao_spam)

# =====================================================================================================

# Etapa 1: Criado um dicionário em que as chaves é o nome da medida calculada e o valor é o resultado do cálculo correspondente
# Etapa 2: Cálculado o máximo da quantidade total de palavras
# Etapa 3: Cálculado o mínimo da quantidade total de palavras
# Etapa 4: Cálculado a média da quantidade total de palavras
# Etapa 5: Cálculado a mediana da quantidade total de palavras
# Etapa 6: Cálculado o desvio padrão da quantidade total de palavras
# Etapa 7: Cálculado a variância da quantidade total de palavras

st.write("""

### Cáluclos e medidas por mês: 

""")

st.write("""
Utilize o menu lateral para selecionar o mês e o cálculo desejado
""")

Total_Palavras = {}

for mes in df.mes.unique():
    df_123 = df[df['mes'] == mes]

    Total_Palavras[('Maximo', mes)] = df_123['Word_Count'].max()

    Total_Palavras[('Mínimo', mes)] = df_123['Word_Count'].min()

    Total_Palavras[('Média', mes)] = df_123['Word_Count'].mean()

    Total_Palavras[('Mediana', mes)] = df_123['Word_Count'].median()

    Total_Palavras[('Desvio Padrão', mes)] = df_123['Word_Count'].std()

    Total_Palavras[('Variância', mes)] = df_123['Word_Count'].var()

left_column, right_column = st.columns(2)

with left_column:
    total_opcao = st.selectbox(
        'Selecione a medida de cálculo: ',
        ('Maximo', 'Mínimo', 'Média', 'Mediana', 'Desvio Padrão', 'Variância'))

    total_mes = st.number_input(
        'Selecione o mês para visualilzação: ',
        min_value=1,
        max_value=3,
        value=1,
        step=1
    )

with right_column:
    st.write(f"##### {total_opcao} do {total_mes}° mês:")
    st.write(f"##### {Total_Palavras[total_opcao, total_mes]}")



# =====================================================================================================

# Etapa 1: Criar uma coluna 'Dia' com base na informação da coluna 'Date';
# Etapa 2: Contar os valores da coluna 'Dia e Mês' e filtrar os valores da mensagens comuns (não spam);
# Etapa 3: Pivotar a tabela, sendo as colunas os valores da coluna 'mes'
# Etapa 4: Pivotar a tabela, sendo as colunas os valores da coluna 'mes'
# Etapa 5: Obter os maiores valores das colunas correspondente aos meses e salvar o valor do dia
# Etapa 6: Para faciliar a visualização, iterei sobre o resultado e salvei num dicionário com as chaves correspondendo ao mês e os valores correspondendo ao dias

st.write("""

### Dia com maior quantidade de mensagens não-spam por mês: 

""")

df['dia'] = pd.DatetimeIndex(df['Date']).day

novo_df = df[df['IsSpam'] == 'no'].value_counts(['dia', 'mes'])

novo_df = novo_df.unstack(level=1)

novo_df = novo_df.idxmax()

dicio_novo = {}

for x in novo_df.items():
    dicio_novo[x[0]] = x[1]

left_column, right_column = st.columns(2)

with left_column:
    mes_input = st.number_input('Selecione o mês: ', min_value=1, max_value=3, value=1, step=1)

with right_column:
    st.metric(label="Dia com a maior quantidade de mensagens não-spam", value=f'{dicio_novo[mes_input]}° dia')

# =====================================================================================================

home = "# Modelo de classificação e análise de regressão "

st.sidebar.markdown(home)
st.markdown(home)

'Avaliando modelo de dados...'

# Add a placeholder
latest_iteration = st.empty()
bar = st.progress(0)

for i in range(100):
    # Update the progress bar with each iteration.
    latest_iteration.text(f'Iteration {i+1}')
    bar.progress(i + 1)
    time.sleep(0.1)

'...clique para visualizar os resultados'

#
nome_colunas_numericas = []

for coluna in colunas:
    tipo = df[coluna].dtype
    if tipo in tipos_numericos:
        nome_colunas_numericas.append(coluna)

x = df[nome_colunas_numericas]

y = df['IsSpam']

modelo = LinearSVC(max_iter=100000)

treino_x, teste_x, treino_y, teste_y = train_test_split(x, y)

modelo.fit(treino_x, treino_y)

previsao = modelo.predict(teste_x)

resultado = accuracy_score(teste_y, previsao) * 100

resultado = round(resultado, 2)

st.metric(label="A taxa de previsao de spam ou não-spam das mensagens é de: ", value=f'{resultado}%')
