"""
Diagrama del Prototipo Serverless con iconos oficiales AWS.
Sigue las reglas del agente aws-diagrams.
"""
import os
from diagrams import Diagram, Cluster, Edge
from diagrams.aws.compute import Lambda
from diagrams.aws.network import APIGateway
from diagrams.aws.database import Dynamodb as DynamoDB
from diagrams.aws.integration import EventbridgeCustomEventBusResource, SQS
from diagrams.aws.management import Cloudwatch
from diagrams.onprem.client import User

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'diagramas', 'to-be')
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "CAM-TOBE-07-prototipo-aws")

graph_attr = {
    "splines": "ortho",
    "nodesep": "0.6",
    "ranksep": "0.8",
    "pad": "0.6",
    "fontname": "Arial",
    "fontsize": "11",
    "bgcolor": "white"
}

with Diagram(
    "Prototipo Serverless - Sistema de Campañas (AWS)",
    filename=OUTPUT_FILE,
    show=False,
    direction="LR",
    graph_attr=graph_attr
):
    # Cliente
    client = User("Cliente HTTP\n(PowerShell)")

    with Cluster("AWS Cloud", graph_attr={"bgcolor": "#EEF4FB"}):

        # API Gateway
        with Cluster("API Layer"):
            apigw = APIGateway("API Gateway\nCampanias API")

        # Lambdas
        with Cluster("Compute (Serverless)"):
            fn_gestion = Lambda("campanias-gestion\nCRUD Campañas")
            fn_reglas = Lambda("campanias-reglas\nMotor de Reglas")
            fn_tracking = Lambda("campanias-tracking\nAuditoría")

        # Event-Driven
        with Cluster("Event-Driven"):
            eventbridge = EventbridgeCustomEventBusResource("EventBridge\ncampanias-events")
            sqs = SQS("SQS\ncampanias-notifications")

        # Data
        with Cluster("Persistencia"):
            ddb_campaigns = DynamoDB("DynamoDB\ncampanias-campaigns")
            ddb_tracking = DynamoDB("DynamoDB\ncampanias-tracking")

        # Observability
        cw = Cloudwatch("CloudWatch\nLogs")

    # Flow
    client >> Edge(label="HTTPS") >> apigw

    apigw >> Edge(label="POST/GET\n/campaigns") >> fn_gestion
    apigw >> Edge(label="POST\n/{id}/evaluate") >> fn_reglas

    fn_gestion >> Edge(label="PUT/GET") >> ddb_campaigns
    fn_gestion >> Edge(label="PutEvents") >> eventbridge
    fn_gestion >> Edge(label="SendMessage") >> sqs

    fn_reglas >> Edge(label="GET/UPDATE") >> ddb_campaigns

    eventbridge >> Edge(label="Rule trigger") >> fn_tracking
    fn_tracking >> Edge(label="PUT") >> ddb_tracking

    fn_gestion >> Edge(style="dashed") >> cw
    fn_reglas >> Edge(style="dashed") >> cw
    fn_tracking >> Edge(style="dashed") >> cw
