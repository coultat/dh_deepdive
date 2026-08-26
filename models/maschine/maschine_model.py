from typing import Literal

from pydantic import BaseModel


class Maschine(BaseModel):
    maschineId: str
    maschineName: str  # "Fräser" o "Schweiss"
    hersteller: str  # "D+H Mechatronic AG"
    maschineStatus: Literal["Aktiv", "Wartung", "Offline", "Ausser Betrieb"]
    cmdId: str
