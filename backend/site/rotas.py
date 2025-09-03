from fastapi import APIRouter 
from simulacoes.status_inversor_simulado import info_inversor
from backend.funcs_auxiliares.funcs_auxiliares import ler_cargas, salvar_cargas_prioritarias, reorganizar_indices, obter_clima
from backend.graficos.graficos import serie_temporal, histograma
from fastapi import APIRouter, HTTPException
# from pydantic import BaseModel
# from backend.chatbot.logica_chatbot import graph 

rota_site= APIRouter(prefix="/site")

@rota_site.get("/status-inversor")
async def obter_status_inversor():
    try:
        return info_inversor()
    except:
        return {"mensagem":"Não foi possível obter as informações sobre seu inversor e bateria."}

@rota_site.post("/escolher_cargas_prioritarias")
async def escolher_carga_prioritaria(dispositivo: str):
    try:
        cargas = ler_cargas()
        novo_id = str(len(cargas) + 1)
        cargas[novo_id] = dispositivo
        salvar_cargas_prioritarias(cargas)
        return {"mensagem": "Carga prioritária registrada com sucesso!"}
    except:
        return {"mensagem":"Não foi possível registrar sua carga prioritária."}
        
@rota_site.get("/lista-cargas-prioritarias")
async def listar_cargas_prioritarias():
    try:
        cargas = ler_cargas()
        return {"cargas_prioritarias": cargas}
    except: 
        return {"mensagem":"Não foi possível acessar sua lista de cargas prioritárias."}

@rota_site.delete("/remover_carga_prioritaria")
async def remover_carga_prioritaria(carga_id: str):
    try:
        cargas = ler_cargas()
        if carga_id in cargas:
            carga_removida = cargas.pop(carga_id)
            cargas = reorganizar_indices(cargas)
            salvar_cargas_prioritarias(cargas)
            return {"mensagem": f"Carga '{carga_removida}' removida com sucesso!"}
        else:
            return {"erro": "ID da carga não encontrado."}
    except:
        return {"mensagem":"Não foi possível deletar sua carga prioritária."}

@rota_site.get("/historico_de_consumo")
async def obter_historico_de_consumo():
    try: 
        graficos = []

        geracao_solar_grafico =  serie_temporal('FV(W)', 'g', 'Geração Solar(W) por Dia no Mês de Agosto', 'Dia', 'Watts')
        graficos.append(geracao_solar_grafico) 

        energia_consumida_concessionaria_grafico = serie_temporal('Rede elétrica (W)', 'r', 'Energia Comprada da Concessionária(W) por Dia no Mês de Agosto', 'Dia', 'Watts')
        graficos.append(energia_consumida_concessionaria_grafico) 

        carga_consumida_grafico = serie_temporal('Carga(W)','b','Consumo da Residência(W) por Dia no Mês de Agosto', 'Dia', 'Watts')
        graficos.append(carga_consumida_grafico)

        dados_bateria_grafico=serie_temporal('Dados da Bateria(W)','orange', 'Uso da Bateria(W) por Dia no Mês de Agosto', 'Dia', 'Watts')
        graficos.append(dados_bateria_grafico) #LEGENDA????
        
        nivel_bateria_grafico = histograma('SOC(%)', 10, 'Nível de Bateria(%) no Mês de Agosto ', 'Porcentagem da Bateria', 'Frequência', None)
        graficos.append(nivel_bateria_grafico)

        return graficos
    except:
        return {"mensagem":"Não foi possível carregar o histório de consumo."}
        

# class Pergunta(BaseModel):
#     question: str

# @rota_site.post("/assistente")
# async def chatbot(pergunta: Pergunta):
#     estado_final = graph.invoke({"question": pergunta.question})
#     return {
#         "pergunta": pergunta.question,
#         "resposta": estado_final["answer"]
#     }

@rota_site.get("/clima")
async def clima(local: str):
    clima = obter_clima(local)

    return clima