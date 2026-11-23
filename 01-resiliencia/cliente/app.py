import time, logging, requests
from fastapi import FastAPI
from tenacity import retry, stop_after_attempt, wait_exponential, RetryError
import pybreaker

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger("cliente")
app = FastAPI(title="Cliente Resiliente")

URL = "http://inestable:8000/datos"

breaker = pybreaker.CircuitBreaker(
    fail_max=3,
    reset_timeout=10,
    name="servicio-inestable"
)

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=0.5, max=4),
    before_sleep=lambda s: log.info(f"RETRY intento {s.attempt_number} – esperando..."),
    reraise=True
)
def llamar():
    log.info("Llamando al servicio inestable (timeout=2s)")
    r = requests.get(URL, timeout=2)
    r.raise_for_status()
    return r.json()

@app.get("/consultar")
def consultar():
    estado = breaker.current_state
    log.info(f"Estado actual del circuit breaker: {estado}")
    try:
        resultado = breaker.call(llamar)
        return {"ok": True, "data": resultado, "estado_circuit": estado}
    except pybreaker.CircuitBreakerError:
        log.warning("CIRCUITO ABIERTO → devolviendo fallback")
        return {
            "ok": False,
            "fallback": True,
            "mensaje": "Servicio temporalmente no disponible (circuit open)",
            "estado_circuit": breaker.current_state
        }
    except Exception as e:
        log.error(f"Error tras retries: {e}")
        return {
            "ok": False,
            "error": str(e),
            "estado_circuit": breaker.current_state
        }

@app.get("/estado")
def estado():
    return {"circuit_state": str(breaker.current_state)}
