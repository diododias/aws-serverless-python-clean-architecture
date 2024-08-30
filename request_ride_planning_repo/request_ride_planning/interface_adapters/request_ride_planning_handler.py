import json

from aws_lambda_powertools import Logger
from aws_lambda_powertools.utilities.parser import parse
from aws_lambda_powertools.utilities.parser.envelopes import ApiGatewayEnvelope
from aws_lambda_powertools.utilities.typing import LambdaContext

from pydantic import ValidationError

from request_ride_planning.application.too_many_requests_error import TooManyRequestsError
from request_ride_planning.domain.entities.address_entity import AddressEntity
from request_ride_planning.domain.use_cases.request_ride_planning_use_case_interface import (
    RequestRidePlanningUseCaseInterface)
from request_ride_planning.domain.value_objects.user_id import UserId
from request_ride_planning.interface_adapters.handler_request import HandlerRequest, BodyRequest
from request_ride_planning.interface_adapters.handler_response import (created_response, validation_error_response,
                                                                       internal_server_error_response, HandlerResponse,
                                                                       too_many_requests_response)


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
            self._logger.debug(f"Processing event: {event.model_dump_json()}")

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
        except TooManyRequestsError as error:
            self._logger.exception(error)
            return too_many_requests_response(str(error))
        # pylint: disable=W0718
        except Exception as error:
            self._logger.exception(error)
            return internal_server_error_response(str(error))
