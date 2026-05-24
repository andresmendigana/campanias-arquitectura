# Specs (Especificaciones de Implementación)

Esta carpeta se utiliza cuando el cliente aprueba la propuesta y se inicia
la fase de construcción del MVP.

## Estructura por dominio

```
specs/
├── campanias/
│   ├── requirements.md    → Requerimientos funcionales y no funcionales detallados
│   ├── design.md          → Diseño técnico (APIs, modelos, contratos)
│   └── tasks.md           → Tareas de implementación priorizadas por sprint
└── creditos/
    ├── requirements.md
    ├── design.md
    └── tasks.md
```

## Cuándo usar

- Después de la aprobación de la propuesta arquitectónica
- Para guiar al equipo de desarrollo en la implementación
- Como contrato técnico entre arquitectura y desarrollo

## Diferencia con docs/

| Carpeta | Audiencia | Propósito |
|---------|-----------|-----------|
| `docs/` | Cliente (banco) | Propuesta y decisiones arquitectónicas |
| `specs/` | Equipo de desarrollo | Guía de implementación técnica |
