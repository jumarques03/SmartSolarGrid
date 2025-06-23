from fastapi import FastAPI, Request
from alexa.rotas import rota_alexa


app=FastAPI()
app.include_router(rota_alexa)


