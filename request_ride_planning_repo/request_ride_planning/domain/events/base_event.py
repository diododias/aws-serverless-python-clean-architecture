import uuid
from dataclasses import dataclass, field
from datetime import datetime, UTC


@dataclass
class EventData:
    pass


@dataclass
class BaseEvent:
    source: str
    data: EventData
    name: str = "base_event"
    spec_version: str = "1.0"
    data_content_type: str = "application/json"
    event_id: str = field(default_factory=uuid.uuid4)
    time: datetime = field(default=lambda x: datetime.now(UTC))
