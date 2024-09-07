import dataclasses
import json
from typing import NewType
from aws_lambda_powertools import Logger

from process_ride_planning_expiration.application.ride_planning_notification_gateway_interface import (
    RidePlanningNotificationGatewayInterface)
from process_ride_planning_expiration.domain.entities.ride_planning_entity import RidePlanningEntity

from process_ride_planning_expiration.domain.events.ride_planning_expired_event import RidePlanningExpiredEvent
from process_ride_planning_expiration.drivers_adapters.mappers.ride_planning_sns_mapper import (
    map_ride_planning_to_expired_event)

SnsClient = NewType("SnsClient", object)
TopicArn = NewType("TopicArn", object)


class RidePlanningSnsNotificationGateway(RidePlanningNotificationGatewayInterface):
    _sns_client: SnsClient
    _topic_arn: TopicArn
    _logger: Logger = Logger(child=True)

    def __init__(self, sns_client: SnsClient, topic_arn: TopicArn):
        self._sns_client = sns_client
        self._topic_arn = topic_arn

    def notify_expired(self, ride_planning: RidePlanningEntity) -> str:
        event: RidePlanningExpiredEvent = map_ride_planning_to_expired_event(ride_planning)
        self._logger.debug(f"notifying event: {event}")
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
