# 01 - Resiliencia: Circuit Breaker + Retry + Timeout

Demostración práctica de los tres patrones de resiliencia más importantes.

## Componentes

- **inestable**: servicio que falla aleatoriamente (70% de fallos por defecto) y puede introducir delay.
- **cliente**: llama al servicio inestable aplicando:
  - **Timeout** de 2 segundos por llamada (`requests.get(..., timeout=2)`)
  - **Retry** con backoff exponencial (máx. 3 intentos) usando `tenacity`
  - **Circuit Breaker** con `pybreaker` (abre tras 3 fallos, se resetea a los 10s)

## Cómo ejecutarlo

```bash
docker compose up --build
```

En otra terminal:

```bash
# Probar varias veces
for i in {1..10}; do curl -s http://localhost:8001/consultar | jq; sleep 1; done
```

## Configurar el servicio inestable (opcional)

```bash
# Hacer que siempre falle
curl -X POST "http://localhost:8000/config?fail_rate=1.0"

# Hacer que siempre funcione
curl -X POST "http://localhost:8000/config?fail_rate=0.0"

# Introducir delay de 3s (provocará timeout)
curl -X POST "http://localhost:8000/config?delay=3"
```

## Evidencia esperada

Logs del cliente mostrando:
- `RETRY intento X`
- `CIRCUITO ABIERTO: respuesta fallback`
- Respuestas exitosas cuando el circuito está cerrado

## Aplicación en GestController

Usar este patrón en llamadas a:
- Servicio de verificación biométrica / facial
- Registro de dispositivos IoT
- Gateways de notificación externos
