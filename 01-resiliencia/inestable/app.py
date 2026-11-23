import random, time
from fastapi import FastAPI, HTTPException
app = FastAPI()
MODE = {"fail_rate": 0.7, "delay": 0}

@app.get("/datos")
def datos():
    time.sleep(MODE["delay"])
    if random.random() < MODE["fail_rate"]:
        raise HTTPException(500, "Fallo simulado")
    return {"ok": True}

@app.post("/config")
def config(fail_rate: float = 0.0, delay: float = 0):
    MODE.update(fail_rate=fail_rate, delay=delay)
    return MODE