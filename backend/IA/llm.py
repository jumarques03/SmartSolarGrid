from huggingface_hub import InferenceClient
import os
from dotenv import load_dotenv

# inicializa cliente com seu token
load_dotenv()
HF_TOKEN = os.getenv("HF_TOKEN")

client = InferenceClient(token=HF_TOKEN)

def gerar_dica(clima: dict, info: dict ):
    prompt = f"""
    Você é um assistente de energia inteligente.
    Aqui estão as condições climáticas atuais:
    {clima}

    Aqui estão as informações sobre os aparelhos atuais:
    {info}

    Com base nisso, caso o usuário peça uma dica com base no clima, dê uma dica curta, simples e útil sobre como economizar energia otimizar o uso de aparelhos em casa. Caso o usuário peça uma dica no geral, utilize as informações dos aparelhos e do clima para dar essa dica. Responda em português, em uma frase só."""

    resposta = client.text_generation(
        model="mistralai/Mistral-7B-Instruct-v0.2",  # modelo recomendado
        inputs=prompt,
        parameters={
            "max_new_tokens": 80,
            "temperature": 0.7
        }
    )
    return str(resposta)
