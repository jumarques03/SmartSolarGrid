import pandas as pd
import random
import openpyxl

def status_inversor():
    dados= pd.read_excel(r"dados\dados_gerais_inversor (1).xlsx")

    dicionario_dados = dados.to_dict(orient="records")
    n = random.randint(0, len(dicionario_dados) - 1)
    
    return dicionario_dados[n]
