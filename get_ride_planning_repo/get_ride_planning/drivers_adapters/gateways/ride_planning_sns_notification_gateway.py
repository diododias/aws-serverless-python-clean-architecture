import dataclasses
import json
from typing import NewType

from aws_lambda_powertools import Logger

from get_ride_planning.application.ride_planning_notification_gateway_interface import \
    RidePlanningNotificationGatewayInterface
from get_ride_planning.domain.entities.ride_planning_entity import RidePlanningEntity
from get_ride_planning.domain.events.ride_planning_waiting_for_expiration_event import \
    RidePlanningWaitingForExpirationEvent
from get_ride_planning.drivers_adapters.mappers.ride_planning_sns_mapper import \
    map_ride_planning_to_waiting_for_expiration_event

SnsClient = NewType("SnsClient", object)
TopicArn = NewType("TopicArn", object)


class RidePlanningSnsNotificationGateway(RidePlanningNotificationGatewayInterface):
    _sns_client: SnsClient
    _topic_arn: TopicArn
    _logger: Logger = Logger(child=True)

    def __init__(self, sns_client: SnsClient, topic_arn: TopicArn):
        self._sns_client = sns_client
        self._topic_arn = topic_arn

    def notify_waiting_for_expiration(self, ride_planning: RidePlanningEntity):
        self._logger.debug(f"notifying ride planning {ride_planning.id} is waiting for expiration")
        event: RidePlanningWaitingForExpirationEvent = map_ride_planning_to_waiting_for_expiration_event(ride_planning)
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
