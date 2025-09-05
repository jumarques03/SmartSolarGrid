import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from dotenv import load_dotenv
import os
import io
from fastapi.responses import StreamingResponse

load_dotenv()
caminho = os.getenv("CAMINHO")
dados= pd.read_excel(caminho)

df = pd.DataFrame(dados)
df['Horário'] = pd.to_datetime(df['Horário'], format="%d.%m.%Y %H:%M:%S")
df = df.set_index('Horário')
df2 = df.copy()
df = df.resample('D').sum()

def serie_temporal(valor: str, cor: str, titulo: str, x: str, y: str):
    plt.plot(df.index, df[valor], marker='o', linestyle='-', markersize=4, color=cor)
    plt.title(titulo)
    plt.xlabel(x)
    plt.ylabel(y)
    plt.grid(True) 
    plt.xticks(rotation=45)
    plt.tight_layout() 

    fig = plt.gcf()
    buf = io.BytesIO()
    fig.savefig(buf, format="png")
    buf.seek(0)
    plt.close(fig)

    return StreamingResponse(buf, media_type="image/png")


def histograma(valor: str, intervalo:int, titulo: str, x: str, y: str):
    plt.hist(df2[valor], bins=intervalo, alpha=0.7, color='lightcoral', edgecolor='black')
    plt.title(titulo)
    plt.xlabel(x)
    plt.ylabel(y)
    plt.tight_layout() 

    fig = plt.gcf()
    buf = io.BytesIO()
    fig.savefig(buf, format="png")
    buf.seek(0)
    plt.close(fig)

    return StreamingResponse(buf, media_type="image/png")

def grafico_bateria():
    y = df["Dados da Bateria(W)"]
    x = df.index

    plt.figure(figsize=(12, 6))

    # 🔹 valores positivos (carregando)
    plt.plot(x[y >= 0], y[y >= 0],
             color="green", marker="o", linestyle="-", label="Bateria Carregando")

    # 🔹 valores negativos (descarregando)
    plt.plot(x[y < 0], y[y < 0],
             color="red", marker="o", linestyle="-", label="Bateria Descarregando")

    plt.title("Uso da Bateria(W) por Dia no Mês de Agosto")
    plt.xlabel("Dia")
    plt.ylabel("Watts")
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.legend()
    plt.tight_layout()

    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    plt.close()
    buf.seek(0)

    return StreamingResponse(buf, media_type="image/png")
