from aws_lambda_powertools.utilities.parser.models import APIGatewayProxyEventModel

from pydantic import BaseModel


class PathParameters(BaseModel):
    ride_planning_id: str


class HandlerRequest(APIGatewayProxyEventModel):
    pathParameters: PathParameters
