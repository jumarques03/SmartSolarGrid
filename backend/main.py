from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

app=FastAPI()

def corpo_resposta_para_Alexa(texto, acabar_sessao):
    resposta = {
            "version": "1.0",
            "response": {
                "outputSpeech": {
                    "type": "PlainText",
                    "text": texto
                },
                "shouldEndSession": acabar_sessao
            }
        }
    
    return JSONResponse(content=resposta, status_code=200)   # Retorna uma resposta HTTP no formato JSON

def resposta_erro_padrao(e):
    print(e)
    corpo_resposta_para_Alexa("Desculpe, houve um problema ao processar sua solicitação.", True)

@app.post("/alexa/status-inversor")
async def saber_status_inversor(request: Request):
    try: 
        corpo_intent= await request.json()  # Espera receber o corpo do intent
        intent=corpo_intent["request"]["intent"]["name"]    # Acessando o nome do intent requerido pelo usuário

        if intent== "StatusInversorIntent":
            texto_resposta = "Status Inversor...."    # Aqui ocorreria uma requisição para a API da Goodwe 
        else:
            texto_resposta= "Desculpe, não entendi sua solicitação! Poderia repetir por favor?"

        # Resposta no formato que a Alexa espera receber
        resposta=corpo_resposta_para_Alexa(texto_resposta, False)
        return resposta
        
    except Exception as e:
        return resposta_erro_padrao(e)
    
# Função para site receber o status do inversor

@app.post("/alexa/acionar-cargas-prioritarias")
async def acionar_cargas_prioritarias(request: Request):
    try: 
        corpo_intent= await request.json()  # Espera receber o corpo do intent
        intent=corpo_intent["request"]["intent"]["name"]    # Acessando o nome do intent requerido pelo usuário

        if intent== "AcionarCargasPrioritariasIntent":
            texto_resposta= "Acionando cargas prioritárias..."   # Aqui ocorreria uma requisição para a API da Goodwe 
        else:
            texto_resposta="Desculpe, não entendi sua solicitação! Poderia repetir por favor?"

        resposta=corpo_resposta_para_Alexa(texto_resposta, False)
        return resposta
    
    except Exception as e:
        return resposta_erro_padrao(e)

# Função para site saber quais cargas prioritárias estão ativas
