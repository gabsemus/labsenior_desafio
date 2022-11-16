from datetime import datetime

#Amazon API Gateway para criar uma API REST
from aws_lambda_powertools.event_handler import APIGatewayRestResolver

#biblioteca que implementa validação de dados (similar ao Pydantic)
from aws_lambda_powertools.utilities.parser import BaseModel, parse, ValidationError

#biblioteca para requisições
import urllib3

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
      
      
#Etapa 0: gerencia o Resources ('/')
#Etapa 1: obtem os dados da requisição
#Etapa 2: valida os dados da requisição com a Classe
#Etapa 3: valida o formato de data/hora 
#Etapa 4: retorna mensagem de erro, caso os campos estejam fora do padrão 
#Etapa 5: realiza a requisição de envio e valida o resultado
#Etapa 6: retorna com o resultado da etapa anterior

# 0
@app.get("/")
def hello_name():
# 1    
    registro_ponto = {}
    registro_ponto['employerId'] = app.current_event.query_string_parameters.get("employerId")
    registro_ponto['employeeId'] = app.current_event.query_string_parameters.get("employeeId")
    registro_ponto['includedAt'] = app.current_event.query_string_parameters.get("includedAt")
# 2    
    registro = validar_dados(registro_ponto)
# 3    
    retorno_data_hora = validar_data_hora(registro_ponto['includedAt'])
# 4    
    if not(registro) or not(retorno_data_hora):
        return {
            "status_code": 400,
            "message": "Campos Incorretos"
        }
# 5
    else:
        retorno = valida_post(

          realizar_post(url, registro.dict(), http)
# 6                    )
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
