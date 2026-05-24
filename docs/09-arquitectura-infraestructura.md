# Arquitectura Serverless Multinube - Sistema de Campañas TO-BE

## AWS (Plataforma de Campañas) + GCP (Analítica y Dashboards)

### Decisión de Re-Platform

| Aspecto | Decisión |
|---------|----------|
| Motivación | Aplicativo actual desactualizado y sin soporte |
| Estrategia | Re-platform a serverless multinube |
| AWS | Rediseño del aplicativo de campañas (compute, integración, datos operacionales) |
| GCP | Almacenamiento de históricos y generación de dashboards con analítica |
| Patrón | Event-driven serverless + streaming cross-cloud |

---

## Diagrama de Solución

```mermaid
graph LR
    subgraph "Actores"
        A1[Analista de Campañas]
        A2[Gerente de Riesgo]
        A3[Cliente 18-25 años]
    end

    subgraph "AWS Cloud"
        subgraph "Edge & Security"
            R53[Route 53]
            CF[CloudFront]
            WAF_N[WAF]
        end

        subgraph "Auth"
            COG[Cognito<br/>OAuth2/OIDC]
        end

        subgraph "API Layer"
            APIGW[API Gateway<br/>REST APIs]
        end

        subgraph "Plataforma Campañas - Serverless"
            L_REG[Lambda<br/>Motor de Reglas]
            L_SIM[Lambda<br/>Simulación Scoring]
            L_CAMP[Lambda<br/>Gestión Campañas]
            L_SCORE[Lambda<br/>Scoring Alternativo]
            L_NOTIF[Lambda<br/>Orquestador Notificaciones]
            L_TRACK[Lambda<br/>Tracking Efectividad]
            SF_APR[Step Functions<br/>Flujo Aprobación]
            SF_EJE[Step Functions<br/>Flujo Ejecución]
        end

        subgraph "Event-Driven"
            EB[EventBridge<br/>Bus de Eventos]
            SQS_N[SQS<br/>Cola Notificaciones]
            SNS_N[SNS<br/>Alertas]
        end

        subgraph "Data AWS"
            DDB_CAMP[DynamoDB<br/>Campañas & Reglas]
            DDB_TRACK[DynamoDB<br/>Tracking]
            S3_D[S3<br/>Documentos & Logs]
        end

        subgraph "Integración Legacy"
            L_ESB[Lambda<br/>ESB Bridge Adapter]
        end

        subgraph "Streaming Cross-Cloud"
            KF[Kinesis Firehose<br/>Streaming a GCP]
        end

        CW[CloudWatch<br/>Observabilidad]
    end

    subgraph "GCP - Analítica & Dashboards"
        DF[Dataflow<br/>ETL & Transformación]
        BQ[BigQuery<br/>Histórico Campañas]
        LK[Looker / Data Studio<br/>Dashboard Mensual<br/>Apetito de Riesgo]
    end

    subgraph "On-Premise"
        CORE[Core Bancario]
        CRM_S[CRM]
        CRED[Sistema Créditos]
    end

    subgraph "Proveedores Externos"
        CR[Centrales de Riesgo]
        TEL[Telecomunicaciones]
        OEF[Otras Entidades Financieras]
        PN[Proveedor Notificaciones<br/>SMS/Email/Push]
    end

    A1 -->|HTTPS| R53
    A2 -->|HTTPS| R53
    R53 --> CF --> WAF_N --> APIGW
    APIGW --> COG
    APIGW --> L_REG
    APIGW --> L_SIM
    APIGW --> L_CAMP

    L_CAMP --> SF_APR
    SF_APR --> L_SCORE
    SF_APR --> SF_EJE
    SF_EJE --> L_NOTIF

    L_REG --> L_SCORE
    L_SCORE --> L_ESB

    L_CAMP --> EB
    L_NOTIF --> SQS_N
    SQS_N --> L_TRACK
    EB --> L_TRACK

    L_REG --> DDB_CAMP
    L_CAMP --> DDB_CAMP
    L_TRACK --> DDB_TRACK
    L_CAMP --> S3_D

    DDB_TRACK --> KF
    KF --> DF --> BQ --> LK

    L_ESB --> CORE
    L_ESB --> CRM_S
    L_ESB --> CRED

    L_SCORE --> CR
    L_SCORE --> TEL
    L_SCORE --> OEF
    L_NOTIF --> PN
    PN -->|SMS/Email/Push| A3

    LK -->|Dashboard Mensual| A2
```

