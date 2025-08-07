import random

def status_inversor():
    return {
        "potencia_atual": round(random.uniform(2500, 3500), 1),  # Watts
        "geracao_fotovoltaica": round(random.uniform(400, 650), 1),        # kWh
        "geracao_total": round(random.uniform(10, 1000), 1), # kWh
    }
