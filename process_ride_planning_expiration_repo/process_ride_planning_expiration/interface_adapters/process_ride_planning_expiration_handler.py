import json
from typing import Dict

from aws_lambda_powertools import Logger
from aws_lambda_powertools.utilities.data_classes.sqs_event import SQSRecord
from aws_lambda_powertools.utilities.typing import LambdaContext
from aws_lambda_powertools.utilities.batch import (
    BatchProcessor,
    process_partial_response,
)

from process_ride_planning_expiration.domain.use_cases.process_ride_planning_expiration_use_case_interface import \
    ProcessRidePlanningExpirationUseCaseInterface
from process_ride_planning_expiration.domain.value_objects.ride_planning_id import RidePlanningId
from process_ride_planning_expiration.domain.value_objects.user_id import UserId
from process_ride_planning_expiration.interface_adapters.handler_request import \
    MessageSchema, \
    SnsSchema
from process_ride_planning_expiration.interface_adapters.handler_response import HandlerResponse


class ProcessRidePlanningExpirationHandler:
    _use_case: ProcessRidePlanningExpirationUseCaseInterface
    _batch_processor: BatchProcessor
    _logger = Logger(serialize_stacktrace=True)

    def __init__(self,
                 request_ride_planning_use_case: ProcessRidePlanningExpirationUseCaseInterface,
                 batch_processor: BatchProcessor):
        self._use_case = request_ride_planning_use_case
        self._batch_processor = batch_processor

    def _process_event(self, record: SQSRecord) -> None:
        self._logger.debug(f"Processing record {record}")
        record_body: Dict = json.loads(record.body)
        event: MessageSchema = SnsSchema.model_validate(record_body).Message  # parse and validate event fields
        self._logger.set_correlation_id(event.correlation_id)
        self._use_case.execute(
            UserId(event.data.user_id),
            RidePlanningId(event.data.ride_planning_id)
        )

    def handle(self, event: Dict, context: LambdaContext) -> HandlerResponse:
        return process_partial_response(
            event=event,
            record_handler=self._process_event,
            processor=self._batch_processor,
            context=context,
        )
