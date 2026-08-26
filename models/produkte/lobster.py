from datetime import datetime
from typing import Union

from dh_deepdive.models.produkte.fraeser import FraeserParams
from dh_deepdive.models.produkte.schweiss import SchweissParams
from pydantic import BaseModel, Field


class ProductLobster(BaseModel):
    """Basis-Modell für Produkte, die von Lobster an die API gesendet werden"""

    auftragsNummer: str = Field(
        ..., description="Auftragsnummer", example="PO-2026-001"
    )
    auftragsZeit: datetime = Field(
        ..., description="Zeitpunkt des Auftrags", example="2026-08-26T10:00:00"
    )
    status: str = Field(..., description="Auftragsstatus", example="in_progress")
    sollMenge: int = Field(..., gt=0, description="Soll-Produktionsmenge", example=100)
    startZeit: datetime = Field(
        ..., description="Geplante Startzeit", example="2026-08-26T10:30:00"
    )
    produktId: str = Field(..., description="Produkt-ID", example="P-001")
    maschineParams: Union["FraeserParams", "SchweissParams"] = Field(
        ..., description="Maschinenspezifische Parameter"
    )
    cmdId: str = Field(..., description="Command ID", example="CMD-12345")


# Für Forward-Referenzen in Pydantic v2
ProductLobster.model_rebuild()
