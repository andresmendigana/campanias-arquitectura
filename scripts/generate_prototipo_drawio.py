"""Genera .drawio del prototipo - v3 layout limpio sin solapamiento."""
import os

OUTPUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'diagramas', 'to-be', 'CAM-TOBE-07-prototipo-aws.drawio')

content = '''<?xml version="1.0" encoding="UTF-8"?>
<mxfile host="app.diagrams.net" pages="1">
  <diagram id="proto_v3" name="Prototipo Serverless AWS">
    <mxGraphModel dx="1800" dy="1200" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="1800" pageHeight="1200" math="0" shadow="0">
      <root>
        <mxCell id="0" />
        <mxCell id="1" parent="0" />

        <!-- Title -->
        <mxCell id="title" value="Prototipo Serverless - Sistema de Campañas (AWS)" style="text;html=1;align=center;verticalAlign=middle;fontSize=16;fontStyle=1;fontColor=#232F3E;" vertex="1" parent="1">
          <mxGeometry x="550" y="20" width="500" height="30" as="geometry" />
        </mxCell>

        <!-- AWS Cloud Group -->
        <mxCell id="aws_cloud" value="AWS Cloud" style="points=[[0,0],[0.25,0],[0.5,0],[0.75,0],[1,0],[1,0.25],[1,0.5],[1,0.75],[1,1],[0.75,1],[0.5,1],[0.25,1],[0,1],[0,0.75],[0,0.5],[0,0.25]];outlineConnect=0;html=1;whiteSpace=wrap;fontSize=11;fontStyle=1;shape=mxgraph.aws4.group;grIcon=mxgraph.aws4.group_aws_cloud_alt;strokeColor=#232F3E;fillColor=none;verticalAlign=top;align=left;spacingLeft=30;dashed=0;rounded=1;" vertex="1" parent="1">
          <mxGeometry x="220" y="70" width="1500" height="1080" as="geometry" />
        </mxCell>

        <!-- CLIENT (outside AWS) -->
        <mxCell id="client" value="Cliente HTTP&#xa;(PowerShell)" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#DBEEF4;strokeColor=#1A5276;fontStyle=1;fontSize=10;" vertex="1" parent="1">
          <mxGeometry x="40" y="500" width="120" height="60" as="geometry" />
        </mxCell>

        <!-- COL 1: API Gateway (x=300) -->
        <mxCell id="apigw" value="API Gateway&#xa;Campanias API" style="sketch=0;outlineConnect=0;fontColor=#232F3E;fillColor=#E7157B;align=center;html=1;fontSize=9;fontStyle=0;aspect=fixed;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.api_gateway;verticalLabelPosition=bottom;verticalAlign=top;labelPosition=center;spacingTop=4;" vertex="1" parent="1">
          <mxGeometry x="300" y="506" width="48" height="48" as="geometry" />
        </mxCell>

        <!-- COL 2: Lambdas (x=550) - 3 rows spread at y=200, y=500, y=830 -->
        <mxCell id="fn_gestion" value="campanias-gestion&#xa;CRUD Campañas" style="sketch=0;outlineConnect=0;fontColor=#232F3E;fillColor=#ED7100;align=center;html=1;fontSize=9;fontStyle=0;aspect=fixed;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.lambda_function;verticalLabelPosition=bottom;verticalAlign=top;labelPosition=center;spacingTop=4;" vertex="1" parent="1">
          <mxGeometry x="550" y="200" width="48" height="48" as="geometry" />
        </mxCell>

        <mxCell id="fn_reglas" value="campanias-reglas&#xa;Motor de Reglas" style="sketch=0;outlineConnect=0;fontColor=#232F3E;fillColor=#ED7100;align=center;html=1;fontSize=9;fontStyle=0;aspect=fixed;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.lambda_function;verticalLabelPosition=bottom;verticalAlign=top;labelPosition=center;spacingTop=4;" vertex="1" parent="1">
          <mxGeometry x="550" y="506" width="48" height="48" as="geometry" />
        </mxCell>

        <mxCell id="fn_tracking" value="campanias-tracking&#xa;Auditoría" style="sketch=0;outlineConnect=0;fontColor=#232F3E;fillColor=#ED7100;align=center;html=1;fontSize=9;fontStyle=0;aspect=fixed;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.lambda_function;verticalLabelPosition=bottom;verticalAlign=top;labelPosition=center;spacingTop=4;" vertex="1" parent="1">
          <mxGeometry x="550" y="830" width="48" height="48" as="geometry" />
        </mxCell>

        <!-- COL 3: EventBridge + SQS (x=850) -->
        <mxCell id="eventbridge" value="EventBridge&#xa;campanias-events" style="sketch=0;outlineConnect=0;fontColor=#232F3E;fillColor=#E7157B;align=center;html=1;fontSize=9;fontStyle=0;aspect=fixed;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.eventbridge;verticalLabelPosition=bottom;verticalAlign=top;labelPosition=center;spacingTop=4;" vertex="1" parent="1">
          <mxGeometry x="850" y="200" width="48" height="48" as="geometry" />
        </mxCell>

        <mxCell id="sqs" value="SQS&#xa;campanias-notifications" style="sketch=0;outlineConnect=0;fontColor=#232F3E;fillColor=#E7157B;align=center;html=1;fontSize=9;fontStyle=0;aspect=fixed;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.sqs;verticalLabelPosition=bottom;verticalAlign=top;labelPosition=center;spacingTop=4;" vertex="1" parent="1">
          <mxGeometry x="850" y="506" width="48" height="48" as="geometry" />
        </mxCell>

        <!-- COL 4: DynamoDB (x=1150) -->
        <mxCell id="ddb_camp" value="DynamoDB&#xa;campanias-campaigns" style="sketch=0;outlineConnect=0;fontColor=#232F3E;fillColor=#3334B9;align=center;html=1;fontSize=9;fontStyle=0;aspect=fixed;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.dynamodb;verticalLabelPosition=bottom;verticalAlign=top;labelPosition=center;spacingTop=4;" vertex="1" parent="1">
          <mxGeometry x="1150" y="350" width="48" height="48" as="geometry" />
        </mxCell>

        <mxCell id="ddb_track" value="DynamoDB&#xa;campanias-tracking" style="sketch=0;outlineConnect=0;fontColor=#232F3E;fillColor=#3334B9;align=center;html=1;fontSize=9;fontStyle=0;aspect=fixed;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.dynamodb;verticalLabelPosition=bottom;verticalAlign=top;labelPosition=center;spacingTop=4;" vertex="1" parent="1">
          <mxGeometry x="1150" y="830" width="48" height="48" as="geometry" />
        </mxCell>

        <!-- COL 5: CloudWatch (x=1450) -->
        <mxCell id="cw" value="CloudWatch&#xa;Logs &amp; Metrics" style="sketch=0;outlineConnect=0;fontColor=#232F3E;fillColor=#E7157B;align=center;html=1;fontSize=9;fontStyle=0;aspect=fixed;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.cloudwatch;verticalLabelPosition=bottom;verticalAlign=top;labelPosition=center;spacingTop=4;" vertex="1" parent="1">
          <mxGeometry x="1450" y="506" width="48" height="48" as="geometry" />
        </mxCell>

        <!-- EDGES: Simple horizontal/vertical flows -->

        <!-- Client -> API Gateway -->
        <mxCell id="e1" value="HTTPS" style="edgeStyle=orthogonalEdgeStyle;rounded=1;fontSize=9;exitX=1;exitY=0.5;exitDx=0;exitDy=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0;" edge="1" source="client" target="apigw" parent="1">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>

        <!-- API GW -> Lambda gestion (up-right) -->
        <mxCell id="e2" value="POST/GET /campaigns" style="edgeStyle=orthogonalEdgeStyle;rounded=1;fontSize=8;exitX=0.5;exitY=0;exitDx=0;exitDy=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0;" edge="1" source="apigw" target="fn_gestion" parent="1">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>

        <!-- API GW -> Lambda reglas (right, same row) -->
        <mxCell id="e3" value="POST /{id}/evaluate" style="edgeStyle=orthogonalEdgeStyle;rounded=1;fontSize=8;exitX=1;exitY=0.5;exitDx=0;exitDy=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0;" edge="1" source="apigw" target="fn_reglas" parent="1">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>

        <!-- Lambda gestion -> EventBridge (right, same row) -->
        <mxCell id="e5" value="PutEvents" style="edgeStyle=orthogonalEdgeStyle;rounded=1;fontSize=8;exitX=1;exitY=0.5;exitDx=0;exitDy=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0;" edge="1" source="fn_gestion" target="eventbridge" parent="1">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>

        <!-- Lambda gestion -> DynamoDB campaigns -->
        <mxCell id="e4" value="PUT / GET" style="edgeStyle=orthogonalEdgeStyle;rounded=1;fontSize=8;exitX=1;exitY=1;exitDx=0;exitDy=0;entryX=0;entryY=0;entryDx=0;entryDy=0;" edge="1" source="fn_gestion" target="ddb_camp" parent="1">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>

        <!-- Lambda gestion -> SQS -->
        <mxCell id="e6" value="SendMessage" style="edgeStyle=orthogonalEdgeStyle;rounded=1;fontSize=8;exitX=0.5;exitY=1;exitDx=0;exitDy=0;entryX=0.5;entryY=0;entryDx=0;entryDy=0;" edge="1" source="fn_gestion" target="sqs" parent="1">
          <mxGeometry relative="1" as="geometry">
            <Array as="points">
              <mxPoint x="574" y="430" />
              <mxPoint x="874" y="430" />
            </Array>
          </mxGeometry>
        </mxCell>

        <!-- Lambda reglas -> DynamoDB campaigns -->
        <mxCell id="e7" value="GET / UPDATE" style="edgeStyle=orthogonalEdgeStyle;rounded=1;fontSize=8;exitX=1;exitY=0.5;exitDx=0;exitDy=0;entryX=0;entryY=1;entryDx=0;entryDy=0;" edge="1" source="fn_reglas" target="ddb_camp" parent="1">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>

        <!-- EventBridge -> Lambda tracking -->
        <mxCell id="e8" value="Rule trigger" style="edgeStyle=orthogonalEdgeStyle;rounded=1;fontSize=8;exitX=0.5;exitY=1;exitDx=0;exitDy=0;entryX=0.5;entryY=0;entryDx=0;entryDy=0;" edge="1" source="eventbridge" target="fn_tracking" parent="1">
          <mxGeometry relative="1" as="geometry">
            <Array as="points">
              <mxPoint x="874" y="750" />
              <mxPoint x="574" y="750" />
            </Array>
          </mxGeometry>
        </mxCell>

        <!-- Lambda tracking -> DynamoDB tracking -->
        <mxCell id="e9" value="PUT" style="edgeStyle=orthogonalEdgeStyle;rounded=1;fontSize=8;exitX=1;exitY=0.5;exitDx=0;exitDy=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0;" edge="1" source="fn_tracking" target="ddb_track" parent="1">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>

        <!-- CloudWatch (dashed, single line from center) -->
        <mxCell id="e10" value="Logs" style="edgeStyle=orthogonalEdgeStyle;rounded=1;fontSize=8;dashed=1;strokeColor=#999999;exitX=1;exitY=0.5;exitDx=0;exitDy=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0;" edge="1" source="sqs" target="cw" parent="1">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>

        <!-- Note -->
        <mxCell id="note" value="Todos los componentes envían logs a CloudWatch.&#xa;Línea punteada representa flujo de observabilidad." style="shape=note;whiteSpace=wrap;html=1;size=14;verticalAlign=top;align=left;fontSize=9;fillColor=#FFF3CD;strokeColor=#856404;" vertex="1" parent="1">
          <mxGeometry x="1350" y="650" width="250" height="60" as="geometry" />
        </mxCell>

      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
'''

with open(OUTPUT, 'w', encoding='utf-8') as f:
    f.write(content)
print(f"Generado: {OUTPUT}")
