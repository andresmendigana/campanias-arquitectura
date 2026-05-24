---
title: "Supuestos y Justificaciones"
section: "Anexo B"
---

# Anexo B - Supuestos y Justificaciones

## Supuestos Generales

| # | Supuesto | Justificación |
|---|----------|---------------|
| S1 | La organización es un banco comercial colombiano | Contexto regulatorio (SFC, Habeas Data) y productos (microcrédito, libre destino, rotativo) |
| S2 | El CRM es Siebel | Producto enterprise común en banca colombiana. No expone servicios web |
| S3 | El Core Bancario es un sistema mainframe/AS400 | Estándar en banca tradicional para host transaccional |
| S4 | El ESB es IBM Integration Bus | Mencionado en el contexto AS-IS |
| S5 | La autenticación corporativa es Active Directory | Estándar en organizaciones bancarias |
| S6 | El proveedor de notificaciones es un tercero genérico | No se especificó proveedor. Puede ser Infobip, Twilio u otro |
| S7 | PSE es el mecanismo de pago interbancario | Estándar en Colombia para pagos desde otros bancos (ACH Colombia) |

## Supuestos Técnicos

| # | Supuesto | Justificación |
|---|----------|---------------|
| S8 | AWS como cloud principal para compute | Re-platform del aplicativo de campañas. Ecosistema serverless maduro |
| S9 | GCP para analítica y dashboards | Data Lake (ya existe parcialmente) + BigQuery + Looker + NEW APP Campañas (SaaS). No es greenfield: ya hay proceso de replicación e ingesta |
| S10 | Arquitectura serverless | Elimina gestión de infraestructura, pay-per-use, auto-scaling |
| S11 | Conectividad AWS-GCP vía Private Connect | Datos financieros no deben transitar por internet público |
| S12 | VPN Site-to-Site para conectividad on-premise | Sistemas legacy no están en cloud |
| S13 | DynamoDB para datos operacionales | Serverless, alta disponibilidad, baja latencia, schema flexible |
| S14 | Kinesis Firehose para streaming cross-cloud | Servicio managed para envío confiable de datos a GCP |
| S15 | DECEVAL para pagarés desmaterializados | Reemplaza documentos físicos del AS-IS. API de tercero vía Internet |
| S16 | MFT existente para intercambio de archivos | Se mantiene para conciliación y archivos cifrados vía SFTP |

## Supuestos de Negocio

| # | Supuesto | Justificación |
|---|----------|---------------|
| S15 | Volumen de campañas: ~100K clientes por campaña | Orden de magnitud para banco mediano-grande en Colombia |
| S16 | Frecuencia: campañas semanales/quincenales | Basado en prácticas del sector |
| S17 | Corte de dashboard: mensual | Especificado en el requerimiento |
| S18 | Evaluación de apetito de riesgo: semestral | Especificado en el requerimiento |
| S19 | El banco tiene app móvil | Necesario para push notifications |
| S20 | Público objetivo 18-25 años usa predominantemente móvil | Demografía digital nativa |

## Supuestos de Integración

| # | Supuesto | Justificación |
|---|----------|---------------|
| S21 | Centrales de riesgo exponen API REST | Estándar actual de Datacrédito/TransUnion |
| S22 | Operadores telecom tienen APIs de consulta | Supuesto para R2, requiere acuerdo comercial |
| S23 | Otras entidades financieras comparten datos vía bureau | Modelo de bureaus de crédito en Colombia |
| S24 | El ESB IBM IB se mantiene como puente a legacy | No se reemplaza en MVP, se adapta |
