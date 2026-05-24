---
title: "Roadmap Evolutivo"
section: "10"
---

# 10. Roadmap Evolutivo

## 10.1 Estrategia de Evolución

La solución se implementa de forma incremental en 3 releases, priorizando
la entrega de valor temprana y la reducción de riesgo técnico.

| Principio | Aplicación |
|-----------|-----------|
| Valor temprano | MVP entrega las capacidades core que resuelven los pain points principales |
| Riesgo técnico primero | Integraciones con legacy y cross-cloud se abordan en MVP |
| Feedback loop | Cada release incorpora aprendizajes del anterior |
| Backward compatible | Releases no rompen funcionalidad existente |

---

## 10.2 MVP (Release 1) — Fundación

### Objetivo
Reemplazar el sistema de campañas actual con una plataforma serverless funcional
que automatice el proceso end-to-end y entregue el dashboard de control.

### Alcance

| Capacidad | Descripción | Componentes AWS |
|-----------|-------------|-----------------|
| Motor de Reglas | Selección automatizada de público objetivo | Lambda + DynamoDB |
| Integración Core | Conexión con Core Bancario, CRM, Créditos vía ESB | Lambda (ESB Bridge) + VPN |
| Integración Centrales | Consulta a Datacrédito para scoring | Lambda + API externa |
| Simulación | Proyección de resultado antes de aprobar | Lambda + Step Functions |
| Gestión de Campañas | CRUD, ciclo de vida, aprobación | Lambda + DynamoDB + S3 |
| Notificación Multicanal | SMS + Email + Push | Lambda + SQS + Proveedor externo |
| Tracking básico | Registro de envíos y respuestas | Lambda + DynamoDB + EventBridge |
| Dashboard | Corte mensual, clientes notificados vs convertidos | Kinesis Firehose + BigQuery + Looker |
| Seguridad | WAF + Cognito + cifrado + auditoría | WAF, Cognito, KMS, CloudTrail |

### Criterios de Éxito MVP

| Criterio | Métrica |
|----------|---------|
| Automatización | 0 procesos manuales en flujo de campaña |
| Disponibilidad | >= 99.9% uptime |
| Performance | Simulación < 2s, ejecución 100K < 30 min |
| Cobertura | Integración con 3 fuentes internas + 1 externa |
| Dashboard | Operativo con corte mensual |

### Duración estimada: 3-4 meses

---

## 10.3 Release 2 — Scoring Alternativo y Fuentes Externas

### Objetivo
Mejorar la calidad del scoring para clientes sin historia crediticia amplia
mediante fuentes alternativas, y habilitar personalización de campañas.

### Alcance

| Capacidad | Descripción | Componentes |
|-----------|-------------|-------------|
| Scoring Alternativo ML | Modelo de ML para scoring con múltiples fuentes | Lambda + SageMaker endpoint |
| Integración Telecom | Datos de comportamiento con operadores | Lambda + API externa |
| Integración Otras Entidades | Productos financieros en otros bancos | Lambda + API externa |
| Personalización | Ofertas personalizadas por segmento | Lambda + reglas dinámicas |
| A/B Testing | Comparar efectividad de variantes de campaña | EventBridge + tracking |
| Dashboard avanzado | Análisis de efectividad por segmento, canal, producto | BigQuery + Looker |

### Criterios de Éxito R2

| Criterio | Métrica |
|----------|---------|
| Scoring | Modelo ML con accuracy > 75% |
| Fuentes | 5+ fuentes heterogéneas integradas |
| Conversión | Incremento >= 15% vs MVP |
| Personalización | >= 3 variantes por campaña |

### Duración estimada: 2-3 meses

---

## 10.4 Release 3 — Optimización y Autoservicio

### Objetivo
Maximizar la autonomía del área de campañas y optimizar automáticamente
las campañas basándose en datos históricos.

### Alcance

| Capacidad | Descripción | Componentes |
|-----------|-------------|-------------|
| Autoservicio de reglas | Analistas configuran reglas sin código (low-code) | Frontend + Lambda + DynamoDB |
| Optimización automática | Sistema sugiere mejores horarios, canales, segmentos | ML + BigQuery + Lambda |
| Predicción de conversión | Modelo predictivo de probabilidad de conversión | SageMaker + Lambda |
| Integración canales digitales | Campañas en app móvil y banca web del banco | API Gateway + SNS |
| Apetito de riesgo dinámico | Ajuste automático de criterios según comportamiento | Lambda + reglas + dashboard |
| Reportería regulatoria | Reportes automáticos para entes de control | BigQuery + Cloud Functions |

### Criterios de Éxito R3

| Criterio | Métrica |
|----------|---------|
| Autoservicio | Analistas crean campañas sin soporte de TI |
| Optimización | Incremento >= 10% conversión vs R2 |
| Predicción | Modelo predictivo con precision > 80% |
| Regulatorio | Reportes generados automáticamente |

### Duración estimada: 3-4 meses

---

## 10.5 Timeline Visual

```
2026 Q3          2026 Q4          2027 Q1          2027 Q2
|--- MVP --------|--- Release 2 ---|--- Release 3 ---|
|                |                  |                  |
| Core campañas  | Scoring ML      | Autoservicio     |
| Integraciones  | Fuentes externas| Optimización     |
| Dashboard      | A/B Testing     | Predicción       |
| Notificaciones | Personalización | Regulatorio      |
```

## 10.6 Dependencias entre Releases

| Release | Depende de | Riesgo |
|---------|-----------|--------|
| MVP | Acceso a ESB y sistemas legacy | Alto - requiere coordinación con equipo de infraestructura |
| MVP | Configuración cross-cloud AWS-GCP | Medio - requiere networking team |
| R2 | Acuerdos con Telecom y otras entidades | Alto - dependencia externa |
| R2 | Datos históricos suficientes para entrenar ML | Medio - MVP debe generar datos |
| R3 | Estabilidad de MVP y R2 | Bajo - evolución natural |

## 10.7 Gestión de Riesgos por Release

| Release | Riesgo | Probabilidad | Mitigación |
|---------|--------|:------------:|-----------|
| MVP | Integración ESB falla | Media | Adapter pattern, mock services, testing temprano |
| MVP | Latencia cross-cloud | Baja | Kinesis Firehose con buffer, async |
| R2 | Datos telecom insuficientes | Media | Scoring funciona sin esa fuente (graceful degradation) |
| R2 | Modelo ML con bajo accuracy | Media | Fallback a reglas del MVP |
| R3 | Adopción baja por analistas | Baja | UX research, capacitación, migración gradual |
