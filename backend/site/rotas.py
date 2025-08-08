from fastapi import APIRouter
import requests
from simulacoes.status_inversor_simulado import status_inversor
from models.cargas import CargasPrioritarias

rota_site= APIRouter(prefix="/site")

@rota_site.get("/status-inversor")
async def site_saber_status_inversor():
    return status_inversor() 

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
async def site_clima():
    '''
    Clima da região onde o usuário está, chatbot usará isso para falar sugestões dicas...
    '''
    
    url = "https://api.open-meteo.com/v1/forecast?latitude=52.52&longitude=13.41&hourly=temperature_2m,relative_humidity_2m,cloud_cover,precipitation_probability,precipitation,rain,direct_radiation_instant"
    pass

