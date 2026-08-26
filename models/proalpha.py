import re
from datetime import datetime

from pydantic import BaseModel, Field, field_validator


class ERPOrder(BaseModel):
    """Produktionsauftrag aus dem ERP-System"""

    auftragsnummer: str = Field(
        ..., description="Auftragsnummer", example="PO-2026-001"
    )
    auftragszeit: datetime = Field(
        ..., description="Datum und Uhrzeit von Auftrags", example="2002-06-30T10:00:00"
    )
    anzahl: int = Field(..., gt=0, description="Produktionsmenge", example=100)
    produkt: str = Field(
        ..., description="Produktbezeichnung", example="Gehäuse_Fräsen"
    )
    produktid: str = Field(..., description="Produkt-ID", example="P-001")
    kunde: str = Field(..., description="Kundenname", example="BMW")
    kunde_id: str = Field(..., description="Kunden-ID", example="K-123")

    @field_validator("auftragsnummer")
    def validate_auftragsnummer(cls, v):
        if not re.match(r"^PO-\d{4}-\d{3}$", v):
            raise ValueError("Format muss PO-YYYY-XXX sein (z.B. PO-2026-001)")
        return v

    @field_validator("produkt")
    def validate_produkt(cls, v):
        # Validierung, um zu entscheiden, welche Maschine verwendet wird
        if not any(keyword in v.lower() for keyword in ["fräsen", "schweissen"]):
            raise ValueError('Produkt muss "Fräsen" oder "Schweissen" enthalten')
        return v
