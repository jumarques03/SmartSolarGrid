import pandas as pd
from dotenv import load_dotenv
import os

def extrair_metricas():
    """
    Carrega os dados de energia, processa as métricas de consumo e geração,
    e identifica os horários de pico e o uso da bateria e da rede.
    Retorna um dicionário com todas as métricas calculadas.
    """
    # Carrega as variáveis de ambiente e o arquivo
    load_dotenv()
    caminho = os.getenv("CAMINHO")
    dados = pd.read_excel(caminho)
    
    df = pd.DataFrame(dados)

    # Converte a coluna 'Horário' para o formato datetime
    df['Horário'] = pd.to_datetime(df['Horário'], format="%d.%m.%Y %H:%M:%S")
    df = df.set_index('Horário')

    # Cria colunas de consumo em kWh para análise
    # Multiplica por 5/60 para converter consumo de 5min em horas
    df['Carga(kWh)'] = df['Carga(W)'] * (5 / 60) / 1000
    df['Geracao Solar(kWh)'] = df['FV(W)'] * (5 / 60) / 1000
    df['Bateria(kWh)'] = df['Dados da Bateria(W)'] * (5 / 60) / 1000
    df['Rede Eletrica(kWh)'] = df['Rede elétrica (W)'] * (5 / 60) / 1000
    
    # Prepara o DataFrame para análise diária e por hora
    df_diario = df.resample('D').sum()
    df_por_hora = df.resample('h').sum()

    # Dicionário para armazenar todas as métricas
    metricas = {}

    # --- MÉTRICAS DIÁRIAS ---
    metricas["consumo_medio_diario"] = round(df_diario["Carga(kWh)"].mean(), 2)
    metricas["geracao_solar_media_diaria"] = round(df_diario["Geracao Solar(kWh)"].mean(), 2)

    # --- MÉTRICAS HORÁRIAS ---
    # Top 3 horas de maior consumo
    consumo_por_hora = df.groupby(df.index.hour)["Carga(kWh)"].sum()
    top_horas = consumo_por_hora.sort_values(ascending=False).head(3)
    metricas["horarios_pico_consumo"] = [f"{int(h)}h" for h in top_horas.index]
    metricas["valor_medio_pico_kWh"] = round(top_horas.mean(), 2)

    # --- USO DA BATERIA E DA REDE ---
    # Horas com maior descarga da bateria
    descarga_bateria_por_hora = df_por_hora[df_por_hora['Bateria(kWh)'] < 0].groupby(df_por_hora[df_por_hora['Bateria(kWh)'] < 0].index.hour)['Bateria(kWh)'].sum()
    top_descarga = descarga_bateria_por_hora.sort_values().head(3)
    metricas["horas_maior_descarga_bateria"] = [f"{int(h)}h" for h in top_descarga.index]
    
    # Horas com maior consumo da rede
    consumo_rede_por_hora = df_por_hora[df_por_hora['Rede Eletrica(kWh)'] < 0].groupby(df_por_hora[df_por_hora['Rede Eletrica(kWh)'] < 0].index.hour)['Rede Eletrica(kWh)'].sum()
    top_rede = consumo_rede_por_hora.sort_values().head(3)
    metricas["horas_maior_consumo_rede"] = [f"{int(h)}h" for h in top_rede.index]

    # --- CONSUMO SEMANA VS FIM DE SEMANA ---
    df_diario["dia_semana"] = df_diario.index.dayofweek
    consumo_semana = df_diario[df_diario["dia_semana"] < 5]["Carga(kWh)"].mean()
    consumo_fim_semana = df_diario[df_diario["dia_semana"] >= 5]["Carga(kWh)"].mean()
    
    metricas["consumo_medio_semana_kWh"] = round(consumo_semana, 2)
    metricas["consumo_medio_fim_semana_kWh"] = round(consumo_fim_semana, 2)
    
    return metricas
