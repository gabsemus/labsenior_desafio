# Read Me

Link do desafio: 

https://github.com/SeniorSA/seniorlabs-challenge/blob/main/data-science.md

App para visualização dos dados e achados: 

https://gabsemus-labsenior-desafio-main-ku99fy.streamlit.app/
  
# Documentação dos Desafios e Soluções:

#  Desafio 1:
Exibir gráfico as palavras mais frequentes em toda a base de dados (Ex.: gráfico de barras, nuvem de palavras, etc).
 
Etapas para resolução do desafio:

  Etapa 1: Listar as colunas
  
  Etapa 2: Definir os tipos que serão somados
  
  Etapa 3: Eliminar os valores de totais acumulados (Common_Words_Count, Word_Count)
  
  Etapa 4: Iterar sobre as colunas e validar as seguintes informações:
  
  A coluna é de valor númerico?
  
  A coluna é dos totais acumulados (Common_Words_Count, Word_Count)?
  
  Etapa 5: Calcular o total da coluna e salvar num dicionário
  
  Etapa 6: Organizar o dicionário em ordem decescente pelo valores
  
  Etapa 7: Questionar o usuário a quantidade de itens que ele deseja visualizar
  
  Etapa 8: Exibir o TOP-N valores com base na quantidade que o usuário solicitou
  
#  Desafio 2:
Exibir gráfico com as quantidades de mensagens comuns e spams para cada mês;
 
Etapas para resolução do desafio:
  
  Etapa 1: Criar uma coluna 'Mês' com base na informação da coluna 'Date'
  
  Etapa 2: Contar os valores da coluna 'Mês' das mensagens spam e não spam
  
  Etapa 3: Exibir gráfico de mensagens spams e não-spams
  
#  Desafio 3:
Calcular o máximo, o mínimo, a média, a mediana, o desvio padrão e a variância da quantidade total de palavras (Word_Count) para cada mês:
 
Etapas para resolução do desafio:
  
  Etapa 1: Criado um dicionário em que as chaves são os nomes das medidas calculadas e o meses e os valores são os resultados dos cálculos correspondentes
  
  Etapa 2: Cálculado o máximo da quantidade total de palavras
  
  Etapa 3: Cálculado o mínimo da quantidade total de palavras
  
  Etapa 4: Cálculado a média da quantidade total de palavras
  
  Etapa 5: Cálculado a mediana da quantidade total de palavras
  
  Etapa 6: Cálculado o desvio padrão da quantidade total de palavras
  
  Etapa 7: Cálculado a variância da quantidade total de palavras
  
  Etapa 8: Questiona o cálculo e o mês e devolve o resultado
  
#  Desafio 4:
Exibir o dia de cada mês que possui a maior sequência de mensagens comuns (não spam):
 
Etapas para resolução do desafio:
  
  Etapa 1: Criar uma coluna 'Dia' com base na informação da coluna 'Date';
  
  Etapa 2: Contar os valores da coluna 'Dia e Mês' e filtrar os valores da mensagens comuns (não spam);
  
  Etapa 3: Pivotar a tabela, sendo as colunas os valores da coluna 'mes'
  
  Etapa 4: Obter os maiores valores das colunas correspondente aos meses e salvar o valor do dia
  
  Etapa 5: Para faciliar a visualização, iterei sobre o resultado e salvei num dicionário com as chaves correspondendo ao mês e os valores correspondendo ao dias
  
  Etapa 6: Questiona o mês e devolve o dia com mais quantidade

#  Desafio 5:
Aplique um método capaz de classificar automaticamente as mensagens como “comum” e “spam”:
 
Etapas para resolução do desafio:
  
  Etapa 1: Separar os atributos númericos dos objetos;
  
  Etapa 2: Separar os valores de treino e teste;
  
  Etapa 3: Define modelo de cálculo LinearSVC e invoca classe;
  
  Etapa 4: Treina modelo de teste
  
  Etapa 5: Cria modelo de previsão binário
  
  Etapa 6: Invoca função de avaliação de resultado (teste x treino)

# Jusitificativa:

O que é SPAM?

SPAM ou Sending and Posting Advertisement in Mass (Enviar e Postar Publicidade em Massa).
O SPAM é uma mensagem eletrônica que chega ao usuário sem a sua permissão ou sem seu desejo em recebê-lo.

Acredito que há uma série de métodos que podem ser utilizados para avaliar se uma mensagem é spam ou não.

O método de avaliação pode variar conforme o local do nó em que o método vai ser implementado na cadeia de envio-recebimento da mensagem e das informações disponivéis.
Exemplo:
  Caso o método seja aplicado no destinatário, podemos ter informações como:
    Contato do Remetente;
    Lista de contatos do destinatário;
    Demais mensagens da conversa;

Caso o método seja aplicado no Remetente, podemos ter informações como:
    Frequência de envio;
    Número de destinatários;
    Número de destinatários diferentes.
    
Neste caso, o método está sendo aplicado em um nó entre os destinatários (N) e remetentes (N) e temos acessos ao teor da mensagem, data de envio e extratificação númerica relacional do número de utilização de determinadas palavras.

Foi utilizado um modelo de classificador linear binário não probabilístico, o modelo toma como entrada um conjunto de dados (quantidade de repetição de palavras comuns por palavra comun, quantidade total de palavras da mensagem, quantidade de palavras comuns na mensagem e retorna, para cada entrada dada, se a mensagem é spam (yes) ou não-spam (no).

O resultado final, comparando os valores de treino e teste, superou ~90% de acertividade.

Ferramentas utilizadas: 
  
  pandas: https://pandas.pydata.org/
  
  streamlit: https://streamlit.io/
  
  scikit-learn: https://scikit-learn.org/
