import dataclasses
import json
from typing import NewType
from aws_lambda_powertools import Logger

from process_ride_planning_request.application.gateways.notification_gateway_interface import \
    NotificationGatewayInterface
from process_ride_planning_request.domain.entities.ride_planning_entity import RidePlanningEntity
from process_ride_planning_request.domain.events.base_event import BaseEvent
from process_ride_planning_request.domain.events.ride_planning_waiting_for_approve_event import \
    RidePlanningWaitingForApproveEvent
from process_ride_planning_request.domain.events.ride_planning_waiting_for_expiration_event import \
    RidePlanningWaitingForExpirationEvent
from process_ride_planning_request.drivers_adapters.mappers.ride_planning_sns_mapper import \
    map_ride_planning_to_waiting_for_approve_event, map_ride_planning_to_waiting_for_expiration_event

SnsClient = NewType("SnsClient", object)
TopicArn = NewType("TopicArn", object)


class SnsNotificationGateway(NotificationGatewayInterface):
    _sns_client: SnsClient
    _topic_arn: TopicArn
    _logger: Logger = Logger(child=True)

    def __init__(self, sns_client: SnsClient, topic_arn: TopicArn):
        self._sns_client = sns_client
        self._topic_arn = topic_arn

    def _notify_event(self, event: BaseEvent) -> str:
        response = self._sns_client.publish(
            TopicArn=self._topic_arn,
            Message=json.dumps(dataclasses.asdict(event), default=str),
            MessageAttributes={
                "source": {
                    "DataType": "String",
                    "StringValue": event.source,
                },
                "event_name": {
                    "DataType": "String",
                    "StringValue": event.name,
                }
            }
        )
        self._logger.info(f"event notified: {dataclasses.asdict(event)}")
        return response.get("MessageId")

    def notify_expired(self, ride_planning: RidePlanningEntity) -> str:
        event: RidePlanningWaitingForExpirationEvent = map_ride_planning_to_waiting_for_expiration_event(ride_planning)
        return self._notify_event(event)

    def notify_waiting_for_approve(self, ride_planning: RidePlanningEntity) -> str:
        event: RidePlanningWaitingForApproveEvent = map_ride_planning_to_waiting_for_approve_event(ride_planning)
        return self._notify_event(event)
