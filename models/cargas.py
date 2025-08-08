from pydantic import BaseModel
from typing import List

class CargasPrioritarias(BaseModel):
    nome: List[str]