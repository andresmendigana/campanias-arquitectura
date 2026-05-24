# Priorización de Atributos de Calidad y Decisiones Arquitectónicas

## Sistema de Campañas TO-BE - Banco

---

## 1. Contexto de Negocio

El banco requiere una plataforma multinube para gestionar campañas de crédito
(microcréditos, libre destino, crédito rotativo) dirigidas a personas naturales
con el objetivo de incrementar la colocación y reducir
pérdidas por descompensación contable.

## 2. Drivers de Negocio

| # | Driver | Descripción |
|---|--------|-------------|
| D1 | Incrementar colocación de créditos | Aumentar la base de clientes jóvenes con productos crediticios |
| D2 | Reducir pérdidas contables | Minimizar descompensación mediante mejor scoring |
| D3 | Automatizar procesos | Eliminar procesos manuales de limpieza y distribución |
| D4 | Control y seguimiento | Dashboard mensual para evaluar apetito de riesgo semestral |
| D5 | Evolución tecnológica | Reemplazar sistema fuera de soporte por plataforma moderna |

## 3. Atributos de Calidad Priorizados

### Matriz de Priorización

| Prioridad | Atributo | Peso | Justificación |
|-----------|----------|------|---------------|
| 1 | **Seguridad** | Alta | Datos financieros y PII. Regulación bancaria. Habeas Data. |
| 2 | **Confiabilidad** | Alta | Campañas incorrectas generan riesgo crediticio y pérdidas |
| 3 | **Mantenibilidad** | Alta | Sistema actual fuera de soporte. Evolución MVP → releases |
| 4 | **Interoperabilidad** | Alta | Múltiples fuentes (core, CRM, centrales, telecom) |
| 5 | **Rendimiento** | Media-Alta | Procesamiento batch de campañas masivas |
| 6 | **Escalabilidad** | Media | Crecimiento gradual de base de clientes jóvenes |
| 7 | **Disponibilidad** | Media | No es tiempo real; batch con ventanas definidas |
| 8 | **Usabilidad** | Media | Analistas necesitan autonomía sin procesos manuales |
| 9 | **Portabilidad** | Media-Baja | Multinube pero no requiere migración frecuente |

### Escenarios de Calidad

#### Seguridad (Prioridad 1)
| Aspecto | Escenario |
|---------|-----------|
| Estímulo | Un usuario no autorizado intenta acceder a datos de clientes |
| Respuesta | El sistema bloquea el acceso, registra el intento en auditoría |
| Medida | 100% de accesos autenticados vía MFA + RBAC. Cifrado AES-256 en reposo |

#### Confiabilidad (Prioridad 2)
| Aspecto | Escenario |
|---------|-----------|
| Estímulo | Se ejecuta una campaña con reglas de scoring |
| Respuesta | El sistema aplica todas las reglas sin omitir validaciones |
| Medida | 0% de clientes incluidos que no cumplen criterios. Trazabilidad completa |

#### Mantenibilidad (Prioridad 3)
| Aspecto | Escenario |
|---------|-----------|
| Estímulo | Se requiere agregar una nueva fuente de datos (telecom) |
| Respuesta | Se integra sin modificar servicios existentes |
| Medida | Nueva integración en < 2 sprints. Despliegue independiente por servicio |

#### Interoperabilidad (Prioridad 4)
| Aspecto | Escenario |
|---------|-----------|
| Estímulo | Se necesita consultar centrales de riesgo + core bancario |
| Respuesta | Pipeline ETL automatizado ingesta datos sin intervención manual |
| Medida | Integración con 5+ fuentes heterogéneas. Sin archivos manuales |

## 4. Trade-offs y Decisiones Arquitectónicas

### ADR-001: Microservicios sobre Monolito

| Aspecto | Decisión |
|---------|----------|
| Contexto | Sistema actual es monolítico, fuera de soporte, sin capacidad de evolución |
| Decisión | Arquitectura de microservicios en contenedores |
| Razón | Favorece mantenibilidad (despliegue independiente), escalabilidad selectiva y evolución incremental (MVP → releases) |
| Trade-off | Mayor complejidad operativa vs. monolito. Se mitiga con observabilidad |
| Atributos favorecidos | Mantenibilidad, Escalabilidad, Portabilidad |
| Atributos afectados | Complejidad operativa (mitigada con observabilidad) |

### ADR-002: Event Bus para Procesamiento Asíncrono

| Aspecto | Decisión |
|---------|----------|
| Contexto | Campañas son procesos batch; tracking de efectividad es eventual |
| Decisión | Event Bus para comunicación asíncrona entre servicios |
| Razón | Desacopla servicios, permite procesamiento paralelo, mejora resiliencia |
| Trade-off | Consistencia eventual vs. inmediata para tracking |
| Atributos favorecidos | Rendimiento, Confiabilidad, Escalabilidad |
| Atributos afectados | Consistencia (aceptable para tracking, no para reglas) |

### ADR-003: Pipeline ETL Automatizado sobre Consultas SQL Directas

