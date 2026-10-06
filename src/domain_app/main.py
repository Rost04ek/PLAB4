from domain_app.value_objects import Priority, Status, EffortEstimate
from domain_app.models import BugTask, FeatureTask, TaskBoard
from domain_app.repositories import InMemoryRepository
from domain_app.services import TaskManagerService, ConsoleNotifier, StrictTaskPolicy
from domain_app.models import Task

def main() -> None:
    # 1. Створюємо Value Objects та Tasks
    bug = BugTask(
        id=1,
        title="Fix login screen crash",
        description="App crashes on empty password",
        priority=Priority.CRITICAL,
        estimate=EffortEstimate(2.5),
        steps_to_reproduce="1. Open App 2. Click Login",
        severity="High"
    )

    feature = FeatureTask(
        id=2,
        title="Add OAuth2 Login",
        description="Support Google/GitHub login",
        priority=Priority.MEDIUM,
        estimate=EffortEstimate(10.0),
        business_value=100
    )

    # 2. Використання Composition (TaskBoard) та Dunder Methods
    board = TaskBoard("Sprint 1")
    board.add_task(bug)
    board.add_task(feature)

    print(f"Total tasks on board: {len(board)}") # __len__
    print(f"Is task 1 on board? {1 in board}")   # __contains__
    
    print("\n--- Board Tasks ---")
    for task in board: # __iter__
        print(task)    # __str__

    print("\n--- Stats ---")
    print(board.stats)

    # 3. Setup Dependencies (DI) та Repository
    repo = InMemoryRepository[Task]()
    repo.add(bug)
    repo.add(feature)

    service = TaskManagerService(
        repository=repo,
        notifier=ConsoleNotifier(),
        policy=StrictTaskPolicy()
    )

    # 4. Виконання бізнес-операцій через Service
    print("\n--- Processing ---")
    # Переводимо баг в In Progress, а потім в Closed
    service.change_task_status(1, Status.IN_PROGRESS, "developer@example.com")
    service.change_task_status(1, Status.CLOSED, "pm@example.com")
    
    print("\n--- Updated Stats ---")
    print(board.stats) # Статистика оновиться, бо об'єкти передаються за посиланням

if __name__ == "__main__":
    main()