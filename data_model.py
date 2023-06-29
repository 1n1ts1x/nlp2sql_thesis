from typing import Any, List
from dataclasses import dataclass, field

@dataclass
class TableRecord:
    data: dict[str, List[Any]] = field(default_factory=dict)

    def __getitem__(self, key: str) -> List[Any]:
        return self.data[key]

    def __setitem__(self, key: str, value: Any) -> None:
        if key not in self.data:
            self.data[key] = []
        self.data[key].append(value)

    def __delitem__(self, key: str) -> None:
        del self.data[key]

@dataclass
class FieldValue:
    _key: List[str]
    _value: List[List[Any]]

    @property
    def key(self):
        return self._key

    @property
    def value(self):
        return self._value


