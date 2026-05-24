---
title: "Propuesta de Arquitectura Evolutiva - Sistema de Campañas y Créditos"
author: "Equipo de Arquitectura"
date: "2026-05-21"
version: "1.0"
client: "Banco"
classification: "Confidencial"
---

# Propuesta de Arquitectura Evolutiva

## Sistema de Campañas y Créditos - MVP y Releases Futuros

---

## Control de Versiones

| Versión | Fecha | Autor | Descripción |
|---------|-------|-------|-------------|
| 1.0 | 2026-05-21 | Equipo de Arquitectura | Versión inicial - Propuesta MVP |
| 2.0 | 2026-05-21 | Equipo de Arquitectura | Incorpora catálogo TO-BE (PSE, Data Lake, NEW APP Campañas, DECEVAL), catálogo AS-IS créditos (BPM, Gestor Documental, MFT, Datacrédito), proceso transaccional AS-IS, y ajustes de seguridad |

---

## Tabla de Contenido

| # | Documento | Descripción |
|---|-----------|-------------|
| 01 | [Contexto del Problema](01-contexto-problema.md) | Análisis del problema, drivers de negocio, restricciones |
| 02 | [Arquitectura AS-IS](02-arquitectura-as-is.md) | Estado actual del sistema, catálogo de aplicaciones |
| 03 | [Atributos de Calidad](03-atributos-calidad.md) | Priorización de atributos y escenarios de calidad |
| 04 | [Decisiones Arquitectónicas](04-decisiones-arquitectonicas.md) | ADRs y trade-offs |
| 05 | [Arquitectura de Solución](05-arquitectura-solucion.md) | Vista de contexto TO-BE y evolución |
| 06 | [Arquitectura de Software](06-arquitectura-software.md) | Microservicios, APIs, componentes |
| 07 | [Arquitectura de Seguridad](07-arquitectura-seguridad.md) | Protocolos, capas, comunicación entre nubes |
| 08 | [Arquitectura de Datos](08-arquitectura-datos.md) | Stores, streaming, analítica, gobernanza |
| 09 | [Arquitectura de Infraestructura](09-arquitectura-infraestructura.md) | Multinube serverless AWS + GCP |
| 10 | [Roadmap Evolutivo](10-roadmap-evolutivo.md) | MVP, Release 2, Release 3 |
| 11 | [Requerimientos No Funcionales](11-requerimientos-no-funcionales.md) | Disponibilidad, performance, cifrado |

## Anexos

| # | Documento | Descripción |
|---|-----------|-------------|
| A | [Glosario](anexos/A-glosario.md) | Términos del dominio bancario |
| B | [Supuestos](anexos/B-supuestos.md) | Supuestos y justificaciones |
| C | [Referencias](anexos/C-referencias.md) | Referencias técnicas |

## Diagramas

| Código | Vista | Formato |
|--------|-------|---------|
| CAM-ASIS-01 | Contexto AS-IS Campañas | PNG, DrawIO |
| CAM-TOBE-01 | Contexto TO-BE Campañas | PNG, DrawIO |
| CAM-TOBE-02 | Aplicación TO-BE | PNG, DrawIO |
| CAM-TOBE-03 | Infraestructura TO-BE | PNG, DrawIO |
| CAM-TOBE-04 | Seguridad TO-BE | PNG, DrawIO |
| CAM-TOBE-05 | Software TO-BE | PNG, DrawIO |
| CAM-TOBE-06 | Serverless AWS+GCP | PNG, DrawIO |
| CRE-ASIS-01 | Contexto AS-IS Créditos | PNG |
| CRE-TOBE-01 | Contexto TO-BE Créditos (PSE) | PNG, DrawIO |
