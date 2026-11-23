# Practice-Patter – Cloud Architecture Patterns

Repositorio práctico para el assignment de Cloud Architecture and Design Patterns.  
Demostraciones locales con Docker Compose de los patrones más relevantes, aplicables a proyectos como **GestController**.

## Contenido

| Carpeta | Patrones / Temas | Cómo demostrarlo |
|---------|------------------|------------------|
| `01-resiliencia` | Circuit Breaker, Retry, Timeout | `docker compose up --build` y consultar `/consultar` |
| `03-gateway-lb-proxy` | Reverse Proxy + Load Balancer (Nginx) | `docker compose up --build` y curl a `:8080` |
| `04-hub-and-spoke` | Hub-and-Spoke (redes Docker) | `docker compose up -d` y probar conectividad entre contenedores |
| `05-bastion` | Bastion / Jump Host (concepto) | Instrucciones y configuración de seguridad |
| `06-serverless-ecs` | Serverless (Lambda) vs Contenedores (ECS) | Ejemplos de código y task definitions |

## Evidencia de ejecución

Cada carpeta contiene o genera logs que demuestran el comportamiento.  
Captura de pantalla o salida de terminal deben incluirse en el informe.

## Relación con GestController

- **Resiliencia**: llamadas del Access Control Service a servicios IoT o de verificación de identidad.
- **Gateway/LB**: punto de entrada único para apps móviles y sistemas hospitalarios.
- **Hub-and-Spoke**: arquitectura de red multi-VPC (prod, IoT, analytics).
- **Bastion**: acceso administrativo seguro a instancias privadas.
- **Serverless/ECS**: procesamiento de eventos IoT (Lambda) y APIs de larga duración (ECS/Fargate).

## Cómo ejecutar

```bash
cd 01-resiliencia
docker compose up --build
# En otra terminal:
curl http://localhost:8001/consultar
```

Ver README específico de cada carpeta para más detalles.
