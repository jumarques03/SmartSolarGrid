# from langchain_community.document_loaders import PyPDFLoader
# import getpass
# import os
# from dotenv import load_dotenv
# from langchain.chat_models import init_chat_model
# from langchain_core.vectorstores import InMemoryVectorStore
# from langchain_community.embeddings import HuggingFaceEmbeddings
# from langchain_text_splitters import RecursiveCharacterTextSplitter
# from langchain import hub
# from langchain_core.documents import Document
# from typing_extensions import List, TypedDict
# from langgraph.graph import START, StateGraph

# load_dotenv()
# contexto = os.getenv("CONTEXTO")
# file_path = f"{contexto}"   #ARRUMAR FILE PATH
# pdf_loader = PyPDFLoader(file_path)

# load_dotenv()
# chave_api = os.getenv("GOOGLE_API_KEY")
# llm = init_chat_model("gemini-1.5-flash", model_provider="google_genai")


# # Define o modelo que será usado. Ele será baixado automaticamente na primeira vez.
# model_name = "sentence-transformers/all-MiniLM-L6-v2"
# model_kwargs = {'device': 'cpu'} # Use 'cuda' se tiver uma GPU configurada
# encode_kwargs = {'normalize_embeddings': False}

# # Inicializa o embedding do Hugging Face
# embeddings = HuggingFaceEmbeddings(
#     model_name=model_name,
#     model_kwargs=model_kwargs,
#     encode_kwargs=encode_kwargs
# )

# vector_store = InMemoryVectorStore(embeddings)

# # Fazendo o splitting dos documentos

# text_splitter = RecursiveCharacterTextSplitter(
#     chunk_size=300,
#     chunk_overlap=30,
#     add_start_index=True,
# )

# splits_pdf = text_splitter.split_documents(pdf_loader.load())
# all_splits = splits_pdf

# document_ids = vector_store.add_documents(documents=all_splits)

# prompt = hub.pull("rlm/rag-prompt")

# prompt.messages[0].prompt.template = """
# Você é o Assistente de Energia Inteligente. Sua missão é ajudar usuários com sistemas solares e baterias a maximizar a autossuficiência e a economia.

# Base de Conhecimento:
# - Autoconsumo: usar a energia solar no momento da geração.
# - Bateria Estratégica: evitar uso da rede em horários de pico.
# - Deslocamento de Carga: usar aparelhos de alto consumo entre 10h e 15h.
# - Eficiência Energética: reduzir consumo desnecessário.
# - Saúde do Sistema: manter equipamentos em bom estado.

# Instruções:
# - Analise a pergunta do usuário: {question}
# - Use o contexto abaixo para responder: {context}

# Regras:
# - Se a pergunta for informativa (ex: “o que é”, “como funciona”), responda de forma objetiva e clara.
# - Se a pergunta pedir ação ou dicas (ex: “como economizar”, “dê dicas”), forneça **no máximo 3 dicas práticas**, com explicações breves e diretas.

# Formato de Resposta:
# Pergunta: {question}

# Resposta:
# - [Dica 1]: [Explicação curta]
# - [Dica 2]: [Explicação curta]
# - [Dica 3]: [Explicação curta]

# Nunca revele que identificou a intenção. Seja direto e útil.
# """


# class State(TypedDict):
#     question: str
#     context: List[Document]
#     answer: str

# def retrieve(state: State):
#     retrieved_docs = vector_store.similarity_search(state["question"], k=3)
#     return {"context": retrieved_docs}

# def generate(state: State):
#     docs_content = "\n\n".join(doc.page_content for doc in state["context"])
#     messages = prompt.invoke({"question": state["question"], "context": docs_content})
#     response = llm.invoke(messages)

#     # Limpeza da resposta
#     resposta_bruta = response.content
#     resposta_limpa = (
#         resposta_bruta
#         .replace("Pergunta:", "")
#         .replace(state["question"], "")
#         .replace("Resposta:", "")
#         .strip()
#     )

#     return {"answer": resposta_limpa}

# graph_builder = StateGraph(State).add_sequence([retrieve, generate])
# graph_builder.add_edge(START, "retrieve")
# graph = graph_builder.compile()

