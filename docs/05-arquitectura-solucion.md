# Arquitectura de Solución TO-BE - Sistema de Campañas

## 1. Vista de Contexto y Capacidades de Negocio

### Descripción
Solución multinube para la gestión automatizada de campañas de crédito dirigidas a personas naturales (18-25 años), con capacidades de simulación, scoring, notificación multicanal y dashboard de control.

### Restricciones de Diseño
- No se proponen procesos manuales
- Historia crediticia del cliente no es amplia — se complementa con fuentes alternativas
- Notificación al cliente por SMS, correo electrónico y mensajes push
- Arquitectura multinube evolutiva (MVP + releases futuros)

### Reglas de Público Objetivo
- Historial crediticio y comportamiento de pago con centrales de riesgo
- Comportamiento de ingresos/egresos en cuentas del pasivo (3-5 años)
- Comportamiento de productos con telefónicas y otras entidades financieras

```mermaid
C4Context
    title Vista de Contexto - Sistema de Campañas TO-BE

    Person(analista, "Analista de Campañas", "Configura reglas, ejecuta simulaciones y monitorea efectividad")
    Person(gerente, "Gerente de Riesgo", "Evalúa apetito de riesgo y aprueba campañas")
    Person(cliente, "Cliente", "Persona natural 18-25 años, receptor de ofertas de crédito")

    Enterprise_Boundary(banco, "Banco") {
        System(campanias_new, "Plataforma de Campañas TO-BE", "Sistema automatizado de gestión de campañas con simulación, scoring alternativo y dashboard de control")
    }

    System_Ext(centrales, "Centrales de Riesgo", "Consulta de historial crediticio y comportamiento de pago")
    System_Ext(telcos, "Operadores Telecomunicaciones", "Datos de comportamiento de productos del cliente")
    System_Ext(otras_entidades, "Otras Entidades Financieras", "Información de productos financieros del cliente")
    System_Ext(notificador, "Proveedor de Notificaciones", "Envío masivo de SMS, email y push notifications")
    System_Ext(core, "Core Bancario (Host Transaccional)", "Movimientos de ahorro y crédito")
    System_Ext(crm, "CRM", "Información de clientes")
    System_Ext(creditos, "Sistema de Créditos", "Reglas y estado de créditos")

    Rel(analista, campanias_new, "Configura reglas y ejecuta simulaciones")
    Rel(gerente, campanias_new, "Aprueba campañas y revisa dashboard")
    Rel(campanias_new, centrales, "Consulta scoring y comportamiento de pago")
    Rel(campanias_new, telcos, "Consulta comportamiento telecom")
    Rel(campanias_new, otras_entidades, "Consulta productos financieros externos")
    Rel(campanias_new, notificador, "Envía campañas multicanal")
    Rel(campanias_new, core, "Consulta movimientos transaccionales")
    Rel(campanias_new, crm, "Consulta datos de clientes")
    Rel(campanias_new, creditos, "Consulta reglas de crédito")
    Rel(notificador, cliente, "SMS / Email / Push")
```

## 2. Vista de Arquitectura de Aplicación (Software)

### MVP (Release 1)
- Motor de reglas automatizado para selección de público objetivo
- Integración con centrales de riesgo
- Módulo de simulación de campañas
- Dashboard de control y seguimiento
- Notificación multicanal (SMS + Email + Push)
- Histórico de campañas

### Release 2 (Evolución)
- Integración con telecomunicaciones y otras entidades financieras
- Motor de Machine Learning para scoring alternativo
- Personalización avanzada de ofertas
- A/B testing de campañas

```mermaid
graph TB
    subgraph "Canales"
        WEB[Portal Web Analistas]
        DASH[Dashboard Gerencial]
    end

    subgraph "Capa de Experiencia / API Gateway"
        APIGW[API Gateway]
        AUTH[Servicio de Autenticación<br/>OAuth2 / OIDC]
    end

    subgraph "Servicios Core de Negocio"
        REGLAS[Motor de Reglas<br/>Selección de Público]
        SIMULACION[Servicio de Simulación<br/>Aprobación de Campañas]
        CAMPANIA_SVC[Servicio de Gestión<br/>de Campañas]
        SCORING[Servicio de Scoring<br/>Alternativo]
        TRACKING[Servicio de Tracking<br/>y Efectividad]
    end

    subgraph "Capa de Integración"
        ESB_NEW[Bus de Integración]
        EVENT_BUS[Event Bus<br/>Eventos Asíncronos]
        ETL[Pipeline de Datos<br/>Ingesta Automatizada]
    end

    subgraph "Sistemas Internos"
        CORE[Core Bancario]
        CRM_INT[CRM]
        CRED[Sistema de Créditos]
    end

    subgraph "Proveedores Externos"
        CENTRALES[Centrales de Riesgo]
        TELCOS[Telecomunicaciones]
        OTRAS_FIN[Otras Entidades Financieras]
        NOTIF[Proveedor Notificaciones<br/>SMS / Email / Push]
    end

    WEB --> APIGW
    DASH --> APIGW
    APIGW --> AUTH
    APIGW --> REGLAS
    APIGW --> SIMULACION
    APIGW --> CAMPANIA_SVC
    APIGW --> TRACKING

    REGLAS --> SCORING
    REGLAS --> ESB_NEW
    SIMULACION --> SCORING
    CAMPANIA_SVC --> EVENT_BUS
    CAMPANIA_SVC --> NOTIF
    TRACKING --> EVENT_BUS

    ESB_NEW --> CORE
    ESB_NEW --> CRM_INT
    ESB_NEW --> CRED
    ETL --> CENTRALES
    ETL --> TELCOS
    ETL --> OTRAS_FIN

    SCORING --> ETL
    EVENT_BUS --> TRACKING
```

