from fastapi import APIRouter, Request
from backend.funcs_auxiliares.funcs_auxiliares import corpo_resposta_para_Alexa, resposta_erro_padrao, ler_cargas, acesso_cargas
from simulacoes.status_inversor_simulado import info_inversor

rota_alexa= APIRouter(prefix="/alexa")

@rota_alexa.post("/")
async def alexa_handler(request: Request):
    try:
        corpo_intent = await request.json()
        intent_nome = corpo_intent["request"]["intent"]["name"]

        if intent_nome == "StatusInversorIntent":
            infos_inversor = info_inversor()
            texto_resposta = (
                f"Seu painel solar está gerando {infos_inversor['FV(W)']} Watts, "
                f"o nível da bateria é {infos_inversor['SOC(%)']} por cento "
                f"e sua rede está consumindo {infos_inversor['Carga(W)']} Watts"
            )

        elif intent_nome == "DicaEconomiaIntent":
            texto_resposta = "A minha dica é..."

        elif intent_nome == "SaberCargasPrioritariasIntent":
            cargas = ler_cargas()
            texto_resposta = f"Suas cargas prioritárias são: {acesso_cargas(cargas)}"

        else:
            texto_resposta = "Desculpe, não entendi sua solicitação! Pode repetir?"

        resposta = corpo_resposta_para_Alexa(texto_resposta, False)
        return resposta

    except Exception as e:
        return resposta_erro_padrao(e)
