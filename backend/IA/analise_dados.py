import pandas as pd
from dotenv import load_dotenv
import os

load_dotenv()
caminho = os.getenv("CAMINHO")
dados= pd.read_excel(caminho)

df = pd.DataFrame(dados)

df['Horário'] = pd.to_datetime(df['Horário'], format="%d.%m.%Y %H:%M:%S")

df = df.set_index('Horário')
df2 = df.copy()

df = df.resample('D').mean()
df2 = df.resample('h').sum()

def extrair_metricas():
    metricas = {}

    # --- MÉTRICAS DIÁRIAS ---
    metricas["consumo_medio"] = round(df["Carga(W)"].mean(), 2)
    metricas["soc_medio"] = round(df["SOC(%)"].mean(), 2)
    metricas["geracao_solar_media"] = round(df["FV(W)"].mean(), 2)

    # --- MÉTRICAS HORÁRIAS ---
    consumo_por_hora = df2.groupby(df2.index.hour)["Carga(W)"].mean()

    # Top 3 horas de maior consumo
    top_horas = consumo_por_hora.sort_values(ascending=False).head(3)
    horas_pico = [f"{int(h)}h" for h in top_horas.index]
    valor_medio_pico = top_horas.mean()

    metricas["horarios_pico_consumo"] = horas_pico
    metricas["valor_medio_pico"] = round(valor_medio_pico, 2)

    # --- CONSUMO SEMANA VS FIM DE SEMANA ---
    df_copia = df.copy()
    df_copia["dia_semana"] = df_copia.index.dayofweek
    semana = df_copia[df_copia["dia_semana"] < 5]["Carga(W)"].mean()
    fim_semana = df_copia[df_copia["dia_semana"] >= 5]["Carga(W)"].mean()

    metricas["consumo_medio_semana"] = round(semana, 2)
    metricas["consumo_medio_fim_semana"] = round(fim_semana, 2)

    return metricas



