from typing import TypedDict
from typing_extensions import NotRequired

class TaskPayload(TypedDict):
    """TypedDict для зовнішніх даних (наприклад, з API)."""
    id: int
    title: str
    description: str
    priority: str
    type: str  # 'bug' або 'feature'
    severity: NotRequired[str]
    business_value: NotRequired[int]