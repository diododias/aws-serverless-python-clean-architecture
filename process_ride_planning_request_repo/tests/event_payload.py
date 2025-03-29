import json
from datetime import datetime

from process_ride_planning_request.interface_adapters.handler_request import MessageSchema, RequestedEventSchema

sqs_event = {
  "Records": [
    {
      "messageId": "059f36b4-87a3-44ab-83d2-661975830a7d",
      "receiptHandle": "AQEBwJnKyrHigUMZj6rYigCgxlaS3SLy0a",
      "body": json.dumps({
          "data": {
            "user_id": "user123",
            "ride_planning_id": "ride123"
          },
          "name": "RidePlanningRequestedEvent",
          "source": "source",
          "spec_version": "1.0",
          "data_content_type": "application/json",
          "event_id": "event123",
          "correlation_id": "correlation123",
          "time": "2023-10-01T12:00:00Z"
        }),
      "attributes": {
        "ApproximateReceiveCount": "1",
        "SentTimestamp": "1545082649183",
        "SenderId": "AIDAIENQZJOLO23YVJ4VO",
        "ApproximateFirstReceiveTimestamp": "1545082649185"
      },
      "messageAttributes": {},
      "md5OfBody": "e4e68fb7bd0e697a0ae8f1bb342846b3",
      "eventSource": "aws:sqs",
      "eventSourceARN": "arn:aws:sqs:us-east-2: 123456789012:my-queue",
      "awsRegion": "us-east-1"
    },
    {
      "messageId": "244fc6b4-87a3-44ab-83d2-361172410c3a",
      "receiptHandle": "AQEBwJnKyrHigUMZj6rYigCgxlaS3SLy0a",
      "body": json.dumps({
          "data": {
            "user_id": "user123"
          },
          "name": "RidePlanningRequestedEvent",
          "source": "source",
          "spec_version": "1.0",
          "data_content_type": "application/json",
          "event_id": "event123",
          "correlation_id": "correlation123",
          "time": "2023-10-01T12:00:00Z"
        }),
      "attributes": {
        "ApproximateReceiveCount": "1",
        "SentTimestamp": "1545082649183",
        "SenderId": "AIDAIENQZJOLO23YVJ4VO",
        "ApproximateFirstReceiveTimestamp": "1545082649185"
      },
      "messageAttributes": {},
      "md5OfBody": "e4e68fb7bd0e697a0ae8f1bb342846b3",
      "eventSource": "aws:sqs",
      "eventSourceARN": "arn:aws:sqs:us-east-2: 123456789012:my-queue",
      "awsRegion": "us-east-1"
    }
  ]
}