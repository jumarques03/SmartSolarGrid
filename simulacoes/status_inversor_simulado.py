import pandas as pd
import random
import openpyxl

def info_inversor():
    dados= pd.read_excel("dados/dados_finais_inversor.xlsx")

    dicionario_dados = dados.to_dict(orient="records")
    n = random.randint(0, len(dicionario_dados) - 1)
    
    return dicionario_dados[n]
