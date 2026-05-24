"""Genera PNG de la vista de arquitectura de software."""
import os
from graphviz import Digraph

OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))

g = Digraph('software', format='png')
g.attr(rankdir='TB', splines='ortho', nodesep='0.6', ranksep='0.8',
       fontname='Arial', fontsize='11', bgcolor='white',
       label='Arquitectura de Software - Sistema de Campañas TO-BE\n\n',
       labelloc='t', labelfontsize='14')
g.attr('node', fontname='Arial', fontsize='9', style='filled', shape='box', penwidth='1.5')
g.attr('edge', fontname='Arial', fontsize='8', color='#555555')

# Frontend
with g.subgraph(name='cluster_fe') as c:
    c.attr(label='Frontend (SPA)', style='rounded', color='#2980B9')
    c.node('portal', 'Portal de Campañas\nReact/Angular', fillcolor='#D6EAF8', color='#2980B9')
    c.node('dash', 'Dashboard Gerencial\nReact/Angular', fillcolor='#D6EAF8', color='#2980B9')

# API Gateway
with g.subgraph(name='cluster_gw') as c:
    c.attr(label='API Gateway', style='rounded', color='#1ABC9C')
    c.node('apigw', 'API Gateway\nKong / Cloud Managed\nAuth + Rate Limit', fillcolor='#D1F2EB', color='#1ABC9C')

# Servicios
with g.subgraph(name='cluster_svc') as c:
    c.attr(label='Microservicios de Negocio', style='rounded', color='#2D5F8A')
    c.node('auth', 'Auth Service\nOAuth2/OIDC\nNode.js', fillcolor='#D6E8F5', color='#2D5F8A')
    c.node('reglas', 'Motor de Reglas\nDrools\nSpring Boot', fillcolor='#D6E8F5', color='#2D5F8A')
    c.node('sim', 'Simulación\nSpring Boot', fillcolor='#D6E8F5', color='#2D5F8A')
    c.node('camp', 'Gestión Campañas\nSpring Boot', fillcolor='#D6E8F5', color='#2D5F8A')
    c.node('scoring', 'Scoring Alternativo\nPython/FastAPI\nML Models', fillcolor='#D6E8F5', color='#2D5F8A')
    c.node('track', 'Tracking\nEfectividad\nSpring Boot', fillcolor='#D6E8F5', color='#2D5F8A')
    c.node('notif', 'Notificaciones\nMulticanal\nNode.js', fillcolor='#D6E8F5', color='#2D5F8A')

# Integración
with g.subgraph(name='cluster_int') as c:
    c.attr(label='Integración', style='rounded', color='#F39C12')
    c.node('kafka', 'Event Bus\nKafka', fillcolor='#FEF9E7', color='#F39C12')
    c.node('esb', 'ESB IBM IB\nLegacy Bridge', fillcolor='#FEF9E7', color='#F39C12')
    c.node('etl', 'Pipeline ETL\nAirflow', fillcolor='#FEF9E7', color='#F39C12')

# Persistencia
with g.subgraph(name='cluster_db') as c:
    c.attr(label='Persistencia', style='rounded', color='#6B4C9A')
    c.node('db_camp', 'PostgreSQL\nCampañas + Reglas', shape='cylinder', fillcolor='#E8DCF5', color='#6B4C9A')
    c.node('db_hist', 'PostgreSQL\nHistórico', shape='cylinder', fillcolor='#E8DCF5', color='#6B4C9A')
    c.node('db_track', 'TimescaleDB\nMétricas', shape='cylinder', fillcolor='#E8DCF5', color='#6B4C9A')
    c.node('redis', 'Redis\nCache', fillcolor='#E8DCF5', color='#6B4C9A')
    c.node('dw', 'Data Warehouse\nAnalítica', shape='cylinder', fillcolor='#E8DCF5', color='#6B4C9A')

# Externos
with g.subgraph(name='cluster_ext') as c:
    c.attr(label='Sistemas Externos', style='rounded', color='#8B4513')
    c.node('core', 'Core Bancario', fillcolor='#FDE8D0', color='#8B4513')
    c.node('crm', 'CRM Siebel', fillcolor='#FDE8D0', color='#8B4513')
    c.node('cred', 'Créditos', fillcolor='#FDE8D0', color='#8B4513')
    c.node('risk', 'Centrales Riesgo', fillcolor='#FDE8D0', color='#8B4513')
    c.node('telco', 'Telecom', fillcolor='#FDE8D0', color='#8B4513')
    c.node('prov_notif', 'Proveedor\nSMS/Email/Push', fillcolor='#FDE8D0', color='#8B4513')

# Edges
g.edge('portal', 'apigw')
g.edge('dash', 'apigw')
g.edge('apigw', 'auth')
g.edge('apigw', 'reglas')
g.edge('apigw', 'sim')
g.edge('apigw', 'camp')
g.edge('apigw', 'track')
g.edge('reglas', 'scoring')
g.edge('sim', 'scoring')
g.edge('camp', 'notif')
g.edge('camp', 'kafka')
g.edge('track', 'kafka')
g.edge('notif', 'kafka')
g.edge('reglas', 'esb')
g.edge('scoring', 'etl')
g.edge('esb', 'core')
g.edge('esb', 'crm')
g.edge('esb', 'cred')
g.edge('etl', 'risk')
g.edge('etl', 'telco')
g.edge('notif', 'prov_notif')
g.edge('reglas', 'db_camp')
g.edge('camp', 'db_camp')
g.edge('camp', 'db_hist')
g.edge('track', 'db_track')
g.edge('scoring', 'redis')
g.edge('auth', 'redis')
g.edge('kafka', 'dw')

output = os.path.join(OUTPUT_DIR, 'campanias-to-be-05-software')
g.render(output, cleanup=True)
print(f"Generado: {output}.png")
