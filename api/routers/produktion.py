from dh_deepdive.core.services.produktion_services import ProduktionService
from dh_deepdive.models.proalpha import ERPOrder
from dh_deepdive.models.production_response import ProduktionResponse
from fastapi import APIRouter, HTTPException

produktion_router = APIRouter()


@produktion_router.post("/produktion/", tags=["produktion"])
async def start_produktion(order: ERPOrder) -> ProduktionResponse:
    """
    Startet die Produktion basierend auf dem ERP-Auftrag
    """
    try:
        result = await ProduktionService.process_order(order)
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:  # Das würde nie in einem Productioncode sein. Aber hier ist nur ein Deepdive PoC
        raise HTTPException(status_code=500, detail=f"Interner Fehler: {e!s}")
