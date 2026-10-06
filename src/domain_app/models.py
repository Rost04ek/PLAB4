from abc import ABC
from dataclasses import dataclass, field
from collections.abc import Iterator
from domain_app.value_objects import Priority, Status, EffortEstimate

@dataclass(kw_only=True)
class Task(ABC):
    """Abstract Base Class для завдань."""
    id: int
    title: str
    description: str
    priority: Priority
    estimate: EffortEstimate
    status: Status = Status.NEW

    @property
    def is_completed(self) -> bool:
        """Property для перевірки завершеності."""
        return self.status in {Status.RESOLVED, Status.CLOSED}

    def __str__(self) -> str:
        return f"[{self.priority.upper()}] {self.title} ({self.status.value})"


@dataclass(kw_only=True)
class BugTask(Task):
    steps_to_reproduce: str
    severity: str


@dataclass(kw_only=True)
class FeatureTask(Task):
    business_value: int


class TaskBoard:
    """Domain class (Composition), що містить список завдань для конкретного проєкту/дошки."""
    
    def __init__(self, name: str) -> None:
        self.name = name
        self._tasks: list[Task] = []

    def add_task(self, task: Task) -> None:
        self._tasks.append(task)

    # --- Dunder Methods ---
    def __len__(self) -> int:
        return len(self._tasks)

    def __iter__(self) -> Iterator[Task]:
        return iter(self._tasks)

    def __contains__(self, task_id: int) -> bool:
        return any(task.id == task_id for task in self._tasks)

    # --- Бізнес-логіка дошки ---
    def filter_by_priority(self, priority: Priority) -> list[Task]:
        return [t for t in self._tasks if t.priority == priority]

    def filter_by_status(self, status: Status) -> list[Task]:
        return [t for t in self._tasks if t.status == status]

    @property
    def stats(self) -> dict[str, int]:
        completed = sum(1 for t in self._tasks if t.is_completed)
        return {
            "total": len(self),
            "completed": completed,
            "uncompleted": len(self) - completed
        }