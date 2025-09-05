import pandas as pd
import random
from dotenv import load_dotenv
import os

def infos():
    load_dotenv()
    caminho = os.getenv("CAMINHO")
    dados= pd.read_excel(caminho)

    dicionario_dados = dados.to_dict(orient="records")
    n = random.randint(0, len(dicionario_dados) - 1)
    
    return dicionario_dados[n]
