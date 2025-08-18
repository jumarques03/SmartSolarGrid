from fastapi.responses import JSONResponse
import json

caminho_arquivo = "dados/cargas_prioritarias.json"

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

def ler_cargas():
    with open(caminho_arquivo, "r", encoding="utf-8") as f:
        return json.load(f)
    
def salvar_cargas_prioritarias(lista):
    with open(caminho_arquivo, 'w', encoding="utf-8") as f:
        json.dump(lista, f, indent=4)

def reorganizar_indices(cargas):
    novas_cargas = {}
    for i, dispositivo in enumerate(cargas.values(), start=1):
        novas_cargas[i] = dispositivo
    return novas_cargas
