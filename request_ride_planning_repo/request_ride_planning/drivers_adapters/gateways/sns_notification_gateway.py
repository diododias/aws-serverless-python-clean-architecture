import dataclasses
import json
from typing import NewType
from aws_lambda_powertools import Logger

from request_ride_planning.application.notification_gateway_interface import (
    NotificationGatewayInterface)
from request_ride_planning.domain.entities.ride_planning_entity import RidePlanningEntity
from request_ride_planning.domain.events.base_event import BaseEvent
from request_ride_planning.domain.events.ride_planning_requested_event import RidePlanningRequestedEvent
from request_ride_planning.domain.events.ride_planning_waiting_for_expiration_event import \
    RidePlanningWaitingForExpirationEvent
from request_ride_planning.drivers_adapters.mappers.ride_planning_sns_mapper import \
    map_ride_planning_to_waiting_for_expiration_event, map_ride_planning_to_requested_event

SnsClient = NewType("SnsClient", object)
TopicArn = NewType("TopicArn", object)


class SnsNotificationGateway(NotificationGatewayInterface):
    _sns_client: SnsClient
    _topic_arn: TopicArn
    _logger: Logger = Logger(child=True)

    def __init__(self, sns_client: SnsClient, topic_arn: TopicArn):
        self._sns_client = sns_client
        self._topic_arn = topic_arn

    def _send(self, event: BaseEvent) -> str:
        self._logger.debug(f"notifying event: {dataclasses.asdict(event)}")
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
        message_id = response.get("MessageId")
        return message_id if message_id else None

    def notify_requested(self, ride_planning: RidePlanningEntity) -> str:
        """
        Notify a new ride planning request
        Args:
            ride_planning: Ride Planning Request Object

        Returns: Message ID of notification
        """
        event: RidePlanningRequestedEvent = map_ride_planning_to_requested_event(ride_planning)
        return self._send(event)

    def notify_waiting_for_expiration(self, ride_planning: RidePlanningEntity) -> str:
        event: RidePlanningWaitingForExpirationEvent = map_ride_planning_to_waiting_for_expiration_event(ride_planning)
        return self._send(event)
