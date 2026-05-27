---
title: "Manual del Prototipo Serverless - Sistema de Campañas"
section: "12"
version: "1.0"
date: "2026-05-26"
---

# 12. Manual del Prototipo Serverless - Sistema de Campañas AWS

## 1. Descripcion General

Prototipo funcional de la arquitectura CAM-TOBE-06-serverless-aws-gcp que demuestra
el flujo end-to-end de creacion, evaluacion y tracking de campañas de credito
usando servicios serverless de AWS.

## 2. Diagrama de Arquitectura del Prototipo

```
                    +------------------+
                    |   PowerShell /   |
                    |   Cliente HTTP   |
                    +--------+---------+
                             |
                             | HTTPS
                             v
                    +------------------+
                    |   API Gateway    |
                    |   (REST API)     |
                    +--------+---------+
                             |
              +--------------+--------------+
              |              |              |
              v              v              v
     +--------+----+ +------+------+ +-----+-------+
     | Lambda      | | Lambda      | | Lambda      |
     | campanias-  | | campanias-  | | campanias-  |
     | gestion     | | reglas      | | tracking    |
     +------+------+ +------+------+ +------+------+
            |              |              ^
            |              |              |
            v              v              | (EventBridge)
     +------+------+ +----+----+   +-----+-------+
     | DynamoDB    | | DynamoDB|   | EventBridge  |
     | campanias-  | | (update)|   | campanias-   |
     | campaigns   | |         |   | events       |
     +------+------+ +---------+   +------+-------+
            |                             ^
            +-----------------------------+
            | (PutEvents)
            |
            v
     +------+------+
     | SQS         |
     | campanias-  |
     | notifications|
     +-------------+
            |
            v
     +------+------+
     | DynamoDB    |
     | campanias-  |
     | tracking    |
     +-------------+
```

## 3. Componentes Desplegados

| Componente | Servicio AWS | Funcion |
|-----------|-------------|---------|
| API Gateway | Amazon API Gateway | Punto de entrada REST. Recibe requests HTTP y los rutea a las Lambdas correspondientes |
| Lambda campanias-gestion | AWS Lambda (Node.js 22) | Crea campañas, las almacena en DynamoDB y publica eventos en EventBridge |
| Lambda campanias-reglas | AWS Lambda (Node.js 22) | Evalua reglas de elegibilidad, genera lista de clientes simulados, actualiza estado de campaña |
| Lambda campanias-tracking | AWS Lambda (Node.js 22) | Consume eventos de EventBridge y registra tracking de auditoria |
| DynamoDB campanias-campaigns | Amazon DynamoDB | Tabla operacional que almacena campañas, reglas y estado |
| DynamoDB campanias-tracking | Amazon DynamoDB | Tabla de auditoria que registra todos los eventos del sistema |
| EventBridge campanias-events | Amazon EventBridge | Bus de eventos que desacopla la comunicacion entre servicios |
| SQS campanias-notifications | Amazon SQS | Cola de mensajes para procesamiento asincrono de notificaciones |

## 4. Prerequisitos

| Herramienta | Version Minima | Comando de verificacion |
|------------|----------------|------------------------|
| AWS CLI | 2.x | aws --version |
| Node.js | 18.x+ | node --version |
| Python | 3.x | python --version |
| AWS CDK | 2.x | cdk --version |
| Cuenta AWS | Con permisos de administrador | aws sts get-caller-identity |

## 5. Instalacion Paso a Paso

### Paso 1: Instalar AWS CDK

```cmd
npm install -g aws-cdk
cdk --version
```

### Paso 2: Verificar autenticacion AWS

```cmd
aws sts get-caller-identity
```

Resultado esperado:
```json
{
    "UserId": "AIDAQ4S6QXXWPFBXZVMZI",
    "Account": "061401513452",
    "Arn": "arn:aws:iam::061401513452:user/Andresjmc"
}
```

### Paso 3: Crear el proyecto CDK

```cmd
mkdir c:\kiro-project\campanias-prototype
cd c:\kiro-project\campanias-prototype
cdk init app --language typescript
```

### Paso 4: Bootstrap CDK (una sola vez por cuenta/region)

```cmd
cdk bootstrap
```

Esto crea un stack CDKToolkit con un bucket S3 y roles IAM necesarios para desplegar.

### Paso 5: Definir la infraestructura

Reemplazar el archivo `lib/campanias-prototype-stack.ts` con el stack que define:
- 2 tablas DynamoDB (campaigns + tracking)
- 1 cola SQS (notifications)
- 1 bus EventBridge (events)
- 3 funciones Lambda (gestion, reglas, tracking)
- 1 API Gateway REST con endpoints
- Permisos IAM (least privilege)
- Regla EventBridge que conecta eventos con Lambda tracking

### Paso 6: Crear las funciones Lambda

Estructura de carpetas:
```
campanias-prototype/
  lambdas/
    campaigns/
      index.js      <- Lambda de gestion de campañas
    rules/
      index.js      <- Lambda de motor de reglas
    tracking/
      index.js      <- Lambda de tracking
```

