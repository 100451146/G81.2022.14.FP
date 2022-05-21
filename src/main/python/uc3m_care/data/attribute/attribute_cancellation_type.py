"""Class's for the attribute PhoneNumber"""
from uc3m_care.data.attribute.attribute import Attribute
from uc3m_care.enumerations.pattern_enum import PatternEnum
from uc3m_care.enumerations.exception_message_enum import ExceptionEnum

# pylint: disable=too-few-public-methods
class CancellationType(Attribute):
    """Class's for the attribute PhoneNumber"""
    _validation_pattern = PatternEnum.CANC_TYPE.value
    _validation_error_message = ExceptionEnum.BAD_CANC_TYPE.value
