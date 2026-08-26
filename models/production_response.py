from dh_deepdive.models.produktion_status import ProduktionStatus
from pydantic import BaseModel, Field


class ProduktionResponse(BaseModel):
    """Antwort der API nach Produktionsauftrag"""

    status: str = Field(..., description="Erfolgreich oder fehlgeschlagen")
    maschine: str = Field(..., description="Verwendete Maschine")
    retry_versuche: int = Field(..., description="Anzahl der Wiederholungsversuche")
    produktion_status: ProduktionStatus = Field(
        ..., description="Detailliertes Produktionsergebnis"
    )
