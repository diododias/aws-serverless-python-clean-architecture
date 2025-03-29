import json
from dataclasses import dataclass
from datetime import datetime
from unittest import mock

import pytest
from aws_lambda_powertools.utilities.batch import BatchProcessor, EventType

from process_ride_planning_request.domain.use_cases.process_ride_planning_request_use_case_interface import ProcessRidePlanningRequestUseCaseInterface
from process_ride_planning_request.domain.value_objects.ride_planning_id import RidePlanningId
from process_ride_planning_request.domain.value_objects.user_id import UserId
from process_ride_planning_request.interface_adapters.handler_request import MessageSchema, RequestedEventSchema
from process_ride_planning_request.interface_adapters.process_ride_planning_request_handler import ProcessRidePlanningRequestHandler
from ..event_payload import sqs_event

@pytest.fixture
def lambda_context():
    @dataclass
    class LambdaContext:
        function_name: str = "test"
        memory_limit_in_mb: int = 128
        invoked_function_arn: str = "arn:aws:lambda:eu-west-1:809313241:function:test"
        aws_request_id: str = "52fdfc07-2182-154f-163f-5f0f9a621d72"

    return LambdaContext()


class TestProcessRidePlanningRequestHandler:

    def test_handle_successful_event_processing(self, lambda_context):
        use_case = mock.Mock(spec=ProcessRidePlanningRequestUseCaseInterface)
        batch_processor = BatchProcessor(event_type=EventType.SQS)
        handler = ProcessRidePlanningRequestHandler(use_case, batch_processor)
        event = {"Records": [
            {"body": json.dumps({"Message": {"data": {"user_id": "user123", "ride_planning_id": "ride123"}}})}]}

        response = handler.handle(event, lambda_context)

        assert response["statusCode"] == 200
        use_case.execute.assert_called_once_with(UserId("user123"), RidePlanningId("ride123"))

    def test_handle_event_with_missing_fields(self, lambda_context):
        use_case = mock.Mock(spec=ProcessRidePlanningRequestUseCaseInterface)
        batch_processor = BatchProcessor(event_type=EventType.SQS)
        handler = ProcessRidePlanningRequestHandler(use_case, batch_processor)
        event = {"Records": [{"body": json.dumps({"Message": {"data": {"user_id": "user123"}}})}]}

        response = handler.handle(event, lambda_context)

        assert len(response["batchItemFailures"]) > 0
        use_case.execute.assert_not_called()

    def test_handle_event_with_processing_error(self, lambda_context):
        use_case = mock.Mock(spec=ProcessRidePlanningRequestUseCaseInterface)
        use_case.execute.side_effect = Exception("Processing error")
        batch_processor = BatchProcessor(event_type=EventType.SQS)
        handler = ProcessRidePlanningRequestHandler(use_case, batch_processor)

        response = handler.handle(sqs_event, lambda_context)

        expected_response = {"batchItemFailures": [{"itemIdentifier": sqs_event.get("Records")[1]["ride_planning_id"]}]}

        assert response == expected_response
        assert len(batch_processor.fail_messages) == 1
        assert len(batch_processor.success_messages) == 1
        #use_case.execute.assert_called_once_with(UserId("user123"), RidePlanningId("ride123"))

        # GERAR EVENTO DO SNS
        