"""Genera .drawio del prototipo AS-IS con grupos verde claro como en la version Python."""
import os

OUTPUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'diagramas', 'as-is', 'PRO-ASIS-01-prototipo-implementado.drawio')

# Color verde claro para los grupos (como en la version Python)
GROUP_FILL = "#F5F5DC"  # Beige/verde muy claro como en el PNG
GROUP_STROKE = "#B8B894"

content = '''<?xml version="1.0" encoding="UTF-8"?>
<mxfile host="app.diagrams.net" pages="1">
  <diagram id="proto_asis" name="Prototipo Implementado AS-IS">
    <mxGraphModel dx="1800" dy="1200" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="1800" pageHeight="1200" math="0" shadow="0">
      <root>
        <mxCell id="0" />
        <mxCell id="1" parent="0" />

        <!-- Title -->
        <mxCell id="title" value="Prototipo Implementado (AS-IS) - Solo componentes desplegados" style="text;html=1;align=center;verticalAlign=middle;fontSize=16;fontStyle=1;fontColor=#232F3E;" vertex="1" parent="1">
          <mxGeometry x="400" y="20" width="600" height="30" as="geometry" />
        </mxCell>

        <!-- AWS Cloud Group -->
        <mxCell id="aws_cloud" value="AWS Cloud - us-east-1" style="points=[[0,0],[0.25,0],[0.5,0],[0.75,0],[1,0],[1,0.25],[1,0.5],[1,0.75],[1,1],[0.75,1],[0.5,1],[0.25,1],[0,1],[0,0.75],[0,0.5],[0,0.25]];outlineConnect=0;html=1;whiteSpace=wrap;fontSize=11;fontStyle=1;shape=mxgraph.aws4.group;grIcon=mxgraph.aws4.group_aws_cloud_alt;strokeColor=#232F3E;fillColor=none;verticalAlign=top;align=left;spacingLeft=30;dashed=0;rounded=1;" vertex="1" parent="1">
          <mxGeometry x="220" y="70" width="1450" height="1050" as="geometry" />
        </mxCell>

        <!-- CLIENT (outside AWS) -->
        <mxCell id="client" value="PowerShell&#xa;(Invoke-RestMethod)" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#DBEEF4;strokeColor=#1A5276;fontStyle=1;fontSize=10;" vertex="1" parent="1">
          <mxGeometry x="40" y="530" width="130" height="60" as="geometry" />
        </mxCell>

        <!-- API Gateway (no group, standalone) -->
        <mxCell id="apigw" value="API Gateway&#xa;Campanias API&#xa;/prod/campaigns" style="sketch=0;outlineConnect=0;fontColor=#232F3E;fillColor=#E7157B;align=center;html=1;fontSize=9;fontStyle=0;aspect=fixed;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.api_gateway;verticalLabelPosition=bottom;verticalAlign=top;labelPosition=center;spacingTop=4;" vertex="1" parent="1">
          <mxGeometry x="280" y="536" width="48" height="48" as="geometry" />
        </mxCell>

        <!-- GROUP: Lambda Functions (verde claro) -->
        <mxCell id="grp_lambda" value="Lambda Functions (Node.js 22)" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#F5F5DC;strokeColor=#B8B894;verticalAlign=top;fontStyle=1;fontSize=10;arcSize=4;" vertex="1" parent="1">
          <mxGeometry x="450" y="100" width="250" height="950" as="geometry" />
        </mxCell>

        <mxCell id="fn_tracking" value="campanias-tracking&#xa;Registrar evento" style="sketch=0;outlineConnect=0;fontColor=#232F3E;fillColor=#ED7100;align=center;html=1;fontSize=9;fontStyle=0;aspect=fixed;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.lambda_function;verticalLabelPosition=bottom;verticalAlign=top;labelPosition=center;spacingTop=4;" vertex="1" parent="1">
          <mxGeometry x="540" y="200" width="48" height="48" as="geometry" />
        </mxCell>

        <mxCell id="fn_reglas" value="campanias-reglas&#xa;Evaluar + Update" style="sketch=0;outlineConnect=0;fontColor=#232F3E;fillColor=#ED7100;align=center;html=1;fontSize=9;fontStyle=0;aspect=fixed;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.lambda_function;verticalLabelPosition=bottom;verticalAlign=top;labelPosition=center;spacingTop=4;" vertex="1" parent="1">
          <mxGeometry x="540" y="500" width="48" height="48" as="geometry" />
        </mxCell>

        <mxCell id="fn_gestion" value="campanias-gestion&#xa;CRUD + PutEvents" style="sketch=0;outlineConnect=0;fontColor=#232F3E;fillColor=#ED7100;align=center;html=1;fontSize=9;fontStyle=0;aspect=fixed;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.lambda_function;verticalLabelPosition=bottom;verticalAlign=top;labelPosition=center;spacingTop=4;" vertex="1" parent="1">
          <mxGeometry x="540" y="800" width="48" height="48" as="geometry" />
        </mxCell>

        <!-- GROUP: DynamoDB (verde claro) -->
        <mxCell id="grp_dynamo" value="DynamoDB (PAY_PER_REQUEST)" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#F5F5DC;strokeColor=#B8B894;verticalAlign=top;fontStyle=1;fontSize=10;arcSize=4;" vertex="1" parent="1">
          <mxGeometry x="900" y="100" width="250" height="650" as="geometry" />
        </mxCell>

        <mxCell id="ddb_track" value="campanias-tracking&#xa;Partition: campaignId&#xa;Sort: clientId" style="sketch=0;outlineConnect=0;fontColor=#232F3E;fillColor=#3334B9;align=center;html=1;fontSize=9;fontStyle=0;aspect=fixed;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.dynamodb;verticalLabelPosition=bottom;verticalAlign=top;labelPosition=center;spacingTop=4;" vertex="1" parent="1">
          <mxGeometry x="990" y="200" width="48" height="48" as="geometry" />
        </mxCell>

        <mxCell id="ddb_camp" value="campanias-campaigns&#xa;Partition: campaignId" style="sketch=0;outlineConnect=0;fontColor=#232F3E;fillColor=#3334B9;align=center;html=1;fontSize=9;fontStyle=0;aspect=fixed;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.dynamodb;verticalLabelPosition=bottom;verticalAlign=top;labelPosition=center;spacingTop=4;" vertex="1" parent="1">
          <mxGeometry x="990" y="500" width="48" height="48" as="geometry" />
        </mxCell>

        <!-- EventBridge (standalone, below) -->
        <mxCell id="eventbridge" value="EventBridge&#xa;campanias-events" style="sketch=0;outlineConnect=0;fontColor=#232F3E;fillColor=#E7157B;align=center;html=1;fontSize=9;fontStyle=0;aspect=fixed;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.eventbridge;verticalLabelPosition=bottom;verticalAlign=top;labelPosition=center;spacingTop=4;" vertex="1" parent="1">
          <mxGeometry x="990" y="850" width="48" height="48" as="geometry" />
        </mxCell>

        <!-- EDGES -->

        <!-- Client -> API Gateway -->
        <mxCell id="e1" value="POST/GET" style="edgeStyle=orthogonalEdgeStyle;rounded=1;fontSize=9;exitX=1;exitY=0.5;exitDx=0;exitDy=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0;" edge="1" source="client" target="apigw" parent="1">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>

        <!-- API GW -> Lambda gestion -->
        <mxCell id="e2" value="/campaigns" style="edgeStyle=orthogonalEdgeStyle;rounded=1;fontSize=8;exitX=0.5;exitY=1;exitDx=0;exitDy=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0;" edge="1" source="apigw" target="fn_gestion" parent="1">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>

        <!-- API GW -> Lambda reglas -->
        <mxCell id="e3" value="/{id}/evaluate" style="edgeStyle=orthogonalEdgeStyle;rounded=1;fontSize=8;exitX=1;exitY=0.5;exitDx=0;exitDy=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0;" edge="1" source="apigw" target="fn_reglas" parent="1">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>

        <!-- Lambda tracking -> DynamoDB tracking -->
        <mxCell id="e4" value="PutItem" style="edgeStyle=orthogonalEdgeStyle;rounded=1;fontSize=8;exitX=1;exitY=0.5;exitDx=0;exitDy=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0;" edge="1" source="fn_tracking" target="ddb_track" parent="1">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>

        <!-- Lambda reglas -> DynamoDB campaigns -->
        <mxCell id="e5" value="GetItem&#xa;UpdateItem" style="edgeStyle=orthogonalEdgeStyle;rounded=1;fontSize=8;exitX=1;exitY=0.5;exitDx=0;exitDy=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0;" edge="1" source="fn_reglas" target="ddb_camp" parent="1">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>

        <!-- Lambda gestion -> DynamoDB campaigns -->
        <mxCell id="e6" value="PutItem" style="edgeStyle=orthogonalEdgeStyle;rounded=1;fontSize=8;exitX=1;exitY=0.25;exitDx=0;exitDy=0;entryX=0;entryY=1;entryDx=0;entryDy=0;" edge="1" source="fn_gestion" target="ddb_camp" parent="1">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>

        <!-- Lambda gestion -> EventBridge -->
        <mxCell id="e7" value="PutEvents" style="edgeStyle=orthogonalEdgeStyle;rounded=1;fontSize=8;exitX=1;exitY=0.75;exitDx=0;exitDy=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0;" edge="1" source="fn_gestion" target="eventbridge" parent="1">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>

        <!-- EventBridge -> Lambda tracking -->
        <mxCell id="e8" value="Rule: source=&#xa;campanias.gestion" style="edgeStyle=orthogonalEdgeStyle;rounded=1;fontSize=8;exitX=0;exitY=0;exitDx=0;exitDy=0;entryX=0.5;entryY=1;entryDx=0;entryDy=0;" edge="1" source="eventbridge" target="fn_tracking" parent="1">
          <mxGeometry relative="1" as="geometry">
            <Array as="points">
              <mxPoint x="800" y="874" />
              <mxPoint x="800" y="350" />
              <mxPoint x="564" y="350" />
            </Array>
          </mxGeometry>
        </mxCell>

      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
'''

with open(OUTPUT, 'w', encoding='utf-8') as f:
    f.write(content)
print(f"Generado: {OUTPUT}")
