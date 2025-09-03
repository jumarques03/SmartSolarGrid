from fastapi.responses import JSONResponse
import json
import random
import os
from dotenv import load_dotenv
import requests

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

def acesso_cargas(cargas):
    separador = ", "
    string_final_cargas = separador.join(cargas.values())
    return string_final_cargas

def dicas():
    dicas = [
        "Concentre o uso de aparelhos de alto consumo entre 10h e 15h.","Programe eletrodomésticos inteligentes para funcionarem no pico solar.","Use ar-condicionado e forno elétrico durante o dia.","Mantenha uma reserva mínima de energia na bateria, como 20%.","Reduza o consumo noturno quando houver previsão de chuva.","Desligue completamente os aparelhos em stand-by.","Use réguas com interruptor para desligar múltiplos eletrônicos.","Prefira iluminação LED à noite.","Evite usar aparelhos de alto consumo à noite.","Mantenha os painéis solares limpos para maior eficiência.","Monitore a produção de energia pelo app do inversor.","Fique atento a quedas inesperadas na geração.","Use a energia da bateria nos horários de tarifa mais cara.","Use aparelhos durante o dia para liberar energia para a bateria.","Configure o sistema conforme sua rotina e tarifas.","Concentre tarefas de alto consumo entre 11h e 14h.","Evite air fryer e grill à noite, prefira micro-ondas.","Diminua o brilho de TVs e monitores à noite.","Revise as configurações do sistema a cada estação.","Instale baterias em locais ventilados e protegidos do sol.","Compare sua geração com a de vizinhos para detectar problemas.","Evite deixar carregadores conectados sem uso.","Use sensores de presença para iluminação automática.","Instale tomadas inteligentes para monitorar consumo.","Configure alertas de consumo excessivo.","Controle dispositivos por voz com assistente virtual.","Escolha eletrodomésticos com selo de eficiência energética.","Crie rotinas de desligamento por horário.","Use cortinas térmicas para reduzir climatização.","Aproveite ventilação cruzada para evitar ar-condicionado.","Realize auditorias energéticas periódicas."
    ]

    n = random.randint(0, len(dicas) - 1)
    return dicas[n]

def obter_clima(cidade: str):
    try:
        load_dotenv()
        chave_api = os.getenv("API_KEY")

        url = f"https://api.hgbrasil.com/weather?key={chave_api}&city_name={cidade}" # Ex de local: Diadema,SP --> Aceita apenas cidades
        resposta = requests.get(url)
        resposta = resposta.json()


        clima = {
            "localizacao": resposta['results']['city'],
            "periodo_do_dia": resposta['results']['currently'],
            "descricao": f"{resposta['results']['forecast'][0]['description']}",
            "dia": resposta['results']['date'],
            "temperatura_maxima": f"{resposta['results']['forecast'][0]['max']}°C",
            "temperatura_minima": f"{resposta['results']['forecast'][0]['min']}°C",
            "preciptacao_total_(mm)": f"{resposta['results']['forecast'][0]['rain']}mm",
            "cobertura_de_nuvens(%)": f"{resposta['results']['forecast'][0]['cloudiness']}%",
            "chance_de_chuva(%)": f"{resposta['results']['forecast'][0]['rain_probability']}%"
        }

        return clima
    except:
        return {"mensagem":"Não foi possível acessar as informações do clima de sua cidade."}