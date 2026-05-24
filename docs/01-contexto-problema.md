---
title: "Contexto del Problema"
section: "01"
---

# 1. Contexto del Problema

## 1.1 Descripción General

Se requiere diseñar la arquitectura evolutiva de una solución multinube que permita
incrementar la colocación de créditos (microcréditos, libre destino y crédito rotativo)
para persona natural en rango de edad de 18 a 25 años, así como el uso de los productos
y la reducción de pérdida de dinero por descompensación contable.

## 1.2 Drivers de Negocio

| # | Driver | Descripción | Métrica de Éxito |
|---|--------|-------------|------------------|
| D1 | Incrementar colocación | Aumentar base de clientes jóvenes con productos crediticios | % incremento colocación semestral |
| D2 | Reducir pérdidas | Minimizar descompensación contable mediante mejor scoring | % reducción pérdidas vs semestre anterior |
| D3 | Automatizar procesos | Eliminar procesos manuales de limpieza y distribución | 0 procesos manuales en flujo de campañas |
| D4 | Control y seguimiento | Dashboard mensual para evaluar apetito de riesgo semestral | Dashboard operativo con corte mensual |
| D5 | Evolución tecnológica | Reemplazar sistema fuera de soporte | Sistema nuevo en producción |

## 1.3 Problemas del Sistema Actual

| # | Problema | Impacto | Categoría |
|---|----------|---------|-----------|
| P1 | Aplicación desactualizada y fuera de soporte | Riesgo operativo, sin parches de seguridad | Tecnológico |
| P2 | Procesos manuales de limpieza de datos | Errores humanos, tiempos altos, dependencia de personas | Operativo |
| P3 | Limitantes de conexión a fuentes de información | Datos incompletos, campañas menos efectivas | Integración |
| P4 | Falta de licenciamiento para todo el personal | Cuellos de botella, dependencia de personas específicas | Licenciamiento |
| P5 | Distribución compleja por producto | Dificultad para segmentar y personalizar | Funcional |
| P6 | Seguimiento y análisis de efectividad limitado | No se mide ROI ni se ajustan estrategias | Analítica |
| P7 | Sin histórico de campañas | No hay trazabilidad ni aprendizaje | Datos |

## 1.4 Restricciones de Diseño

| # | Restricción | Justificación |
|---|-------------|---------------|
| R1 | No proponer soluciones con procesos manuales | Requisito explícito del negocio |
| R2 | Historia crediticia del cliente no es amplia | Público objetivo 18-25 años, requiere scoring alternativo |
| R3 | Notificación por SMS, correo y push | Canales definidos por el negocio |
| R4 | Arquitectura multinube | Requisito de resiliencia y mejores servicios por cloud |
| R5 | Solución evolutiva (MVP + releases) | Entrega incremental de valor |

## 1.5 Reglas de Negocio - Público Objetivo de Campañas

| # | Regla | Fuente de Datos |
|---|-------|-----------------|
| RN1 | Revisar historial crediticio y comportamiento de pago | Centrales de Riesgo (Datacrédito) |
| RN2 | Comportamiento de ingresos/egresos en cuentas del pasivo (3-5 años) | Core Bancario |
| RN3 | Analizar comportamiento de productos con telefónicas y otras entidades | Telecomunicaciones, Otras Entidades Financieras |
| RN4 | Excluir clientes que ya solicitaron productos del banco | Sistema de Tracking interno |

## 1.6 Características Requeridas - Sistema de Campañas

| # | Característica | Descripción |
|---|---------------|-------------|
| C1 | Simulación de campañas | Permitir simular resultado antes de aprobar |
| C2 | Dashboard de control | Registro de clientes notificados vs. convertidos |
| C3 | Exclusión automática | No incluir en siguiente campaña a quienes ya solicitaron |
| C4 | Scoring alternativo | Evaluar clientes sin historia crediticia amplia |
| C5 | Notificación multicanal | SMS + Email + Push notifications |
| C6 | Histórico de campañas | Trazabilidad completa de campañas ejecutadas |

## 1.7 Características Requeridas - Sistema de Créditos

| # | Característica | Descripción |
|---|---------------|-------------|
| CC1 | Radicación multicanal | Oficinas + app móvil + sitio web |
| CC2 | Validación biométrica | Mitigar suplantación de identidad |
| CC3 | Firma digital de pagaré | A través de DECEVAL (pagarés desmaterializados) |
| CC4 | Pago desde otros bancos | Abono a créditos vía PSE (API de ATH) desde cuentas externas |

## 1.8 Catálogo de Aplicaciones TO-BE

| Aplicación | Descripción | Despliegue | Restricción Técnica |
|-----------|-------------|-----------|---------------------|
| PSE | API de ATH para pagos desde otras entidades financieras | Internet | Cumplir protocolos de seguridad y ciberseguridad según normativas vigentes |
| Data Lake | Patrón de arquitectura basado en espacios y acceso directo, almacenamiento de grandes volúmenes | Nube Pública GCP | No todos los datos requeridos se replican aún. Existe proceso de replicación, ingesta y calidad |
| NEW APP Campañas | Servicio SaaS conectado al Data Lake para modelos de analítica avanzada | Nube Pública GCP | — |
| DECEVAL | API de tercero para el proceso de pagarés desmaterializados | Internet | — |

## 1.9 Catálogo de Aplicaciones AS-IS - Créditos

| Aplicación | Descripción | Despliegue | Restricción Técnica |
|-----------|-------------|-----------|---------------------|
| BPM | Administración de procesos y automatización de flujos de solicitudes de créditos | Nube Privada | Personas de desarrollo limitadas |
| Gestor Documental | Almacenamiento de documentación de soporte de solicitudes de crédito | Nube Privada | — |
| MFT | Managed File Transfer - Intercambio seguro de archivos | Nube Privada | Información cifrada vía protocolo SFTP |
| Datacrédito | Central de riesgo para persona natural, expone servicio para consultar historial crediticio | Internet | — |

## 1.8 Requerimientos No Funcionales (Resumen)

| # | RNF | Descripción |
|---|-----|-------------|
| RNF1 | Alta disponibilidad | Sistema disponible 99.9% del tiempo |
| RNF2 | Tolerancia a fallos | Recuperación automática ante fallos |
| RNF3 | Performance | Prioridad alta por ser transacciones monetarias |
| RNF4 | Cifrado | Todas las transacciones viajan cifradas |
| RNF5 | Seguridad multinube | Protocolos y capas de seguridad entre nubes y sistemas |

## 1.9 Entregables Esperados

- Vista de arquitectura de solución (contexto, evolución MVP y releases)
- Vista de arquitectura de software de las aplicaciones
- Vista de arquitectura de seguridad de todo el contexto
- Priorización de atributos de calidad y decisiones tomadas
- Roadmap evolutivo (MVP → Release 2 → Release 3)
