from dataclasses import dataclass, field
from typing import List, Set, Mapping, Union, Any, Dict, Tuple, Final, Annotated, Optional

import pytest

from .base_validator import TypeValidator
from .base_dataclass import BaseDataclass, StrictDataclass
from .validators import NotEmpty, ValueRange, Options, LimitedLength


@pytest.mark.internal
@pytest.mark.parametrize('param_type, param_value, exp_res, exp_errors', [
    (str, 'test_string', True, []),
    (str, '', True, []),
    (str, 0, False, ["""Expected that attr "test_variable" would be of type "<class \'str\'>". Value 0, of type "<class \'int\'>" was passed."""]),
    (int, 1, True, []),
    (int, -1, True, []),
    (int, 'bad_val', False, ["""Expected that attr "test_variable" would be of type "<class \'int\'>". Value bad_val, of type "<class \'str\'>" was passed."""]),
    (float, 0.0, True, []),
    (float, 1, False, ["""Expected that attr "test_variable" would be of type "<class \'float\'>". Value 1, of type "<class \'int\'>" was passed."""]),
    (bool, True, True, []),
    (bool, 0, False, ["""Expected that attr "test_variable" would be of type "<class \'bool\'>". Value 0, of type "<class \'int\'>" was passed."""]),
    (bytes, b'test_string', True, []),
    (bytes, 'simple_string', False, ["""Expected that attr "test_variable" would be of type "<class \'bytes\'>". Value simple_string, of type "<class \'str\'>" was passed."""]),
    (List, field(default_factory=list), True, []),
    (list, field(default_factory=lambda: ['item_1', 'item_2']), True, []),
    (list[TypeValidator], field(default_factory=lambda: [TypeValidator(), TypeValidator()]), True, []),
    (list[int], field(default_factory=lambda: [1, 2]), True, []),
    (list[str], field(default_factory=lambda: ['item_1', 'item_2']), True, []),
    (list[str], field(default_factory=lambda: ['item_1', 2]), False, ["""Expected that attr "test_variable" would be of type "list[str]". Value [\'item_1\', 2], of type "<class \'list\'>" was passed."""]),
    (list[str | int], field(default_factory=lambda: ['item_1', 2]), True, []),
    (list[str, int], field(default_factory=lambda: ['item_1', 2]), True, []),
    (list, 'bad_value', False, ["""Expected that attr "test_variable" would be of type "<class \'list\'>". Value bad_value, of type "<class \'str\'>" was passed."""]),
    (list[Any], field(default_factory=lambda: ['item_1', 2, [], {}]), True, []),
    (Set, field(default_factory=set), True, []),
    (set, field(default_factory=lambda: {'item_1', 'item_2'}), True, []),
    (set[int], field(default_factory=lambda: {1, 2}), True, []),
    (set[str], field(default_factory=lambda: {'item_1', 'item_2'}), True, []),
    (set[str], field(default_factory=lambda: {1, 'item_2'}), False, ["""Expected that attr "test_variable" would be of type "set[str]". Value {1, \'item_2\'}, of type "<class \'set\'>" was passed."""]),
    (set[str | int], field(default_factory=lambda: ['item_1', 2]), True, []),
    (set[str, int], field(default_factory=lambda: ['item_1', 2]), True, []),
    (set, 'bad_value', False, ["""Expected that attr "test_variable" would be of type "<class \'set\'>". Value bad_value, of type "<class \'str\'>" was passed."""]),
    (set[Any], field(default_factory=lambda: {'item_1', 2, (1, 2)}), True, []),
    (tuple[int], (1, ), True, []),
    (tuple[str, int], ('item_1', 2), True, []),
    (tuple[str, int], (1, 2), False, ["""Expected that attr "test_variable" would be of type "tuple[str, int]". Value 1, of type "<class \'int\'>" was passed."""]),
    (tuple[str], 'bad_value', False, ["""Expected that attr "test_variable" would be of type "tuple[str]". Value bad_value, of type "<class \'str\'>" was passed."""]),
    (tuple[str | int], (1, ), True, []),
    (tuple[str | int], ('item_1', ), True, []),
    (tuple[str | int], ([], ), False, ["""Expected that attr "test_variable" would be of type "tuple[str | int]". Value [], of type "<class \'list\'>" was passed."""]),
    (tuple[str | int, int], ('item_1', 2), True, []),
    (tuple[str | int, int], ('item_1', 'item_2'), False, ["""Expected that attr "test_variable" would be of type "tuple[str | int, int]". Value item_2, of type "<class \'str\'>" was passed."""]),
    (tuple, (1, 2, 3), True, []),
    (Tuple, (1, 2, 3), True, []),
    (Tuple[int, int, int], (1, 2, 'item_3'), False, ["""Expected that attr "test_variable" would be of type "typing.Tuple[int, int, int]". Value item_3, of type "<class \'str\'>" was passed."""]),
    (Tuple[int, ...], (1, 2, 3), True, []),
    (Tuple[int, ...], (1, 2, 'item_3'), False, ["""Expected that attr "test_variable" would be of type "typing.Tuple[int, ...]". Value item_3, of type "<class \'str\'>" was passed."""]),
    (tuple[Any], (1, '2', {1, 2}), True, []),
    (tuple[Any, ...], (1, '2', {1, 2}), True, []),
    (Tuple[Any], (1, '2', {1, 2}), True, []),
    (Tuple[Any, ...], (1, '2', {1, 2}), True, []),
    (dict, field(default_factory=dict), True, []),
    (Dict, field(default_factory=dict), True, []),
    (Mapping, field(default_factory=dict), True, []),
    (dict[str, str], 'bad_value', False, ["""Expected that attr "test_variable" would be of type "<class \'dict\'>". Value bad_value, of type "<class \'str\'>" was passed."""]),
    (dict[str, str], field(default_factory=lambda: {'key': 'val'}), True, []),
    (dict[str, str], field(default_factory=lambda: {'key': 1}), False, ["""Expected that attr "test_variable" would be of type "<class \'str\'>". Value 1, of type "<class \'int\'>" was passed."""]),
    (dict[int | str, str], field(default_factory=lambda: {1: 'val'}), True, []),
    (dict[int | str, str], field(default_factory=lambda: {'key': 'val'}), True, []),
    (dict[int | str, str], field(default_factory=lambda: {('tuple',): 'val'}), False, ["""Expected that attr "test_variable" would be of type "(<class \'int\'>, <class \'str\'>)". Value (\'tuple\',), of type "<class \'tuple\'>" was passed."""]),
    (dict[str, int | str], field(default_factory=lambda: {'key': 'val'}), True, []),
    (dict[str, int | str], field(default_factory=lambda: {'key': 2}), True, []),
    (dict[str, int | str], field(default_factory=lambda: {'key': []}), False, ["""Expected that attr "test_variable" would be of type "(<class \'int\'>, <class \'str\'>)". Value [], of type "<class \'list\'>" was passed."""]),
    (Dict[int | str, str], field(default_factory=lambda: {1: 'val'}), True, []),
    (Dict[int | str, str], field(default_factory=lambda: {'key': 'val'}), True, []),
    (Dict[int | str, str], field(default_factory=lambda: {('tuple',): 'val'}), False, ["""Expected that attr "test_variable" would be of type "(<class \'int\'>, <class \'str\'>)". Value (\'tuple\',), of type "<class \'tuple\'>" was passed."""]),
    (Dict[str, int | str], field(default_factory=lambda: {'key': 'val'}), True, []),
    (Dict[str, int | str], field(default_factory=lambda: {'key': 2}), True, []),
    (Dict[str, int | str], field(default_factory=lambda: {'key': []}), False, ["""Expected that attr "test_variable" would be of type "(<class \'str\'>, <class \'int\'>)". Value [], of type "<class \'list\'>" was passed."""]),
    (Mapping[int | str, str], field(default_factory=lambda: {1: 'val'}), True, []),
    (Mapping[int | str, str], field(default_factory=lambda: {'key': 'val'}), True, []),
    (Mapping[int | str, str], field(default_factory=lambda: {('tuple',): 'val'}), False, ["""Expected that attr "test_variable" would be of type "(<class \'int\'>, <class \'str\'>)". Value (\'tuple\',), of type "<class \'tuple\'>" was passed."""]),
    (Mapping[str, int | str], field(default_factory=lambda: {'key': 'val'}), True, []),
    (Mapping[str, int | str], field(default_factory=lambda: {'key': 2}), True, []),
    (Mapping[str, int | str], field(default_factory=lambda: {'key': []}), False, ["""Expected that attr "test_variable" would be of type "(<class \'int\'>, <class \'str\'>)". Value [], of type "<class \'list\'>" was passed."""]),
    (dict[Any, Any], field(default_factory=lambda: {'key': 'val'}), True, []),
    (dict[Any, Any], field(default_factory=lambda: {1: 2}), True, []),
    (dict[Any, str], field(default_factory=lambda: {'key': 'val'}), True, []),
    (dict[Any, str], field(default_factory=lambda: {1: 'val'}), True, []),
    (dict[Any, str], field(default_factory=lambda: {'bad val': 1}), False, ["""Expected that attr "test_variable" would be of type "<class \'str\'>". Value 1, of type "<class \'int\'>" was passed."""]),
    (dict[str, Any], field(default_factory=lambda: {1: 'bad key'}), False, ["""Expected that attr "test_variable" would be of type "<class \'str\'>". Value 1, of type "<class \'int\'>" was passed."""]),
    (Dict[Any, Any], field(default_factory=lambda: {'key': 'val'}), True, []),
    (Dict[Any, Any], field(default_factory=lambda: {1: 2}), True, []),
    (Dict[Any, str], field(default_factory=lambda: {'key': 'val'}), True, []),
    (Dict[Any, str], field(default_factory=lambda: {1: 'val'}), True, []),
    (Dict[Any, str], field(default_factory=lambda: {'bad val': 1}), False, ["""Expected that attr "test_variable" would be of type "<class \'str\'>". Value 1, of type "<class \'int\'>" was passed."""]),
    (Dict[str, Any], field(default_factory=lambda: {1: 'bad key'}), False, ["""Expected that attr "test_variable" would be of type "<class \'str\'>". Value 1, of type "<class \'int\'>" was passed."""]),
    (Mapping[Any, Any], field(default_factory=lambda: {'key': 'val'}), True, []),
    (Mapping[Any, Any], field(default_factory=lambda: {1: 2}), True, []),
    (Mapping[Any, str], field(default_factory=lambda: {'key': 'val'}), True, []),
    (Mapping[Any, str], field(default_factory=lambda: {1: 'val'}), True, []),
    (Mapping[Any, str], field(default_factory=lambda: {'bad val': 1}), False, ["""Expected that attr "test_variable" would be of type "<class \'str\'>". Value 1, of type "<class \'int\'>" was passed."""]),
    (Mapping[str, Any], field(default_factory=lambda: {1: 'bad key'}), False, ["""Expected that attr "test_variable" would be of type "<class \'str\'>". Value 1, of type "<class \'int\'>" was passed."""]),
    (Final[str], 'valid_str', True, []),
    (Final[str], 1, False, ["""Expected that attr "test_variable" would be of type "typing.Final[str]". Value 1, of type "<class \'int\'>" was passed."""]),
    (Union[str], 'valid_str', True, []),
    (Union[str], 1, False, ["""Expected that attr "test_variable" would be of type "<class \'str\'>". Value 1, of type "<class \'int\'>" was passed."""]),
    (Union[str | int], 1, True, []),
    (Union[str | int], 'valid_str', True, []),
    (Union[str | int], (1, 2), False, ["""Expected that attr "test_variable" would be of type "(<class \'str\'>, <class \'int\'>)". Value (1, 2), of type "<class \'tuple\'>" was passed."""]),
    (str | int, 'valid_str', True, []),
    (str | int, (1, 2), False, ["""Expected that attr "test_variable" would be of type "(<class \'str\'>, <class \'int\'>)". Value (1, 2), of type "<class \'tuple\'>" was passed."""]),
    (Any, 1, True, []),
    (Any, 'valid_str', True, []),
    (Annotated[int, ValueRange(-10, 10)], 0, True, []),
    (Annotated[int, ValueRange(-10, 10)], -10, True, []),
    (Annotated[int, ValueRange(-10, 10)], -9, True, []),
    (Annotated[int, ValueRange(-10, 10)], 9, True, []),
    (Annotated[int, ValueRange(-10, 10)], 10, True, []),
    (Annotated[int, ValueRange(-10, 10)], -11, False, ["""Expected that attr "test_variable" would be of type "typing.Annotated[int, ValueRange(lo=-10, hi=10)]". Value -11, of type "<class \'int\'>" was passed.Value "-11" should met this condition: -10 <= <value> <= 10."""]),
    (Annotated[int, ValueRange(-10, 10)], 11, False, ["""Expected that attr "test_variable" would be of type "typing.Annotated[int, ValueRange(lo=-10, hi=10)]". Value 11, of type "<class \'int\'>" was passed.Value "11" should met this condition: -10 <= <value> <= 10."""]),
    (Annotated[float, ValueRange(-10.0, 10.0)], 0.0, True, []),
    (Annotated[float, ValueRange(-10.0, 10.0)], -10.0, True, []),
    (Annotated[float, ValueRange(-10.0, 10.0)], -9.9, True, []),
    (Annotated[float, ValueRange(-10.0, 10.0)], 9.9, True, []),
    (Annotated[float, ValueRange(-10.0, 10.0)], 10.0, True, []),
    (Annotated[float, ValueRange(-10.0, 10.0)], -10.1, False, ["""Expected that attr "test_variable" would be of type "typing.Annotated[float, ValueRange(lo=-10.0, hi=10.0)]". Value -10.1, of type "<class \'float\'>" was passed.Value "-10.1" should met this condition: -10.0 <= <value> <= 10.0."""]),
    (Annotated[float, ValueRange(-10.0, 10.0)], 10.1, False, ["""Expected that attr "test_variable" would be of type "typing.Annotated[float, ValueRange(lo=-10.0, hi=10.0)]". Value 10.1, of type "<class \'float\'>" was passed.Value "10.1" should met this condition: -10.0 <= <value> <= 10.0."""]),
    (Annotated[str, NotEmpty()], 'valid_str', True, []),
    (Annotated[str, NotEmpty()], '', False, ["""Expected that attr "test_variable" would be of type "typing.Annotated[str, NotEmpty()]". Value , of type "<class \'str\'>" was passed.Value "" should be not empty."""]),
    (Annotated[list, NotEmpty()], field(default_factory=lambda: [1, 2, 3]), True, []),
    (Annotated[list, NotEmpty()], field(default_factory=lambda: []), False, ["""Expected that attr "test_variable" would be of type "typing.Annotated[list, NotEmpty()]". Value [], of type "<class \'list\'>" was passed.Value "[]" should be not empty."""]),
    (Annotated[tuple, NotEmpty()], (1, 2, 3), True, []),
    (Annotated[tuple, NotEmpty()], tuple(), False, ["""Expected that attr "test_variable" would be of type "typing.Annotated[tuple, NotEmpty()]". Value (), of type "<class \'tuple\'>" was passed.Value "()" should be not empty."""]),
    (Annotated[set, NotEmpty()], field(default_factory=lambda: {1, 2, 3}), True, []),
    (Annotated[set, NotEmpty()], field(default_factory=lambda: set()), False, ["""Expected that attr "test_variable" would be of type "typing.Annotated[set, NotEmpty()]". Value set(), of type "<class \'set\'>" was passed.Value "set()" should be not empty."""]),
    (Annotated[dict, NotEmpty()], field(default_factory=lambda: {1: 1, 2: 2, 3: 3}), True, []),
    (Annotated[dict, NotEmpty()], field(default_factory=lambda: {}), False, ["""Expected that attr "test_variable" would be of type "typing.Annotated[dict, NotEmpty()]". Value {}, of type "<class \'dict\'>" was passed.Value "{}" should be not empty."""]),
    (Annotated[str, Options({'opt_1', 'opt_2'})], 'opt_1', True, []),
    (Annotated[str, Options({'opt_1', 'opt_2'})], 'opt_2', True, []),
    (Annotated[str, Options({'opt_1', 'opt_2'})], 'bad_opt', False, ["""Expected that attr "test_variable" would be of type "typing.Annotated[str, Options(opts={\'opt_1\', \'opt_2\'})]". Value bad_opt, of type "<class \'str\'>" was passed.Value "bad_opt" should be chosen from this options: {\'opt_1\', \'opt_2\'}"""]),
    (Annotated[int, Options({1, 2})], 1, True, []),
    (Annotated[int, Options({1, 2})], 2, True, []),
    (Annotated[int, Options({1, 2})], 100, False, ["""Expected that attr "test_variable" would be of type "typing.Annotated[int, Options(opts={1, 2})]". Value 100, of type "<class \'int\'>" was passed.Value "100" should be chosen from this options: {1, 2}"""]),
    (Annotated[str, LimitedLength(2)], 'ok', True, []),
    (Annotated[str, LimitedLength(2)], '!', True, []),
    (Annotated[str, LimitedLength(2)], 'not', False, ["""Expected that attr "test_variable" would be of type "typing.Annotated[str, LimitedLength(length=2)]". Value not, of type "<class \'str\'>" was passed.Value "not" length should be <= 2. Actual is 3"""]),
    (Annotated[list, LimitedLength(2)], field(default_factory=lambda: [1, 2]), True, []),
    (Annotated[list, LimitedLength(2)], field(default_factory=lambda: [1]), True, []),
    (Annotated[list, LimitedLength(2)], field(default_factory=lambda: [1, 2, 3]), False, ["""Expected that attr "test_variable" would be of type "typing.Annotated[list, LimitedLength(length=2)]". Value [1, 2, 3], of type "<class \'list\'>" was passed.Value "[1, 2, 3]" length should be <= 2. Actual is 3"""]),
    (Annotated[dict, LimitedLength(2)], field(default_factory=lambda: {'1': 1, '2': 2}), True, []),
    (Annotated[dict, LimitedLength(2)], field(default_factory=lambda: {'1': 1}), True, []),
    (Annotated[dict, LimitedLength(1)], field(default_factory=lambda: {'1': 1, '2': 2}), False, ["""Expected that attr "test_variable" would be of type "typing.Annotated[dict, LimitedLength(length=1)]". Value {\'1\': 1, \'2\': 2}, of type "<class \'dict\'>" was passed.Value "{\'1\': 1, \'2\': 2}" length should be <= 1. Actual is 2"""]),
    (Annotated[str, NotEmpty(), LimitedLength(10)], '', False, ["""Expected that attr "test_variable" would be of type "typing.Annotated[str, NotEmpty(), LimitedLength(length=10)]". Value , of type "<class \'str\'>" was passed.Value "" should be not empty."""]),
    (Annotated[str, NotEmpty(), LimitedLength(10)], '1', True, []),
    (Annotated[str, NotEmpty(), LimitedLength(10)], '1234567890', True, []),
    (Annotated[str, NotEmpty(), LimitedLength(10)], '12345678901', False, ["""Expected that attr "test_variable" would be of type "typing.Annotated[str, NotEmpty(), LimitedLength(length=10)]". Value 12345678901, of type "<class \'str\'>" was passed.Value "12345678901" length should be <= 10. Actual is 11"""]),
    (Optional[str], 'valid_str', True, []),
    (Optional[str], None, True, []),
    (Optional[str], 1, False, ["""Expected that attr "test_variable" would be of type "(<class \'str\'>, <class \'NoneType\'>)". Value 1, of type "<class \'int\'>" was passed."""]),
    (str | None, 'valid_str', True, []),
    (str | None, None, True, []),
    (str | None, 1, False, ["""Expected that attr "test_variable" would be of type "(<class \'str\'>, <class \'NoneType\'>)". Value 1, of type "<class \'int\'>" was passed."""]),
])
def test_type_checker(param_type, param_value, exp_res, exp_errors):
    @dataclass
    class TestDataClass:
        test_variable: param_type = param_value

    tdc = TestDataClass()
    checker = TypeValidator()
    act_res, act_errors = checker.check_types(tdc)
    assert act_res == exp_res and act_errors == exp_errors, \
        (f'Case failed: {param_type} = {param_value}.\n'
         f'Actual res: {act_res} - {act_errors}\n'
         f'Expected res: {exp_res} - {exp_errors}')


@pytest.mark.internal
def test_strict_dtcls_raises():
    @dataclass
    class TestDataClass(StrictDataclass):
        test_variable: str = 1

    with pytest.raises(ValueError):
        TestDataClass()


@pytest.mark.internal
def test_base_dtcls_rnot_aises():
    @dataclass
    class TestDataClass(BaseDataclass):
        test_variable: str = 1

    TestDataClass()
