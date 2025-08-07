import random

def nivel_bateria():
    estado_opcoes = ["carregando", "descarregando"]

    return {
        "nivel_percentual": random.randint(0, 100),
        "estado": random.choice(estado_opcoes),
        "temperatura": round(random.uniform(25, 40), 1)         # Celsius
    }