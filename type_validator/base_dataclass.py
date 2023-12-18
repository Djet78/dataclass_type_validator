from dataclasses import dataclass, asdict, astuple

from .base_validator import TypeValidator


@dataclass
class BaseDataclass:
    """Extension class, that add ability to a dataclass to verify own properties values."""

    TYPE_VALIDATOR = TypeValidator()
    ENFORCE_VALIDATION = False

    def __post_init__(self):
        if self.ENFORCE_VALIDATION is True:
            self.check_properties_type()
            self.run_prop_validator_funcs()

    def check_properties_type(self) -> None:
        """Validate all properties against it annotation type."""
        res, errors = self.TYPE_VALIDATOR.check_types(self)
        if res is False:
            raise ValueError(errors)

    def run_prop_validator_funcs(self) -> None:
        """Execute all custom validators

        Validators should be defined as follows: `def <param_name>_validator(self) -> None:...`
        Also, user should define how he want to handle an errors. Raise, or store it somewhere for a while.
        """
        for param in self.as_dict():
            validator_func = getattr(self, f'{param}_validator', None)
            validator_func()

    # TODO add tests for a method.
    def dict2object(self, kwargs: dict) -> None:
        """Parse dict into an instance params.

        Dict keys should be exact the same, as instance params.
        if self.ENFORCE_VALIDATION is True -> will run full verification of a properties.
        """
        for param, value in kwargs.items():
            getattr(self, param)  # Verify that class has required param.
            setattr(self, param, value)

        if self.ENFORCE_VALIDATION is True:
            self.check_properties_type()
            self.run_prop_validator_funcs()

    def as_dict(self) -> dict:
        return asdict(self)

    def as_tuple(self) -> tuple:
        return astuple(self)


@dataclass
class StrictDataclass(BaseDataclass):
    """Extension class, that enforce dataclass validation of own properties values."""

    ENFORCE_VALIDATION = True
