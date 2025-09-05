from fastapi import APIRouter 
from simulacoes.status_aparelhos import infos
from backend.funcs_auxiliares.funcs_auxiliares import ler_cargas, salvar_cargas_prioritarias, reorganizar_indices, obter_clima
from backend.graficos.graficos import serie_temporal, histograma
from backend.IA.llm import assistente_llm_site

rota_site= APIRouter(prefix="/site")

@rota_site.get("/status_aparelhos")
async def status_aparelhos():
    try:
        return infos()
    except:
        return {"mensagem":"Não foi possível obter as informações sobre seu inversor e bateria."}

@rota_site.post("/escolher_cargas_prioritarias")
async def escolher_carga_prioritaria(dispositivo: str):
    try:
        cargas = ler_cargas()
        novo_id = str(len(cargas) + 1)
        cargas[novo_id] = dispositivo
        salvar_cargas_prioritarias(cargas)
        return {"mensagem": "Carga prioritária registrada com sucesso!"}
    except:
        return {"mensagem":"Não foi possível registrar sua carga prioritária."}
        
@rota_site.get("/lista_cargas_prioritarias")
async def listar_cargas_prioritarias():
    try:
        cargas = ler_cargas()
        return {"cargas_prioritarias": cargas}
    except: 
        return {"mensagem":"Não foi possível acessar sua lista de cargas prioritárias."}

@rota_site.delete("/remover_carga_prioritaria")
async def remover_carga_prioritaria(carga_id: str):
    try:
        cargas = ler_cargas()
        if carga_id in cargas:
            carga_removida = cargas.pop(carga_id)
            cargas = reorganizar_indices(cargas)
            salvar_cargas_prioritarias(cargas)
            return {"mensagem": f"Carga '{carga_removida}' removida com sucesso!"}
        else:
            return {"erro": "ID da carga não encontrado."}
    except:
        return {"mensagem":"Não foi possível deletar sua carga prioritária."}


@rota_site.get("/geracao_solar")
async def obter_historico_de_consumo():
    try: 
        geracao_solar_grafico =  serie_temporal('FV(W)', 'g', 'Geração Solar(W) por Dia no Mês de Agosto', 'Dia', 'Watts')
        return geracao_solar_grafico
    except:
        return {"mensagem":"Não foi possível o gráfico!"}
    
@rota_site.get("/energia_consumida_concessionaria")
async def obter_historico_de_consumo():
    try:
        energia_consumida_concessionaria_grafico = serie_temporal('Rede elétrica (W)', 'r', 'Energia Comprada da Concessionária(W) por Dia no Mês de Agosto', 'Dia', 'Watts')
        return energia_consumida_concessionaria_grafico
    except:
        return {"mensagem":"Não foi possível o gráfico!"}
    
@rota_site.get("/carga_consumida")
async def obter_historico_de_consumo():
    try:
        carga_consumida_grafico = serie_temporal('Carga(W)','b','Consumo da Residência(W) por Dia no Mês de Agosto', 'Dia', 'Watts')
        return carga_consumida_grafico
    except:
        return {"mensagem":"Não foi possível o gráfico!"}

@rota_site.get("/dados_bateria")
async def obter_historico_de_consumo():
    try:
        dados_bateria_grafico=serie_temporal('Dados da Bateria(W)','orange', 'Uso da Bateria(W) por Dia no Mês de Agosto', 'Dia', 'Watts')
        return dados_bateria_grafico
    except:
        return {"mensagem":"Não foi possível o gráfico!"}

@rota_site.get("/nivel_bateria")
async def obter_historico_de_consumo():
    try:
        nivel_bateria_grafico = histograma('SOC(%)', 10, 'Nível de Bateria(%) no Mês de Agosto ', 'Porcentagem da Bateria', 'Frequência', None)
        return nivel_bateria_grafico
    except:
        return {"mensagem":"Não foi possível o gráfico!"}


@rota_site.post("/assistente")
async def chatbot(pergunta: str):
    try:
        info_aparelhos = infos()
        dialogo = assistente_llm_site(info_aparelhos, pergunta)
        return dialogo
    except:
        return {"mensagem":"Desculpe não consegui processar sua pergunta. Tente novamente mais tarde!"}

@rota_site.get("/clima")
async def clima(local: str):
    try:
        clima = obter_clima(local)
        return clima
    except:
        return {"mensagem":"Não foi possível acessar as informações do clima de sua cidade."}