"""Module provides Base dataclass for subclassing, providing validation functionality of dataclass params."""
from .base_validator import TypeValidator
from .validators import NotEmpty, ValueRange, LimitedLength, Options
from .base_dataclass import BaseDataclass, StrictDataclass
