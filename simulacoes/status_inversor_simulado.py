import pandas as pd
import random
import openpyxl
from pathlib import Path

def info_inversor():
    caminho_base = Path(__file__).resolve().parent.parent
    caminho_arquivo = caminho_base / "dados" / "dados_finais_inversor.xlsx"
    dados= pd.read_excel(caminho_arquivo)

    dicionario_dados = dados.to_dict(orient="records")
    n = random.randint(0, len(dicionario_dados) - 1)
    
    return dicionario_dados[n]
