# Deepdive

**Deep Dive – Integration Engineer**

Dieses Projekt demonstriert eine Produktionsintegrationslösung für die D+H Mechatronic AG.  
Es zeigt den Datenfluss vom ERP-System über eine Integrationsplattform (Lobster) bis zur Maschine und zurück.

---


## 🚀 Installation & Start

### 1. Repository klonen

```bash
git clone <repo-url>
cd dh_deepdive
```

Virtuelle Umgebung erstellen 

```bash
python -m venv venv
source venv/bin/activate      # Linux/Mac
venv\Scripts\activate         # Windows
```

Abhängigkeiten installieren

```bash
pip install -r requirements.txt
```

Server starten

```bash
python run.py
```

Oder direkt mit uvicorn

```bash
uvicorn api.main:app --reload
```

Startet einen Produktionsauftrag. Die Maschine (Fräser oder Schweiss) wird automatisch anhand des Produktnamens ausgewählt.
Request-Body (JSON)


{
  "auftragsnummer": "PO-2026-001",
  "auftragszeit": "2026-08-26T10:00:00",
  "anzahl": 100,
  "produkt": "Gehäuse_Fräsen",
  "produktid": "P-001",
  "kunde": "BMW",
  "kunde_id": "K-123"
}

Response

{
  "status": "erfolgreich",
  "maschine": "Fräser",
  "retry_versuche": 1,
  "produktion_status": {
    "auftragsnummer": "PO-2026-001",
    "produktId": "P-001",
    "sollMenge": 100,
    "fertigMenge": 97,
    "ausschussMenge": 3,
    "maschineId": "FR-001",
    "startZeit": "2026-08-26T10:15:30.123456",
    "endeZeit": "2026-08-26T10:16:31.123456",
    "maschineStatus": "OK"
  }
}

Technologien:

- Python 3.12+
- FastAPI – Web-Framework
- Pydantic v2 – Datenvalidierung
- Uvicorn – ASGI-Server
- Ruff – Linting & Formatierung