import asyncio
import logging
import random
from datetime import datetime

from dh_deepdive.models.produkte.lobster import ProductLobster
from dh_deepdive.models.produktion_status import ProduktionStatus

logger = logging.getLogger(__name__)


async def simulate_schweiss(product_lobster: ProductLobster) -> ProduktionStatus:
    """
    Simuliert die Schweissmaschine

    Args:
        product_lobster: ProductLobster-Objekt mit den Produktionsdaten

    Returns:
        ProduktionStatus: Produktionsergebnis
    """
    logger.info(f"Schweiss startet für Auftrag: {product_lobster.auftragsNummer}")

    startzeit = datetime.now()
    # Produktionszeit simulieren
    ampere_factor = product_lobster.maschineParams.ampere / 180
    dauer = product_lobster.sollMenge * 0.015 / ampere_factor
    dauer = max(0.5, min(dauer, 6.0))

    logger.info(
        f"Schweiss: Produziere {product_lobster.sollMenge} Einheiten in {dauer:.2f}s"
    )
    await asyncio.sleep(dauer)

    # Ergebnisse simulieren
    voltage_factor = product_lobster.maschineParams.voltage / 25
    ausschuss_rate = 0.02 + (voltage_factor - 1) * 0.06
    ausschuss_rate = max(0.01, min(ausschuss_rate, 0.12))

    ausschuss = int(
        product_lobster.sollMenge * ausschuss_rate * random.uniform(0.8, 1.2)
    )
    ausschuss = min(ausschuss, product_lobster.sollMenge)
    fertig_menge = product_lobster.sollMenge - ausschuss

    endzeit = datetime.now()

    # Maschinenstatus
    status_roll = random.random()
    if status_roll < 0.07:
        maschinenstatus = "FEHLER"
        logger.warning(f"Schweiss: FEHLER bei Auftrag {product_lobster.auftragsNummer}")
    elif status_roll < 0.15:
        maschinenstatus = "WARNUNG"
        logger.warning(
            f"Schweiss: WARNUNG bei Auftrag {product_lobster.auftragsNummer}"
        )
    else:
        maschinenstatus = "OK"

    logger.info(
        f"Schweiss fertig: {fertig_menge} Stück produziert, {ausschuss} Ausschuss"
    )
    # ProduktionStatus zurückgeben
    return ProduktionStatus(
        auftragsnummer=product_lobster.auftragsNummer,
        produktId=product_lobster.produktId,
        sollMenge=product_lobster.sollMenge,
        fertigMenge=fertig_menge,
        ausschussMenge=ausschuss,
        maschineId="SW-001",
        startZeit=startzeit,
        endeZeit=endzeit,
        letzteAktualisierung=endzeit,
        cmdId=product_lobster.cmdId,
        maschineStatus=maschinenstatus,
    )
