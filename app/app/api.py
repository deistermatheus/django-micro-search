from ninja import NinjaAPI
from typing import Dict

api = NinjaAPI()

@api.get("/health")
def health(request)-> Dict[str, bool]:
    return {"ok": True}
