import json
from dataclasses import asdict

from typing import TypedDict
from pydantic import ValidationError

from get_ride_planning.domain.entities.ride_planning_entity import RidePlanningEntity

OK_STATUS_CODE = 200
BAD_REQUEST_STATUS_CODE = 400
NOT_FOUND = 404
INTERNAL_SERVER_ERROR_STATUS_CODE = 500


class HandlerResponse(TypedDict):
    # pylint: disable=C0103
    statusCode: int
    body: str


def ok_response(ride_planning: RidePlanningEntity) -> HandlerResponse:
    return {
        "statusCode": OK_STATUS_CODE,
        "body": json.dumps({
            "id": ride_planning.id,
            "user_id": ride_planning.user_id,
            "address_from": {
              "street": ride_planning.address_from.street,
              "city": ride_planning.address_from.city,
              "country": ride_planning.address_from.country,
              "postal_code": ride_planning.address_from.postal_code
            },
            "address_to": {
              "street": ride_planning.address_to.street,
              "city": ride_planning.address_to.city,
              "country": ride_planning.address_to.country,
              "postal_code": ride_planning.address_to.postal_code
            },
            "status": ride_planning.status.value,
            "ride_options": [{
                "id": ro.id,
                "provider_id": ro.provider_id,
                "provider": ro.provider,
                "tier": ro.tier,
                "price": ro.price,
                "accepted": ro.accepted
            } for ro in ride_planning.ride_options],
            "departure_datetime": ride_planning.departure_datetime.isoformat(),
            "created_at": ride_planning.created_at.isoformat(),
            "modified_at": ride_planning.modified_at.isoformat()
          })
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
