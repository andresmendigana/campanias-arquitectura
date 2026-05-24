---
title: "Diagramas de Secuencia - Arquitectura Serverless AWS+GCP"
section: "06b"
---

# 6b. Diagramas de Secuencia - CAM-TOBE-06 Serverless AWS+GCP

## 1. Flujo Principal: Creación y Ejecución de Campaña

```mermaid
sequenceDiagram
    participant A as Analista
    participant CF as CloudFront + WAF
    participant APIGW as API Gateway
    participant COG as Cognito
    participant L_CAMP as Lambda<br/>Gestión Campañas
    participant L_REG as Lambda<br/>Motor de Reglas
    participant L_SCORE as Lambda<br/>Scoring
    participant L_ESB as Lambda<br/>ESB Bridge
    participant SF as Step Functions<br/>Aprobación
    participant DDB as DynamoDB<br/>Campañas
    participant CORE as Core Bancario
    participant CRM as CRM Siebel
    participant DC as Datacrédito

    A->>CF: HTTPS - Login
    CF->>APIGW: Request
    APIGW->>COG: Validar credenciales
    COG-->>APIGW: JWT Token (access + refresh)
    APIGW-->>CF: Token
    CF-->>A: Autenticado

    Note over A,DC: Fase 1: Configuración de Campaña

    A->>CF: POST /campaigns (reglas, producto, segmento)
    CF->>APIGW: Forward + JWT
    APIGW->>COG: Validar token
    COG-->>APIGW: OK
    APIGW->>L_CAMP: Crear campaña
    L_CAMP->>DDB: Guardar campaña (estado: BORRADOR)
    DDB-->>L_CAMP: OK
    L_CAMP-->>APIGW: campaignId: 45
    APIGW-->>A: 201 Created

    Note over A,DC: Fase 2: Evaluación de Reglas y Scoring

    A->>APIGW: POST /campaigns/45/evaluate
    APIGW->>L_REG: Evaluar reglas de elegibilidad
    L_REG->>L_ESB: Consultar ingresos/egresos (3-5 años)
    L_ESB->>CORE: SOAP/REST vía VPN
    CORE-->>L_ESB: Movimientos del cliente
    L_ESB-->>L_REG: Datos normalizados

    L_REG->>L_ESB: Consultar datos demográficos
    L_ESB->>CRM: Query vía ESB IBM
    CRM-->>L_ESB: Datos cliente
    L_ESB-->>L_REG: Datos normalizados

    L_REG->>L_SCORE: Calcular scoring alternativo
    L_SCORE->>DC: GET /score/{clienteId}
    DC-->>L_SCORE: Score + comportamiento pago
    L_SCORE-->>L_REG: Score consolidado

    L_REG->>DDB: Guardar lista elegibles
    L_REG-->>APIGW: 85,000 clientes elegibles
    APIGW-->>A: Lista de elegibles + resumen
```

## 2. Flujo de Simulación y Aprobación

```mermaid
sequenceDiagram
    participant A as Analista
    participant G as Gerente Riesgo
    participant APIGW as API Gateway
    participant L_SIM as Lambda<br/>Simulación
    participant L_SCORE as Lambda<br/>Scoring
    participant SF as Step Functions<br/>Aprobación
    participant L_CAMP as Lambda<br/>Gestión Campañas
    participant DDB as DynamoDB
    participant EB as EventBridge
    participant SNS as SNS

    Note over A,SNS: Fase 3: Simulación

    A->>APIGW: POST /campaigns/45/simulate
    APIGW->>L_SIM: Ejecutar simulación
    L_SIM->>DDB: Leer lista elegibles + reglas
    DDB-->>L_SIM: 85,000 clientes + parámetros
    L_SIM->>L_SCORE: Proyectar conversión por segmento
    L_SCORE-->>L_SIM: Proyección: 8% conversión estimada
    L_SIM->>DDB: Guardar resultado simulación
    L_SIM-->>APIGW: Proyección: 6,800 conversiones, riesgo: MEDIO
    APIGW-->>A: Resultado simulación
    
    Note over A,SNS: Campaña pasa a estado SIMULADA

    A->>APIGW: PUT /campaigns/45 (estado: SIMULADA)
    APIGW->>L_CAMP: Actualizar estado
    L_CAMP->>DDB: Estado → SIMULADA
    L_CAMP->>EB: Evento: CampañaSimulada
    EB->>SNS: Notificar al Gerente de Riesgo
    SNS-->>G: Email: "Campaña 45 lista para aprobación"

    Note over A,SNS: Fase 4: Aprobación (Step Functions)

    G->>APIGW: POST /campaigns/45/approve
    APIGW->>SF: Iniciar flujo de aprobación
    SF->>L_CAMP: Validar prerrequisitos
    L_CAMP->>DDB: Verificar: simulación OK, reglas completas
    L_CAMP-->>SF: Prerrequisitos OK
    SF->>L_CAMP: Cambiar estado → APROBADA
    L_CAMP->>DDB: Estado → APROBADA (approvedBy: gerente, timestamp)
    L_CAMP->>EB: Evento: CampañaAprobada
    SF-->>APIGW: Campaña aprobada
    APIGW-->>G: 200 OK - Aprobada
```

