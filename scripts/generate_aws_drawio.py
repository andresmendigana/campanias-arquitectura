"""Genera archivo .drawio con stencils AWS4 para la arquitectura serverless."""
import os

OUTPUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "campanias-serverless-aws-gcp.drawio")

def aws_icon(id, label, x, y, res_icon, fill, w=60, h=60):
    return (f'        <mxCell id="{id}" value="{label}" style="sketch=0;points=[[0,0,0],[0.25,0,0],[0.5,0,0],'
            f'[0.75,0,0],[1,0,0],[0,1,0],[0.25,1,0],[0.5,1,0],[0.75,1,0],[1,1,0],[0,0.25,0],[0,0.5,0],'
            f'[0,0.75,0],[1,0.25,0],[1,0.5,0],[1,0.75,0]];outlineConnect=0;fontColor=#232F3E;'
            f'fillColor={fill};align=center;html=1;fontSize=8;fontStyle=0;aspect=fixed;'
            f'shape=mxgraph.aws4.resourceIcon;resIcon={res_icon};'
            f'verticalLabelPosition=bottom;verticalAlign=top;labelPosition=center;" '
            f'vertex="1" parent="1"><mxGeometry x="{x}" y="{y}" width="{w}" height="{h}" as="geometry" /></mxCell>\n')

def aws_group(id, label, x, y, w, h, gr_icon, stroke):
    return (f'        <mxCell id="{id}" value="{label}" style="points=[[0,0],[0.25,0],[0.5,0],[0.75,0],[1,0],'
            f'[1,0.25],[1,0.5],[1,0.75],[1,1],[0.75,1],[0.5,1],[0.25,1],[0,1],[0,0.75],[0,0.5],[0,0.25]];'
            f'outlineConnect=0;html=1;whiteSpace=wrap;fontSize=10;fontStyle=1;'
            f'shape=mxgraph.aws4.group;grIcon={gr_icon};strokeColor={stroke};fillColor=none;'
            f'verticalAlign=top;align=left;spacingLeft=30;dashed=0;rounded=1;" '
            f'vertex="1" parent="1"><mxGeometry x="{x}" y="{y}" width="{w}" height="{h}" as="geometry" /></mxCell>\n')

def gcp_rect(id, label, x, y, w, h, fill="#E8F5E9", stroke="#34A853"):
    return (f'        <mxCell id="{id}" value="{label}" style="rounded=1;whiteSpace=wrap;html=1;'
            f'fillColor={fill};strokeColor={stroke};fontStyle=1;fontSize=9;" '
            f'vertex="1" parent="1"><mxGeometry x="{x}" y="{y}" width="{w}" height="{h}" as="geometry" /></mxCell>\n')

def ext_rect(id, label, x, y, w=120, h=50, fill="#FDE8D0", stroke="#8B4513"):
    return (f'        <mxCell id="{id}" value="{label}" style="rounded=1;whiteSpace=wrap;html=1;'
            f'fillColor={fill};strokeColor={stroke};fontStyle=1;fontSize=9;" '
            f'vertex="1" parent="1"><mxGeometry x="{x}" y="{y}" width="{w}" height="{h}" as="geometry" /></mxCell>\n')

def person(id, label, x, y):
    return (f'        <mxCell id="{id}" value="{label}" style="rounded=1;whiteSpace=wrap;html=1;'
            f'fillColor=#AED6F1;strokeColor=#1A5276;fontStyle=1;fontSize=9;" '
            f'vertex="1" parent="1"><mxGeometry x="{x}" y="{y}" width="100" height="50" as="geometry" /></mxCell>\n')

def edge(id, src, tgt, label="", dashed=False):
    style = "edgeStyle=orthogonalEdgeStyle;rounded=1;"
    if dashed:
        style += "dashed=1;"
    return (f'        <mxCell id="{id}" value="{label}" style="{style}" '
            f'edge="1" source="{src}" target="{tgt}" parent="1">'
            f'<mxGeometry relative="1" as="geometry" /></mxCell>\n')

# Build
c = '<?xml version="1.0" encoding="UTF-8"?>\n<mxfile host="app.diagrams.net" pages="1">\n'
c += '  <diagram id="aws_serverless" name="Arquitectura Serverless AWS+GCP">\n'
c += '    <mxGraphModel dx="2000" dy="1200" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="2200" pageHeight="1400" math="0" shadow="0">\n'
c += '      <root>\n        <mxCell id="0" />\n        <mxCell id="1" parent="0" />\n'

