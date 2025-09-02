from langchain_community.document_loaders import PyPDFLoader
import getpass
import os
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain import hub
from langchain_core.documents import Document
from typing_extensions import List, TypedDict
from langgraph.graph import START, StateGraph

file_path = r"dados\CONTEXTO.pdf"
pdf_loader = PyPDFLoader(file_path)

load_dotenv()
chave_api = os.getenv("GOOGLE_API_KEY")
llm = init_chat_model("gemini-1.5-flash", model_provider="google_genai")


# Define o modelo que será usado. Ele será baixado automaticamente na primeira vez.
model_name = "sentence-transformers/all-MiniLM-L6-v2"
model_kwargs = {'device': 'cpu'} # Use 'cuda' se tiver uma GPU configurada
encode_kwargs = {'normalize_embeddings': False}

# Inicializa o embedding do Hugging Face
embeddings = HuggingFaceEmbeddings(
    model_name=model_name,
    model_kwargs=model_kwargs,
    encode_kwargs=encode_kwargs
)

vector_store = InMemoryVectorStore(embeddings)

# Fazendo o splitting dos documentos

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=300,
    chunk_overlap=30,
    add_start_index=True,
)

splits_pdf = text_splitter.split_documents(pdf_loader.load())
all_splits = splits_pdf

document_ids = vector_store.add_documents(documents=all_splits)

prompt = hub.pull("rlm/rag-prompt")

prompt.messages[0].prompt.template = """
1. Persona e Missão:
Você é o Assistente de Energia Inteligente. Sua missão: ajudar usuários com sistema solar e baterias a maximizar a autossuficiência e a economia.

2. Base de Conhecimento (Pilares):

Autoconsumo Máximo: Usar a própria energia solar primeiro.

Bateria Estratégica: Evitar a rede em horários de pico.

Deslocamento de Carga: Usar aparelhos de alto consumo com o sol forte (10h-15h).

Eficiência Energética: Reduzir o consumo desnecessário.

Saúde do Sistema: Manter o equipamento para gerar o máximo.

3. Lógica de Execução (Regra Crítica):
Analise a {question} do usuário e siga estritamente:

Se a intenção for INFORMATIVA ("o que é?", "como funciona?"):

Responda de forma objetiva e sem dicas.

Termine perguntando se o usuário deseja receber dicas.

Se a intenção for de AÇÃO ("como economizar?", "dê dicas"):

Forneça dicas práticas, personalizadas com o {context}.

4. Uso do Contexto e da Pergunta

* **Pergunta do Usuário:** {question}

* **Informações do Sistema (Contexto):** {context}

Use obrigatoriamente o formato abaixo.

5. Formato Obrigatório para Dicas:
**[Título Impactante da Dica]:** [Explicação simples conectando a ação ao benefício.]

Importante: Nunca revele ao usuário qual intenção você identificou."""

class State(TypedDict):
    question: str
    context: List[Document]
    answer: str

def retrieve(state: State):
    retrieved_docs = vector_store.similarity_search(state["question"])
    return {"context": retrieved_docs}

def generate(state: State):
    docs_content = "\n\n".join(doc.page_content for doc in state["context"])
    messages = prompt.invoke({"question": state["question"], "context": docs_content})
    response = llm.invoke(messages)
    return {"answer": response.content}

graph_builder = StateGraph(State).add_sequence([retrieve, generate])
graph_builder.add_edge(START, "retrieve")
graph = graph_builder.compile()

