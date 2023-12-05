from dataclasses import dataclass, asdict, astuple

from .base_validator import TypeValidator


@dataclass
class BaseDataclass:
    TYPE_VALIDATOR = TypeValidator()
    ENFORCE_VALIDATION = False

    def __post_init__(self):
        if self.ENFORCE_VALIDATION is True:
            self.check_properties_type()
            self.run_prop_validator_funcs()

    def check_properties_type(self) -> None:
        res, errors = self.TYPE_VALIDATOR.check_types(self)
        if res is False:
            raise ValueError(errors)

    def run_prop_validator_funcs(self) -> None:
        for param in self.as_dict().keys():
            validator_func = getattr(self, f'{param}_validator', None)
            validator_func()

    def dict2object(self, kwargs: dict) -> None:
        for param, value in kwargs.items():
            getattr(self, param)  # Verify that class has required param.
            setattr(self, param, value)

    def as_dict(self) -> dict:
        return asdict(self)

    def as_tuple(self) -> tuple:
        return astuple(self)


@dataclass
class StrictDataclass(BaseDataclass):
    ENFORCE_VALIDATION = True
