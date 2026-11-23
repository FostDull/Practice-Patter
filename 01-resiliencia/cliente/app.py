import time, logging, requests
from fastapi import FastAPI
from tenacity import retry, stop_after_attempt, wait_exponential, RetryError
import pybreaker

logging.basicConfig(level=logging.INFO)
log = logging.getLogger("cliente")
app = FastAPI()
URL = "http://inestable:8000/datos"

breaker = pybreaker.CircuitBreaker(fail_max=3, reset_timeout=10)

@retry(stop=stop_after_attempt(3),
       wait=wait_exponential(multiplier=0.5, max=4),
       before_sleep=lambda s: log.info(f"RETRY intento {s.attempt_number}"))
def llamar():
    # TIMEOUT: 2 segundos máximo por llamada
    r = requests.get(URL, timeout=2)
    r.raise_for_status()
    return r.json()

@app.get("/consultar")
def consultar():
    try:
        return breaker.call(llamar)          # CIRCUIT BREAKER envuelve al retry
    except pybreaker.CircuitBreakerError:
        log.warning("CIRCUITO ABIERTO: respuesta fallback")
        return {"ok": False, "fallback": True, "estado": breaker.current_state}
    except Exception as e:
        return {"ok": False, "error": str(e), "estado": breaker.current_state}