import json
from typing import Dict, Any

from aws_lambda_powertools import Logger
from aws_lambda_powertools.utilities.typing import LambdaContext

from pydantic import ValidationError

from get_ride_planning.application.ride_planning_not_found_exception import RidePlanningNotFound
from get_ride_planning.domain.entities.ride_planning_entity import RidePlanningEntity
from get_ride_planning.domain.use_cases.get_ride_planning_use_case_interface import GetRidePlanningUseCaseInterface
from get_ride_planning.domain.value_objects.ride_planning_id import RidePlanningId
from get_ride_planning.domain.value_objects.user_id import UserId
from get_ride_planning.interface_adapters.handler_request import HandlerRequest
from get_ride_planning.interface_adapters.handler_response import HandlerResponse, ok_response, \
    validation_error_response, not_found_response, internal_server_error_response


class GetRidePlanningHandler:
    _use_case: GetRidePlanningUseCaseInterface
    _logger = Logger(serialize_stacktrace=True)

    def __init__(self, request_ride_planning_use_case: GetRidePlanningUseCaseInterface):
        self._use_case = request_ride_planning_use_case

    def handle(self, request: Dict[str, Any], context: LambdaContext) -> HandlerResponse:
        self._logger.debug(f"Processing event: {json.dumps(request)}")
        self._logger.set_correlation_id(context.aws_request_id)
        try:
            event: HandlerRequest = HandlerRequest(**request)
            ride_planning: RidePlanningEntity = self._use_case.execute(
                UserId(event.requestContext.identity.user),
                RidePlanningId(event.pathParameters.ride_planning_id)
            )
            return ok_response(ride_planning)
        except ValidationError as error:
            self._logger.exception(error)
            return validation_error_response(error)
        except RidePlanningNotFound as error:
            self._logger.exception(error)
            return not_found_response(str(error))
        # pylint: disable=W0718
        except Exception as error:
            self._logger.exception(error)
            return internal_server_error_response(str(error))
