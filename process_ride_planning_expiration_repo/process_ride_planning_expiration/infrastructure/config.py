import os

import boto3
from botocore.config import Config
from lagom import Container, Singleton
from aws_lambda_powertools.utilities.parser import parse
from aws_lambda_powertools.utilities.batch import BatchProcessor, EventType

from process_ride_planning_expiration.application.process_ride_planning_expiration_use_case_impl import \
    ProcessRidePlanningExpirationUseCaseImpl
from process_ride_planning_expiration.application.notification_gateway_interface import \
    NotificationGatewayInterface
from process_ride_planning_expiration.application.persistence_gateway_interface import \
    PersistenceGatewayInterface
from process_ride_planning_expiration.domain.use_cases.process_ride_planning_expiration_use_case_interface import \
    ProcessRidePlanningExpirationUseCaseInterface
from process_ride_planning_expiration.drivers_adapters.gateways.dynamodb_persistence_gateway import \
    DynamodbResourceTable, DynamodbPersistenceGateway
from process_ride_planning_expiration.drivers_adapters.gateways.sns_notification_gateway import TopicArn,\
    SnsClient, SnsNotificationGateway
from process_ride_planning_expiration.interface_adapters.process_ride_planning_expiration_handler import \
    ProcessRidePlanningExpirationHandler


def start_app() -> ProcessRidePlanningExpirationHandler:
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
    container[PersistenceGatewayInterface] = DynamodbPersistenceGateway
    container[NotificationGatewayInterface] = SnsNotificationGateway
    container[ProcessRidePlanningExpirationUseCaseInterface] = ProcessRidePlanningExpirationUseCaseImpl

    # HANDLER
    container[BatchProcessor] = Singleton(lambda c: BatchProcessor(event_type=EventType.SQS))
    return container[ProcessRidePlanningExpirationHandler]