## 3. Vista de Arquitectura de Infraestructura (Multinube)

```mermaid
graph TB
    subgraph "Zona Pública (Edge)"
        CDN[CDN / WAF]
        LB[Load Balancer]
    end

    subgraph "Zona de Aplicación (Nube Privada / Cloud)"
        subgraph "Compute"
            CONTAINERS[Contenedores<br/>Microservicios]
            SERVERLESS[Funciones Serverless<br/>Procesamiento Eventos]
        end
        subgraph "Integración"
            APIGW_INFRA[API Gateway Managed]
            MQ[Message Queue / Event Bus]
        end
    end

    subgraph "Zona de Datos (Nube Privada)"
        DB_OPS[BD Operacional<br/>Campañas + Histórico]
        DB_ANALYTICS[BD Analítica<br/>Dashboard + Reportes]
        CACHE[Cache Distribuido]
        STORAGE[Object Storage<br/>Archivos y Logs]
    end

    subgraph "Zona On-Premise (Legacy)"
        CORE_INFRA[Core Bancario]
        CRM_INFRA[CRM Siebel]
        CRED_INFRA[Sistema Créditos]
        ESB_IBM[ESB IBM IB]
    end

    subgraph "Proveedores Externos"
        RISK[Centrales de Riesgo]
        TELCO[Telecomunicaciones]
        NOTIF_INFRA[Proveedor Notificaciones]
    end

    subgraph "Observabilidad"
        MON[Monitoreo y Alertas]
        LOG[Logging Centralizado]
        TRACE[Tracing Distribuido]
    end

    CDN --> LB
    LB --> APIGW_INFRA
    APIGW_INFRA --> CONTAINERS
    CONTAINERS --> MQ
    CONTAINERS --> DB_OPS
    CONTAINERS --> CACHE
    MQ --> SERVERLESS
    SERVERLESS --> DB_ANALYTICS
    SERVERLESS --> STORAGE

    CONTAINERS --> ESB_IBM
    ESB_IBM --> CORE_INFRA
    ESB_IBM --> CRM_INFRA
    ESB_IBM --> CRED_INFRA

    CONTAINERS --> RISK
    CONTAINERS --> TELCO
    CONTAINERS --> NOTIF_INFRA

    CONTAINERS --> MON
    CONTAINERS --> LOG
    CONTAINERS --> TRACE
```

## 4. Vista de Arquitectura de Seguridad

```mermaid
graph TB
    subgraph "Identidad y Acceso"
        IAM[IAM / Identity Provider]
        MFA[Autenticación Multifactor]
        RBAC[Control de Acceso<br/>Basado en Roles]
        AD_INT[Integración Active Directory]
    end

    subgraph "Protección de Borde"
        WAF[Web Application Firewall]
        DDOS[Protección DDoS]
        APIGW_SEC[API Gateway<br/>Rate Limiting + Throttling]
        TLS[TLS 1.3 End-to-End]
    end

    subgraph "Controles de Aplicación"
        OAUTH[OAuth2 / OIDC<br/>Tokens JWT]
        ENCRYPT_TRANSIT[Cifrado en Tránsito]
        INPUT_VAL[Validación de Entrada]
        AUDIT_LOG[Auditoría de Acciones]
    end

    subgraph "Controles de Plataforma"
        NET_SEG[Segmentación de Red<br/>VPC / Subnets]
        SEC_GROUPS[Security Groups / NACLs]
        SECRETS[Gestión de Secretos<br/>Vault]
        PATCH[Gestión de Parches]
    end

    subgraph "Protección de Datos"
        ENCRYPT_REST[Cifrado en Reposo<br/>AES-256]
        MASK[Enmascaramiento de Datos<br/>PII / Datos Sensibles]
        BACKUP[Backup y Recuperación<br/>RPO/RTO definidos]
        DLP[Prevención de Fuga<br/>de Datos]
    end

    subgraph "Detección y Respuesta"
        SIEM[SIEM<br/>Correlación de Eventos]
        IDS[IDS/IPS<br/>Detección de Intrusos]
        INCIDENT[Plan de Respuesta<br/>a Incidentes]
        VULN[Escaneo de<br/>Vulnerabilidades]
    end

    IAM --> RBAC
    IAM --> MFA
    IAM --> AD_INT
    WAF --> APIGW_SEC
    APIGW_SEC --> OAUTH
    OAUTH --> ENCRYPT_TRANSIT
    NET_SEG --> SEC_GROUPS
    ENCRYPT_REST --> MASK
    SIEM --> IDS
    IDS --> INCIDENT
```

