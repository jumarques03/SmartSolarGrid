from fastapi import APIRouter, Request
from backend.funcs_auxiliares.funcs_auxiliares import corpo_resposta_para_Alexa, resposta_erro_padrao, ler_cargas, acesso_cargas
from simulacoes.status_inversor_simulado import info_inversor

rota_alexa= APIRouter(prefix="/alexa")

@rota_alexa.post("/info-inversor")
async def obter_status_inversor_alexa(request: Request):
    try: 
        corpo_intent= await request.json()  
        intent_nome=corpo_intent["request"]["intent"]["name"]    

        if intent_nome== "StatusInversorIntent":
            infos_inversor = info_inversor()
            
            texto_resposta = f"Seu painel solar está gerando {infos_inversor['FV(W)']} Watts, o nível de sua bateria é {infos_inversor['SOC(%)']} por cento e sua rede está consumindo no total {infos_inversor['Carga(W)']} Watts"
        else:
            texto_resposta= "Desculpe, não entendi sua solicitação! Poderia repetir por favor?"

        resposta=corpo_resposta_para_Alexa(texto_resposta, False)
        return resposta
        
    except Exception as e:
        return resposta_erro_padrao(e)

@rota_alexa.post("/dica-economia")
async def obter_dica_economia_alexa(request: Request):
    try: 
        corpo_intent= await request.json()  
        intent_nome=corpo_intent["request"]["intent"]["name"]    

        if intent_nome== "DicaEconomiaIntent":
            texto_resposta= "A minha dica é..."  
        else:
            texto_resposta="Desculpe, não entendi sua solicitação! Poderia repetir por favor?"

        resposta=corpo_resposta_para_Alexa(texto_resposta, False)
        return resposta
    
    except Exception as e:
        return resposta_erro_padrao(e)
    

@rota_alexa.post("/cargas-prioritarias")
async def obter_cargas_prioritarias_alexa(request: Request):
    try: 
        corpo_intent= await request.json()  
        intent_nome=corpo_intent["request"]["intent"]["name"]    

        if intent_nome== "SaberCargasPrioritariasIntent":
            cargas = ler_cargas()
            texto_resposta= f"Suas cargas prioritárias são: {acesso_cargas(cargas)}"
        else:
            texto_resposta="Desculpe, não entendi sua solicitação! Poderia repetir por favor?"

        resposta=corpo_resposta_para_Alexa(texto_resposta, False)
        return resposta
    
    except Exception as e:
        return resposta_erro_padrao(e)
