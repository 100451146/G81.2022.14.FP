"""Class's for the attribute FullName"""
from uc3m_care.data.attribute.attribute import Attribute
from uc3m_care.enumerations.pattern_enum import PatternEnum
from uc3m_care.enumerations.exception_message_enum import ExceptionEnum

# pylint: disable=too-few-public-methods
class FullName(Attribute):
    """Class's for the attribute FullName"""
    _validation_pattern = PatternEnum.NAME.value
    _validation_error_message = ExceptionEnum.BAD_NAME.value
