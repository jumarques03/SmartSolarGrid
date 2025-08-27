from fastapi import APIRouter, Request
from backend.funcs_auxiliares.funcs_auxiliares import corpo_resposta_para_Alexa, resposta_erro_padrao, ler_cargas,acesso_cargas
from simulacoes.status_inversor_simulado import info_inversor

rota_alexa = APIRouter(prefix="/alexa")

@rota_alexa.post("/")
async def alexa_entry(request: Request):
    try:
        body = await request.json()
        req_type = body.get("request", {}).get("type")

        if req_type == "LaunchRequest":
            texto = "Olá — posso informar o status do inversor, dar uma dica de economia ou listar suas cargas prioritárias. O que deseja?"
            return corpo_resposta_para_Alexa(texto, False)

        if req_type == "IntentRequest":
            intent = body["request"]["intent"]["name"]

            if intent == "StatusInversorIntent":
                infos = info_inversor()
                texto = (f"Seu painel solar está gerando {infos['FV(W)']} Watts, "
                         f"a bateria está em {infos['SOC(%)']} por cento e a rede está consumindo {infos['Carga(W)']} Watts.")
            elif intent == "DicaEconomiaIntent":
                texto = "A minha dica é: desligue cargas não essenciais durante picos de consumo."
            elif intent == "SaberCargasPrioritariasIntent":
                cargas = ler_cargas()
                texto = f"Suas cargas prioritárias são: {acesso_cargas(cargas)}"
            else:
                texto = "Desculpe, não entendi sua solicitação. Pode repetir?"
            return corpo_resposta_para_Alexa(texto, False)

        # outros tipos (SessionEndedRequest, etc.)
        return corpo_resposta_para_Alexa("Tipo de requisição não tratado.", True)

    except Exception as e:
        return resposta_erro_padrao(e)
