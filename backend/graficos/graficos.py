import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from dotenv import load_dotenv
import os

load_dotenv()
caminho = os.getenv("CAMINHO")
dados= pd.read_excel(caminho)

df = pd.DataFrame(dados)
df['Horário'] = pd.to_datetime(df['Horário'], format="%d.%m.%Y %H:%M:%S")
df = df.set_index('Horário')
df2 = df.copy()
df = df.resample('D').sum()

def serie_temporal(valor: str, cor: str, titulo: str, x: str, y: str):
    plt.figure(figsize=(10, 8))
    plt.plot(df.index, df[valor], marker='o', linestyle='-', markersize=4, color=cor)
    plt.title(titulo)
    plt.xlabel(x)
    plt.ylabel(y)
    plt.grid(True) 
    plt.xticks(rotation=45)
    plt.tight_layout() 
    plt.show()

def histograma(valor: str, intervalo:int, titulo: str, x: str, y: str, legenda: str):
    plt.hist(df2[valor], bins=intervalo, alpha=0.7, color='lightcoral', edgecolor='black')
    plt.title(titulo)
    plt.xlabel(x)
    plt.ylabel(y)
    plt.tight_layout() 
    plt.show()
