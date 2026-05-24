"""Genera diagrama TO-BE de Créditos v2 con PSE + DECEVAL + Validación Biométrica."""
import os
from graphviz import Digraph

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'diagramas', 'to-be')

g = Digraph('credito_tobe_v2', format='png')
g.attr(rankdir='LR', splines='ortho', nodesep='0.6', ranksep='0.9',
       fontname='Arial', fontsize='11', bgcolor='white',
       label='Sistema de Crédito TO-BE v2 (PSE + DECEVAL + Biometría)\n\n', labelloc='t', labelfontsize='14')
g.attr('node', fontname='Arial', fontsize='9', style='filled', shape='box', penwidth='1.5')
g.attr('edge', fontname='Arial', fontsize='8', color='#555555')

# Actores
g.node('asesor', 'Asesor Comercial', fillcolor='#AED6F1', color='#1A5276')
g.node('cliente', 'Cliente', fillcolor='#AED6F1', color='#1A5276')

# Canales
with g.subgraph(name='cluster_canales') as c:
    c.attr(label='Canales (Multicanal)', style='rounded', color='#27AE60')
    c.node('pc', 'PC Oficina', fillcolor='#D5F5E3', color='#27AE60')
    c.node('web', 'App Web', fillcolor='#D5F5E3', color='#27AE60')
    c.node('movil', 'App Móvil', fillcolor='#D5F5E3', color='#27AE60')

# Orquestación
g.node('bpm', 'BPM\nFlujo Aprobación', fillcolor='#FCF3CF', color='#F39C12')
g.node('apigw', 'API Gateway', fillcolor='#D1F2EB', color='#1ABC9C')

# Sistema de Crédito
with g.subgraph(name='cluster_credito') as c:
    c.attr(label='Sistema de Créditos (Nube Privada)', style='rounded', color='#2D5F8A')
    c.node('mod_cred', 'Módulo de Crédito\nAprobación', fillcolor='#D6E8F5', color='#2D5F8A')
    c.node('mod_doc', 'Gestor Documental\n(Digital)', fillcolor='#D6E8F5', color='#2D5F8A')
    c.node('mod_pago', 'Módulo de Pagos\nExtendido\nInterno + PSE', fillcolor='#D6E8F5', color='#2D5F8A')

# Integración
g.node('esb', 'ESB\nIBM Integration Bus', fillcolor='#FEF9E7', color='#F39C12')
g.node('mft', 'MFT\nIntercambio Archivos\nSFTP Cifrado', fillcolor='#FEF9E7', color='#F39C12')

# Externos - Existentes
g.node('datacredito', 'Datacrédito\nCentrales de Riesgo', fillcolor='#FDE8D0', color='#8B4513')
g.node('core', 'Core Bancario\nHost Transaccional\nCta Ahorros', fillcolor='#D9F0E0', color='#4A8C5C')

# Externos - Nuevos TO-BE
with g.subgraph(name='cluster_nuevos') as c:
    c.attr(label='Nuevos Proveedores TO-BE', style='rounded', color='#8E44AD')
    c.node('pse', 'PSE (ATH)\nPagos Interbancarios', fillcolor='#F4ECF7', color='#8E44AD')
    c.node('deceval', 'DECEVAL\nPagarés\nDesmaterializados', fillcolor='#F4ECF7', color='#8E44AD')
    c.node('biometria', 'Proveedor\nValidación Biométrica', fillcolor='#F4ECF7', color='#8E44AD')
    c.node('banco_ext', 'Bancos Externos', fillcolor='#F4ECF7', color='#8E44AD')

# Edges - Flujo onboarding (multicanal)
g.edge('asesor', 'pc')
g.edge('cliente', 'web')
g.edge('cliente', 'movil')
g.edge('pc', 'bpm')
g.edge('web', 'apigw')
g.edge('movil', 'apigw')
g.edge('apigw', 'bpm')

# BPM -> Módulos
g.edge('bpm', 'mod_cred')
g.edge('bpm', 'mod_doc')

# Integraciones onboarding
g.edge('mod_cred', 'esb')
g.edge('esb', 'datacredito')
g.edge('mod_cred', 'biometria')
g.edge('mod_doc', 'deceval')
g.edge('mod_doc', 'mft')

# Flujo pago
g.edge('apigw', 'mod_pago')
g.edge('mod_pago', 'core')
g.edge('mod_pago', 'pse')
g.edge('pse', 'banco_ext')

output = os.path.join(OUTPUT_DIR, 'CRE-TOBE-01-contexto-v2')
g.render(output, cleanup=True)
print(f"Generado: {output}.png")
