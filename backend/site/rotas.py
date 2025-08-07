from fastapi import APIRouter
import requests
from dados_simulados.status_inversor_simulado import status_inversor
from dados_simulados.nivel_bateria_simulado import nivel_bateria

rota_site= APIRouter(prefix="/site")

@rota_site.get("/status-inversor")
async def site_saber_status_inversor():
   status_inversor() 

@rota_site.get("/nivel-da-bateria")
async def site_nivel_da_bateria():
    nivel_bateria()

@rota_site.get("/escolher_cargas_prioritarias")
async def site_escolher_cargas_prioritarias():
    '''
    Usuário escolhe as cargas prioritárias por meio de digitação dos nomes dos dispositivos
    '''
    pass

@rota_site.get("/lista-cargas-prioritarias")
async def site_lista_das_cargas_prioritarias():
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

