import inspect
from collections.abc import Mapping
from dataclasses import dataclass, asdict
from types import UnionType
from typing import Union, Any, Final, Annotated, Optional, get_origin, get_args


# TODO Add support for following annotation types
#  Probably need to add a recursion for checking an every param.
#  (Need to define how to pass correct expected type. According to data nesting and annotation syntax logic.)
# c: List[int] | set[str] = 'test'
class TypeValidator:

    def __init__(self):
        self.errors: list = []
        self.validators_mapping = {
            str: self.primitives_validator,
            bool: self.primitives_validator,
            bytes: self.primitives_validator,
            int: self.primitives_validator,
            float: self.primitives_validator,
            list: self.set_n_list_validator,
            set: self.set_n_list_validator,
            tuple: self.tuple_validator,
            dict: self.dict_validator,
            Mapping: self.dict_validator,
            Final: self.final_validator,
            Union: self.union_validator,
            UnionType: self.union_validator,
            Any: self.any_validator,
            Annotated: self.annotated_validator,
            Optional: self.union_validator,
        }

    def check_types(self, cls: dataclass) -> tuple[bool, list[str]]:
        self.errors = []

        exp_types = inspect.get_annotations(cls.__class__)
        for attr_name, attr_value in asdict(cls).items():
            lookup_type = get_origin(exp_types[attr_name]) or exp_types[attr_name]
            type_validator = self.validators_mapping.get(lookup_type, self.any_validator)
            type_validator(attr_name, attr_value, exp_types[attr_name])

        res: bool = False if self.errors else True
        return res, self.errors

    def primitives_validator(self, attr_name: str, attr_value, exp_type) -> None:
        if not isinstance(attr_value, exp_type):
            self.put_error(attr_name, attr_value, exp_type)

    def final_validator(self, attr_name: str, attr_value, exp_type) -> None:
        if not isinstance(attr_value, get_args(exp_type)[0]):
            self.put_error(attr_name, attr_value, exp_type)

    def any_validator(self, attr_name: str, attr_value, exp_type) -> None:
        # Validation for Any not needed
        pass

    def union_validator(self, attr_name: str, attr_value, exp_type) -> None:
        expected_types = get_args(exp_type)
        self.primitives_validator(attr_name, attr_value, expected_types)

    def annotated_validator(self, attr_name: str, attr_value, exp_type) -> None:
        lookup_args = get_args(exp_type)
        base_expected_type = lookup_args[0]
        extra_validators = lookup_args[1:]

        if not isinstance(attr_value, base_expected_type):
            self.put_error(attr_name, attr_value, exp_type)
            return

        for validator in extra_validators:
            res, error = validator.validate(attr_value)
            if res is False:
                self.put_error(attr_name, attr_value, exp_type, extra_msg=error)

    def set_n_list_validator(self, attr_name: str, attr_value, exp_type) -> None:
        lookup_args = get_args(exp_type) or exp_type

        # Means that annotation don't have specified values stored in the collection. Passed simple: list / set / ...
        if not isinstance(lookup_args, tuple):
            self.primitives_validator(attr_name, attr_value, exp_type)
            return

        # Get values from UnionType. Handles pipe (|) from: set[int | str | float]
        allowed_entries = set(get_args(arg) or arg for arg in lookup_args)

        if not isinstance(attr_value, (list, set)):
            self.put_error(attr_name, attr_value, exp_type)
            return

        if Any in allowed_entries:
            return

        if not all((isinstance(act_val, tuple(allowed_entries)) for act_val in attr_value)):
            self.put_error(attr_name, attr_value, exp_type)

    def tuple_validator(self, attr_name: str, attr_value, exp_type) -> None:
        lookup_args = get_args(exp_type) or exp_type

        # Means that annotation don't have specified values stored in the collection. Passed simple: list / set / ...
        if not isinstance(lookup_args, tuple):  # tuple
            self.primitives_validator(attr_name, attr_value, exp_type)
            return

        if not isinstance(attr_value, tuple):
            self.put_error(attr_name, attr_value, exp_type)
            return

        if Ellipsis not in lookup_args:  # tuple[int, ...]
            for act_val, exp_index_type in zip(attr_value, lookup_args):
                exp_index_type = get_args(exp_index_type) or exp_index_type
                if exp_index_type == Any:
                    continue
                if not isinstance(act_val, exp_index_type):
                    self.put_error(attr_name, act_val, exp_type)
        else:  # tuple[str, int | str]
            for act_val in attr_value:
                if lookup_args[0] == Any:
                    break
                if not isinstance(act_val, lookup_args[0]):
                    self.put_error(attr_name, act_val, exp_type)

    def dict_validator(self, attr_name: str, attr_value, exp_type) -> None:
        origin = get_origin(exp_type)
        lookup_args = get_args(exp_type) or exp_type

        # Means that annotation don't have specified values stored in the collection. Passed simple: dict / Mapping / Dict
        if not isinstance(lookup_args, tuple):
            self.primitives_validator(attr_name, attr_value, exp_type)
            return

        valid_keys = get_args(lookup_args[0]) or lookup_args[0]
        valid_vals = get_args(lookup_args[1]) or lookup_args[1]

        if valid_keys == (0,):  # Mapping
            if not isinstance(attr_value, exp_type):
                self.put_error(attr_name, attr_value, exp_type)
            return

        self.primitives_validator(attr_name, attr_value, origin)
        if self.errors:
            return

        for key, val in attr_value.items():  # dict[str, str | int]
            if valid_keys != Any and not isinstance(key, valid_keys):
                self.put_error(attr_name, key, valid_keys)
            if valid_vals != Any and not isinstance(val, valid_vals):
                self.put_error(attr_name, val, valid_vals)

    def put_error(self, attr_name: str, attr_value, exp_type, extra_msg=''):
        self.errors.append(
            f'Expected that attr "{attr_name}" would be of type "{exp_type}". '
            f'Value {attr_value}, of type "{type(attr_value)}" was passed.'
            f'{extra_msg}'
        )
