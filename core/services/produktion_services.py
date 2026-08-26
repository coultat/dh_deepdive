import asyncio
import logging
from datetime import datetime

from dh_deepdive.maschine.fraeser import simulate_fraeser
from dh_deepdive.maschine.schweiss import simulate_schweiss
from dh_deepdive.models.proalpha import ERPOrder
from dh_deepdive.models.produkte.fraeser import FraeserParams
from dh_deepdive.models.produkte.lobster import ProductLobster
from dh_deepdive.models.produkte.schweiss import SchweissParams

logger = logging.getLogger(__name__)


class ProduktionService:
    """Orchestriert die Produktion mit Retry-Logik"""

    @staticmethod
    async def process_order(order: ERPOrder, max_retries: int = 3) -> dict:
        """
        Verarbeitet einen ERP-Auftrag mit Retry-Logik
        """
        logger.info(f"Verarbeite ERP-Auftrag: {order.auftragsnummer}")

        produkt = order.produkt.lower()

        # Maschinenparameter vorbereiten
        if "fräsen" in produkt or "fraesen" in produkt:
            params = FraeserParams(rpm=3000, tief=2.0)
            maschine_name = "Fräser"
            maschine_func = simulate_fraeser
        elif "schweissen" in produkt:
            params = SchweissParams(ampere=180.5, gas=15.0, voltage=25.3)
            maschine_name = "Schweiss"
            maschine_func = simulate_schweiss
        else:
            raise ValueError(
                f'Produkt "{order.produkt}" muss "Fräsen" oder "Schweissen" enthalten'
            )  # Das ist redundant aber nicht schlecht

        # ProductLobster erstellen
        product_lobster = ProductLobster(
            auftragsNummer=order.auftragsnummer,
            auftragsZeit=order.auftragszeit,
            status="in_progress",
            sollMenge=order.anzahl,
            startZeit=datetime.now(),
            produktId=order.produktid,
            maschineParams=params,
            cmdId=f"CMD-{int(datetime.now().timestamp())}",
        )

        # Retry-Logik
        for attempt in range(1, max_retries + 1):
            try:
                logger.info(
                    f"Versuche Produktion für Auftrag {order.auftragsnummer} (Versuch {attempt}/{max_retries})"
                )

                # Maschine starten
                produktion_status = await maschine_func(product_lobster)

                # Bei FEHLER und nicht letzter Versuch → Retry
                if (
                    produktion_status.maschineStatus == "FEHLER"
                    and attempt < max_retries
                ):
                    logger.warning(
                        f"FEHLER bei Auftrag {order.auftragsnummer} - Wiederhole in 1s..."
                    )
                    await asyncio.sleep(1)  # Wartezeit vor Retry
                    continue

                # Erfolg oder letzter Versuch mit FEHLER
                if (
                    produktion_status.maschineStatus == "FEHLER"
                    and attempt == max_retries
                ):
                    logger.error(
                        f"AUFTRAG FEHLGESCHLAGEN nach {max_retries} Versuchen: {order.auftragsnummer}"
                    )

                return {
                    "status": "erfolgreich"
                    if produktion_status.maschineStatus == "OK"
                    else "fehlgeschlagen",
                    "maschine": maschine_name,
                    "retry_versuche": attempt,
                    "produktion_status": produktion_status,
                }

            except Exception as e:
                logger.error(f"Fehler bei Versuch {attempt}: {e!s}")
                if attempt == max_retries:
                    raise
                await asyncio.sleep(0.5)

        raise RuntimeError("Maximale Retry-Anzahl überschritten")
