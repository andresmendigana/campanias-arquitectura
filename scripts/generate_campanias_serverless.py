"""
Diagrama de Arquitectura Serverless - Sistema de Campañas TO-BE
AWS (Plataforma de Campañas) + GCP (Analítica y Dashboards)
Usa la librería 'diagrams' con iconos oficiales AWS y GCP.
Ejecutar: python campanias-serverless-aws-gcp.py
Requiere: pip install diagrams
"""
import os
from diagrams import Diagram, Cluster, Edge
from diagrams.aws.compute import Lambda
from diagrams.aws.integration import StepFunctions, EventbridgeCustomEventBusResource, SQS, SNS
from diagrams.aws.network import APIGateway, CloudFront, Route53
from diagrams.aws.database import Dynamodb as DynamoDB, RDS
from diagrams.aws.storage import S3
from diagrams.aws.security import Cognito, WAF, IAMRole
from diagrams.aws.analytics import KinesisDataFirehose
from diagrams.aws.management import Cloudwatch
from diagrams.gcp.analytics import BigQuery, Dataflow
from diagrams.gcp.database import Datastore
from diagrams.gcp.operations import Monitoring as GCPMonitoring
from diagrams.onprem.client import User, Users
from diagrams.onprem.network import Internet
from diagrams.generic.database import SQL

OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "campanias-serverless-aws-gcp")

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
    "Sistema de Campañas TO-BE - Arquitectura Serverless Multinube",
    filename=OUTPUT_FILE,
    show=False,
    direction="LR",
    graph_attr=graph_attr
):
    # Actores
    analista = User("Analista de\nCampañas")
    gerente = User("Gerente de\nRiesgo")
    cliente = Users("Cliente\n(18-25 años)")

    # Edge / CDN
    with Cluster("AWS Cloud", graph_attr={"bgcolor": "#EEF4FB"}):

        with Cluster("Edge & Security"):
            waf = WAF("WAF")
            cdn = CloudFront("CloudFront")
            dns = Route53("Route 53")

        with Cluster("Autenticación"):
            cognito = Cognito("Cognito\nOAuth2/OIDC")

        with Cluster("API Layer"):
            apigw = APIGateway("API Gateway\nREST APIs")

        with Cluster("Plataforma de Campañas (Serverless)"):
            # Lambdas - Core Services
            fn_reglas = Lambda("Motor de Reglas\nSelección Público")
            fn_simulacion = Lambda("Simulación\nScoring")
            fn_campania = Lambda("Gestión\nCampañas")
            fn_scoring = Lambda("Scoring\nAlternativo")
            fn_notif = Lambda("Orquestador\nNotificaciones")
            fn_tracking = Lambda("Tracking\nEfectividad")

            # Step Functions - Orquestación
            sf_aprobacion = StepFunctions("Flujo Aprobación\nCampaña")
            sf_ejecucion = StepFunctions("Flujo Ejecución\nCampaña")

        with Cluster("Event-Driven"):
            eventbridge = EventbridgeCustomEventBusResource("EventBridge\nBus de Eventos")
            sqs = SQS("SQS\nCola Notificaciones")
            sns = SNS("SNS\nAlertas")

        with Cluster("Data (AWS)"):
            dynamo_camp = DynamoDB("DynamoDB\nCampañas & Reglas")
            dynamo_track = DynamoDB("DynamoDB\nTracking")
            s3_docs = S3("S3\nDocumentos & Logs")

        with Cluster("Integración Legacy"):
            fn_esb_bridge = Lambda("ESB Bridge\nAdapter")

        with Cluster("Streaming a GCP"):
            firehose = KinesisDataFirehose("Kinesis Firehose\nStreaming a GCP")

        # Observabilidad
        cw = Cloudwatch("CloudWatch\nLogs & Metrics")

    # GCP
    with Cluster("GCP (Data Lake + Analítica)", graph_attr={"bgcolor": "#E8F5E9"}):
        datalake = Datastore("Data Lake GCS\nAlmacenamiento\nGrandes Volúmenes")
        bq = BigQuery("BigQuery\nHistórico Campañas\nAnalítica")
        dataflow = Dataflow("Dataflow\nETL, Ingesta\ny Calidad")
        looker = GCPMonitoring("NEW APP Campañas\nSaaS Analítica\nAvanzada + Dashboard")

    # Sistemas Externos (On-premise / Terceros)
    with Cluster("Sistemas Internos (On-Premise)"):
        core = SQL("Core Bancario")
        crm = SQL("CRM")
        creditos = SQL("Sistema Créditos")

    with Cluster("Proveedores Externos"):
        centrales = Internet("Centrales\nde Riesgo")
        telcos = Internet("Telecomunicaciones")
        otras_fin = Internet("Otras Entidades\nFinancieras")
        prov_notif = Internet("Proveedor\nNotificaciones\nSMS/Email/Push")

    # === FLUJO ===

    # Actores -> Edge
    analista >> Edge(label="HTTPS") >> dns
    gerente >> Edge(label="HTTPS") >> dns
    dns >> cdn >> waf >> apigw

    # Auth
    apigw >> Edge(label="Valida token") >> cognito

    # API -> Lambdas
    apigw >> fn_reglas
    apigw >> fn_simulacion
    apigw >> fn_campania

    # Orquestación
    fn_campania >> sf_aprobacion
    sf_aprobacion >> fn_scoring
    sf_aprobacion >> sf_ejecucion
    sf_ejecucion >> fn_notif

    # Motor de reglas
    fn_reglas >> fn_scoring
    fn_scoring >> fn_esb_bridge

    # Event-driven
    fn_campania >> eventbridge
    fn_notif >> sqs
    sqs >> fn_tracking
    eventbridge >> fn_tracking
    fn_tracking >> sns

    # Data AWS
    fn_reglas >> dynamo_camp
    fn_campania >> dynamo_camp
    fn_tracking >> dynamo_track
    fn_campania >> s3_docs

    # Streaming a GCP
    dynamo_track >> firehose
    firehose >> dataflow
    dataflow >> datalake
    datalake >> bq
    bq >> looker

    # Integración Legacy
    fn_esb_bridge >> core
    fn_esb_bridge >> crm
    fn_esb_bridge >> creditos

    # Proveedores externos
    fn_scoring >> centrales
    fn_scoring >> telcos
    fn_scoring >> otras_fin
    fn_notif >> prov_notif

    # Notificación al cliente
    prov_notif >> Edge(label="SMS/Email/Push") >> cliente

    # Observabilidad
    fn_reglas >> Edge(style="dashed") >> cw
    fn_campania >> Edge(style="dashed") >> cw

    # Dashboard -> Gerente
    looker >> Edge(label="Dashboard\nMensual") >> gerente
