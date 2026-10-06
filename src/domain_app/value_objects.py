from dataclasses import dataclass
from enum import Enum

class Priority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class Status(str, Enum):
    NEW = "new"
    IN_PROGRESS = "in_progress"
    RESOLVED = "resolved"
    CLOSED = "closed"

@dataclass(frozen=True, slots=True)
class EffortEstimate:
    """Frozen value object для оцінки часу на завдання."""
    hours: float

    def __post_init__(self) -> None:
        if self.hours < 0:
            raise ValueError("Effort cannot be negative")

    def __add__(self, other: "EffortEstimate") -> "EffortEstimate":
        return EffortEstimate(self.hours + other.hours)

    def __str__(self) -> str:
        return f"{self.hours}h"