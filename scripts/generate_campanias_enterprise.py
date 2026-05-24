"""
Generador de diagramas de arquitectura TO-BE - Sistema de Campañas
Usa Graphviz para generar vistas enterprise-grade.
Ejecutar: python campanias-to-be-architecture.py
Requiere: pip install graphviz
"""

import os
from graphviz import Digraph

OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))

# Estilos compartidos
GRAPH_ATTRS = {
    'rankdir': 'TB',
    'splines': 'ortho',
    'nodesep': '0.8',
    'ranksep': '1.0',
    'fontname': 'Arial',
    'fontsize': '11',
    'bgcolor': 'white'
}

NODE_ATTRS = {
    'fontname': 'Arial',
    'fontsize': '10',
    'style': 'filled',
    'shape': 'box',
    'penwidth': '1.5'
}

EDGE_ATTRS = {
    'fontname': 'Arial',
    'fontsize': '9',
    'color': '#555555'
}

COLORS = {
    'primary': '#2D5F8A',
    'primary_fill': '#D6E8F5',
    'secondary': '#4A8C5C',
    'secondary_fill': '#D9F0E0',
    'external': '#8B4513',
    'external_fill': '#FDE8D0',
    'data': '#6B4C9A',
    'data_fill': '#E8DCF5',
    'security': '#C0392B',
    'security_fill': '#FADBD8',
    'person': '#1A5276',
    'person_fill': '#AED6F1',
}


def create_context_view():
    """Vista 1: Contexto y Capacidades de Negocio"""
    g = Digraph('context', format='png')
    g.attr(**GRAPH_ATTRS)
    g.attr('node', **NODE_ATTRS)
    g.attr('edge', **EDGE_ATTRS)
    g.attr(label='Vista de Contexto - Sistema de Campañas TO-BE\n\n', labelloc='t', fontsize='14', fontname='Arial Bold')

    # Actores
    with g.subgraph(name='cluster_actors') as c:
        c.attr(label='Actores', style='dashed', color='#888888')
        c.node('analista', 'Analista de\nCampañas', shape='box', fillcolor=COLORS['person_fill'], color=COLORS['person'])
        c.node('gerente', 'Gerente de\nRiesgo', shape='box', fillcolor=COLORS['person_fill'], color=COLORS['person'])
        c.node('cliente', 'Cliente\n(18-25 años)', shape='box', fillcolor=COLORS['person_fill'], color=COLORS['person'])

    # Sistema principal
    g.node('plataforma', 'Plataforma de Campañas TO-BE\n\n• Motor de Reglas Automatizado\n• Simulación de Campañas\n• Scoring Alternativo\n• Dashboard de Control\n• Notificación Multicanal\n• Histórico de Campañas',
           shape='box', style='filled,bold', fillcolor=COLORS['primary_fill'], color=COLORS['primary'], width='4')

    # Sistemas internos
    with g.subgraph(name='cluster_internal') as c:
        c.attr(label='Sistemas Internos del Banco', style='rounded', color=COLORS['primary'])
        c.node('core', 'Core Bancario\n(Host Transaccional)', fillcolor=COLORS['secondary_fill'], color=COLORS['secondary'])
        c.node('crm', 'CRM', fillcolor=COLORS['secondary_fill'], color=COLORS['secondary'])
        c.node('creditos', 'Sistema de\nCréditos', fillcolor=COLORS['secondary_fill'], color=COLORS['secondary'])

    # Proveedores externos
    with g.subgraph(name='cluster_external') as c:
        c.attr(label='Proveedores Externos', style='rounded', color=COLORS['external'])
        c.node('centrales', 'Centrales de\nRiesgo', fillcolor=COLORS['external_fill'], color=COLORS['external'])
        c.node('telcos', 'Operadores\nTelecomunicaciones', fillcolor=COLORS['external_fill'], color=COLORS['external'])
        c.node('otras_fin', 'Otras Entidades\nFinancieras', fillcolor=COLORS['external_fill'], color=COLORS['external'])
        c.node('notif', 'Proveedor\nNotificaciones\n(SMS/Email/Push)', fillcolor=COLORS['external_fill'], color=COLORS['external'])

    # Relaciones
    g.edge('analista', 'plataforma', label='Configura reglas\ny simulaciones')
    g.edge('gerente', 'plataforma', label='Aprueba campañas\ny revisa dashboard')
    g.edge('plataforma', 'core', label='Movimientos\ntransaccionales')
    g.edge('plataforma', 'crm', label='Datos de\nclientes')
    g.edge('plataforma', 'creditos', label='Reglas de\ncrédito')
    g.edge('plataforma', 'centrales', label='Scoring y\ncomportamiento')
    g.edge('plataforma', 'telcos', label='Comportamiento\ntelecom')
    g.edge('plataforma', 'otras_fin', label='Productos\nfinancieros')
    g.edge('plataforma', 'notif', label='Campañas\nmulticanal')
    g.edge('notif', 'cliente', label='SMS / Email / Push')

    output_path = os.path.join(OUTPUT_DIR, 'campanias-to-be-01-contexto')
    g.render(output_path, cleanup=True)
    print(f"  Generado: {output_path}.png")


