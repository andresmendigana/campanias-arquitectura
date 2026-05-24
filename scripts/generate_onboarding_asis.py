"""Genera diagrama AS-IS de Onboarding de Créditos."""
import os
from graphviz import Digraph

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'diagramas', 'as-is')

g = Digraph('onboarding_asis', format='png')
g.attr(rankdir='LR', splines='ortho', nodesep='0.7', ranksep='1.0',
       fontname='Arial', fontsize='11', bgcolor='white',
       label='Onboarding Créditos AS-IS\n\n', labelloc='t', labelfontsize='14')
g.attr('node', fontname='Arial', fontsize='9', style='filled', shape='box', penwidth='1.5')
g.attr('edge', fontname='Arial', fontsize='8', color='#555555')

# Actor
g.node('cliente', 'Cliente\n(Solicitante)', fillcolor='#AED6F1', color='#1A5276')
g.node('asesor', 'Asesor Comercial', fillcolor='#AED6F1', color='#1A5276')

# Canal
g.node('pc', 'PC Oficina\n(Único canal)', fillcolor='#D5F5E3', color='#27AE60')

# BPM
g.node('bpm', 'BPM\nFlujo de Aprobación\nde Crédito', fillcolor='#FCF3CF', color='#F39C12')

# Sistema de Créditos
with g.subgraph(name='cluster_credito') as c:
    c.attr(label='Sistema de Créditos (Nube Privada)', style='rounded', color='#2D5F8A')
    c.node('mod_cred', 'Módulo de Crédito\nAprobación y\nadministración', fillcolor='#D6E8F5', color='#2D5F8A')
    c.node('mod_doc', 'Módulo Gestión\nDocumental\nPagarés y documentos\nFÍSICOS', fillcolor='#D6E8F5', color='#2D5F8A')

# CRM
g.node('crm', 'CRM\nAdministración clientes\n\nNo expone servicios web\nIntegración vía ESB\no archivos planos', fillcolor='#D6E8F5', color='#2D5F8A')

# Integración
g.node('esb', 'ESB\nIBM Integration Bus', fillcolor='#FEF9E7', color='#F39C12')

# File Server
g.node('fileserver', 'File Server\nRepositorio de archivos\n(Interno)', fillcolor='#EAECEE', color='#7F8C8D')

# Externos
g.node('datacredito', 'Datacrédito\nCentrales de Riesgo', fillcolor='#FDE8D0', color='#8B4513')

# Restricciones (nota)
g.node('nota', 'Restricciones AS-IS:\n• Solo radicación en oficina\n• Documentos físicos (pagarés)\n• Sin validación biométrica\n• Sin firma digital\n• Pago solo con cuentas del banco',
       shape='note', fillcolor='#FADBD8', color='#C0392B', fontsize='8')

# Edges
g.edge('cliente', 'asesor', label='Se presenta\nen oficina')
g.edge('asesor', 'pc', label='Ingresa al\nsistema')
g.edge('pc', 'bpm', label='Inicia flujo')
g.edge('bpm', 'mod_cred', label='Flujo\naprobación')
g.edge('bpm', 'mod_doc', label='Adjunta\ndocumentos\nfísicos')
g.edge('mod_cred', 'esb', label='Consulta')
g.edge('mod_cred', 'crm', label='Datos cliente')
g.edge('esb', 'datacredito', label='Verificación\ncomportamiento\nfinanciero')
g.edge('mod_doc', 'fileserver', label='Almacena\ndigitalizaciones')

output = os.path.join(OUTPUT_DIR, 'ONB-ASIS-01-onboarding-creditos')
g.render(output, cleanup=True)
print(f"Generado: {output}.png")
