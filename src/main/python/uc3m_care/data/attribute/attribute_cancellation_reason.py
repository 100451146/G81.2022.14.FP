"""Class's for the attribute PhoneNumber"""
from uc3m_care.data.attribute.attribute import Attribute
from uc3m_care.enumerations.exception_message_enum import ExceptionEnum
from uc3m_care.enumerations.pattern_enum import PatternEnum

# pylint: disable=too-few-public-methods
class CancellationReason(Attribute):
    """Class's for the attribute PhoneNumber"""
    _validation_pattern = PatternEnum.CANC_REASON.value
    _validation_error_message = ExceptionEnum.BAD_CANC_REASON.value
