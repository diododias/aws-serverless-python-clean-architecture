import dataclasses
import json
from typing import NewType
from aws_lambda_powertools import Logger

from request_ride_planning.application.ride_planning_notification_gateway_interface import RidePlanningNotificationGatewayInterface
from request_ride_planning.domain.entities.ride_planning_entity import RidePlanningEntity

SnsClient = NewType("SnsClient", object)
TopicArn = NewType("TopicArn", object)


class RidePlanningSnsGateway(RidePlanningNotificationGatewayInterface):
    _sns_client: SnsClient
    _topic_arn: TopicArn
    _logger: Logger = Logger(child=True)

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
        self._logger.debug(f"notifying a new requested ride planning {ride_planning.id}")
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
