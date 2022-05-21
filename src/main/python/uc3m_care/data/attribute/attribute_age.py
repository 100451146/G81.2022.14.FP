"""Class's for the attribute age"""
from uc3m_care.data.attribute.attribute import Attribute
from uc3m_care.exception.vaccine_management_exception import VaccineManagementException
from uc3m_care.enumerations.exception_message_enum import ExceptionEnum

# pylint: disable=too-few-public-methods
class Age(Attribute):
    """Class's for the attribute age"""
    _validation_error_message = ExceptionEnum.AGE_NOT_VALID.value

    def _validate(self, attr_value: str) -> str:
        """Validates the age according to the requirements"""
        if attr_value.isnumeric():
            if int(attr_value) < 6 or int(attr_value) > 125:
                raise VaccineManagementException(self._validation_error_message)
        else:
            raise VaccineManagementException(self._validation_error_message)
        return attr_value
