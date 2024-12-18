from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any

from .exception import BusinessRuleValidationException
from .rule import BaseBusinessRule


@dataclass(frozen=True)
class ValueObject(ABC):
    """Base class for Value Objects in DDD, providing equality, hashing, and string representation."""

    @abstractmethod
    def __eq__(self, other: Any) -> bool:
        """Override equality comparison to compare values of the object."""
        if not isinstance(other, ValueObject):
            return False
        return self.__dict__ == other.__dict__

    @abstractmethod
    def __hash__(self) -> int:
        """Override hash function for ValueObjects to ensure consistent behavior."""
        return hash(tuple(sorted(self.__dict__.items())))

    def __repr__(self) -> str:
        """Provide a meaningful string representation for debugging."""
        return f"{self.__class__.__name__}({', '.join(f'{k}={v!r}' for k, v in self.__dict__.items())})"

    def check_rule(self, rule: BaseBusinessRule) -> None:
        if not rule.is_valid():
            raise BusinessRuleValidationException(rule)

    @classmethod
    @abstractmethod
    def create(cls, *args, **kwargs) -> "ValueObject":
        """Abstract method for creating the value object, enforcing rule validation."""
        # Default implementation returns True. Subclasses may override this method to enforce specific validation rules.
