from fastapi import APIRouter 
import requests
from simulacoes.status_inversor_simulado import info_inversor
from models.cargas import CargasPrioritarias
import os
from dotenv import load_dotenv

rota_site= APIRouter(prefix="/site")

@rota_site.get("/status-inversor")
async def site_saber_status_inversor():
    return info_inversor() 

@rota_site.post("/escolher_cargas_prioritarias")
async def site_escolher_cargas_prioritarias(dispositivo: CargasPrioritarias):

    dispositivos_prioritarios = dispositivo.nome
    return {"mensagem": "Cargas prioritárias registradas com sucesso!", "cargas": dispositivos_prioritarios}

@rota_site.get("/lista-cargas-prioritarias")
async def site_lista_de_cargas_prioritarias():
    pass

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

    url = f"http://api.weatherapi.com/v1/current.json?key={api_chave}&lang=pt&q={local}&aqi=no" 
    resposta = requests.get(url)
    resposta = resposta.json()

    infos_clima = {
        "ultima atualizacao": f"{resposta['current']['last_updated']}",
        "temperatura": f"{resposta['current']['temp_c']}°C",
        "é dia?": f"{resposta['current']['is_day']}",
        "cobertura nuvens (%)": f"{resposta['current']['cloud']}%",
        "preciptacao (mm)": f"{resposta['current']['precip_mm']}mm"
        }

    return infos_clima