## 3. Flujo de Ejecución y Notificación Multicanal

```mermaid
sequenceDiagram
    participant A as Analista
    participant APIGW as API Gateway
    participant SF as Step Functions<br/>Ejecución
    participant L_CAMP as Lambda<br/>Gestión Campañas
    participant L_NOTIF as Lambda<br/>Notificaciones
    participant SQS as SQS<br/>Cola Notificaciones
    participant PROV as Proveedor<br/>Notificaciones
    participant DDB as DynamoDB
    participant EB as EventBridge
    participant CLI as Cliente

    Note over A,CLI: Fase 5: Ejecución de Campaña

    A->>APIGW: POST /campaigns/45/execute
    APIGW->>SF: Iniciar flujo de ejecución
    SF->>L_CAMP: Preparar lotes de envío
    L_CAMP->>DDB: Leer lista de 85,000 clientes elegibles
    DDB-->>L_CAMP: Lista completa con datos de contacto
    L_CAMP->>SQS: Encolar en lotes de 1,000 (85 mensajes)
    L_CAMP->>DDB: Estado → EN_EJECUCION
    L_CAMP->>EB: Evento: CampañaEnEjecución

    Note over A,CLI: Procesamiento asíncrono por lotes

    loop Cada lote de 1,000 clientes
        SQS->>L_NOTIF: Lote de 1,000 clientes
        L_NOTIF->>L_NOTIF: Seleccionar canal por cliente (SMS/Email/Push)
        
        alt Canal SMS
            L_NOTIF->>PROV: POST /sms/bulk (números, mensaje)
            PROV-->>L_NOTIF: 200 OK - Encolado
        else Canal Email
            L_NOTIF->>PROV: POST /email/bulk (emails, template, datos)
            PROV-->>L_NOTIF: 200 OK - Encolado
        else Canal Push
            L_NOTIF->>PROV: POST /push/bulk (deviceTokens, payload)
            PROV-->>L_NOTIF: 200 OK - Encolado
        end

        L_NOTIF->>EB: Evento: LoteEnviado (1,000 clientes, canal, status)
        PROV-->>CLI: SMS / Email / Push Notification
    end

    Note over A,CLI: Finalización

    SF->>L_CAMP: Todos los lotes procesados
    L_CAMP->>DDB: Estado → COMPLETADA
    L_CAMP->>EB: Evento: CampañaCompletada
```

## 4. Flujo de Tracking y Dashboard (Cross-Cloud)

```mermaid
sequenceDiagram
    participant PROV as Proveedor<br/>Notificaciones
    participant EB as EventBridge
    participant L_TRACK as Lambda<br/>Tracking
    participant DDB_T as DynamoDB<br/>Tracking
    participant CORE as Core Bancario
    participant KF as Kinesis Firehose
    participant DF as GCP Dataflow
    participant BQ as GCP BigQuery
    participant LK as Looker Dashboard
    participant G as Gerente Riesgo

    Note over PROV,G: Fase 6: Tracking de Efectividad (días/semanas)

    PROV->>EB: Webhook: EmailAbierto (clienteId, timestamp)
    EB->>L_TRACK: Procesar evento de interacción
    L_TRACK->>DDB_T: Registrar: {cliente:123, acción:abrió_email, fecha}
    
    PROV->>EB: Webhook: SMSEntregado (clienteId, timestamp)
    EB->>L_TRACK: Procesar evento
    L_TRACK->>DDB_T: Registrar: {cliente:456, acción:sms_entregado, fecha}

    Note over PROV,G: Detección de Conversión

    CORE->>EB: Evento: ClienteSolicitóProducto (clienteId, producto)
    EB->>L_TRACK: Procesar solicitud de producto
    L_TRACK->>DDB_T: Buscar: ¿cliente estaba en campaña activa?
    DDB_T-->>L_TRACK: Sí - Campaña 45, notificado hace 3 días
    L_TRACK->>DDB_T: Registrar CONVERSIÓN + marcar EXCLUIDO
    L_TRACK->>EB: Evento: ClienteConvertido (campañaId:45, clienteId:123)

    Note over PROV,G: Streaming Cross-Cloud (AWS → GCP)

    DDB_T->>KF: DynamoDB Streams → Kinesis Firehose (cada 5 min)
    KF->>DF: Batch de eventos → GCP Dataflow
    DF->>DF: Transformar, enriquecer, agregar métricas
    DF->>BQ: INSERT INTO historico_campanias

    Note over PROV,G: Dashboard Mensual

    G->>LK: Consultar dashboard (corte mensual)
    LK->>BQ: SELECT conversiones, exclusiones, efectividad...
    BQ-->>LK: Datos agregados
    LK-->>G: Dashboard: 8% conversión, 6,800 convertidos, 1,200 excluidos
    
    Note over G: Decisión: ajustar apetito de riesgo para siguiente semestre
```