## 5. Vista de Datos

```mermaid
graph LR
    subgraph "Fuentes Operacionales"
        SRC_CORE[Core Bancario<br/>Movimientos 3-5 años]
        SRC_CRM[CRM<br/>Datos de Clientes]
        SRC_CRED[Sistema Créditos<br/>Reglas y Estado]
        SRC_RISK[Centrales de Riesgo<br/>Scoring]
        SRC_TELCO[Telecomunicaciones<br/>Comportamiento]
    end

    subgraph "Ingesta y Procesamiento"
        ETL_PIPE[Pipeline ETL<br/>Ingesta Automatizada]
        STREAM[Event Streaming<br/>Eventos en Tiempo Real]
        QUALITY[Data Quality<br/>Validación y Limpieza]
    end

    subgraph "Almacenamiento"
        DB_CAMP[BD Campañas<br/>Gestión y Reglas]
        DB_HIST[BD Histórico<br/>Campañas Ejecutadas]
        DB_TRACK[BD Tracking<br/>Respuestas y Conversiones]
        DW[Data Warehouse<br/>Analítica y Reportes]
    end

    subgraph "Consumo"
        DASH_DATA[Dashboard<br/>Corte Mensual]
        REPORT[Reportes<br/>Apetito de Riesgo]
        ML[Modelos ML<br/>Scoring Alternativo]
    end

    subgraph "Gobernanza"
        CATALOG[Catálogo de Datos]
        LINEAGE[Linaje de Datos]
        RETENTION[Retención<br/>Políticas 5 años]
        PII_GOV[Gobierno PII<br/>Habeas Data]
    end

    SRC_CORE --> ETL_PIPE
    SRC_CRM --> ETL_PIPE
    SRC_CRED --> ETL_PIPE
    SRC_RISK --> ETL_PIPE
    SRC_TELCO --> ETL_PIPE

    ETL_PIPE --> QUALITY
    QUALITY --> DB_CAMP
    QUALITY --> DW
    STREAM --> DB_TRACK
    DB_CAMP --> DB_HIST

    DW --> DASH_DATA
    DW --> REPORT
    DW --> ML
    DB_TRACK --> DASH_DATA

    CATALOG --> LINEAGE
    LINEAGE --> RETENTION
```

## Roadmap de Evolución

| Release | Alcance | Capacidades |
|---------|---------|-------------|
| **MVP (R1)** | Core de campañas automatizado | Motor de reglas, integración core bancario + CRM + créditos + centrales de riesgo, simulación de campañas, dashboard de control, notificación SMS/Email/Push, histórico de campañas |
| **Release 2** | Scoring alternativo y fuentes externas | Integración telecomunicaciones y otras entidades financieras, motor ML para scoring alternativo, personalización de ofertas, A/B testing |
| **Release 3** | Optimización y autoservicio | Autoservicio para analistas (reglas sin código), optimización automática de campañas, predicción de conversión, integración con canales digitales del banco |

## Decisiones Arquitectónicas Base

| Aspecto | Decisión |
|---------|----------|
| Estilo de servicio | Microservicios en contenedores con funciones serverless para procesamiento de eventos |
| Integración síncrona | API REST vía API Gateway para servicios internos |
| Integración asíncrona | Event Bus para tracking, notificaciones y procesamiento batch |
| Integración legacy | ESB IBM Integration Bus como puente hacia core bancario, CRM y créditos |
| Consistencia | Eventual consistency para tracking y analítica; strong consistency para reglas y aprobación |
| Disponibilidad | Alta disponibilidad en zona de aplicación (multi-AZ); RPO < 1h, RTO < 4h |
| Compliance | Habeas Data, regulación bancaria local, cifrado de PII |
| Multinube | Capa de aplicación cloud-agnostic (contenedores); datos sensibles en nube privada |

## Sobre Mensajes Push

Los mensajes push son notificaciones enviadas directamente al dispositivo móvil del cliente a través de la app del banco (si existe) o servicios como Firebase Cloud Messaging / Apple Push Notifications. **Generan valor** porque:
- Tasa de apertura ~90% vs ~20% del email
- Entrega inmediata sin costo por mensaje (a diferencia de SMS)
- Permiten deep linking a la solicitud de crédito en la app
- Se incluyen en la propuesta como canal adicional del MVP
