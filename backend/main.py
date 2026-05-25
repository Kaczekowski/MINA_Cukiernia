from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

app = FastAPI(title="Cukiernia Clicker")

@app.get("/health")
def check_health():
    return {"status": "ok"}

app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")