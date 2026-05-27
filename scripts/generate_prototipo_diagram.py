"""Genera PNG del diagrama de arquitectura del prototipo serverless."""
import os
from graphviz import Digraph

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'diagramas', 'to-be')

g = Digraph('prototipo', format='png')
g.attr(rankdir='TB', splines='ortho', nodesep='0.7', ranksep='0.9',
       fontname='Arial', fontsize='11', bgcolor='white',
       label='Arquitectura del Prototipo Serverless - Sistema de Campañas\n\n',
       labelloc='t', labelfontsize='14')
g.attr('node', fontname='Arial', fontsize='9', style='filled', shape='box', penwidth='1.5')
g.attr('edge', fontname='Arial', fontsize='8', color='#555555')

# Cliente
g.node('client', 'Cliente HTTP\n(PowerShell / Browser)', fillcolor='#AED6F1', color='#1A5276')

# API Gateway
g.node('apigw', 'API Gateway\nCampanias API\nREST Endpoints', fillcolor='#D1F2EB', color='#1ABC9C')

# Lambdas
with g.subgraph(name='cluster_lambdas') as c:
    c.attr(label='AWS Lambda (Node.js 22)', style='rounded', color='#ED7100')
    c.node('l_gestion', 'campanias-gestion\n\nPOST /campaigns\nGET /campaigns\nGET /campaigns/{id}', fillcolor='#FEF3E2', color='#ED7100')
    c.node('l_reglas', 'campanias-reglas\n\nPOST /campaigns/{id}/evaluate\nSimula scoring', fillcolor='#FEF3E2', color='#ED7100')
    c.node('l_tracking', 'campanias-tracking\n\nConsume eventos\nRegistra auditoria', fillcolor='#FEF3E2', color='#ED7100')

# DynamoDB
with g.subgraph(name='cluster_dynamo') as c:
    c.attr(label='Amazon DynamoDB', style='rounded', color='#3334B9')
    c.node('ddb_camp', 'campanias-campaigns\n\nCampañas, reglas,\nestado, elegibles', shape='cylinder', fillcolor='#E8E0F5', color='#3334B9')
    c.node('ddb_track', 'campanias-tracking\n\nEventos de auditoria,\ntimestamps', shape='cylinder', fillcolor='#E8E0F5', color='#3334B9')

# EventBridge
g.node('eventbridge', 'EventBridge\ncampanias-events\n\nBus de eventos\nDesacopla servicios', fillcolor='#FCE4EC', color='#E7157B')

# SQS
g.node('sqs', 'SQS\ncampanias-notifications\n\nCola para notificaciones\n(futuro)', fillcolor='#FCE4EC', color='#E7157B')

# Edges
g.edge('client', 'apigw', label='HTTPS')
g.edge('apigw', 'l_gestion', label='POST/GET\n/campaigns')
g.edge('apigw', 'l_reglas', label='POST\n/campaigns/{id}/evaluate')
g.edge('l_gestion', 'ddb_camp', label='PUT/GET')
g.edge('l_gestion', 'eventbridge', label='PutEvents\nCampañaCreada')
g.edge('l_gestion', 'sqs', label='SendMessage')
g.edge('l_reglas', 'ddb_camp', label='GET/UPDATE')
g.edge('eventbridge', 'l_tracking', label='Rule:\nsource=campanias.gestion')
g.edge('l_tracking', 'ddb_track', label='PUT')

output = os.path.join(OUTPUT_DIR, 'CAM-TOBE-07-prototipo-serverless')
g.render(output, cleanup=True)
print(f"Generado: {output}.png")

# Copiar a entregables
import shutil
shutil.copy(f"{output}.png", os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'entregables', 'CAM-TOBE-07-prototipo-serverless.png'))
print("Copiado a entregables/")
