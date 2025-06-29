from fastapi import FastAPI
from backend.alexa.rotas import rota_alexa
from backend.site.rotas import rota_site
 
app=FastAPI()
app.include_router(rota_alexa)
app.include_router(rota_site)


