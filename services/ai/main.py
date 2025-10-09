from fastapi import FastAPI
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
@app.post("/capsule/reconstruct")
def compute(payload: Payload):
    seed = (payload.text or str(payload.data) or "").encode("utf-8")
    h = int(hashlib.sha256(seed).hexdigest(), 16) % 1000
    score = round((math.sin(h) + 1) / 2, 4)
    return {"ok": True, "endpoint": "/capsule/reconstruct", "score": score, "note": "placeholder logic"}
