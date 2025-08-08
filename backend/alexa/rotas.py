from fastapi import APIRouter, Request
from backend.funcs_auxiliares.funcs_auxiliares import corpo_resposta_para_Alexa, resposta_erro_padrao
from simulacoes.status_inversor_simulado import info_inversor

rota_alexa= APIRouter(prefix="/alexa")

@rota_alexa.post("/info-inversor")
async def alexa_saber_info_inversor(request: Request):
    try: 
        corpo_intent= await request.json()  # Espera receber o corpo do intent
        intent=corpo_intent["request"]["intent"]["name"]    # Acessando o nome do intent requerido pelo usuário

        if intent== "StatusInversorIntent":
            infos_inversor = info_inversor()
            texto_resposta = f"Seu painel solar está gerando {infos_inversor['FV(W)']} Watts, o nível de sua bateria é {infos_inversor['SOC(%)']} e sua rede está consumindo no total {infos_inversor['Carga(W)']} Watts"
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