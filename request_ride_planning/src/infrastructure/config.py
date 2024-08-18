import os
import time
import boto3
from aws_lambda_powertools.utilities.parser import parse

from src.drivers_adapters.gateways.ride_planning_notification_gateway_impl import RidePlanningNotificationGatewayImpl
from src.drivers_adapters.gateways.ride_planning_persistence_gateway_impl import RidePlanningPersistenceGatewayImpl
from src.application.request_ride_planning_use_case_impl import RequestRidePlanningUseCaseImpl
from src.application.ride_planning_notification_gateway import RidePlanningNotificationGateway
from src.application.ride_planning_persistence_gateway import RidePlanningPersistenceGateway
from src.domain.use_cases.request_ride_planning_use_case import RequestRidePlanningUseCase
from src.interface_adapters.request_ride_planning_handler import RequestRidePlanningHandler


def start_app() -> RequestRidePlanningHandler:
    os.environ["TZ"] = "America/Sao_Paulo"
    time.tzset()

    # SNS BLOCK
    topic_arn = os.environ.get("SNS_TOPIC_ARN")
    sns_client = boto3.client("sns")
    notification_gateway: RidePlanningNotificationGateway = RidePlanningNotificationGatewayImpl(sns_client, topic_arn)

    # DYNAMODB BLOCK
    table_name = os.environ.get("DYNAMODB_TABLE_NAME")
    dynamodb_resource = boto3.resource("dynamodb")
    table = dynamodb_resource.Table(table_name)
    persistence_gateway: RidePlanningPersistenceGateway = RidePlanningPersistenceGatewayImpl(table)

    use_case: RequestRidePlanningUseCase = RequestRidePlanningUseCaseImpl(persistence_gateway, notification_gateway)
    return RequestRidePlanningHandler(use_case, parse)