def create_application_view():
    """Vista 2: Arquitectura de Aplicación / Software"""
    g = Digraph('application', format='png')
    g.attr(**GRAPH_ATTRS)
    g.attr('node', **NODE_ATTRS)
    g.attr('edge', **EDGE_ATTRS)
    g.attr(label='Vista de Aplicación - Sistema de Campañas TO-BE\n\n', labelloc='t', fontsize='14', fontname='Arial Bold')

    # Canales
    with g.subgraph(name='cluster_channels') as c:
        c.attr(label='Canales', style='rounded', color='#2980B9')
        c.node('portal', 'Portal Web\nAnalistas', fillcolor='#D6EAF8', color='#2980B9')
        c.node('dashboard', 'Dashboard\nGerencial', fillcolor='#D6EAF8', color='#2980B9')

    # API Layer
    with g.subgraph(name='cluster_api') as c:
        c.attr(label='Capa API / Experiencia', style='rounded', color='#1ABC9C')
        c.node('apigw', 'API Gateway', fillcolor='#D1F2EB', color='#1ABC9C')
        c.node('auth', 'Autenticación\nOAuth2/OIDC', fillcolor='#D1F2EB', color='#1ABC9C')

    # Core Services
    with g.subgraph(name='cluster_core') as c:
        c.attr(label='Servicios Core de Negocio', style='rounded', color=COLORS['primary'])
        c.node('reglas', 'Motor de Reglas\nSelección Público', fillcolor=COLORS['primary_fill'], color=COLORS['primary'])
        c.node('simulacion', 'Servicio de\nSimulación', fillcolor=COLORS['primary_fill'], color=COLORS['primary'])
        c.node('campania_svc', 'Gestión de\nCampañas', fillcolor=COLORS['primary_fill'], color=COLORS['primary'])
        c.node('scoring', 'Scoring\nAlternativo', fillcolor=COLORS['primary_fill'], color=COLORS['primary'])
        c.node('tracking', 'Tracking y\nEfectividad', fillcolor=COLORS['primary_fill'], color=COLORS['primary'])

    # Integration
    with g.subgraph(name='cluster_integration') as c:
        c.attr(label='Capa de Integración', style='rounded', color='#F39C12')
        c.node('esb_new', 'Bus de\nIntegración', fillcolor='#FEF9E7', color='#F39C12')
        c.node('event_bus', 'Event Bus\n(Asíncrono)', fillcolor='#FEF9E7', color='#F39C12')
        c.node('etl', 'Pipeline ETL\nIngesta Automatizada', fillcolor='#FEF9E7', color='#F39C12')

    # External
    with g.subgraph(name='cluster_ext') as c:
        c.attr(label='Sistemas Externos', style='rounded', color=COLORS['external'])
        c.node('core_app', 'Core Bancario', fillcolor=COLORS['external_fill'], color=COLORS['external'])
        c.node('crm_app', 'CRM', fillcolor=COLORS['external_fill'], color=COLORS['external'])
        c.node('cred_app', 'Créditos', fillcolor=COLORS['external_fill'], color=COLORS['external'])
        c.node('risk_app', 'Centrales\nde Riesgo', fillcolor=COLORS['external_fill'], color=COLORS['external'])
        c.node('telco_app', 'Telecom', fillcolor=COLORS['external_fill'], color=COLORS['external'])
        c.node('notif_app', 'Notificaciones\nSMS/Email/Push', fillcolor=COLORS['external_fill'], color=COLORS['external'])

    # Edges
    g.edge('portal', 'apigw')
    g.edge('dashboard', 'apigw')
    g.edge('apigw', 'auth')
    g.edge('apigw', 'reglas')
    g.edge('apigw', 'simulacion')
    g.edge('apigw', 'campania_svc')
    g.edge('apigw', 'tracking')
    g.edge('reglas', 'scoring')
    g.edge('reglas', 'esb_new')
    g.edge('simulacion', 'scoring')
    g.edge('campania_svc', 'event_bus')
    g.edge('campania_svc', 'notif_app')
    g.edge('tracking', 'event_bus')
    g.edge('esb_new', 'core_app')
    g.edge('esb_new', 'crm_app')
    g.edge('esb_new', 'cred_app')
    g.edge('etl', 'risk_app')
    g.edge('etl', 'telco_app')
    g.edge('scoring', 'etl')

    output_path = os.path.join(OUTPUT_DIR, 'campanias-to-be-02-aplicacion')
    g.render(output_path, cleanup=True)
    print(f"  Generado: {output_path}.png")


