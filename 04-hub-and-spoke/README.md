# 04 - Hub-and-Spoke

Simulación local de topología Hub-and-Spoke usando redes Docker.

## Arquitectura

```
spoke-a ←→ [ hub ] ←→ spoke-b
```

- `app-a` solo está en red `spoke-a`
- `app-b` solo está en red `spoke-b`
- `hub` está en ambas redes → puede hablar con ambos spokes
- Los spokes **no** se ven entre sí directamente

## Cómo probarlo

```bash
docker compose up -d

# Desde el hub se puede llegar a ambos
docker compose exec hub ping -c 2 app-a
docker compose exec hub ping -c 2 app-b

# Desde app-a NO se puede llegar a app-b (aislados)
docker compose exec app-a ping -c 2 app-b || echo "Correcto: no hay conectividad directa"
```

## Equivalente en AWS

- **Hub**: AWS Transit Gateway + VPC de inspección/shared services
- **Spokes**: VPCs de producción, desarrollo, IoT, analytics
- Conectividad on-premise vía Direct Connect o Site-to-Site VPN al Transit Gateway

## GestController

- Hub: servicios compartidos (logging, identity, monitoring)
- Spokes: VPC de control de acceso, VPC de dispositivos IoT, VPC de analytics/IA
