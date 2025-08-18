import pandas as pd
import random
import openpyxl
from dotenv import load_dotenv
import os

def info_inversor():
    load_dotenv()
    caminho = os.getenv("CAMINHO")
    dados= pd.read_excel(caminho)

    dicionario_dados = dados.to_dict(orient="records")
    n = random.randint(0, len(dicionario_dados) - 1)
    
    return dicionario_dados[n]
