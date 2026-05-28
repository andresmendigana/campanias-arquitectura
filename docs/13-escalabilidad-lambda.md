---
title: "Escalabilidad de AWS Lambda"
section: "13"
---

# 13. Escalabilidad de AWS Lambda

## Como escala Lambda

Lambda escala automaticamente sin configuracion. Cuando llegan multiples requests simultaneos, AWS crea instancias adicionales de la funcion en paralelo:

- 1 request = 1 instancia de Lambda
- 10 requests simultaneos = 10 instancias en paralelo
- 1000 requests simultaneos = 1000 instancias en paralelo

No hay servidores que levantar ni configuracion de auto-scaling. AWS lo hace automaticamente.

## Limites por defecto

| Limite | Valor | Configurable |
|--------|-------|--------------|
| Concurrencia por cuenta/region | 1,000 instancias simultaneas | Si, se puede pedir aumento a AWS |
| Burst inicial | 500-3000 (depende de la region) | No |
| Escalado despues del burst | +500 instancias/minuto | No |
| Timeout maximo | 15 minutos | Si (en el codigo CDK) |
| Memoria | 128 MB - 10 GB | Si (en el codigo CDK) |

## Donde se configura

En el stack CDK (lib/campanias-prototype-stack.ts), los parametros de cada Lambda:

```typescript
timeout: cdk.Duration.seconds(30),
memorySize: 256,
```

## Provisioned Concurrency (opcional, para produccion)

Si se requiere garantizar que siempre haya instancias calientes (sin cold start):

```typescript
fn_gestion.addAlias('live', {
  provisionedConcurrentExecutions: 5  // 5 instancias siempre listas
});
```

Costo: aproximadamente $0.015/hora por instancia reservada. Para el prototipo no es necesario.

## Configuracion del prototipo actual

| Aspecto | Valor actual |
|---------|-------------|
| Escalabilidad | Automatica (0 a 1000 simultaneas) |
| Configuracion necesaria | Ninguna |
| Costo cuando no se usa | $0 (pay-per-invocation) |
| Cold start | 200-500ms en la primera invocacion |
| Timeout | 30 segundos |
| Memoria | 256 MB |

## Cuando considerar ajustes

| Escenario | Accion |
|-----------|--------|
| Mas de 1000 requests/segundo | Solicitar aumento de limite a AWS Support |
| Latencia critica (< 100ms) | Activar Provisioned Concurrency |
| Procesamiento pesado (ML, ETL) | Aumentar memoria (hasta 10 GB) |
| Procesos largos (> 15 min) | Usar Step Functions o ECS/Fargate en su lugar |
| Campañas masivas (100K+ notificaciones) | Usar SQS como buffer + multiples Lambdas consumidoras |

## Relacion con otros servicios del prototipo

| Servicio | Escalabilidad |
|---------|--------------|
| API Gateway | Automatica (10,000 req/s por defecto) |
| DynamoDB (PAY_PER_REQUEST) | Automatica (sin limite practico) |
| EventBridge | Automatica (ilimitada) |
| SQS | Automatica (ilimitada) |

Todos los servicios del prototipo escalan automaticamente sin intervencion manual.
