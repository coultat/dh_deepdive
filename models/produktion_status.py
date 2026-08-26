from datetime import datetime

from pydantic import BaseModel, Field


class ProduktionStatus(BaseModel):
    """Produktionsergebnis für Rückmeldung an Lobster/ERP"""

    auftragsnummer: str = Field(..., description="Auftragsnummer")
    produktId: str = Field(..., description="Produkt-ID")
    sollMenge: int = Field(..., description="Geplante Menge")
    fertigMenge: int = Field(..., description="Tatsächlich produzierte Menge")
    ausschussMenge: int = Field(..., description="Ausschussmenge")
    maschineId: str = Field(..., description="Maschinen-ID")
    startZeit: datetime = Field(..., description="Startzeit der Produktion")
    endeZeit: datetime = Field(..., description="Endzeit der Produktion")
    letzteAktualisierung: datetime = Field(
        ..., description="Letzte Statusaktualisierung"
    )
    cmdId: str = Field(..., description="Command ID")
    maschineStatus: str | None = Field(
        None, description="Status der Maschine (OK, WARNUNG, FEHLER)"
    )
