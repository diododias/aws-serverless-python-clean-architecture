import dataclasses
import json
from typing import NewType

from src.application.ride_planning_notification_gateway_interface import RidePlanningNotificationGatewayInterface
from src.domain.entities.ride_planning_entity import RidePlanningEntity

SnsClient = NewType("SnsClient", object)
TopicArn = NewType("TopicArn", object)


class RidePlanningSnsGateway(RidePlanningNotificationGatewayInterface):
    _sns_client: SnsClient
    _topic_arn: TopicArn

    def __init__(self, sns_client: SnsClient, topic_arn: TopicArn):
        self._sns_client = sns_client
        self._topic_arn = topic_arn

    def send(self, ride_planning: RidePlanningEntity) -> str:
        """
        Notify a new ride planning request
        Args:
            ride_planning: Ride Planning Request Object

        Returns: Message ID of notification
        """
        response = self._sns_client.publish(
            TopicArn=self._topic_arn,
            Message=json.dumps(dataclasses.asdict(ride_planning), default=str),
            MessageAttributes={
                "ride_planning": {
                    "DataType": "String",
                    "StringValue": "REQUEST_RIDE_PLANNING",
                }
            }
        )
        message_id = response.get("MessageId")
        return message_id if message_id else None
