import json

from typing import TypedDict
from pydantic import ValidationError

OK_STATUS_CODE = 200
BAD_REQUEST_STATUS_CODE = 400
NOT_FOUND = 404
INTERNAL_SERVER_ERROR_STATUS_CODE = 500


class HandlerResponse(TypedDict):
    # pylint: disable=C0103
    statusCode: int
    body: str


def ok_response(body: dict) -> HandlerResponse:
    return {
        "statusCode": OK_STATUS_CODE,
        "body": json.dumps({"data": body})
    }


def not_found_response(error: str) -> HandlerResponse:
    return {
        "statusCode": NOT_FOUND,
        "body": json.dumps({"error": error})
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
