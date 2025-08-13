import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

dados= pd.read_excel(r"dados\dados_finais_inversor.xlsx")

df = pd.DataFrame(dados)
df['Horário'] = pd.to_datetime(df['Horário'], format="%d.%m.%Y %H:%M:%S")

def mapa_de_calor(valor: str, titulo: str):
    df['Hora'] = pd.to_datetime(df['Horário']).dt.hour
    df['Data'] = pd.to_datetime(df['Horário']).dt.date

    mapa_calor = df.pivot_table(index='Hora', columns='Data', values=valor, aggfunc='mean')

    plt.figure(figsize=(10, 6))
    sns.heatmap(mapa_calor, cmap='Reds')
    plt.title(titulo)
    plt.xlabel('Dia')
    plt.ylabel('Hora do Dia')
    plt.show()

def histograma():
    plt.hist(df['SOC(%)'], bins=5, alpha=0.7, color='skyblue', edgecolor='black')
    plt.title('Histograma: Nível da Bateria (%)')
    plt.xlabel('%')
    plt.ylabel('Frequência')
    plt.show()
