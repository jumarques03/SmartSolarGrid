import google.generativeai as genai
import os
from dotenv import load_dotenv
from backend.IA.analise_dados import extrair_metricas

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Configura a API do Google com sua chave
genai.configure(api_key=GOOGLE_API_KEY)

def assistente_llm_site(info: dict, pergunta: str):
    metricas = extrair_metricas()

    system_prompt = f"""

    metricas = {metricas}

    Você é um assistente de energia inteligente, sua função é servir de apoio para o usuário e ajudá-lo com explicações, dicas ou recomendações sobre consumo inteligente, uso de inversores hibridos da empresa GoodWe, baterias de armazenamento de energia da empresa GoodWe e paineis solares. O usuário é um utilizador recorrente dessas tecnologias. 

    Não faça suposições, utilize apenas fatos e as metricas fornecidas a você. O consumo e geração solar estão em kWh, o soc médio é medido em %, os horários de pico são em horas. 

    Responda sempre em português, com no máximo 3 fraes e bem explicativa, sem usar markdown ou formatação especial. 
    Caso você não saiba a resposta, responda: Desculpe, não possuo essa informação disponível! Posso te ajudar em outro assunto?
    """

    # Configurações de geração de resposta
    generation_config = {
        "temperature": 0.7,
        "max_output_tokens": 200, # Equivalente ao 'max_new_tokens' ou 'max_tokens'
    }
    
    # Inicializa o modelo com a instrução de sistema
    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash-latest",
        system_instruction=system_prompt,
        generation_config=generation_config
    )

    try:
        resposta = model.generate_content(pergunta)

        return {
            "pergunta": pergunta,
            "resposta": resposta.text.strip()
        }
    
    except Exception as e:
        return {
            "pergunta": pergunta,
            "resposta": "Desculpe, não consegui processar sua pergunta com o assistente Gemini no momento. Tente novamente mais tarde."
        }
    
def assistente_llm_alexa(pergunta_usuario):
    """
    Processa a pergunta do usuário e gera uma resposta dinâmica e contextualizada
    com base nas métricas de energia.
    """
    metricas = extrair_metricas()
    if "erro" in metricas:
        return {"pergunta": pergunta_usuario, "resposta": "Desculpe, não foi possível carregar os dados de energia. Tente novamente mais tarde."}
    
    # Prepara o prompt para o modelo, instruindo-o a gerar a resposta
    system_prompt = f"""
    Métricas de energia do usuário: {metricas}

    Você é um assistente de energia inteligente para usuários de sistemas solares da GoodWe. Sua função é dar dicas de otimização de consumo e economia.
    
    Analise as métricas de energia (picos de consumo, uso da bateria, consumo da rede, etc.) para criar uma dica prática e personalizada que ajude o usuário a economizar ou a usar melhor a energia.
    
    Responda em uma única frase curta e bem explicativa, em português, sem usar markdown ou formatação especial.
    """

    generation_config = {
        "temperature": 0.7,
        "max_output_tokens": 50, # Mantido curto para frases concisas
    }
    
    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash-latest",
        system_instruction=system_prompt,
        generation_config=generation_config
    )

    try:
        resposta = model.generate_content(f"A minha pergunta é: {pergunta_usuario}")
        return {
            "resposta": resposta.text.strip()
        }
    
    except Exception as e:
        return {
            "resposta": "Desculpe, não consegui processar sua pergunta. Tente novamente mais tarde."
        }
