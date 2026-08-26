from pydantic import BaseModel, Field


class SchweissParams(BaseModel):
    """Parameters für Schweissmaschine"""

    ampere: float = Field(..., gt=0, description="Schweissstrom in A", example=180.5)
    gas: float = Field(..., gt=0, description="Gasdurchfluss in l/min", example=15.0)
    voltage: float = Field(..., gt=0, description="Schweissspannung in V", example=25.3)
