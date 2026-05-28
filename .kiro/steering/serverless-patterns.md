---
inclusion: auto
---

# Patrones de Arquitectura Serverless

Referencia basada en "Serverless Architectures on AWS" (Sbarski & Kroonenburg) y mejores practicas AWS.
Aplicar estos patrones al diseñar soluciones serverless para este proyecto.

## Principios Fundamentales

1. **Compute as glue** — Lambda es el pegamento entre servicios, no el lugar para logica monolitica
2. **Event-driven** — Los servicios reaccionan a eventos, no se llaman directamente entre si
3. **Stateless** — Cada invocacion es independiente. Estado en DynamoDB, S3 o cache
4. **Single responsibility** — Una Lambda = una responsabilidad clara
5. **Push not pull** — Preferir que los eventos lleguen (push) en vez de hacer polling

## Patrones de Diseño Serverless

### Command Pattern
- Cada accion del usuario se traduce en un comando discreto
- El comando se ejecuta en una Lambda dedicada
- Aplicacion: POST /campaigns → Lambda campanias-gestion ejecuta el comando "CrearCampaña"

### Messaging Pattern (Fan-out)
- Un evento se publica y multiples consumidores lo procesan independientemente
- Usar EventBridge o SNS para fan-out
- Aplicacion: Evento "CampañaCreada" → Tracking lo registra, Notificaciones lo procesa

### Queue-based Load Leveling
- Usar SQS entre productor y consumidor para absorber picos de carga
- El consumidor procesa a su ritmo sin saturarse
- Aplicacion: 85K notificaciones → SQS → Lambda procesa en lotes de 1000

### Circuit Breaker
- Proteger contra fallos en cascada de servicios externos
- Despues de N fallos, dejar de llamar por un periodo
- Aplicacion: Si Datacredito falla 3 veces → usar cache → reintentar en 60s

### CQRS (Command Query Responsibility Segregation)
- Separar escritura (commands) de lectura (queries) en modelos distintos
- Optimizar cada lado independientemente
- Aplicacion: DynamoDB para escritura operacional, BigQuery para lectura analitica

### Event Sourcing
- Almacenar la secuencia de eventos, no solo el estado final
- Permite reconstruir estado y auditar completamente
- Aplicacion: Tracking almacena cada evento (enviado, abierto, convertido)

### Saga Pattern (Orquestacion)
- Coordinar transacciones distribuidas entre multiples servicios
- Usar Step Functions como orquestador
- Aplicacion: Flujo de aprobacion → simulacion → aprobacion → ejecucion → notificacion

### Strangler Fig (Migracion)
- Migrar gradualmente de un sistema legacy a uno nuevo
- Rutear trafico progresivamente al nuevo sistema
- Aplicacion: ESB Bridge adapta llamadas al core bancario legacy

## Patrones de Integracion

### API Gateway Pattern
- Punto de entrada unico para todos los clientes
- Maneja auth, rate limiting, routing, CORS
- Nunca exponer Lambdas directamente

### Adapter Pattern
- Traducir interfaces de sistemas externos al modelo interno
- Desacoplar logica de negocio de protocolos legacy
- Una Lambda adapter por sistema externo

### Event Bus Pattern
- Bus centralizado (EventBridge) para comunicacion entre servicios
- Productores publican sin conocer a los consumidores
- Reglas de enrutamiento en el bus, no en el codigo

## Anti-patrones (evitar)

1. **Lambda monolitica** — No poner toda la logica en una sola Lambda grande
2. **Llamadas sincronas en cadena** — Lambda A llama a Lambda B que llama a Lambda C (latencia acumulada)
3. **Estado en memoria** — No guardar estado entre invocaciones (usar DynamoDB)
4. **Polling** — No hacer polling a colas o tablas. Usar triggers y eventos
5. **Timeout largo sin razon** — Configurar timeout justo para la operacion
6. **Paquetes grandes** — Mantener el zip de Lambda pequeño (< 50 MB) para reducir cold start

## Seguridad Serverless

- IAM roles con least privilege por Lambda (no compartir roles)
- Variables de entorno para configuracion (nunca hardcodear secretos)
- Secrets Manager para credenciales con rotacion automatica
- Validar input en API Gateway (JSON Schema) antes de llegar a Lambda
- Cifrar variables de entorno con KMS

## Observabilidad

- Structured logging (JSON) en todas las Lambdas
- X-Ray para tracing distribuido entre servicios
- Metricas custom en CloudWatch para KPIs de negocio
- Alarmas en: errores 5xx, throttling, DLQ con mensajes

## Costos

- Lambda: $0.20 por millon de requests + $0.0000166667 por GB-segundo
- Optimizar memoria (mas memoria = mas CPU = ejecucion mas rapida = menos costo)
- Usar ARM64 (Graviton) para 20% menos costo
- DynamoDB on-demand para cargas impredecibles, provisioned para cargas estables
- Revisar CloudWatch Logs retention (no dejar en "Never expire")
