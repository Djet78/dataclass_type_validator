from abc import ABC, abstractmethod
from collections.abc import Sized
from dataclasses import dataclass
from typing import Any


@dataclass
class ValidatorBase(ABC):
    @abstractmethod
    def validate(self, value: Any) -> tuple[bool, str]:
        pass


@dataclass
class ValueRange(ValidatorBase):
    lo: int | float
    hi: int | float

    def validate(self, value: int | float) -> tuple[bool, str]:
        res = self.lo <= value <= self.hi
        return res, '' if res is True else (
            f'Value "{value}" should met this condition: ' f'{self.lo} <= <value> <= {self.hi}.'
        )


@dataclass
class NotEmpty(ValidatorBase):
    def validate(self, value: Sized) -> tuple[bool, str]:
        res = len(value) > 0
        return res, '' if res is True else f'Value "{value}" should be not empty.'


@dataclass
class Options(ValidatorBase):
    opts: set[str | int]

    def validate(self, value: str | int) -> tuple[bool, str]:
        res = value in self.opts
        return res, '' if res is True else f'Value "{value}" should be chosen from this options: {self.opts}'


@dataclass
class LimitedLength(ValidatorBase):
    length: int

    def __post_init__(self):
        if self.length < 1:
            raise ValueError('length should bigger than 0.')

    def validate(self, value: Sized) -> tuple[bool, str]:
        res = len(value) <= self.length
        return res, '' if res is True else f'Value "{value}" length should be <= {self.length}. Actual is {len(value)}'
