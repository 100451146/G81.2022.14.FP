"""Class's for the attribute PhoneNumber"""
from uc3m_care.data.attribute.attribute import Attribute


# pylint: disable=too-few-public-methods
class CancellationReason(Attribute):
    """Class's for the attribute PhoneNumber"""
    _validation_pattern = r"^.{2,100}$/gm"
    _validation_error_message = "Reason for cancellation length is not between 2 and 100"