### Paso 7: Compilar

```cmd
npm run build
```

### Paso 8: Verificar cambios (sin desplegar)

```cmd
cdk diff
```

### Paso 9: Desplegar

```cmd
cdk deploy
```

Confirmar con `y` cuando pregunte sobre cambios IAM.

Resultado esperado:
```
Outputs:
CampaniasPrototypeStack.ApiUrl = https://XXXXXXXX.execute-api.us-east-1.amazonaws.com/prod/
```

## 6. Estructura del Proyecto

```
campanias-prototype/
+-- bin/
|   +-- campanias-prototype.ts       # Punto de entrada CDK
+-- lib/
|   +-- campanias-prototype-stack.ts  # Definicion de infraestructura
+-- lambdas/
|   +-- campaigns/
|   |   +-- index.js                  # Lambda gestion de campañas
|   +-- rules/
|   |   +-- index.js                  # Lambda motor de reglas
|   +-- tracking/
|       +-- index.js                  # Lambda tracking
+-- test/
+-- cdk.json
+-- package.json
+-- tsconfig.json
```

## 7. Codigo de las Lambdas

### 7.1 Lambda: campanias-gestion (campaigns/index.js)

Responsabilidades:
- POST /campaigns: Crea una campaña con estado BORRADOR
- GET /campaigns: Lista todas las campañas
- GET /campaigns/{id}: Obtiene detalle de una campaña

Flujo al crear:
1. Recibe JSON con nombre, producto, reglas
2. Genera ID unico (CAM-timestamp)
3. Guarda en DynamoDB con estado BORRADOR
4. Publica evento CampañaCreada en EventBridge
5. Retorna la campaña creada

### 7.2 Lambda: campanias-reglas (rules/index.js)

Responsabilidades:
- POST /campaigns/{id}/evaluate: Evalua reglas y genera clientes elegibles

Flujo:
1. Lee la campaña de DynamoDB
2. Simula evaluacion de reglas (genera clientes ficticios con score)
3. Actualiza la campaña: estado SIMULADA + eligibleCount
4. Retorna lista de clientes elegibles + proyeccion de conversion

### 7.3 Lambda: campanias-tracking (tracking/index.js)

Responsabilidades:
- Consume eventos de EventBridge automaticamente
- Registra cada evento en la tabla de tracking

Flujo:
1. EventBridge invoca la Lambda cuando detecta un evento con source campanias.gestion
2. Extrae el detalle del evento
3. Guarda registro en DynamoDB tracking con timestamp

## 8. API Endpoints

| Metodo | Endpoint | Lambda | Descripcion |
|--------|----------|--------|-------------|
| POST | /campaigns | campanias-gestion | Crear nueva campaña |
| GET | /campaigns | campanias-gestion | Listar todas las campañas |
| GET | /campaigns/{id} | campanias-gestion | Obtener campaña por ID |
| POST | /campaigns/{id}/evaluate | campanias-reglas | Evaluar reglas y simular |

## 9. Pruebas del Prototipo

### Prueba 1: Crear una campaña

```powershell
Invoke-RestMethod -Method POST -Uri "https://f23y4ls7s6.execute-api.us-east-1.amazonaws.com/prod/campaigns" -ContentType "application/json" -Body '{"name":"Microcredito Jovenes Q3","product":"microcredito","targetAge":"18-25","rules":["score>500","ingresos>1SMMLV"]}'
```

Resultado esperado:
```
campaignId : CAM-1779757227819
name       : Microcredito Jovenes Q3
product    : microcredito
targetAge  : 18-25
status     : BORRADOR
createdAt  : 2026-05-26T01:00:27.819Z
rules      : {score>500, ingresos>1SMMLV}
```

### Prueba 2: Evaluar reglas de la campaña

```powershell
Invoke-RestMethod -Method POST -Uri "https://f23y4ls7s6.execute-api.us-east-1.amazonaws.com/prod/campaigns/CAM-1779757227819/evaluate"
```

Resultado esperado:
```
campaignId          : CAM-1779757227819
status              : SIMULADA
eligibleClients     : 35
projectedConversion : 8%
riskLevel           : MEDIO
clients             : {lista de clientes con score}
```

### Prueba 3: Listar todas las campañas

```powershell
Invoke-RestMethod -Method GET -Uri "https://f23y4ls7s6.execute-api.us-east-1.amazonaws.com/prod/campaigns"
```

### Prueba 4: Consultar campaña especifica

```powershell
Invoke-RestMethod -Method GET -Uri "https://f23y4ls7s6.execute-api.us-east-1.amazonaws.com/prod/campaigns/CAM-1779757227819"
```

### Prueba 5: Crear segunda campaña (otro producto)

```powershell
Invoke-RestMethod -Method POST -Uri "https://f23y4ls7s6.execute-api.us-east-1.amazonaws.com/prod/campaigns" -ContentType "application/json" -Body '{"name":"Libre Destino Universitarios","product":"libre-destino","targetAge":"18-22","rules":["score>600","antiguedad>1año"]}'
```