# Title
c += '        <mxCell id="title" value="Sistema de Campañas TO-BE - Arquitectura Serverless (AWS + GCP)" style="text;html=1;align=center;verticalAlign=middle;fontSize=16;fontStyle=1" vertex="1" parent="1"><mxGeometry x="600" y="20" width="700" height="30" as="geometry" /></mxCell>\n'

# Actores
c += person("p1", "Analista de\\nCampañas", 30, 200)
c += person("p2", "Gerente de\\nRiesgo", 30, 350)
c += person("p3", "Cliente\\n(18-25 años)", 2050, 600)

# AWS Cloud Group
c += aws_group("aws_cloud", "AWS Cloud", 200, 70, 1200, 900, "mxgraph.aws4.group_aws_cloud_alt", "#232F3E")

# Edge
c += aws_icon("r53", "Route 53", 230, 250, "mxgraph.aws4.route_53", "#8C4FFF", 50, 50)
c += aws_icon("cf", "CloudFront", 310, 250, "mxgraph.aws4.cloudfront", "#8C4FFF", 50, 50)
c += aws_icon("waf", "WAF", 390, 250, "mxgraph.aws4.waf", "#DD344C", 50, 50)

# Auth
c += aws_icon("cog", "Cognito", 390, 130, "mxgraph.aws4.cognito", "#DD344C", 50, 50)

# API Gateway
c += aws_icon("apigw", "API Gateway", 490, 250, "mxgraph.aws4.api_gateway", "#E7157B", 50, 50)

# Lambdas
c += aws_icon("l_reg", "Lambda\\nMotor Reglas", 620, 130, "mxgraph.aws4.lambda_function", "#ED7100", 50, 50)
c += aws_icon("l_sim", "Lambda\\nSimulación", 620, 220, "mxgraph.aws4.lambda_function", "#ED7100", 50, 50)
c += aws_icon("l_camp", "Lambda\\nGestión Campañas", 620, 310, "mxgraph.aws4.lambda_function", "#ED7100", 50, 50)
c += aws_icon("l_score", "Lambda\\nScoring", 750, 130, "mxgraph.aws4.lambda_function", "#ED7100", 50, 50)
c += aws_icon("l_notif", "Lambda\\nNotificaciones", 750, 400, "mxgraph.aws4.lambda_function", "#ED7100", 50, 50)
c += aws_icon("l_track", "Lambda\\nTracking", 750, 500, "mxgraph.aws4.lambda_function", "#ED7100", 50, 50)

# Step Functions
c += aws_icon("sf1", "Step Functions\\nAprobación", 620, 400, "mxgraph.aws4.step_functions", "#E7157B", 50, 50)
c += aws_icon("sf2", "Step Functions\\nEjecución", 620, 500, "mxgraph.aws4.step_functions", "#E7157B", 50, 50)

# Event-driven
c += aws_icon("eb", "EventBridge", 880, 310, "mxgraph.aws4.eventbridge", "#E7157B", 50, 50)
c += aws_icon("sqs", "SQS", 880, 420, "mxgraph.aws4.sqs", "#E7157B", 50, 50)
c += aws_icon("sns", "SNS", 880, 530, "mxgraph.aws4.sns", "#E7157B", 50, 50)

# Data
c += aws_icon("ddb1", "DynamoDB\\nCampañas", 1000, 130, "mxgraph.aws4.dynamodb", "#3334B9", 50, 50)
c += aws_icon("ddb2", "DynamoDB\\nTracking", 1000, 250, "mxgraph.aws4.dynamodb", "#3334B9", 50, 50)
c += aws_icon("s3", "S3\\nDocs & Logs", 1000, 370, "mxgraph.aws4.s3", "#277116", 50, 50)

# Kinesis
c += aws_icon("kf", "Kinesis Firehose", 1130, 250, "mxgraph.aws4.kinesis_data_firehose", "#8C4FFF", 50, 50)

# ESB Bridge
c += aws_icon("l_esb", "Lambda\\nESB Bridge", 880, 130, "mxgraph.aws4.lambda_function", "#ED7100", 50, 50)

# CloudWatch
c += aws_icon("cw", "CloudWatch", 1130, 500, "mxgraph.aws4.cloudwatch", "#E7157B", 50, 50)

