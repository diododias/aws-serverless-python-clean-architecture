import os

import boto3
import botocore
from botocore.config import Config
from lagom import Container, Singleton
from aws_lambda_powertools.utilities.parser import parse

from request_ride_planning.application.request_ride_planning_use_case_impl import RequestRidePlanningUseCaseImpl
from request_ride_planning.application.ride_planning_notification_gateway_interface import (
    RidePlanningNotificationGatewayInterface)
from request_ride_planning.application.ride_planning_persistence_gateway_interface import (
    RidePlanningPersistenceGatewayInterface)
from request_ride_planning.domain.use_cases.request_ride_planning_use_case_interface import (
    RequestRidePlanningUseCaseInterface)
from request_ride_planning.drivers_adapters.gateways.ride_planning_sns_notification_gateway import (
    TopicArn, SnsClient, RidePlanningSnsNotificationGateway)
from request_ride_planning.drivers_adapters.gateways.ride_planning_dynamodb_persistence_gateway import (
    DynamodbResourceTable, RidePlanningDynamodbPersistenceGateway)
from request_ride_planning.interface_adapters.request_ride_planning_handler import RequestRidePlanningHandler


def start_app() -> RequestRidePlanningHandler:
    # DEPENDENCY INJECTION CONTAINER
    container = Container()

    # SNS DEPENDENCIES
    container[TopicArn] = os.environ.get("SNS_TOPIC_ARN")
    container[SnsClient] = Singleton(lambda c: boto3.client("sns"))

    # DYNAMODB DEPENDENCIES
    table_name = os.environ.get("DYNAMODB_TABLE_NAME")
    dynamodb_config = Config(tcp_keepalive=True)
    dynamodb_resource = boto3.resource("dynamodb", config=dynamodb_config)
    container[DynamodbResourceTable] = Singleton(lambda c: dynamodb_resource.Table(table_name))

    # SET INTERFACE IMPLEMENTATIONS
    container[RidePlanningPersistenceGatewayInterface] = RidePlanningDynamodbPersistenceGateway
    container[RidePlanningNotificationGatewayInterface] = RidePlanningSnsNotificationGateway
    container[RequestRidePlanningUseCaseInterface] = RequestRidePlanningUseCaseImpl

    # HANDLER
    container[parse] = Singleton(lambda c: parse)
    return container[RequestRidePlanningHandler]
