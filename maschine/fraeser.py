import asyncio
import logging
import random
from datetime import datetime

from dh_deepdive.models.produkte.lobster import ProductLobster
from dh_deepdive.models.produktion_status import ProduktionStatus

logger = logging.getLogger(__name__)


async def simulate_fraeser(product_lobster: ProductLobster) -> ProduktionStatus:
    """
    Simuliert die Fräsmaschine

    Args:
        product_lobster: ProductLobster-Objekt mit den Produktionsdaten

    Returns:
        ProduktionStatus: Produktionsergebnis
    """
    logger.info(f"Fräser startet für Auftrag: {product_lobster.auftragsNummer}")

    startzeit = datetime.now()

    # Produktionszeit simulieren
    rpm_factor = product_lobster.maschineParams.rpm / 3000
    dauer = product_lobster.sollMenge * 0.01 / rpm_factor
    dauer = max(0.5, min(dauer, 5.0))

    logger.info(
        f"Fräser: Produziere {product_lobster.sollMenge} Einheiten in {dauer:.2f}s"
    )
    await asyncio.sleep(dauer)

    # Ergebnisse simulieren
    ausschuss_rate = 0.01 + (product_lobster.maschineParams.tief / 10) * 0.04
    ausschuss_rate = min(ausschuss_rate, 0.10)

    ausschuss = int(
        product_lobster.sollMenge * ausschuss_rate * random.uniform(0.8, 1.2)
    )
    ausschuss = min(ausschuss, product_lobster.sollMenge)
    fertig_menge = product_lobster.sollMenge - ausschuss

    endzeit = datetime.now()

    # Maschinenstatus
    status_roll = random.random()
    if status_roll < 0.05:
        maschinenstatus = "FEHLER"
        logger.warning(f"Fräser: FEHLER bei Auftrag {product_lobster.auftragsNummer}")
    elif status_roll < 0.10:
        maschinenstatus = "WARNUNG"
        logger.warning(f"Fräser: WARNUNG bei Auftrag {product_lobster.auftragsNummer}")
    else:
        maschinenstatus = "OK"

    logger.info(
        f"Fräser fertig: {fertig_menge} Stück produziert, {ausschuss} Ausschuss"
    )

    # ProduktionStatus zurückgeben
    return ProduktionStatus(
        auftragsnummer=product_lobster.auftragsNummer,
        produktId=product_lobster.produktId,
        sollMenge=product_lobster.sollMenge,
        fertigMenge=fertig_menge,
        ausschussMenge=ausschuss,
        maschineId="FR-001",
        startZeit=startzeit,
        endeZeit=endzeit,
        letzteAktualisierung=endzeit,
        cmdId=product_lobster.cmdId,
        maschineStatus=maschinenstatus,
    )
