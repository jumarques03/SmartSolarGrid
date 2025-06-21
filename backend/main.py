from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

app=FastAPI()

@app.post("status-inversor")
async def saber_status_inversor(request: Request):
    corpo_intent= await request.json()  # Espera receber o corpo do intent
    intent=corpo_intent["request"]["intent"]["name"]    # Acessando o nome do intent requerido pelo usuário

    if intent== "StatusInversor":
        texto_resposta = "Status Inversor...."    # Aqui ocorreria uma requisição para a API da Goodwe referente ao status do inversor
    else:
        texto_resposta= "Desculpe, não entendi sua solicitação! Poderia repetir por favor?"

    # Resposta no formato que a Alexa espera receber
    resposta = {
        "version": "1.0",
        "response": {
            "outputSpeech": {
                "type": "PlainText",
                "text": texto_resposta
            },
            "shouldEndSession": False
        }
    }

    return JSONResponse(content=resposta)   # Retorna uma resposta HTTP no formato JSON