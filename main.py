import streamlit as st
import pandas as pd
import time
from sklearn.svm import LinearSVC
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

st.markdown("# Senior Labs Challenge ")

# lê a base de dados
df = pd.read_csv('https://raw.githubusercontent.com/SeniorSA/seniorlabs-challenge/main/sms_senior.csv',
                 encoding='unicode_escape')
# df.head()

# Definindo as guias
desafio1, desafio2, desafio3, desafio4, desafio5 = st.tabs(
    ["Desafio 1", "Desafio 2", "Desafio 3", "Desafio 4", "Desafio 5"])

with desafio1:
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

    ### Avaliando a nossa base de dados, separamos as palavras mais comuns: 

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
# Etapa 3: Exibir gráfico de mensagens spams e não-spams

with desafio2:
    st.write("""

    ### Avaliação de mensagens Spams e Não-Spams por mês: 

    """)
    # 1
    df['mes'] = pd.DatetimeIndex(df['Date']).month

    # 2
    df_mes_spam = df[df['IsSpam'] == 'yes']

    df_mes_nao_spam = df[df['IsSpam'] == 'no']

    df_mes_spam = df_mes_spam['mes'].value_counts()

    df_mes_nao_spam = df_mes_nao_spam['mes'].value_counts()

    # 3
    st.write("""
    ##### Mensagens de spam por mês: 
    """)

    st.bar_chart(df_mes_spam)

    st.write("""
    ##### Mensagens não-spam por mês: 
    """)

    st.bar_chart(df_mes_nao_spam)

# =====================================================================================================

# Etapa 1: Criado um dicionário em que as chaves são os nomes das medidas calculadas e o meses e os valores são os resultados dos cálculos correspondentes
# Etapa 2: Cálculado o máximo da quantidade total de palavras
# Etapa 3: Cálculado o mínimo da quantidade total de palavras
# Etapa 4: Cálculado a média da quantidade total de palavras
# Etapa 5: Cálculado a mediana da quantidade total de palavras
# Etapa 6: Cálculado o desvio padrão da quantidade total de palavras
# Etapa 7: Cálculado a variância da quantidade total de palavras
# Etapa 8: Questiona o cálculo e o mês e devolve o resultado

with desafio3:
    st.write("""

    ### Cáluclos e medidas por mês: 

    """)

    st.write("""
    Utilize o menu lateral para selecionar o mês e o cálculo desejado
    """)
    # 1
    Total_Palavras = {}

    for mes in df.mes.unique():
        df_123 = df[df['mes'] == mes]
        # 2
        Total_Palavras[('Maximo', mes)] = df_123['Word_Count'].max()
        # 3
        Total_Palavras[('Mínimo', mes)] = df_123['Word_Count'].min()
        # 4
        Total_Palavras[('Média', mes)] = df_123['Word_Count'].mean()
        # 5
        Total_Palavras[('Mediana', mes)] = df_123['Word_Count'].median()
        # 6
        Total_Palavras[('Desvio Padrão', mes)] = df_123['Word_Count'].std()
        # 7
        Total_Palavras[('Variância', mes)] = df_123['Word_Count'].var()
    # 8

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
# Etapa 4: Obter os maiores valores das colunas correspondente aos meses e salvar o valor do dia
# Etapa 5: Para faciliar a visualização, iterei sobre o resultado e salvei num dicionário com as chaves correspondendo ao mês e os valores correspondendo ao dias
# Etapa 6: Questiona o mês e devolve o dia com mais quantidade
with desafio4:
    st.write("""

    ### Dia com maior quantidade de mensagens não-spam por mês: 

    """)
    # 1
    df['dia'] = pd.DatetimeIndex(df['Date']).day
    # 2
    novo_df = df[df['IsSpam'] == 'no'].value_counts(['dia', 'mes'])
    # 3
    novo_df = novo_df.unstack(level=1)
    # 4
    novo_df = novo_df.idxmax()
    # 5
    dicio_novo = {}

    for x in novo_df.items():
        dicio_novo[x[0]] = x[1]
    # 6
    left_column, right_column = st.columns(2)

    with left_column:
        mes_input = st.number_input('Selecione o mês: ', min_value=1, max_value=3, value=1, step=1)

    with right_column:
        st.metric(label="Dia com a maior quantidade de mensagens não-spam", value=f'{dicio_novo[mes_input]}° dia')

# =====================================================================================================

# Etapa 1: Separar os atributos númericos dos objetos;
# Etapa 2: Separar os valores de treino e teste;
# Etapa 3: Define modelo de cálculo LinearSVC e invoca classe;
# Etapa 4: Treina modelo de teste
# Etapa 5: Cria modelo de previsão binário
# Etapa 6: Invoca função de avaliação de resultado (teste x treino)
with desafio5:
    "# Modelo de classificação e análise de regressão "
    
    botao_resultado = st.button('Exibir Resultados')
    
    # 1
    nome_colunas_numericas = []

    for coluna in colunas:
        tipo = df[coluna].dtype
        if tipo in tipos_numericos:
            nome_colunas_numericas.append(coluna)

    x = df[nome_colunas_numericas]

    y = df['IsSpam']

    # 2
    treino_x, teste_x, treino_y, teste_y = train_test_split(x, y)

    # 3
    modelo = LinearSVC(max_iter=100000)

    # 4
    modelo.fit(treino_x, treino_y)

    # 5
    previsao = modelo.predict(teste_x)

    # 6
    resultado = accuracy_score(teste_y, previsao) * 100

    resultado = round(resultado, 2)
    
    if botao_resultado:

        latest_iteration = st.empty()
        bar = st.progress(0)
        'Avaliando modelo de dados...'
        for i in range(100):
            # Update the progress bar with each iteration.
            latest_iteration.text(f'Iteration {i + 1}')
            bar.progress(i + 1)
            time.sleep(0.05)
            if i == 25:
                '...separando os spams'
            if i == 50:
                '...separando os não-spams'
            if i == 75:
                '...validando resultados'
            if i == 95:
                '...exibindo métricas'
        
        st.write("##### A taxa de previsao de spam ou não-spam das mensagens é de: ")
        st.write(f"##### {resultado}")
