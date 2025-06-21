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
    return resposta

def erro(e):
    print(e)
    resposta_erro=corpo_resposta_para_Alexa("Desculpe, houve um problema ao processar sua solicitação.", True)
    return JSONResponse(content=resposta_erro, status_code=200) 

@app.post("/status-inversor")
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
        return JSONResponse(content=resposta, status_code=200)   # Retorna uma resposta HTTP no formato JSON
    
    except Exception as e:
        return erro(e)
    
@app.post("/acionar-cargas-prioritarias")
async def acionar_cargas_prioritarias(request: Request):
    try: 
        corpo_intent= await request.json()  # Espera receber o corpo do intent
        intent=corpo_intent["request"]["intent"]["name"]    # Acessando o nome do intent requerido pelo usuário

        if intent== "AcionarCargasPrioritariasIntent":
            texto_resposta= "Acionando cargas prioritárias..."   # Aqui ocorreria uma requisição para a API da Goodwe 
        else:
            texto_resposta="Desculpe, não entendi sua solicitação! Poderia repetir por favor?"

        resposta=corpo_resposta_para_Alexa(texto_resposta, False)
        return JSONResponse(content=resposta, status_code=200)
    
    except Exception as e:
        return erro(e)
