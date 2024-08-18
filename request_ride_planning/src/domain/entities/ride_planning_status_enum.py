from enum import Enum


class RidePlanningStatusEnum(Enum):
    REQUESTED = "REQUESTED"
    WAITING_FOR_APPROVAL = "WAITING_FOR_APPROVAL"
    APPROVED = "APPROVED"
    EXPIRED = "EXPIRED"
    REQUEST_FAILED = "REQUEST_FAILED"
