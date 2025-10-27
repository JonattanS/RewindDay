from fastapi import FastAPI, Response
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional
import hashlib, math
app = FastAPI(title="RewindDay AI")
class Payload(BaseModel):
    text: Optional[str] = None
    data: Optional[dict] = None
@app.get("/health")
def health():
    return {"ok": True, "name": "RewindDay ai"}
@app.get("/", include_in_schema=False)
def root():
    # Responde 200 en la raíz y apunta a /docs
    return {"ok": True, "service": "RewindDay AI", "docs": "/docs", "health": "/health"}
 
@app.get("/health", include_in_schema=False)
def health():
    return {"ok": True}
 
@app.get("/favicon.ico", include_in_schema=False)
def favicon():
    # Evita 404 del favicon con una respuesta vacía
    return Response(status_code=204)
@app.post("/capsule/reconstruct")
def compute(payload: Payload):
    seed = (payload.text or str(payload.data) or "").encode("utf-8")
    h = int(hashlib.sha256(seed).hexdigest(), 16) % 1000
    score = round((math.sin(h) + 1) / 2, 4)
    return {"ok": True, "endpoint": "/capsule/reconstruct", "score": score, "note": "placeholder logic"}
