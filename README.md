# Propuesta de Arquitectura Evolutiva - Sistema de Campañas y Créditos

## Descripción

Propuesta de arquitectura para la modernización del sistema de campañas de un banco,
migrando de una aplicación legacy (fuera de soporte) a una solución serverless multinube
(AWS + GCP) que automatiza el proceso de campañas de crédito para personas naturales
entre 18-25 años.

## Estructura del Proyecto

```
├── docs/                    Documentación entregable (Markdown → PDF/DOCX)
│   ├── 00-indice-general.md
│   ├── 01-contexto-problema.md
│   ├── 03-atributos-calidad.md
│   ├── 05-arquitectura-solucion.md
│   ├── 06-arquitectura-software.md
│   ├── 07-arquitectura-seguridad.md
│   ├── 09-arquitectura-infraestructura.md
│   ├── 10-roadmap-evolutivo.md
│   ├── 11-requerimientos-no-funcionales.md
│   └── anexos/
├── diagramas/               Artefactos visuales finales
│   ├── as-is/              Diagramas del estado actual
│   ├── to-be/              Diagramas de la solución propuesta
│   └── fuentes/            Imágenes originales del requerimiento
├── scripts/                 Scripts de generación de diagramas
├── specs/                   Especificaciones SDD por dominio
├── entregables/             PDFs y DOCX generados
└── .kiro/                   Configuración de agentes
```

## Generar Diagramas

```bash
pip install graphviz diagrams
python scripts/generate_campanias_enterprise.py
python scripts/generate_campanias_serverless.py
python scripts/generate_credito_diagrams.py
```

## Generar PDF

```bash
pip install fpdf2
python scripts/generate_pdf.py
```

## Convención de Nomenclatura

- Documentos: `NN-nombre-descriptivo.md`
- Diagramas: `{DOMINIO}-{FASE}-{NN}-{vista}.{ext}`
  - DOMINIO: CAM (Campañas), CRE (Créditos)
  - FASE: ASIS, TOBE
  - Ejemplo: `CAM-TOBE-06-serverless-aws-gcp.png`

## Tecnologías de la Solución

| Cloud | Uso |
|-------|-----|
| AWS | Plataforma de campañas (Lambda, API Gateway, DynamoDB, Step Functions) |
| GCP | Analítica y dashboards (BigQuery, Dataflow, Looker) |