def create_infrastructure_view():
    """Vista 3: Arquitectura de Infraestructura Multinube"""
    g = Digraph('infrastructure', format='png')
    g.attr(**GRAPH_ATTRS)
    g.attr('node', **NODE_ATTRS)
    g.attr('edge', **EDGE_ATTRS)
    g.attr(label='Vista de Infraestructura Multinube - Sistema de Campañas TO-BE\n\n', labelloc='t', fontsize='14', fontname='Arial Bold')

    # Edge
    with g.subgraph(name='cluster_edge') as c:
        c.attr(label='Zona Pública (Edge)', style='rounded', color='#E74C3C')
        c.node('cdn', 'CDN / WAF', fillcolor='#FADBD8', color='#E74C3C')
        c.node('lb', 'Load Balancer', fillcolor='#FADBD8', color='#E74C3C')

    # Application Zone
    with g.subgraph(name='cluster_app') as c:
        c.attr(label='Zona de Aplicación (Cloud)', style='rounded', color=COLORS['primary'])
        c.node('containers', 'Contenedores\nMicroservicios', fillcolor=COLORS['primary_fill'], color=COLORS['primary'])
        c.node('serverless', 'Funciones Serverless\nProcesamiento Eventos', fillcolor=COLORS['primary_fill'], color=COLORS['primary'])
        c.node('apigw_i', 'API Gateway\nManaged', fillcolor=COLORS['primary_fill'], color=COLORS['primary'])
        c.node('mq', 'Message Queue\nEvent Bus', fillcolor=COLORS['primary_fill'], color=COLORS['primary'])

    # Data Zone
    with g.subgraph(name='cluster_data') as c:
        c.attr(label='Zona de Datos (Nube Privada)', style='rounded', color=COLORS['data'])
        c.node('db_ops', 'BD Operacional\nCampañas + Histórico', shape='cylinder', fillcolor=COLORS['data_fill'], color=COLORS['data'])
        c.node('db_analytics', 'BD Analítica\nDashboard + Reportes', shape='cylinder', fillcolor=COLORS['data_fill'], color=COLORS['data'])
        c.node('cache', 'Cache\nDistribuido', fillcolor=COLORS['data_fill'], color=COLORS['data'])
        c.node('storage', 'Object Storage\nArchivos y Logs', shape='cylinder', fillcolor=COLORS['data_fill'], color=COLORS['data'])

    # On-premise
    with g.subgraph(name='cluster_onprem') as c:
        c.attr(label='Zona On-Premise (Legacy)', style='rounded', color='#7F8C8D')
        c.node('core_i', 'Core Bancario', fillcolor='#EAECEE', color='#7F8C8D')
        c.node('crm_i', 'CRM Siebel', fillcolor='#EAECEE', color='#7F8C8D')
        c.node('cred_i', 'Sistema Créditos', fillcolor='#EAECEE', color='#7F8C8D')
        c.node('esb_i', 'ESB IBM IB', fillcolor='#EAECEE', color='#7F8C8D')

    # Observability
    with g.subgraph(name='cluster_obs') as c:
        c.attr(label='Observabilidad', style='rounded', color='#27AE60')
        c.node('mon', 'Monitoreo\ny Alertas', fillcolor='#D5F5E3', color='#27AE60')
        c.node('log', 'Logging\nCentralizado', fillcolor='#D5F5E3', color='#27AE60')
        c.node('trace', 'Tracing\nDistribuido', fillcolor='#D5F5E3', color='#27AE60')

    # Edges
    g.edge('cdn', 'lb')
    g.edge('lb', 'apigw_i')
    g.edge('apigw_i', 'containers')
    g.edge('containers', 'mq')
    g.edge('containers', 'db_ops')
    g.edge('containers', 'cache')
    g.edge('mq', 'serverless')
    g.edge('serverless', 'db_analytics')
    g.edge('serverless', 'storage')
    g.edge('containers', 'esb_i')
    g.edge('esb_i', 'core_i')
    g.edge('esb_i', 'crm_i')
    g.edge('esb_i', 'cred_i')
    g.edge('containers', 'mon')
    g.edge('containers', 'log')
    g.edge('containers', 'trace')

    output_path = os.path.join(OUTPUT_DIR, 'campanias-to-be-03-infraestructura')
    g.render(output_path, cleanup=True)
    print(f"  Generado: {output_path}.png")


