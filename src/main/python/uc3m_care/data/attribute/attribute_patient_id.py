"""Class's for the attribute PatientId"""
import uuid
from uc3m_care.data.attribute.attribute import Attribute
from uc3m_care.exception.vaccine_management_exception import VaccineManagementException
from uc3m_care.enumerations.pattern_enum import PatternEnum
from uc3m_care.enumerations.exception_message_enum import ExceptionEnum

# pylint: disable=too-few-public-methods
class PatientId(Attribute):
    """Class's for the attribute PatientId"""
    _validation_pattern = PatternEnum.PATIENT_ID.value
    _validation_error_message = ExceptionEnum.BAD_UUID.value

    def _validate(self, attr_value):
        """overrides the validate method to include the validation of  UUID values"""
        try:
            patient_uuid = uuid.UUID(attr_value)
        except ValueError as val_er:
            raise VaccineManagementException(ExceptionEnum.NOT_UUID.value) from val_er
        return super()._validate(patient_uuid.__str__())
