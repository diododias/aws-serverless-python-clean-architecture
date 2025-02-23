import os
from typing import List

import boto3
from aws_lambda_powertools.utilities.batch import BatchProcessor, EventType
from botocore.config import Config
from lagom import Container, Singleton

from process_ride_planning_request.application.gateways.notification_gateway_interface import \
    NotificationGatewayInterface
from process_ride_planning_request.application.gateways.persistence_gateway_interface import PersistenceGatewayInterface
from process_ride_planning_request.application.gateways.ride_option_partner_gateway_interface import \
    RideOptionPartnerGatewayInterface
from process_ride_planning_request.application.use_cases.process_ride_planning_request_use_case_impl import \
    ProcessRidePlanningRequestUseCaseImpl
from process_ride_planning_request.domain.use_cases.process_ride_planning_request_use_case_interface import \
    ProcessRidePlanningRequestUseCaseInterface
from process_ride_planning_request.drivers_adapters.gateways.dynamodb_persistence_gateway import DynamodbResourceTable, \
    DynamodbPersistenceGateway
from process_ride_planning_request.drivers_adapters.gateways.ride_option_nine_nine_partner_gateway import \
    RideOptionNineNinePartnerGateway
from process_ride_planning_request.drivers_adapters.gateways.ride_option_uber_partner_gateway import \
    RideOptionUberPartnerGateway
from process_ride_planning_request.drivers_adapters.gateways.sns_notification_gateway import TopicArn, SnsClient, \
    SnsNotificationGateway
from process_ride_planning_request.interface_adapters.process_ride_planning_expiration_handler import \
    ProcessRidePlanningRequestHandler


def start_app() -> ProcessRidePlanningRequestHandler:
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
    container[ProcessRidePlanningRequestUseCaseInterface] = ProcessRidePlanningRequestUseCaseImpl

    # Partners Gateways
    partners_gateways: List[RideOptionPartnerGatewayInterface] = list()
    partners_gateways.append(RideOptionUberPartnerGateway())
    partners_gateways.append(RideOptionNineNinePartnerGateway())
    container[List[RideOptionPartnerGatewayInterface]] = Singleton(lambda c: partners_gateways)

    # HANDLER
    container[BatchProcessor] = Singleton(lambda c: BatchProcessor(event_type=EventType.SQS))
    return container[ProcessRidePlanningRequestHandler]
