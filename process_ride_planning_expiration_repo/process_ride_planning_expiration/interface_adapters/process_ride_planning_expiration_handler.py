import json
from typing import Dict

from aws_lambda_powertools import Logger
from aws_lambda_powertools.utilities.parser import parse
from aws_lambda_powertools.utilities.parser.envelopes import SnsEnvelope
from aws_lambda_powertools.utilities.data_classes.sqs_event import SQSRecord
from aws_lambda_powertools.utilities.typing import LambdaContext
from aws_lambda_powertools.utilities.batch import (
    BatchProcessor,
    process_partial_response,
)
from pydantic_core._pydantic_core import ValidationError

from process_ride_planning_expiration.domain.use_cases.process_ride_planning_expiration_use_case_interface import \
    ProcessRidePlanningExpirationUseCaseInterface
from process_ride_planning_expiration.domain.value_objects.ride_planning_id import RidePlanningId
from process_ride_planning_expiration.domain.value_objects.user_id import UserId
from process_ride_planning_expiration.interface_adapters.handler_request import \
    RidePlanningWaitingForExpirationEvent, SnsWaitingForExpirationMessage
from process_ride_planning_expiration.interface_adapters.handler_response import HandlerResponse


class ProcessRidePlanningExpirationHandler:
    _use_case: ProcessRidePlanningExpirationUseCaseInterface
    _parser: parse
    _batch_processor: BatchProcessor
    _logger = Logger(serialize_stacktrace=True)

    def __init__(self,
                 request_ride_planning_use_case: ProcessRidePlanningExpirationUseCaseInterface,
                 parser: parse,
                 batch_processor: BatchProcessor):
        self._use_case = request_ride_planning_use_case
        self._parser = parser
        self._batch_processor = batch_processor

    def _process_event(self, record: SQSRecord) -> None:
        print(record)
        try:
            event: RidePlanningWaitingForExpirationEvent = SnsWaitingForExpirationMessage.parse_obj(
                json.loads(record.body)
            ).Message
            print(event)

            user_id: UserId = UserId(event.data.user_id)
            ride_planning_id: RidePlanningId = RidePlanningId(event.data.ride_planning_id)
            self._use_case.execute(user_id, ride_planning_id)
        except ValidationError as error:
            print(error.errors())

    def handle(self, event: Dict, context: LambdaContext) -> HandlerResponse:
        print(event)
        return process_partial_response(
            event=event,
            record_handler=self._process_event,
            processor=self._batch_processor,
            context=context,
        )
