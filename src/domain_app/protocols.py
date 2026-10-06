from typing import Protocol

class Notifier(Protocol):
    def send(self, recipient: str, message: str) -> None:
        ...

class HasId(Protocol):
    id: int