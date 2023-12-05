from dataclasses import dataclass, asdict, astuple

from .base_validator import TypeValidator


@dataclass
class BaseDataclass:
    TYPE_VALIDATOR = TypeValidator()
    ENFORCE_VALIDATION = False

    def __post_init__(self):
        if self.ENFORCE_VALIDATION is True:
            self.check_properties_type()
            # TODO add an call for any validation methods that occur for a field.
            #  Match following naming_convention: `def validate_<name_of_a_prop>(self)`

    def check_properties_type(self) -> None:
        res, errors = self.TYPE_VALIDATOR.check_types(self)
        if res is False:
            raise ValueError(errors)

    def dict2object(self, kwargs: dict) -> None:
        for param, value in kwargs.items():
            getattr(self, param)  # Verify that class has required param.
            setattr(self, param, value)

    def as_dict(self) -> dict:
        return asdict(self)

    def as_tuple(self) -> tuple:
        return astuple(self)

    def check_params_type(self) -> None:
        self.TYPE_VALIDATOR.check_types(self)


@dataclass
class StrictDataclass(BaseDataclass):
    ENFORCE_VALIDATION = True
