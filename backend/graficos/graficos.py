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
    # Suponha que df já está definido e contém os dados.
    # df = pd.DataFrame(...)
    y = df["Dados da Bateria(W)"]
    x = df.index

    plt.figure(figsize=(12, 6))

    # Definir as cores com base nos valores de Y
    colors = ['green' if val >= 0 else 'red' for val in y]

    # Plotar a linha contínua, segmentando por cor
    for i in range(len(x) - 1):
        color = 'green' if y[i] >= 0 and y[i+1] >= 0 else 'red'
        # Adiciona a condição para valores que atravessam o eixo 0
        if (y[i] >= 0 and y[i+1] < 0) or (y[i] < 0 and y[i+1] >= 0):
            # Encontrar o ponto de intersecção com o eixo X
            x_intercept = x[i] - y[i] * (x[i+1] - x[i]) / (y[i+1] - y[i])
            
            # Plotar o segmento até o eixo
            plt.plot([x[i], x_intercept], [y[i], 0], color='green' if y[i] >= 0 else 'red', marker='o' if i == 0 else None)
            
            # Plotar o segmento a partir do eixo
            plt.plot([x_intercept, x[i+1]], [0, y[i+1]], color='green' if y[i+1] >= 0 else 'red', marker='o' if i+1 == len(x)-1 else None)
        else:
            plt.plot([x[i], x[i+1]], [y[i], y[i+1]], color=color, marker='o' if i == 0 or i == len(x)-2 else None)
    
    # Criar um ponto para cada dado, garantindo que todos os marcadores 'o' apareçam
    plt.plot(x, y, color='none', marker='o', markeredgecolor='black', markersize=6)
    
    # Adicionando legendas manualmente, sem precisar de um plot completo para isso
    plt.plot([], [], color="green", marker="o", linestyle="-", label="Bateria Carregando")
    plt.plot([], [], color="red", marker="o", linestyle="-", label="Bateria Descarregando")

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
