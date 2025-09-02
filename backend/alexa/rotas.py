from fastapi import APIRouter, Request

from backend.funcs_auxiliares.funcs_auxiliares import corpo_resposta_para_Alexa, resposta_erro_padrao, ler_cargas, acesso_cargas 
from simulacoes.status_inversor_simulado import info_inversor
from backend.site.rotas import chatbot 

rota_alexa = APIRouter(prefix="/alexa")

@rota_alexa.post("/")
async def alexa_webhook(request: Request):
    try:
        corpo_intent = await request.json()
        tipo_request = corpo_intent["request"]["type"]

        # 1) LaunchRequest (quando abre a skill)
        if tipo_request == "LaunchRequest":
            texto_resposta = (
                "Bem-vindo ao SmartSolarGrid! "
                "Você pode pedir o status de seus aparelhos de energia, "
                "uma dica sobre energia e consumo ou saber suas cargas prioritárias."
            )

        # 2) IntentRequest (quando o usuário pede algo)
        elif tipo_request == "IntentRequest":
            intent_nome = corpo_intent["request"]["intent"]["name"]

            if intent_nome == "StatusAparelhosDeEnergiaIntent":
                infos_inversor = info_inversor()
                texto_resposta = (
                    f"Seu painel solar está gerando {infos_inversor['FV(W)']} Watts, "
                    f"o nível de sua bateria é {infos_inversor['SOC(%)']} por cento "
                    f"e sua rede está consumindo no total {infos_inversor['Carga(W)']} Watts."
                )

            elif intent_nome == "DicaIntent":
                texto_resposta = "Minha dica de economia é: use os eletrodomésticos pesados durante o dia, aproveitando a geração solar."

            elif intent_nome == "SaberCargasPrioritariasIntent":
                cargas = ler_cargas()
                texto_resposta = f"Suas cargas prioritárias são: {acesso_cargas(cargas)}"

            else:
                texto_resposta = "Desculpe, não entendi sua solicitação! Você pode repetir, por favor?"

        # 3) SessionEndedRequest (quando a Alexa encerra a sessão)
        elif tipo_request == "SessionEndedRequest":
            texto_resposta = "Até logo! Obrigado por usar o SmartSolarGrid."

        else:
            texto_resposta = "Desculpe, ocorreu um problema ao processar sua solicitação."

        resposta = corpo_resposta_para_Alexa(texto_resposta, False)
        return resposta

    except Exception as e:
        return resposta_erro_padrao(e)
