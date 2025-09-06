import google.generativeai as genai
import os
from dotenv import load_dotenv
from backend.IA.analise_dados import extrair_metricas
from backend.funcs_auxiliares.funcs_auxiliares import obter_clima
# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Configura a API do Google com sua chave
genai.configure(api_key=GOOGLE_API_KEY)

def assistente_llm_site(info: dict, pergunta: str):
    metricas = extrair_metricas()

    system_prompt = f"""

    metricas = {metricas}
    informações dos aparelhos = {info}

    Você é um assistente de energia inteligente, sua função é servir de apoio para o usuário e ajudá-lo com explicações, dicas ou recomendações sobre consumo inteligente, uso de inversores hibridos da empresa GoodWe, baterias de armazenamento de energia da empresa GoodWe e paineis solares. O usuário é um utilizador recorrente dessas tecnologias. 

    Não faça suposições, utilize apenas as informações dos aparelhos e as metricas fornecidas a você. O consumo e geração solar estão em kWh, o soc médio é medido em %, os horários de pico são em horas. 

    Responda sempre em português,de forma bem coesa e coerente, sem usar markdown ou formatação especial. 
    Caso você não saiba a resposta, responda: Desculpe, não possuo essa informação disponível! Posso te ajudar em outro assunto?
    """


    generation_config = {
        "temperature": 0.7,
        "max_output_tokens": 300, 
    }
    
    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash-latest",
        system_instruction=system_prompt,
        generation_config=generation_config
    )


    resposta = model.generate_content(pergunta)

    return {
        "pergunta": pergunta,
        "resposta": resposta.text.strip()
    }
    