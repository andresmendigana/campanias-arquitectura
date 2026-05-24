---
title: "Requerimientos No Funcionales"
section: "11"
---

# 11. Requerimientos No Funcionales

## 11.1 Matriz de RNFs

| ID | Atributo | Requerimiento | Métrica | Prioridad |
|----|----------|---------------|---------|-----------|
| RNF-01 | Disponibilidad | El sistema debe estar disponible 99.9% del tiempo | Uptime mensual >= 99.9% (max 43 min downtime/mes) | Alta |
| RNF-02 | Tolerancia a fallos | Recuperación automática ante fallo de componente | Failover automático < 30 segundos | Alta |
| RNF-03 | Performance | Tiempo de respuesta para operaciones de consulta | P95 < 2 segundos para APIs síncronas | Alta |
| RNF-04 | Performance (Batch) | Procesamiento de campañas masivas | Procesar 100K notificaciones en < 30 minutos | Alta |
| RNF-05 | Cifrado en tránsito | Todas las comunicaciones cifradas | TLS 1.3 en todas las conexiones | Alta |
| RNF-06 | Cifrado en reposo | Datos sensibles cifrados en almacenamiento | AES-256 para datos PII y financieros | Alta |
| RNF-07 | Escalabilidad | Soportar crecimiento de base de clientes | Auto-scaling horizontal sin intervención manual | Media |
| RNF-08 | Mantenibilidad | Despliegue independiente de servicios | Deploy de un servicio sin afectar otros | Alta |
| RNF-09 | Auditabilidad | Registro de todas las acciones del sistema | Logs inmutables con retención 5 años | Alta |
| RNF-10 | Recuperabilidad | Recuperación ante desastre | RPO < 1 hora, RTO < 4 horas | Alta |

## 11.2 Disponibilidad

### Estrategia
- Arquitectura serverless (Lambda, API Gateway) con alta disponibilidad nativa multi-AZ
- DynamoDB con replicación automática
- Sin single points of failure

### Escenario
| Aspecto | Detalle |
|---------|---------|
| Fuente | Fallo de una zona de disponibilidad |
| Estímulo | AZ completa no disponible |
| Respuesta | Tráfico se redirige automáticamente a AZ saludable |
| Medida | Tiempo de failover < 30 segundos. Sin pérdida de datos |

## 11.3 Tolerancia a Fallos

### Estrategia
- Circuit breaker en integraciones con sistemas legacy y externos
- Dead Letter Queues (DLQ) para mensajes fallidos
- Retry con backoff exponencial
- Step Functions con manejo de errores y compensación

### Escenario
| Aspecto | Detalle |
|---------|---------|
| Fuente | Fallo en consulta a Centrales de Riesgo |
| Estímulo | Timeout o error 5xx del proveedor externo |
| Respuesta | Circuit breaker se activa, se usa cache de último scoring conocido |
| Medida | Campaña continúa con datos parciales. Alerta generada. Retry en 5 min |

## 11.4 Performance

### Estrategia
- Serverless auto-scaling (Lambda concurrency)
- Cache en Redis/DynamoDB DAX para consultas frecuentes
- Procesamiento asíncrono para operaciones batch
- Event-driven para desacoplar latencia

### Escenarios

| Operación | Tipo | SLA |
|-----------|------|-----|
| Consulta de campaña | Síncrona | P95 < 500ms |
| Simulación de campaña | Síncrona | P95 < 2s |
| Ejecución de campaña (100K clientes) | Asíncrona/Batch | < 30 min |
| Consulta de dashboard | Síncrona | P95 < 3s |
| Scoring de cliente individual | Síncrona | P95 < 1s |

## 11.5 Seguridad - Cifrado

