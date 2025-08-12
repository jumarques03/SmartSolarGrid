from fastapi import APIRouter 
import requests
from simulacoes.status_inversor_simulado import info_inversor
import os
from dotenv import load_dotenv
from backend.funcs_auxiliares.funcs_auxiliares import ler_cargas, salvar_cargas_prioritarias

rota_site= APIRouter(prefix="/site")

@rota_site.get("/status-inversor")
async def site_saber_status_inversor():
    return info_inversor() 

@rota_site.post("/escolher_cargas_prioritarias")
async def site_escolher_cargas_prioritarias(dispositivo: str):
    cargas = ler_cargas()
    novo_id = str(len(cargas) + 1)
    cargas[novo_id] = dispositivo
    salvar_cargas_prioritarias(cargas)
    return {"mensagem": "Carga prioritária registrada com sucesso!"}

@rota_site.get("/lista-cargas-prioritarias")
async def site_lista_de_cargas_prioritarias():
    cargas = ler_cargas()
    return {"cargas prioritarias": cargas}

@rota_site.delete("/remover_carga_prioritaria")
async def site_remover_carga(carga_id: str):
    cargas = ler_cargas()
    if carga_id in cargas:
        removida = cargas.pop(carga_id)
        salvar_cargas_prioritarias(cargas)
        return {"mensagem": f"Carga '{removida}' removida com sucesso!"}
    else:
        return {"erro": "ID da carga não encontrado."}

@rota_site.get("/historico-de-consumo")
async def site_historico_de_consumo():
    pass

@rota_site.get("/dica_economia")
async def site_dica_de_economia():
    pass

@rota_site.get("/clima")
async def site_clima(local: str):
    load_dotenv()
    api_chave = os.getenv("API_KEY")

    url = f"http://api.weatherapi.com/v1/forecast.json?key={api_chave}&lang=pt&q={local}&aqi=no&alerts=no" 
    resposta = requests.get(url)
    resposta = resposta.json()

    infos_clima = {
        "dia": resposta['forecast']['forecastday'][0]['date'],
        "temperatura maxima": f"{resposta['forecast']['forecastday'][0]['day']['maxtemp_c']}°C",
        "temperatura minima": f"{resposta['forecast']['forecastday'][0]['day']['mintemp_c']}°C",
        "temperatura media": f"{resposta['forecast']['forecastday'][0]['day']['avgtemp_c']}°C",
        "preciptacao total (mm)": f"{resposta['forecast']['forecastday'][0]['day']['totalprecip_mm']}mm",
        "chance de chuva(%)": f"{resposta['forecast']['forecastday'][0]['day']['daily_chance_of_rain']}%",
        "indice UV (intensidade da radiação solar)": resposta['forecast']['forecastday'][0]['day']['uv'],
        "nascer do sol": resposta['forecast']['forecastday'][0]['astro']['sunrise'],
        "por do sol": resposta['forecast']['forecastday'][0]['astro']['sunset']
    }

    return infos_clima

