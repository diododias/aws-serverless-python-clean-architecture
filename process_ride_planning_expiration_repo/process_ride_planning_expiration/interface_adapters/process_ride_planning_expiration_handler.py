from typing import Dict

from aws_lambda_powertools import Logger
from aws_lambda_powertools.utilities.typing import LambdaContext
from aws_lambda_powertools.utilities.batch import (
    BatchProcessor,
    process_partial_response,
)

from process_ride_planning_expiration.domain.use_cases.process_ride_planning_expiration_use_case_interface import \
    ProcessRidePlanningExpirationUseCaseInterface
from process_ride_planning_expiration.domain.value_objects.ride_planning_id import RidePlanningId
from process_ride_planning_expiration.domain.value_objects.user_id import UserId
from process_ride_planning_expiration.interface_adapters.handler_request import SqsWaitingForExpirationRecord, \
    RidePlanningWaitingForExpirationEvent
from process_ride_planning_expiration.interface_adapters.handler_response import HandlerResponse


class ProcessRidePlanningExpirationHandler:
    _use_case: ProcessRidePlanningExpirationUseCaseInterface
    _logger = Logger(serialize_stacktrace=True)
    _batch_processor: BatchProcessor

    def __init__(self,
                 request_ride_planning_use_case: ProcessRidePlanningExpirationUseCaseInterface,
                 batch_processor: BatchProcessor):
        self._use_case = request_ride_planning_use_case
        self._batch_processor = batch_processor

    def _process_event(self, event: SqsWaitingForExpirationRecord):
        body: RidePlanningWaitingForExpirationEvent = event.body
        user_id: UserId = UserId(body.data.user_id)
        ride_planning_id: RidePlanningId = RidePlanningId(body.data.ride_planning_id)
        self._use_case.execute(user_id, ride_planning_id)

    def handle(self, event: Dict, context: LambdaContext) -> HandlerResponse:
        return process_partial_response(
            event=event,
            record_handler=self._process_event,
            processor=self._batch_processor,
            context=context,
        )
