from abc import ABC, abstractmethod
from domain_app.models import Task
from domain_app.value_objects import Status
from domain_app.protocols import Notifier
from domain_app.repositories import InMemoryRepository

class TaskPolicy(ABC):
    """ABC для стратегії/політики роботи з тасками (OCP)."""
    @abstractmethod
    def can_close(self, task: Task) -> bool:
        ...

class StrictTaskPolicy(TaskPolicy):
    def can_close(self, task: Task) -> bool:
        # Завдання можна закрити лише якщо воно було в роботі або вирішене
        return task.status in {Status.IN_PROGRESS, Status.RESOLVED}

class ConsoleNotifier:
    """Concrete implementation of Notifier Protocol."""
    def send(self, recipient: str, message: str) -> None:
        print(f"[Email to {recipient}]: {message}")

class TaskManagerService:
    """Application Service, що демонструє Dependency Injection та оркестрацію."""
    
    def __init__(
        self,
        repository: InMemoryRepository[Task],
        notifier: Notifier,
        policy: TaskPolicy
    ) -> None:
        self._repository = repository
        self._notifier = notifier
        self._policy = policy

    def change_task_status(self, task_id: int, new_status: Status, user_email: str) -> None:
        task = self._repository.get(task_id)
        if not task:
            raise ValueError(f"Task {task_id} not found")

        if new_status == Status.CLOSED and not self._policy.can_close(task):
            raise ValueError("Policy violation: Cannot close task from current status.")

        old_status = task.status
        task.status = new_status
        
        self._notifier.send(
            user_email, 
            f"Status of '{task.title}' changed from {old_status.value} to {new_status.value}"
        )