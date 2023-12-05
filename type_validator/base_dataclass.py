from dataclasses import dataclass, asdict, astuple

from .base_validator import TypeValidator


@dataclass
class BaseDataclass:
    TYPE_VALIDATOR = TypeValidator()

    def __post_init__(self):
        self._check_properties_type()
        # TODO add an call for any validation methods that occur for a field.
        #  Match following naming_convention: `def validate_<name_of_a_prop>(self)`

    def _check_properties_type(self):
        res, errors = self.TYPE_VALIDATOR.check_types(self)
        if res is False:
            raise ValueError(errors)

    def as_dict(self):
        return asdict(self)

    def as_tuple(self):
        return astuple(self)
