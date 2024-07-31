from enum import Enum


class CreationStatus(Enum):
    CREATED = "CREATED"
    FAILED = "FAILED"
    REFUSED = "REFUSED"