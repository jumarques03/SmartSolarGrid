from fastapi import APIRouter 
import requests
from simulacoes.status_inversor_simulado import info_inversor
import os
from dotenv import load_dotenv
from backend.funcs_auxiliares.funcs_auxiliares import ler_cargas, salvar_cargas_prioritarias
from backend.graficos.graficos import mapa_de_calor, histograma

rota_site= APIRouter(prefix="/site")

@rota_site.get("/status-inversor")
async def site_saber_status_inversor():
    try:
        return info_inversor()
    except:
        return {"mensagem":"Não foi possível obter as informações sobre seu inversor e bateria."}

@rota_site.post("/escolher_cargas_prioritarias")
async def site_escolher_cargas_prioritarias(dispositivo: str):
    try:
        cargas = ler_cargas()
        novo_id = str(len(cargas) + 1)
        cargas[novo_id] = dispositivo
        salvar_cargas_prioritarias(cargas)
        return {"mensagem": "Carga prioritária registrada com sucesso!"}
    except:
        return {"mensagem":"Não foi possível registrar sua carga prioritária."}
        
@rota_site.get("/lista-cargas-prioritarias")
async def site_lista_de_cargas_prioritarias():
    try:
        cargas = ler_cargas()
        return {"cargas prioritarias": cargas}
    except: 
        return {"mensagem":"Não foi possível acessar sua lista de cargas prioritárias."}

@rota_site.delete("/remover_carga_prioritaria")
async def site_remover_carga(carga_id: str):
    try:
        cargas = ler_cargas()
        if carga_id in cargas:
            removida = cargas.pop(carga_id)
            salvar_cargas_prioritarias(cargas)
            return {"mensagem": f"Carga '{removida}' removida com sucesso!"}
        else:
            return {"erro": "ID da carga não encontrado."}
    except:
        return {"mensagem":"Não foi possível deletar sua carga prioritária."}

@rota_site.get("/historico-de-consumo")
async def site_historico_de_consumo():
    lista_de_mapas_e_graficos = []

    producao_de_energia =  mapa_de_calor('FV(W)', 'Mapa de Calor: Produção de Energia por Hora x Dia')
    lista_de_mapas_e_graficos.append(producao_de_energia) # Esse OK, só rever nome

    rede_eletrica = mapa_de_calor('Rede elétrica (W)', 'Mapa de Calor: Rede Elétrica por Hora x Dia')
    lista_de_mapas_e_graficos.append(rede_eletrica) # Esse OK, só rever nome

    carga_consumida = mapa_de_calor('Carga(W)','Mapa de Calor: Carga Consumida pela Residência por Hora x Dia')
    lista_de_mapas_e_graficos.append(carga_consumida)   # Rever esse, ficou estranho 
    
    nivel_bateria = histograma()    
    lista_de_mapas_e_graficos.append(nivel_bateria) # OK, só rever nome

    # ver como fazer sobre os Dados da Bateria(W)

    return lista_de_mapas_e_graficos

@rota_site.get("/dica_economia")
async def site_dica_de_economia():
    pass

@rota_site.get("/clima")
async def site_clima(local: str):
    try:
        load_dotenv()
        api_chave = os.getenv("API_KEY")

        url = f"https://api.hgbrasil.com/weather?key={api_chave}&city_name={local}" # Ex de local: Diadema,SP --> Aceita apenas cidades
        resposta = requests.get(url)
        resposta = resposta.json()


        infos_clima = {
            "localizacao": resposta['results']['city'],
            "periodo do dia": resposta['results']['currently'],
            "descricao": f"{resposta['results']['forecast'][0]['description']}",
            "dia": resposta['results']['date'],
            "temperatura maxima": f"{resposta['results']['forecast'][0]['max']}°C",
            "temperatura minima": f"{resposta['results']['forecast'][0]['min']}°C",
            "preciptacao total (mm)": f"{resposta['results']['forecast'][0]['rain']}mm",
            "cobertura de nuvens (%)": f"{resposta['results']['forecast'][0]['cloudiness']}%",
            "chance de chuva(%)": f"{resposta['results']['forecast'][0]['rain_probability']}%",
            "nascer do sol": resposta['results']['sunrise'],
            "por do sol": resposta['results']['sunset']
        }

        return infos_clima
    except:
        return {"mensagem":"Não foi possível acessar as informações do clima de sua cidade."}