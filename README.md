# Dataclass Type Validator
Provides base api for verification of dataclass params, based on specified params annotation type. 

Installation: 
1. Python 3.12.0: https://www.python.org/downloads/release/python-3120/
2. Install required packages: `pip install -r requirements.txt` 

Run tests:
1. From within a folder: `pytest`
2. As a part of another project: `pytest -m "internal"`

Usage: 
1. Use `BaseDataclass` if you want to get specification freedom of your data. 
This class doesn't enforce validation of passed dataclass params. To verify params you need manually call `<YourDataClassInst>.check_properties_type()`
```python
@dataclass
class TestDataClass(BaseDataclass):
    test_variable: str = 1

TestDataClass().check_properties_type()  # ValueError. str field have an int.
```
2. Use `StrictDataclass` to enforce validation. All params would be checked during object initialization period.
```python
@dataclass
class TestDataClass(StrictDataclass):
    test_variable: str = 1

TestDataClass()  # ValueError. str field have an int.
```
3. You can specify additional validation functions in your subclass. 
They should follow this definition convention: `def <param_name_to_verify>_validar(self) -> None:...`
To invoke this validation in `BaseDataclass` -> `BaseDataclass().run_prop_validator_funcs()`
Note, that user should define own `raise` for this function.
```python
@dataclass
class NotZero(StrictDataclass):
    test_variable: int

    def test_variable_validator(self) -> None:
        if self.test_variable == 0:
            raise ValueError("test_variable could not be 0")

TestDataClass(0)  # ValueError. test_variable could not be 0
```