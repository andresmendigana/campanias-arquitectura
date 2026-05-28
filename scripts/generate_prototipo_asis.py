"""
Diagrama del prototipo tal como está implementado (AS-IS).
Solo los componentes que realmente se desplegaron y probaron.
"""
import os
from diagrams import Diagram, Cluster, Edge
from diagrams.aws.compute import Lambda
from diagrams.aws.network import APIGateway
from diagrams.aws.database import Dynamodb as DynamoDB
from diagrams.aws.integration import EventbridgeCustomEventBusResource
from diagrams.onprem.client import User

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'diagramas', 'as-is')
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "PRO-ASIS-01-prototipo-implementado")

graph_attr = {
    "splines": "ortho",
    "nodesep": "0.8",
    "ranksep": "1.0",
    "pad": "0.6",
    "fontname": "Arial",
    "fontsize": "11",
    "bgcolor": "white"
}

with Diagram(
    "Prototipo Implementado (AS-IS) - Solo componentes desplegados",
    filename=OUTPUT_FILE,
    show=False,
    direction="LR",
    graph_attr=graph_attr
):
    client = User("PowerShell\n(Invoke-RestMethod)")

    with Cluster("AWS Cloud - us-east-1", graph_attr={"bgcolor": "#EEF4FB"}):

        apigw = APIGateway("API Gateway\nCampanias API\n/prod/campaigns")

        with Cluster("Lambda Functions (Node.js 22)"):
            fn_gestion = Lambda("campanias-gestion\nCRUD + PutEvents")
            fn_reglas = Lambda("campanias-reglas\nEvaluar + Update")
            fn_tracking = Lambda("campanias-tracking\nRegistrar evento")

        eventbridge = EventbridgeCustomEventBusResource("EventBridge\ncampanias-events")

        with Cluster("DynamoDB (PAY_PER_REQUEST)"):
            ddb_campaigns = DynamoDB("campanias-campaigns\nPartition: campaignId")
            ddb_tracking = DynamoDB("campanias-tracking\nPartition: campaignId\nSort: clientId")

    # Flujo probado
    client >> Edge(label="POST/GET") >> apigw

    apigw >> Edge(label="/campaigns") >> fn_gestion
    apigw >> Edge(label="/{id}/evaluate") >> fn_reglas

    fn_gestion >> Edge(label="PutItem") >> ddb_campaigns
    fn_gestion >> Edge(label="PutEvents") >> eventbridge

    fn_reglas >> Edge(label="GetItem\nUpdateItem") >> ddb_campaigns

    eventbridge >> Edge(label="Rule: source=\ncampanias.gestion") >> fn_tracking
    fn_tracking >> Edge(label="PutItem") >> ddb_tracking
