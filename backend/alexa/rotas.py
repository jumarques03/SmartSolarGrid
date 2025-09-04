from fastapi import APIRouter, Request
from backend.funcs_auxiliares.funcs_auxiliares import corpo_resposta_para_Alexa, resposta_erro_padrao, ler_cargas, acesso_cargas, dicas, obter_clima
from simulacoes.status_inversor_simulado import info_inversor
from backend.IA.llm import assistente_llm_alexa
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
                "saber o clima de sua cidade, "
                "a dica do dia sobre energia e saber suas cargas prioritárias."
            )

        # 2) IntentRequest (quando o usuário pede algo)
        elif tipo_request == "IntentRequest":
            intent_nome = corpo_intent["request"]["intent"]["name"]
            
            # Pega a pergunta do usuário para passar para a IA
            if 'slots' in corpo_intent['request']['intent'] and 'pergunta' in corpo_intent['request']['intent']['slots']:
                pergunta_usuario = corpo_intent['request']['intent']['slots']['pergunta']['value']
            else:
                pergunta_usuario = "Me dê uma dica de energia." # Pergunta padrão se o slot não for preenchido

            if intent_nome == "StatusAparelhosDeEnergiaIntent":
                infos_inversor = info_inversor()
                texto_resposta = (
                    f"Seu painel solar está gerando {infos_inversor['FV(W)']} Watts, "
                    f"o nível de sua bateria é {infos_inversor['SOC(%)']} por cento "
                    f"e sua rede está consumindo no total {infos_inversor['Carga(W)']} Watts."
                )

            elif intent_nome == "DicaIntent":
                # Chama a nova função com a pergunta do usuário
                resposta_assistente = assistente_llm_alexa(pergunta_usuario)
                texto_resposta = f"Sua dica é: {resposta_assistente['resposta']}"

            elif intent_nome == "SaberCargasPrioritariasIntent":
                cargas = ler_cargas()
                texto_resposta = f"Suas cargas prioritárias são: {acesso_cargas(cargas)}"
            
            elif intent_nome == "ClimaIntent":
                try:
                    cidade = corpo_intent["request"]["intent"]["slots"]["cidade"]["value"]
                    clima = obter_clima(cidade)
                    
                    texto_resposta = (
                        f"Em {clima['localizacao']},"
                        f"A descrição do clima é de {clima['descricao']}. "
                        f"A temperatura máxima será de {clima['temperatura_maxima']} "
                        f"e a mínima de {clima['temperatura_minima']}. "
                        f"A chance de chuva é de {clima['chance_de_chuva(%)']}"
                        f" e as nuvens cobrirão {clima['cobertura_de_nuvens(%)']} do céu."
                    )

                except KeyError:
                    texto_resposta = "Por favor, me diga o nome da cidade que deseja consultar."

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