## 5. Flujo de Scoring Alternativo (Detalle)

```mermaid
sequenceDiagram
    participant L_REG as Lambda<br/>Motor de Reglas
    participant L_SCORE as Lambda<br/>Scoring
    participant CACHE as DynamoDB DAX<br/>Cache
    participant DC as Datacrédito
    participant TEL as Telecomunicaciones
    participant OEF as Otras Entidades
    participant CB as Circuit Breaker

    L_REG->>L_SCORE: Calcular score (clienteId: 123)
    
    L_SCORE->>CACHE: GET score:123
    alt Cache HIT (< 24h)
        CACHE-->>L_SCORE: Score: 720, fuentes: [DC, TEL]
        L_SCORE-->>L_REG: Score desde cache
    else Cache MISS
        L_SCORE->>CB: Verificar estado circuit breaker
        
        alt Circuit Breaker CERRADO (normal)
            L_SCORE->>DC: GET /score/123
            DC-->>L_SCORE: Score: 680, comportamiento: BUENO
            
            L_SCORE->>TEL: GET /comportamiento/123
            TEL-->>L_SCORE: Antigüedad: 4 años, pago: puntual
            
            L_SCORE->>OEF: GET /productos/123
            OEF-->>L_SCORE: 2 productos activos, sin mora
            
            L_SCORE->>L_SCORE: Calcular score consolidado (ponderado)
            L_SCORE->>CACHE: SET score:123 = 720, TTL: 24h
            L_SCORE-->>L_REG: Score: 720, confianza: ALTA
            
        else Circuit Breaker ABIERTO (Datacrédito caído)
            L_SCORE->>CACHE: GET last_known_score:123
            CACHE-->>L_SCORE: Último score conocido: 650
            L_SCORE-->>L_REG: Score: 650, confianza: BAJA (degradado)
            Note over L_SCORE: Alerta enviada a CloudWatch
        end
    end
```

## 6. Flujo de Autenticación y Seguridad

```mermaid
sequenceDiagram
    participant A as Analista
    participant R53 as Route 53
    participant CF as CloudFront
    participant WAF as WAF
    participant APIGW as API Gateway
    participant COG as Cognito
    participant AD as Active Directory

    A->>R53: DNS lookup: campanias.banco.com.co
    R53-->>A: IP de CloudFront

    A->>CF: HTTPS (TLS 1.3) - POST /auth/login
    CF->>WAF: Inspeccionar request
    WAF->>WAF: Verificar: rate limit, geo, SQLi, XSS
    
    alt WAF BLOQUEA
        WAF-->>CF: 403 Forbidden
        CF-->>A: Acceso denegado
    else WAF PERMITE
        WAF->>APIGW: Request limpio
        APIGW->>COG: InitiateAuth (username, password)
        COG->>AD: Validar credenciales (LDAP)
        AD-->>COG: Credenciales válidas
        COG->>COG: Generar JWT (15 min) + Refresh Token (7 días)
        COG-->>APIGW: Tokens
        APIGW-->>CF: 200 + Tokens
        CF-->>A: JWT Access Token + Refresh Token
    end

    Note over A,AD: Requests subsiguientes

    A->>CF: GET /campaigns (Authorization: Bearer JWT)
    CF->>WAF: Inspeccionar
    WAF->>APIGW: OK
    APIGW->>APIGW: Validar JWT (firma, expiración, roles)
    
    alt Token válido + rol autorizado
        APIGW->>APIGW: Extraer userId, roles del JWT
        Note over APIGW: Route to Lambda con contexto de usuario
    else Token expirado
        APIGW-->>A: 401 Unauthorized
        A->>APIGW: POST /auth/refresh (refreshToken)
        APIGW->>COG: Refresh token
        COG-->>APIGW: Nuevo JWT
        APIGW-->>A: Nuevo Access Token
    end
```

## Resumen de Flujos

| # | Flujo | Servicios involucrados | Tipo |
|---|-------|----------------------|------|
| 1 | Creación y evaluación | API GW → Lambda Campañas → Lambda Reglas → Lambda Scoring → ESB Bridge → Core/CRM/Datacrédito | Síncrono |
| 2 | Simulación y aprobación | API GW → Lambda Simulación → Step Functions → DynamoDB → EventBridge → SNS | Síncrono + Evento |
| 3 | Ejecución y notificación | Step Functions → Lambda Campañas → SQS → Lambda Notificaciones → Proveedor externo | Asíncrono (batch) |
| 4 | Tracking y dashboard | EventBridge → Lambda Tracking → DynamoDB → Kinesis Firehose → Dataflow → BigQuery → Looker | Asíncrono (streaming) |
| 5 | Scoring alternativo | Lambda Scoring → Cache → Datacrédito/Telecom/Otras + Circuit Breaker | Síncrono con fallback |
| 6 | Autenticación | CloudFront → WAF → API Gateway → Cognito → Active Directory | Síncrono |
