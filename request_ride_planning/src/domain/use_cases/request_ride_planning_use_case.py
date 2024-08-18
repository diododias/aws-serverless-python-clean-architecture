from abc import ABCMeta, abstractmethod
from datetime import datetime

from src.domain.entities.address_entity import AddressEntity
from src.domain.value_objects.user_id import UserId


class RequestRidePlanningUseCase(metaclass=ABCMeta):
    @abstractmethod
    def execute(self,
                      user_id: UserId,
                      address_from: AddressEntity,
                      address_to: AddressEntity,
                      departure_datetime: datetime) -> str:
        raise NotImplementedError()