def create_security_view():
    """Vista 4: Arquitectura de Seguridad"""
    g = Digraph('security', format='png')
    g.attr(**GRAPH_ATTRS)
    g.attr('node', **NODE_ATTRS)
    g.attr('edge', **EDGE_ATTRS)
    g.attr(label='Vista de Seguridad - Sistema de Campañas TO-BE\n\n', labelloc='t', fontsize='14', fontname='Arial Bold')

    # Identity
    with g.subgraph(name='cluster_identity') as c:
        c.attr(label='Identidad y Acceso', style='rounded', color=COLORS['security'])
        c.node('iam', 'IAM / IdP', fillcolor=COLORS['security_fill'], color=COLORS['security'])
        c.node('mfa', 'MFA', fillcolor=COLORS['security_fill'], color=COLORS['security'])
        c.node('rbac', 'RBAC', fillcolor=COLORS['security_fill'], color=COLORS['security'])
        c.node('ad_sec', 'Active Directory', fillcolor=COLORS['security_fill'], color=COLORS['security'])

    # Edge Protection
    with g.subgraph(name='cluster_edge_sec') as c:
        c.attr(label='Protección de Borde', style='rounded', color='#E67E22')
        c.node('waf', 'WAF', fillcolor='#FDEBD0', color='#E67E22')
        c.node('ddos', 'Anti-DDoS', fillcolor='#FDEBD0', color='#E67E22')
        c.node('rate', 'Rate Limiting\nThrottling', fillcolor='#FDEBD0', color='#E67E22')
        c.node('tls', 'TLS 1.3\nEnd-to-End', fillcolor='#FDEBD0', color='#E67E22')

    # App Controls
    with g.subgraph(name='cluster_app_sec') as c:
        c.attr(label='Controles de Aplicación', style='rounded', color=COLORS['primary'])
        c.node('oauth', 'OAuth2/OIDC\nJWT', fillcolor=COLORS['primary_fill'], color=COLORS['primary'])
        c.node('encrypt_t', 'Cifrado en\nTránsito', fillcolor=COLORS['primary_fill'], color=COLORS['primary'])
        c.node('input_val', 'Validación\nde Entrada', fillcolor=COLORS['primary_fill'], color=COLORS['primary'])
        c.node('audit', 'Auditoría\nde Acciones', fillcolor=COLORS['primary_fill'], color=COLORS['primary'])

    # Platform Controls
    with g.subgraph(name='cluster_plat_sec') as c:
        c.attr(label='Controles de Plataforma', style='rounded', color=COLORS['secondary'])
        c.node('netseg', 'Segmentación\nde Red', fillcolor=COLORS['secondary_fill'], color=COLORS['secondary'])
        c.node('secgroups', 'Security Groups\nNACLs', fillcolor=COLORS['secondary_fill'], color=COLORS['secondary'])
        c.node('secrets', 'Gestión de\nSecretos (Vault)', fillcolor=COLORS['secondary_fill'], color=COLORS['secondary'])
        c.node('patch', 'Gestión de\nParches', fillcolor=COLORS['secondary_fill'], color=COLORS['secondary'])

    # Data Protection
    with g.subgraph(name='cluster_data_sec') as c:
        c.attr(label='Protección de Datos', style='rounded', color=COLORS['data'])
        c.node('encrypt_r', 'Cifrado en Reposo\nAES-256', fillcolor=COLORS['data_fill'], color=COLORS['data'])
        c.node('mask', 'Enmascaramiento\nPII', fillcolor=COLORS['data_fill'], color=COLORS['data'])
        c.node('backup_sec', 'Backup y\nRecuperación', fillcolor=COLORS['data_fill'], color=COLORS['data'])
        c.node('dlp', 'Prevención Fuga\nde Datos (DLP)', fillcolor=COLORS['data_fill'], color=COLORS['data'])

    # Detection
    with g.subgraph(name='cluster_detect') as c:
        c.attr(label='Detección y Respuesta', style='rounded', color='#8E44AD')
        c.node('siem', 'SIEM', fillcolor='#F4ECF7', color='#8E44AD')
        c.node('ids', 'IDS/IPS', fillcolor='#F4ECF7', color='#8E44AD')
        c.node('incident', 'Respuesta a\nIncidentes', fillcolor='#F4ECF7', color='#8E44AD')
        c.node('vuln', 'Escaneo\nVulnerabilidades', fillcolor='#F4ECF7', color='#8E44AD')

    # Flow
    g.edge('iam', 'mfa')
    g.edge('iam', 'rbac')
    g.edge('iam', 'ad_sec')
    g.edge('waf', 'rate')
    g.edge('rate', 'oauth')
    g.edge('oauth', 'encrypt_t')
    g.edge('netseg', 'secgroups')
    g.edge('encrypt_r', 'mask')
    g.edge('siem', 'ids')
    g.edge('ids', 'incident')

    output_path = os.path.join(OUTPUT_DIR, 'campanias-to-be-04-seguridad')
    g.render(output_path, cleanup=True)
    print(f"  Generado: {output_path}.png")


if __name__ == '__main__':
    print("Generando diagramas de arquitectura TO-BE...")
    create_context_view()
    create_application_view()
    create_infrastructure_view()
    create_security_view()
    print("\nTodos los diagramas generados exitosamente.")
