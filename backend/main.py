from fastapi import FastAPI
from backend.alexa.rotas import rota_alexa

app=FastAPI()
app.include_router(rota_alexa)


