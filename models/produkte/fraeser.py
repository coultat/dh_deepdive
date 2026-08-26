from pydantic import BaseModel, Field


class FraeserParams(BaseModel):
    """Parameters für Fräsmaschine"""

    rpm: int = Field(..., gt=0, description="Drehzahl in RPM", example=3000)
    tief: float = Field(..., gt=0, description="Schnitttiefe in mm", example=2.0)
