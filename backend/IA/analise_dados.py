import pandas as pd
from dotenv import load_dotenv
import os

load_dotenv()
caminho = os.getenv("CAMINHO")
dados = pd.read_excel(caminho)

df = pd.DataFrame(dados)

# Converte a coluna 'Horário' para o formato datetime
df['Horário'] = pd.to_datetime(df['Horário'], format="%d.%m.%Y %H:%M:%S")
df = df.set_index('Horário')

# Converte a coluna 'Carga(W)' para 'Carga(kWh)', já que os dados são a cada 5 minutos (1/12 de uma hora)
df['Carga(kWh)'] = df['Carga(W)'] * (5 / 60) / 1000

# Resample e soma os valores diários
df_diario = df.resample('D').sum()

def extrair_metricas():
    metricas = {}

    # --- MÉTRICAS DIÁRIAS ---
    # O consumo médio diário em kWh é a média da soma diária
    metricas["consumo_medio_diario"] = round(df_diario["Carga(kWh)"].mean(), 2)
    metricas["geracao_solar_media_diaria"] = round((df_diario["FV(W)"] * (5 / 60) / 1000).mean(), 2)

    # --- MÉTRICAS HORÁRIAS ---
    # Calcula a soma do consumo por hora para identificar os picos
    consumo_por_hora = df.groupby(df.index.hour)["Carga(kWh)"].sum()

    # Top 3 horas de maior consumo
    top_horas = consumo_por_hora.sort_values(ascending=False).head(3)
    horas_pico = [f"{int(h)}h" for h in top_horas.index]
    valor_medio_pico = top_horas.mean()

    metricas["horarios_pico_consumo"] = horas_pico
    metricas["valor_medio_pico_kWh"] = round(valor_medio_pico, 2)

    # --- CONSUMO SEMANA VS FIM DE SEMANA ---
    df_copia = df_diario.copy()
    df_copia["dia_semana"] = df_copia.index.dayofweek
    semana = df_copia[df_copia["dia_semana"] < 5]["Carga(kWh)"].mean()
    fim_semana = df_copia[df_copia["dia_semana"] >= 5]["Carga(kWh)"].mean()

    metricas["consumo_medio_semana_kWh"] = round(semana, 2)
    metricas["consumo_medio_fim_semana_kWh"] = round(fim_semana, 2)

    return metricas

teste = extrair_metricas()

print(teste)