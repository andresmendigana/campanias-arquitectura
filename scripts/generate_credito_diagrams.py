"""Genera PNGs del sistema de crédito AS-IS y TO-BE."""
import os
from graphviz import Digraph

OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))

def create_credito_asis():
    g = Digraph('credito_asis', format='png')
    g.attr(rankdir='LR', splines='ortho', nodesep='0.7', ranksep='1.0',
           fontname='Arial', fontsize='11', bgcolor='white',
           label='Sistema de Crédito AS-IS\n\n', labelloc='t', labelfontsize='14')
    g.attr('node', fontname='Arial', fontsize='9', style='filled', shape='box', penwidth='1.5')
    g.attr('edge', fontname='Arial', fontsize='8', color='#555555')

    # Actor
    g.node('asesor', 'Asesor Comercial', fillcolor='#AED6F1', color='#1A5276')
    g.node('pc', 'PC Oficina', fillcolor='#D5F5E3', color='#27AE60')

    # BPM
    g.node('bpm', 'BPM\nFlujo de Aprobación', fillcolor='#FCF3CF', color='#F39C12')

    # Módulos
    with g.subgraph(name='cluster_modulos') as c:
        c.attr(label='Sistema de Crédito', style='rounded', color='#2D5F8A')
        c.node('mod_cred', 'Módulo de Crédito\nAprobación', fillcolor='#D6E8F5', color='#2D5F8A')
        c.node('mod_doc', 'Módulo Gestión\nDocumental\nPagarés y soportes', fillcolor='#D6E8F5', color='#2D5F8A')
        c.node('mod_pago', 'Módulo de Pago\n⚠ Solo productos\ndel mismo banco', fillcolor='#FADBD8', color='#C0392B')

    # Integración
    g.node('esb', 'ESB\nIBM Integration Bus', fillcolor='#FEF9E7', color='#F39C12')

    # Externos
    g.node('datacredito', 'Datacrédito\nCentrales de Riesgo', fillcolor='#FDE8D0', color='#8B4513')
    g.node('core', 'Core Bancario\nCuentas del cliente', fillcolor='#D9F0E0', color='#4A8C5C')

    # Edges
    g.edge('asesor', 'pc')
    g.edge('pc', 'bpm')
    g.edge('bpm', 'mod_cred')
    g.edge('bpm', 'mod_doc')
    g.edge('mod_cred', 'esb')
    g.edge('esb', 'datacredito')
    g.edge('mod_pago', 'core')

    output = os.path.join(OUTPUT_DIR, 'credito-as-is')
    g.render(output, cleanup=True)
    print(f"  Generado: {output}.png")


def create_credito_tobe():
    g = Digraph('credito_tobe', format='png')
    g.attr(rankdir='LR', splines='ortho', nodesep='0.6', ranksep='0.9',
           fontname='Arial', fontsize='11', bgcolor='white',
           label='Sistema de Crédito TO-BE (con PSE)\n\n', labelloc='t', labelfontsize='14')
    g.attr('node', fontname='Arial', fontsize='9', style='filled', shape='box', penwidth='1.5')
    g.attr('edge', fontname='Arial', fontsize='8', color='#555555')

    # Actores
    g.node('asesor', 'Asesor Comercial', fillcolor='#AED6F1', color='#1A5276')
    g.node('cliente', 'Cliente', fillcolor='#AED6F1', color='#1A5276')

    # Canales
    with g.subgraph(name='cluster_canales') as c:
        c.attr(label='Canales', style='rounded', color='#27AE60')
        c.node('pc', 'PC Oficina', fillcolor='#D5F5E3', color='#27AE60')
        c.node('web', 'Portal Web / App\nAutoservicio Pago', fillcolor='#D5F5E3', color='#27AE60')

    # BPM
    g.node('bpm', 'BPM\nFlujo de Aprobación', fillcolor='#FCF3CF', color='#F39C12')

    # Módulos
    with g.subgraph(name='cluster_modulos') as c:
        c.attr(label='Sistema de Crédito', style='rounded', color='#2D5F8A')
        c.node('mod_cred', 'Módulo de Crédito\nAprobación', fillcolor='#D6E8F5', color='#2D5F8A')
        c.node('mod_doc', 'Módulo Gestión\nDocumental', fillcolor='#D6E8F5', color='#2D5F8A')
        c.node('mod_pago', 'Módulo de Pagos\nExtendido\nInterno + PSE', fillcolor='#D6E8F5', color='#2D5F8A')

    # API Gateway
    g.node('apigw', 'API Gateway', fillcolor='#D1F2EB', color='#1ABC9C')

    # Integración
    g.node('esb', 'ESB\nIBM Integration Bus', fillcolor='#FEF9E7', color='#F39C12')

    # Externos
    g.node('datacredito', 'Datacrédito\nCentrales de Riesgo', fillcolor='#FDE8D0', color='#8B4513')
    g.node('core', 'Core Bancario\nCuentas del cliente', fillcolor='#D9F0E0', color='#4A8C5C')

    # PSE
    with g.subgraph(name='cluster_pse') as c:
        c.attr(label='Pagos Externos (NUEVO)', style='rounded', color='#8E44AD')
        c.node('pse', 'PSE\nACH Colombia', fillcolor='#F4ECF7', color='#8E44AD')
        c.node('banco_ext', 'Bancos Externos\nCuentas en otras\nentidades', fillcolor='#F4ECF7', color='#8E44AD')

    # Edges - Flujo aprobación (sin cambios)
    g.edge('asesor', 'pc')
    g.edge('pc', 'bpm')
    g.edge('bpm', 'mod_cred')
    g.edge('bpm', 'mod_doc')
    g.edge('mod_cred', 'esb')
    g.edge('esb', 'datacredito')

    # Edges - Flujo pago (nuevo)
    g.edge('cliente', 'web')
    g.edge('web', 'apigw')
    g.edge('apigw', 'mod_pago')
    g.edge('mod_pago', 'core')
    g.edge('mod_pago', 'pse')
    g.edge('pse', 'banco_ext')

    output = os.path.join(OUTPUT_DIR, 'credito-to-be')
    g.render(output, cleanup=True)
    print(f"  Generado: {output}.png")


if __name__ == '__main__':
    print("Generando diagramas de crédito...")
    create_credito_asis()
    create_credito_tobe()
    print("\nListo.")
