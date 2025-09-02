from fastapi.responses import JSONResponse
import json
import random

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
        "Concentre o uso de aparelhos de alto consumo, como máquinas de lavar, para o período de maior geração solar, entre 10:00 e 15:00.",
        "Programe seus eletrodomésticos inteligentes para funcionarem automaticamente nos horários de pico de geração solar.",
        "Use o ar-condicionado e o forno elétrico preferencialmente durante o dia para consumir a energia gratuita do sol diretamente.",
        "Configure seu inversor para priorizar o uso da bateria durante os horários de ponta, geralmente entre 18:00 e 21:00.",
        "Evite descarregar completamente a sua bateria, pois isso aumenta a vida útil do equipamento.",
        "Configure seu sistema para manter uma reserva mínima de energia na bateria, como por exemplo, 20%.",
        "Em dias com previsão de chuva, economize a energia da bateria na noite anterior para garantir uma reserva.",
        "Reduza o 'consumo fantasma' desligando da tomada os aparelhos que ficam em modo stand-by.",
        "Use réguas com interruptor para desligar múltiplos eletrônicos de uma só vez e evitar o consumo desnecessário.",
        "À noite, priorize o uso de iluminação LED, que consome menos energia da sua bateria.",
        "Evite usar aparelhos de alto consumo que não sejam essenciais durante a noite para prolongar a autonomia da bateria.",
        "Mantenha seus painéis solares sempre limpos para não reduzir a eficiência da geração de energia.",
        "Saiba que poeira e detritos podem reduzir a eficiência dos seus painéis em até 25%.",
        "Monitore regularmente a produção de energia do seu sistema através do aplicativo do inversor.",
        "Fique atento a quedas inesperadas na geração de energia, pois elas podem indicar um problema técnico.",
        "Explore os diferentes modos de operação do seu inversor, como 'Autoconsumo' ou 'Time of Use', para automatizar a economia.",
        "Utilize a energia armazenada na sua bateria para evitar a compra de energia da rede nos horários em que a tarifa é mais cara.",
        "Ao usar aparelhos de alto consumo durante o dia, você permite que o excedente de energia carregue suas baterias para o uso noturno.",
        "Desligue os eletrônicos da tomada para impedir que o consumo em stand-by drene sua bateria desnecessariamente durante a noite.",
        "Alinhe a configuração do seu inversor com seus hábitos e com as tarifas da sua concessionária para uma economia automática."
    ]

    n = random.randint(0, len(dicas) - 1)
    
    return dicas[n]
