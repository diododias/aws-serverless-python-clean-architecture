from dataclasses import dataclass


@dataclass
class AddressEntity:
    street: str
    city: str
    country: str
    postal_code: str