---

## Componentes AWS (Plataforma de Campañas)

| Servicio AWS | Componente | Función |
|-------------|-----------|---------|
| Route 53 | DNS | Resolución de dominio |
| CloudFront | CDN | Distribución de contenido estático (SPA) |
| WAF | Firewall | Protección contra ataques web |
| Cognito | Auth | Autenticación OAuth2/OIDC, MFA, integración AD |
| API Gateway | API Layer | Exposición de APIs REST, rate limiting, versionado |
| Lambda (x6) | Compute | Motor de reglas, simulación, gestión campañas, scoring, notificaciones, tracking |
| Step Functions (x2) | Orquestación | Flujo de aprobación y ejecución de campañas |
| EventBridge | Eventos | Bus de eventos para comunicación asíncrona |
| SQS | Cola | Buffer para notificaciones masivas |
| SNS | Alertas | Notificaciones internas y alertas operativas |
| DynamoDB (x2) | Data operacional | Campañas/reglas y tracking de efectividad |
| S3 | Storage | Documentos, logs, archivos de integración |
| Kinesis Firehose | Streaming | Envío de datos de tracking hacia GCP |
| CloudWatch | Observabilidad | Logs, métricas, alarmas, tracing |

## Componentes GCP (Analítica y Dashboards)

| Servicio GCP | Componente | Función |
|-------------|-----------|---------|
| Data Lake (GCS + BigQuery) | Almacenamiento | Patrón de espacios y acceso directo. Almacena grandes volúmenes de datos replicados desde sistemas internos |
| Dataflow | ETL | Transformación de datos streaming desde AWS. Ingesta y calidad de datos |
| NEW APP Campañas (SaaS) | Analítica Avanzada | Servicio SaaS conectado al Data Lake para modelos de analítica avanzada y scoring |
| Looker / Data Studio | Dashboard | Dashboard mensual, apetito de riesgo, efectividad |

### Restricción del Data Lake
> No todos los datos requeridos para las campañas se están replicando al Data Lake actualmente,
> aunque ya se tiene un proceso de replicación, ingesta de datos y calidad de información.
> El MVP debe contemplar completar la replicación de las fuentes faltantes.

## Flujo Cross-Cloud (AWS → GCP)

```
DynamoDB (Tracking) → DynamoDB Streams → Kinesis Firehose → GCP Dataflow → BigQuery → Looker
```

| Paso | Servicio | Acción |
|------|---------|--------|
| 1 | DynamoDB Streams | Captura cambios en tabla de tracking |
| 2 | Kinesis Firehose | Bufferea y envía batch a GCP (cada 5 min o 5MB) |
| 3 | Dataflow | Transforma y enriquece datos para analítica |
| 4 | BigQuery | Almacena histórico, permite queries SQL analíticos |
| 5 | Looker | Genera dashboard con corte mensual para gerencia |

## Notas de Arquitectura

| Aspecto | Detalle |
|---------|---------|
| Resiliencia | Lambda con retry automático, DLQ en SQS, Step Functions con manejo de errores |
| Escalabilidad | Serverless auto-escala. DynamoDB on-demand. Firehose auto-scaling |
| Seguridad | WAF + Cognito + IAM Roles (least privilege) + cifrado en tránsito y reposo |
| Costo | Pay-per-use. Sin servidores idle. BigQuery por consulta |
| Observabilidad | CloudWatch Logs + Metrics + X-Ray tracing |
| Compliance | Datos PII cifrados. Cognito MFA. Audit trail en CloudTrail |
| Disponibilidad | Multi-AZ automático (Lambda, DynamoDB, API Gateway) |
