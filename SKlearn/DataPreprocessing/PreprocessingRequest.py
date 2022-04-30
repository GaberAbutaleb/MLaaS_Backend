
from pydantic import BaseModel, Field
from typing import ClassVar, List

class PreProcesingRequest(BaseModel):
    handleDataCleaning: bool
    dC_HandlingMethod : str
    dC_columnList : List[str] = []
    dC_Threshold : int
    dC_regTarColumn : str