# GCP Group
c += '        <mxCell id="gcp_group" value="GCP - Analítica &amp; Dashboards" style="rounded=1;whiteSpace=wrap;html=1;fillColor=none;strokeColor=#34A853;dashed=1;verticalAlign=top;fontStyle=1;fontSize=11;" vertex="1" parent="1"><mxGeometry x="1450" y="150" width="350" height="300" as="geometry" /></mxCell>\n'
c += gcp_rect("df", "Dataflow\\nETL", 1480, 220, 100, 50)
c += gcp_rect("bq", "BigQuery\\nHistórico", 1480, 310, 100, 50)
c += gcp_rect("lk", "Looker\\nDashboard Mensual\\nApetito de Riesgo", 1630, 310, 130, 60)

# On-Premise
c += '        <mxCell id="onprem_g" value="On-Premise" style="rounded=1;whiteSpace=wrap;html=1;fillColor=none;strokeColor=#7F8C8D;dashed=1;verticalAlign=top;fontStyle=1;fontSize=11;" vertex="1" parent="1"><mxGeometry x="1450" y="520" width="350" height="100" as="geometry" /></mxCell>\n'
c += ext_rect("core", "Core Bancario", 1470, 550, 100, 40, "#EAECEE", "#7F8C8D")
c += ext_rect("crm_d", "CRM", 1580, 550, 80, 40, "#EAECEE", "#7F8C8D")
c += ext_rect("cred_d", "Créditos", 1670, 550, 80, 40, "#EAECEE", "#7F8C8D")

# Proveedores Externos
c += '        <mxCell id="ext_g" value="Proveedores Externos" style="rounded=1;whiteSpace=wrap;html=1;fillColor=none;strokeColor=#8B4513;dashed=1;verticalAlign=top;fontStyle=1;fontSize=11;" vertex="1" parent="1"><mxGeometry x="1450" y="660" width="500" height="100" as="geometry" /></mxCell>\n'
c += ext_rect("cr", "Centrales\\nde Riesgo", 1470, 690, 100, 45)
c += ext_rect("tel", "Telecomunicaciones", 1580, 690, 110, 45)
c += ext_rect("oef", "Otras Entidades\\nFinancieras", 1700, 690, 110, 45)
c += ext_rect("pn", "Proveedor\\nNotificaciones", 1820, 690, 110, 45)

# Edges - Flow
c += edge("e1", "p1", "r53", "HTTPS")
c += edge("e2", "p2", "r53", "HTTPS")
c += edge("e3", "r53", "cf")
c += edge("e4", "cf", "waf")
c += edge("e5", "waf", "apigw")
c += edge("e6", "apigw", "cog", "", True)
c += edge("e7", "apigw", "l_reg")
c += edge("e8", "apigw", "l_sim")
c += edge("e9", "apigw", "l_camp")
c += edge("e10", "l_reg", "l_score")
c += edge("e11", "l_camp", "sf1")
c += edge("e12", "sf1", "l_score")
c += edge("e13", "sf1", "sf2")
c += edge("e14", "sf2", "l_notif")
c += edge("e15", "l_camp", "eb")
c += edge("e16", "l_notif", "sqs")
c += edge("e17", "sqs", "l_track")
c += edge("e18", "eb", "l_track")
c += edge("e19", "l_reg", "ddb1")
c += edge("e20", "l_camp", "ddb1")
c += edge("e21", "l_track", "ddb2")
c += edge("e22", "l_camp", "s3")
c += edge("e23", "ddb2", "kf")
c += edge("e24", "kf", "df")
c += edge("e25", "df", "bq")
c += edge("e26", "bq", "lk")
c += edge("e27", "l_score", "l_esb")
c += edge("e28", "l_esb", "core")
c += edge("e29", "l_esb", "crm_d")
c += edge("e30", "l_esb", "cred_d")
c += edge("e31", "l_score", "cr", "Scoring", True)
c += edge("e32", "l_score", "tel", "Comportamiento", True)
c += edge("e33", "l_score", "oef", "Productos", True)
c += edge("e34", "l_notif", "pn")
c += edge("e35", "pn", "p3", "SMS/Email/Push")
c += edge("e36", "lk", "p2", "Dashboard")

c += '      </root>\n    </mxGraphModel>\n  </diagram>\n</mxfile>\n'

with open(OUTPUT, 'w', encoding='utf-8') as f:
    f.write(c)
print(f"Generado: {OUTPUT}")
