from fastapi import APIRouter, Request
from backend.funcs_auxiliares.funcs_auxiliares import corpo_resposta_para_Alexa, resposta_erro_padrao

rota_alexa= APIRouter(prefix="/alexa")

@rota_alexa.post("/status-inversor")
async def alexa_saber_status_inversor(request: Request):
    try: 
        corpo_intent= await request.json()  # Espera receber o corpo do intent
        intent=corpo_intent["request"]["intent"]["name"]    # Acessando o nome do intent requerido pelo usuário

        if intent== "StatusInversorIntent":
            texto_resposta = "Status Inversor...."    # Alexa falará sobre o inversor (se está tudo normal, se tem alguma coisa a ser feita...)
        else:
            texto_resposta= "Desculpe, não entendi sua solicitação! Poderia repetir por favor?"

        # Resposta no formato que a Alexa espera receber
        resposta=corpo_resposta_para_Alexa(texto_resposta, False)
        return resposta
        
    except Exception as e:
        return resposta_erro_padrao(e)

@rota_alexa.post("/dica-economia")
async def alexa_dica_de_economia(request: Request):
    try: 
        corpo_intent= await request.json()  # Espera receber o corpo do intent
        intent=corpo_intent["request"]["intent"]["name"]    # Acessando o nome do intent requerido pelo usuário

        if intent== "DicaEconomiaIntent":
            texto_resposta= "A minha dica é..."   # Alexa dará uma sugestão baseada no consumo de energia da casa 
        else:
            texto_resposta="Desculpe, não entendi sua solicitação! Poderia repetir por favor?"

        resposta=corpo_resposta_para_Alexa(texto_resposta, False)
        return resposta
    
    except Exception as e:
        return resposta_erro_padrao(e)
 
@rota_alexa.post("/nivel-energia-bateria")
async def alexa_nivel_energia_bateria(request: Request):
    try:
        corpo_intent= await request.json()  # Espera receber o corpo do intent
        intent=corpo_intent["request"]["intent"]["name"]    # Acessando o nome do intent requerido pelo usuário

        if intent== "NivelBateriaIntent":
            texto_resposta = "Nível da bateria...."    # Alexa falará o nivel da bateria e mostrará se ela está carregando ou sendo consumida
        else:
            texto_resposta= "Desculpe, não entendi sua solicitação! Poderia repetir por favor?"

        resposta=corpo_resposta_para_Alexa(texto_resposta, False)
        return resposta
        
    except Exception as e:
        return resposta_erro_padrao(e)