### Cifrado en Tránsito
| Comunicación | Protocolo | Detalle |
|-------------|-----------|---------|
| Cliente → CloudFront | TLS 1.3 | Certificado ACM |
| CloudFront → API Gateway | TLS 1.3 | Internal AWS |
| API Gateway → Lambda | TLS 1.3 | Internal AWS |
| Lambda → DynamoDB | TLS 1.3 | VPC Endpoint |
| Lambda → Sistemas Legacy (ESB) | mTLS | Certificados mutuos |
| AWS → GCP (Kinesis → Dataflow) | TLS 1.3 | Cross-cloud encrypted |
| Lambda → Proveedores Externos | TLS 1.2+ | APIs externas |

### Cifrado en Reposo
| Store | Algoritmo | Gestión de Llaves |
|-------|-----------|-------------------|
| DynamoDB | AES-256 | AWS KMS (CMK) |
| S3 | AES-256 | AWS KMS (CMK) |
| BigQuery (GCP) | AES-256 | Google Cloud KMS |
| Kinesis Firehose | AES-256 | AWS KMS |

### Comunicación entre Nubes (AWS ↔ GCP)
| Aspecto | Implementación |
|---------|---------------|
| Transporte | TLS 1.3 end-to-end |
| Autenticación | Service accounts con tokens de corta duración |
| Autorización | IAM roles (AWS) + Service Account (GCP) con least privilege |
| Red | No se expone a internet público. Usar Private Connect o VPN site-to-site |
| Datos en tránsito | Cifrado adicional a nivel de aplicación para PII |

## 11.6 Escalabilidad

### Estrategia
| Componente | Mecanismo |
|-----------|-----------|
| Lambda | Concurrency auto-scaling (hasta 1000 concurrent por defecto) |
| API Gateway | Auto-scaling nativo (10K req/s por defecto) |
| DynamoDB | On-demand capacity (auto-scaling) |
| SQS | Ilimitado (auto-scaling nativo) |
| Kinesis Firehose | Auto-scaling de throughput |
| BigQuery | Serverless, escala automáticamente |

## 11.7 Mantenibilidad

### Estrategia
- Microservicios independientes (una Lambda por función de negocio)
- CI/CD por servicio (deploy independiente)
- Infrastructure as Code (CloudFormation / Terraform)
- Versionado de APIs (v1, v2)
- Feature flags para releases graduales

## 11.8 Auditabilidad y Compliance

### Estrategia
| Control | Implementación |
|---------|---------------|
| Audit trail | CloudTrail (AWS) + Audit Logs (GCP) |
| Logs de aplicación | CloudWatch Logs con retención 5 años |
| Acceso a datos PII | Logging de acceso con identidad del usuario |
| Regulación Habeas Data | Enmascaramiento de PII en logs, derecho al olvido |
| Trazabilidad de campañas | Event sourcing en tracking, inmutable |

## 11.9 Recuperabilidad (DR)

| Métrica | Valor | Estrategia |
|---------|-------|-----------|
| RPO (Recovery Point Objective) | < 1 hora | DynamoDB PITR, S3 versioning, BigQuery snapshots |
| RTO (Recovery Time Objective) | < 4 horas | Serverless (sin infraestructura que levantar), IaC para recrear |
| Backup | Diario | DynamoDB backup automático, S3 lifecycle, BigQuery export |
| DR Region | Región secundaria AWS | Replicación cross-region para DynamoDB Global Tables |

## 11.10 Matriz de Trazabilidad RNF → Componente

| RNF | Lambda | API GW | DynamoDB | S3 | Kinesis | BigQuery | EventBridge |
|-----|:------:|:------:|:--------:|:--:|:-------:|:--------:|:-----------:|
| Disponibilidad | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| Tolerancia fallos | ✓ | - | ✓ | - | ✓ | - | ✓ |
| Performance | ✓ | ✓ | ✓ | - | - | ✓ | - |
| Cifrado tránsito | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| Cifrado reposo | - | - | ✓ | ✓ | ✓ | ✓ | - |
| Escalabilidad | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| Auditabilidad | ✓ | ✓ | ✓ | ✓ | - | ✓ | ✓ |
