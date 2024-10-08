import json

from typing import TypedDict
from pydantic import ValidationError

OK_STATUS_CODE = 200
CREATED_STATUS_CODE = 201
BAD_REQUEST_STATUS_CODE = 400
INTERNAL_SERVER_ERROR_STATUS_CODE = 500


class HandlerResponse(TypedDict):
    # pylint: disable=C0103
    statusCode: int
    body: str


def created_response(body: dict) -> HandlerResponse:
    return {
        "statusCode": CREATED_STATUS_CODE,
        "body": json.dumps({"data": body})
    }


def validation_error_response(error: ValidationError) -> HandlerResponse:
    return bad_request_response(
        json.dumps(
            error.errors(
                include_url=False,
                include_context=False,
                include_input=False
            )
        )
    )


def bad_request_response(error: str) -> HandlerResponse:
    return {
        "statusCode": BAD_REQUEST_STATUS_CODE,
        "body": json.dumps({"error": error})
    }


def internal_server_error_response(error: str) -> HandlerResponse:
    return {
        "statusCode": INTERNAL_SERVER_ERROR_STATUS_CODE,
        "body": json.dumps({"error": error})
    }
