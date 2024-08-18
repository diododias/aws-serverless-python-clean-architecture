import copy
import json
import uuid
from unittest import mock

from aws_lambda_powertools.utilities.parser import parse
from aws_lambda_powertools.utilities.typing import LambdaContext

from src.domain.use_cases.request_ride_planning_use_case import RequestRidePlanningUseCase
from src.interface_adapters.handler_response import HandlerResponse
from src.interface_adapters.request_ride_planning_handler import RequestRidePlanningHandler


class TestRequestRidePlanningHandler:
    event = {
        "user_id": "cace4a159ff9f2512dd42373760608767b62855d",
        "address_from": {
          "street": "Rua Augusta, 321",
          "city": "Sao Paulo",
          "country": "Brazil",
          "postal_code": "03881100"
        },
        "address_to": {
          "street": "Avenida 25 de Marco, 322",
          "city": "Sao Paulo",
          "country": "Brazil",
          "postal_code": "03881100"
        },
        "departure_datetime": "2024-12-01T05:33:20.000Z"
      }
    mock_event = {
      "resource": "/my/path",
      "path": "/my/path",
      "httpMethod": "GET",
      "headers": {
        "header1": "value1",
        "header2": "value1,value2"
      },
      "multiValueHeaders": {
        "header1": [
          "value1"
        ],
        "header2": [
          "value1",
          "value2"
        ]
      },
      "queryStringParameters": {
        "parameter1": "value1,value2",
        "parameter2": "value"
      },
      "multiValueQueryStringParameters": {
        "parameter1": [
          "value1",
          "value2"
        ],
        "parameter2": [
          "value"
        ]
      },
      "requestContext": {
        "accountId": "123456789012",
        "apiId": "id",
        "authorizer": {
          "claims": None,
          "scopes": None
        },
        "domainName": "id.execute-api.us-east-1.amazonaws.com",
        "domainPrefix": "id",
        "extendedRequestId": "request-id",
        "httpMethod": "GET",
        "identity": {
          "accessKey": "accessKey",
          "accountId": "accountId",
          "sourceIp": "192.168.0.1",
          "caller": None,
          "cognitoAuthenticationProvider": None,
          "cognitoAuthenticationType": None,
          "cognitoIdentityId": None,
          "cognitoIdentityPoolId": None,
          "principalOrgId": None,
          "user": None,
          "userAgent": "user-agent",
          "userArn": None,
          "clientCert": {
            "clientCertPem": "CERT_CONTENT",
            "subjectDN": "www.example.com",
            "issuerDN": "Example issuer",
            "serialNumber": "a1:a1:a1:a1:a1:a1:a1:a1:a1:a1:a1:a1:a1:a1:a1:a1",
            "validity": {
              "notBefore": "May 28 12:30:02 2019 GMT",
              "notAfter": "Aug  5 09:36:04 2021 GMT"
            }
          }
        },
        "path": "/my/path",
        "protocol": "HTTP/1.1",
        "requestId": "id=",
        "requestTime": "04/Mar/2020:19:15:17 +0000",
        "requestTimeEpoch": 1583349317135,
        "resourceId": None,
        "resourcePath": "/my/path",
        "stage": "$default"
      },
      "pathParameters": None,
      "stageVariables": None,
      "body": json.dumps(event),
      "isBase64Encoded": False
    }
    context = LambdaContext()
    context._aws_request_id = uuid.uuid4()

    def test_return_success_when_payload_correct(self):
        # arrange
        mock_return_value = "cace4a159ff9f2512dd42373760608767b62855d"
        use_case = mock.Mock(spec=RequestRidePlanningUseCase)
        use_case.execute = mock.Mock(return_value=mock_return_value)
        handler = RequestRidePlanningHandler(use_case, parse)

        # act
        response: HandlerResponse = handler.handle(self.mock_event, self.context)

        # assert
        assert response.get("statusCode") == 201
        assert isinstance(json.loads(response.get("body")).get("data").get("ride_planning_id"), str)
        use_case.execute.assert_called()

    def test_return_bad_request_when_payload_incorrect(self):
        # arrange
        use_case = mock.Mock(spec=RequestRidePlanningUseCase)
        use_case.execute = mock.Mock()
        handler = RequestRidePlanningHandler(use_case, parse)

        request = copy.copy(self.mock_event)
        request["body"] = json.dumps({
          "user_id": "cace4a159ff9f2512dd42373760608767b62855d",
          "address_from": {
            "street": "Rua Augusta, 321",
            "city": "Sao Paulo",
            "country": "Brazil",
            "postal_code": "03881100",
          },
          "departure_datetime": "2024-12-01T05:33:20.000Z"
        })

        # act
        response: HandlerResponse = handler.handle(request, self.context)

        # assert
        assert response.get("statusCode") == 400
        use_case.execute.assert_not_called()

    def test_return_internal_server_error_when_use_case_fail(self):
        # arrange
        use_case = mock.Mock(spec=RequestRidePlanningUseCase)
        use_case.execute = mock.Mock()
        use_case.execute.side_effect = Exception()
        handler = RequestRidePlanningHandler(use_case, parse)
        request = copy.copy(self.mock_event)

        # act
        response: HandlerResponse = handler.handle(request, self.context)

        # assert
        assert response.get("statusCode") == 500
        use_case.execute.assert_called()

