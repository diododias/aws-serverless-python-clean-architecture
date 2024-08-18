import dataclasses
import json
from typing import Any

from src.application.ride_planning_notification_gateway import RidePlanningNotificationGateway
from src.domain.entities.ride_planning_entity import RidePlanningEntity


class RidePlanningNotificationGatewayImpl(RidePlanningNotificationGateway):
    # TODO: encontrar um tipo compativel
    _sns_client: Any
    _topic_arn: str

    def __init__(self, sns_client: object, topic_arn):
        self._sns_client = sns_client
        self._topic_arn = topic_arn

    def send(self, ride_planning: RidePlanningEntity) -> str:
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
        if response.get("MessageId"):
            return response.get("MessageId")