### Prueba 6: Verificar tracking (eventos registrados automaticamente)

```powershell
aws dynamodb scan --table-name campanias-tracking --output table
```

Este comando muestra todos los eventos que el sistema registro automaticamente
via EventBridge cada vez que se creo una campaña.

## 10. Recorrido de una Request

### Crear Campaña (POST /campaigns)

```
1. Cliente HTTP (PowerShell)
   |
   | HTTPS POST con JSON
   v
2. API Gateway (Campanias API)
   |
   | Rutea a Lambda segun path + method
   v
3. Lambda campanias-gestion
   |
   | a) Parsea el body JSON
   | b) Genera campaignId unico
   | c) Crea objeto con estado BORRADOR
   |
   +---> 4. DynamoDB (campanias-campaigns)
   |         INSERT: guarda la campaña
   |
   +---> 5. EventBridge (campanias-events)
   |         PutEvents: {source: campanias.gestion, detail-type: CampañaCreada}
   |
   | Retorna 201 + campaña creada
   v
6. EventBridge Rule (TrackingRule)
   |
   | Detecta evento con source=campanias.gestion
   | Invoca Lambda tracking (asincrono)
   v
7. Lambda campanias-tracking
   |
   | Registra el evento
   v
8. DynamoDB (campanias-tracking)
      INSERT: {campaignId, eventType, timestamp, data}
```

### Evaluar Reglas (POST /campaigns/{id}/evaluate)

```
1. Cliente HTTP (PowerShell)
   |
   | HTTPS POST
   v
2. API Gateway
   |
   v
3. Lambda campanias-reglas
   |
   +---> 4. DynamoDB (campanias-campaigns)
   |         GET: lee la campaña
   |
   | 5. Simula evaluacion de reglas
   |    - Genera clientes ficticios
   |    - Calcula scores aleatorios
   |    - Proyecta conversion
   |
   +---> 6. DynamoDB (campanias-campaigns)
   |         UPDATE: estado=SIMULADA, eligibleCount=N
   |
   | Retorna lista de elegibles + proyeccion
   v
7. Cliente recibe resultado
```

## 11. Costos del Prototipo

| Servicio | Free Tier | Uso del prototipo | Costo |
|---------|-----------|-------------------|-------|
| Lambda | 1M requests/mes | ~100 invocaciones | $0.00 |
| API Gateway | 1M llamadas/mes (12 meses) | ~50 llamadas | $0.00 |
| DynamoDB | 25 GB + on-demand | ~1 MB datos | $0.00 |
| EventBridge | 14M eventos gratis | ~20 eventos | $0.00 |
| SQS | 1M requests/mes | ~50 mensajes | $0.00 |
| CloudWatch | 5 GB logs/mes | Logs minimos | $0.00 |
| TOTAL | | | $0.00 |

## 12. Comandos Utiles

### Ver logs de una Lambda

```powershell
aws logs tail /aws/lambda/campanias-gestion --follow
aws logs tail /aws/lambda/campanias-reglas --follow
aws logs tail /aws/lambda/campanias-tracking --follow
```

### Ver contenido de tablas DynamoDB

```powershell
aws dynamodb scan --table-name campanias-campaigns --output table
aws dynamodb scan --table-name campanias-tracking --output table
```

### Destruir el prototipo (eliminar todos los recursos)

```cmd
cdk destroy
```

Confirmar con `y`. Elimina todos los recursos creados (tablas, lambdas, API, etc.)

### Redesplegar despues de cambios

```cmd
npm run build
cdk deploy
```

## 13. Problemas Conocidos y Soluciones

| Problema | Causa | Solucion |
|----------|-------|----------|
| curl no funciona en Windows | PowerShell alias curl = Invoke-WebRequest | Usar Invoke-RestMethod en su lugar |
| Lambda sin permiso UpdateItem | grantReadData no incluye escritura | Cambiar a grantReadWriteData |
| cdk deploy no muestra outputs | Stack ya existia sin recursos | Verificar que bin/ instancia el stack |
| LF will be replaced by CRLF | Diferencia de finales de linea Unix/Windows | Ignorar, no afecta funcionalidad |

## 14. Siguiente Paso: Produccion

Para llevar este prototipo a produccion se necesita agregar:

| Componente | Servicio | Prioridad |
|-----------|---------|-----------|
| Autenticacion | Cognito + JWT | Alta |
| WAF | AWS WAF | Alta |
| CDN | CloudFront | Media |
| Notificaciones reales | SQS + Lambda + Proveedor externo | Alta |
| Streaming a GCP | Kinesis Firehose + Dataflow + BigQuery | Media |
| CI/CD | CodePipeline o GitHub Actions | Alta |
| Monitoreo | CloudWatch Dashboards + Alarmas | Alta |
| Tests automatizados | Jest + Integration tests | Alta |
