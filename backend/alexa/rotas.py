from fastapi import APIRouter, Request
from funcs_auxiliares.funcs_auxiliares import corpo_resposta_para_Alexa, resposta_erro_padrao

rota_alexa= APIRouter(prefix="/alexa")

@rota_alexa.post("/status-inversor")
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
    
@rota_alexa.post("/acionar-cargas-prioritarias")
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
    
@rota_alexa.post("/armazenar-energia")
async def armazenar_energia(request: Request):
    try:
        corpo_intent= await request.json()  # Espera receber o corpo do intent
        intent=corpo_intent["request"]["intent"]["name"]    # Acessando o nome do intent requerido pelo usuário

        if intent== "ArmazenarEnergiaIntent":
            texto_resposta = "Armazenando energia...."    # Aqui ocorreria uma requisição para a API da Goodwe 
        else:
            texto_resposta= "Desculpe, não entendi sua solicitação! Poderia repetir por favor?"

        resposta=corpo_resposta_para_Alexa(texto_resposta, False)
        return resposta
        
    except Exception as e:
        return resposta_erro_padrao(e)
    
@rota_alexa.post("/ativar-modo")
async def ativar_modo(request: Request):
    try:
        corpo_intent = await request.json()
        intent = corpo_intent["request"]["intent"]["name"]

        if intent == "AtivarModoIntent":
            slot_valor = corpo_intent["request"]["intent"]["slots"]["modo"]["value"]

            if slot_valor.lower() == "on":
                texto_resposta = "Ativando modo On Grid..." # Aqui ocorreria uma requisição para a API da Goodwe 
            elif slot_valor.lower() == "off":
                texto_resposta = "Ativando modo Off Grid..."    # Aqui ocorreria uma requisição para a API da Goodwe 
            else:
                texto_resposta = "Modo informado não é reconhecido."

        else:
            texto_resposta = "Desculpe, não entendi sua solicitação! Poderia repetir por favor?"

        return corpo_resposta_para_Alexa(texto_resposta, False)
    except Exception as e:
        return resposta_erro_padrao(e)
