from aws_lambda_powertools import Logger
from aws_lambda_powertools.utilities.parser import parse
from aws_lambda_powertools.utilities.parser.envelopes import ApiGatewayEnvelope
from aws_lambda_powertools.utilities.typing import LambdaContext

from pydantic import ValidationError

from src.domain.entities.address_entity import AddressEntity
from src.domain.use_cases.request_ride_planning_use_case_interface import RequestRidePlanningUseCaseInterface
from src.domain.value_objects.user_id import UserId
from src.interface_adapters.handler_request import HandlerRequest, BodyRequest
from src.interface_adapters.handler_response import (created_response, validation_error_response,
                                                     internal_server_error_response, HandlerResponse)


class RequestRidePlanningHandler:
    _use_case: RequestRidePlanningUseCaseInterface
    _parser: parse
    _logger = Logger(serialize_stacktrace=True)

    def __init__(self, request_ride_planning_use_case: RequestRidePlanningUseCaseInterface, parser: parse):
        self._use_case = request_ride_planning_use_case
        self._parser = parser

    def handle(self, request: HandlerRequest, context: LambdaContext) -> HandlerResponse:
        self._logger.set_correlation_id(context.aws_request_id)
        try:
            event: BodyRequest = self._parser(event=request, model=BodyRequest, envelope=ApiGatewayEnvelope)
            ride_planning_id: str = self._use_case.execute(
                user_id=UserId(event.user_id),
                address_from=AddressEntity(**event.address_from.model_dump()),
                address_to=AddressEntity(**event.address_to.model_dump()),
                departure_datetime=event.departure_datetime
            )
            return created_response({"ride_planning_id": ride_planning_id})
        except ValidationError as error:
            self._logger.exception(error)
            return validation_error_response(error)
        # pylint: disable=W0718
        except Exception as error:
            self._logger.exception(error)
            return internal_server_error_response(str(error))
