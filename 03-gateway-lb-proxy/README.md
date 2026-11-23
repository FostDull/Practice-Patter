# 03 - API Gateway / Load Balancer / Reverse Proxy

Demostración local de **Reverse Proxy + Load Balancer** usando Nginx.

## Arquitectura

```
Cliente → Nginx (puerto 8080) → api1 / api2 / api3 (round-robin)
```

Nginx actúa como:
- **Reverse Proxy**: oculta los backends y termina la conexión.
- **Load Balancer**: distribuye tráfico entre las 3 instancias idénticas.

## Cómo ejecutarlo

```bash
docker compose up --build
```

```bash
# Ver distribución de carga
for i in {1..6}; do curl -s http://localhost:8080/ | jq; done
```

Salida esperada (diferentes hostnames):
```json
{"atendido_por": "api1"}
{"atendido_por": "api2"}
{"atendido_por": "api3"}
...
```

## Relación con el assignment

- **Reverse Proxy**: Nginx
- **Load Balancer**: upstream round-robin
- **API Gateway**: en AWS se usaría Amazon API Gateway delante de este tipo de servicios (auth, rate limiting, etc.)

## GestController

Punto de entrada único para apps móviles y sistemas del hospital → API Gateway → ALB → microservicios ECS.
