"""Class's for the attribute DateSignature"""
from uc3m_care.data.attribute.attribute import Attribute
from uc3m_care.enumerations.pattern_enum import PatternEnum
from uc3m_care.enumerations.exception_message_enum import ExceptionEnum

# pylint: disable=too-few-public-methods
class DateSignature(Attribute):
    """Class's for the attribute DateSignature"""
    _validation_pattern = PatternEnum.DATE_SIGNATURE.value
    _validation_error_message = ExceptionEnum.BAD_DATE_SIGNATURE.value