| Aspecto | Decisión |
|---------|----------|
| Contexto | Sistema actual usa SQL directo a BDs de otros sistemas (acoplamiento) |
| Decisión | Pipeline ETL automatizado con validación de calidad de datos |
| Razón | Elimina procesos manuales, garantiza calidad, desacopla fuentes |
| Trade-off | Latencia de datos (minutos) vs. tiempo real |
| Atributos favorecidos | Interoperabilidad, Confiabilidad, Mantenibilidad |
| Atributos afectados | Latencia (aceptable para campañas batch) |

### ADR-004: Scoring Alternativo con Fuentes Externas

| Aspecto | Decisión |
|---------|----------|
| Contexto | Clientes no tienen historia crediticia amplia |
| Decisión | Scoring alternativo usando centrales de riesgo + telecom + otras entidades |
| Razón | Complementa historia crediticia limitada con comportamiento financiero alternativo |
| Trade-off | Costo de consultas externas vs. mejor calidad de scoring |
| Atributos favorecidos | Confiabilidad (mejor scoring = menos pérdidas) |
| Atributos afectados | Costo operativo (justificado por reducción de pérdidas) |

### ADR-005: Multinube con Datos Sensibles en Nube Privada

| Aspecto | Decisión |
|---------|----------|
| Contexto | Regulación bancaria exige control sobre datos financieros y PII |
| Decisión | Capa de aplicación cloud-agnostic (contenedores); datos en nube privada |
| Razón | Cumplimiento regulatorio sin sacrificar modernización |
| Trade-off | Complejidad de red híbrida vs. todo en cloud público |
| Atributos favorecidos | Seguridad, Portabilidad |
| Atributos afectados | Complejidad de infraestructura (mitigada con IaC) |

### ADR-006: Dashboard con Corte Mensual y Registro de Control

| Aspecto | Decisión |
|---------|----------|
| Contexto | Se necesita evaluar apetito de riesgo semestral y evitar re-contacto |
| Decisión | BD analítica separada + dashboard con tracking de conversión |
| Razón | Permite medir efectividad, excluir clientes que ya solicitaron productos |
| Trade-off | Almacenamiento adicional vs. capacidad analítica |
| Atributos favorecidos | Usabilidad, Confiabilidad |
| Atributos afectados | Costo de almacenamiento (marginal) |

### ADR-007: Notificación Multicanal (SMS + Email + Push)

| Aspecto | Decisión |
|---------|----------|
| Contexto | Público joven (18-25) usa predominantemente móvil |
| Decisión | Incluir push notifications además de SMS y email |
| Razón | Push tiene ~90% tasa apertura vs ~20% email. Sin costo por mensaje. Deep linking a app |
| Trade-off | Requiere que el cliente tenga la app del banco instalada |
| Atributos favorecidos | Usabilidad, Rendimiento (mejor conversión) |
| Atributos afectados | Cobertura (solo clientes con app; SMS/email como fallback) |

## 5. Matriz de Impacto: Decisiones vs Atributos

| Decisión | Seguridad | Confiabilidad | Mantenibilidad | Interoperabilidad | Rendimiento | Escalabilidad |
|----------|:---------:|:-------------:|:--------------:|:-----------------:|:-----------:|:-------------:|
| ADR-001 Microservicios | ○ | ○ | ↑↑ | ↑ | ○ | ↑↑ |
| ADR-002 Event Bus | ○ | ↑ | ↑ | ○ | ↑↑ | ↑ |
| ADR-003 ETL Automatizado | ○ | ↑↑ | ↑↑ | ↑↑ | ○ | ○ |
| ADR-004 Scoring Alternativo | ○ | ↑↑ | ○ | ↑ | ○ | ○ |
| ADR-005 Multinube Híbrida | ↑↑ | ○ | ○ | ○ | ○ | ↑ |
| ADR-006 Dashboard Control | ○ | ↑ | ○ | ○ | ○ | ○ |
| ADR-007 Multicanal + Push | ○ | ○ | ○ | ↑ | ↑ | ○ |

*↑↑ = Impacto positivo alto | ↑ = Impacto positivo | ○ = Neutro*

## 6. Riesgos y Mitigaciones

| Riesgo | Probabilidad | Impacto | Mitigación |
|--------|:------------:|:-------:|------------|
| Integración con sistemas legacy falla | Media | Alto | ESB como mediador; circuit breaker; retry policies |
| Datos de centrales de riesgo incompletos | Media | Medio | Scoring con múltiples fuentes; fallback a reglas básicas |
| Adopción lenta por analistas | Baja | Medio | UX intuitiva; capacitación; migración gradual |
| Incumplimiento regulatorio | Baja | Alto | Cifrado, auditoría, enmascaramiento PII desde MVP |
| Sobrecosto de consultas externas | Media | Bajo | Cache de consultas; batch optimizado; monitoreo de costos |

## 7. Conclusión

La priorización coloca **Seguridad** y **Confiabilidad** como atributos dominantes
dado el contexto regulatorio bancario y el riesgo crediticio del público objetivo.
**Mantenibilidad** e **Interoperabilidad** son críticos para la evolución incremental
y la integración con múltiples fuentes heterogéneas. Las decisiones arquitectónicas
están alineadas para resolver los pain points del AS-IS mientras habilitan la
evolución planificada en el roadmap MVP → Release 2 → Release 3.
