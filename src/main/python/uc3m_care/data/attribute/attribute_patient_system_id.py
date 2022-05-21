"""Class's for the attribute PatientSystemId"""
from uc3m_care.data.attribute.attribute import Attribute
from uc3m_care.enumerations.pattern_enum import PatternEnum
from uc3m_care.enumerations.exception_message_enum import ExceptionEnum

# pylint: disable=too-few-public-methods
class PatientSystemId(Attribute):
    """Class's for the attribute PatientSystemId"""
    _validation_pattern = PatternEnum.PATIENT_SYS_ID.value
    _validation_error_message = ExceptionEnum.BAD_PATIENT_SYS_ID.value
