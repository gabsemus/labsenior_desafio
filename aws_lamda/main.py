from datetime import datetime

#biblioteca para requisições
import urllib3

#Amazon API Gateway para criar uma API REST
from aws_lambda_powertools.event_handler import APIGatewayRestResolver

#biblioteca que implementa validação de dados (similar ao Pydantic)
from aws_lambda_powertools.utilities.parser import BaseModel, parse, ValidationError

#instância para criação de requisições
http = urllib3.PoolManager()
#instância para gerenciar o gateway api
app = APIGatewayRestResolver()

#endereço do sistema legado
url = 'https://api.mockytonk.com/proxy/ab2198a3-cafd-49d5-8ace-baac64e72222'

#classe para registro ponto
class RegistroPonto(BaseModel):
    employerId: int
    employeeId: int
    includedAt: str
    
# obtem os dados da sessão e devolve como um dict
def captura_dados(dados_requisicao):
    registro_ponto = {}
    registro_ponto['employerId'] = dados_requisicao.get("employerId")
    registro_ponto['employeeId'] = dados_requisicao.get("employeeId")
    registro_ponto['includedAt'] = dados_requisicao.get("includedAt")
    return registro_ponto
    
#parsear os dados do objeto na classe
#caso seja encontrado dados, deveretornar status False
#caso seja não encontrado dados, deveretornar o objeto da classe
def validar_dados(objeto):
    try:
        parsed_payload: RegistroPonto = parse(model=RegistroPonto, event=objeto)
        return parsed_payload
    except ValidationError:
        return False
        
#cria a requisição de envio do registro ponto
#devolve o status
def realizar_post(url, payload_integracao, resquests):
    r = resquests.request('POST', url, fields = payload_integracao)
    return r.status

#valida o retorno da requisição
#retorna mensagem de sucesso ou erro
def valida_post(status):
    if status != 200:
        return {"message": "Erro de Envio!"}
    return {"message": "Registrado com Sucesso!"}
    
#valida o atribuo 'includedAt' com o modelo de dados datetime
#devolve o resultado da validação
def validar_data_hora(datetime_str):
    try:
        datetime_object = datetime.strptime(datetime_str, '%Y-%m-%d %H:%M:%S')
        return True 
    except ValueError as ve:
        return False

#valida se todos os dados foram enviados        
def validar_atributos(dados_requisicao):
    lista_validacao = []
    lista_validacao.append(dados_requisicao.get("employerId"))
    lista_validacao.append(dados_requisicao.get("employeeId"))
    lista_validacao.append(dados_requisicao.get("includedAt"))
    if None in lista_validacao:
        return False
    else:
        return True
        
#Etapa 0: gerencia o Resources ('/')
#Etapa 1: valida o envio das informações
#Etapa 2: obtem os dados da requisição
#Etapa 3: valida os dados da requisição com a Classe
#Etapa 4: valida o formato de data/hora 
#Etapa 5: retorna mensagem de erro, caso os campos estejam fora do padrão 
#Etapa 6: realiza a requisição de envio e valida o resultado
#Etapa 7: retorna com o resultado da etapa anterior

# 0
@app.get("/")
def hello_name():
# 1
    dados_requisicao = app.current_event.query_string_parameters
    
    if not(validar_atributos(dados_requisicao)):
    
        return {"message": "Aguardando dados!"}        
    else:
# 2        
        registro_ponto = captura_dados(dados_requisicao)
# 3        
        registro = validar_dados(registro_ponto)
# 4        
        retorno_data_hora = validar_data_hora(registro_ponto['includedAt'])
# 5    
        if not(registro) or not(retorno_data_hora):
            
            return {
                "status_code": 400,
                "message": "Campos Incorretos"
                }
# 6                
        else:
            retorno = valida_post(
                        realizar_post(url, registro.dict(), http)
                    )
# 7                    
        return retorno

#Etapa 1: Devolve o retorno do recurso ('/') a função lamba
#Etapa 2: valida erro da função lambda
#Etapa 3: caso erro, devolve erro

def lambda_handler(event, context):
# 1
    try:
        return app.resolve(event, context)
# 2        
    except Exception as e:
# 3
        return {
                'body': f'Erro:{e}'
            }
