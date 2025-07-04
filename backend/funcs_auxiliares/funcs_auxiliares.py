from fastapi.responses import JSONResponse

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
    
    return JSONResponse(content=resposta)   # Retorna uma resposta HTTP no formato JSON

def resposta_erro_padrao(e):
    print(e)
    return corpo_resposta_para_Alexa("Desculpe, houve um problema ao processar sua solicitação.", True)