"""Class's for the attribute age"""
from datetime import datetime

from uc3m_care.data.attribute.attribute import Attribute
from uc3m_care.exception.vaccine_management_exception import VaccineManagementException


# pylint: disable=too-few-public-methods
class ISOFormat(Attribute):
    """Class's for the attribute age"""
    _validation_error_message = "Date is not ISO format"

    def _validate(self, attr_value) -> float:
        """Validates the age according to the requirements"""
        if not isinstance(attr_value, str):
            raise VaccineManagementException("Date is not a string")

        try:
            date_value = datetime.timestamp(datetime.fromisoformat(attr_value))
        except ValueError as exception:
            raise VaccineManagementException(self._validation_error_message) from exception
        return date_value