from fastapi import APIRouter

rota_site= APIRouter(prefix="/site")

@rota_site.get("/status-inversor")
async def site_saber_status_inversor():
    pass

@rota_site.get("/acionar-cargas-prioritarias")
async def site_acionar_cargas_prioritarias():
    pass

@rota_site.get("/armazenar-energia")
async def site_armazenar_energia():
    pass

@rota_site.get("/ativar-modo")
async def site_ativar_modo():
    pass

