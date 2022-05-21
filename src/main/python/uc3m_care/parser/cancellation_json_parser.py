"""Subclass of JsonParer for parsing inputs of get_vaccine_date"""
from uc3m_care.parser.json_parser import JsonParser
from uc3m_care.enumerations.attribute_enum import AttributeEnum
from uc3m_care.enumerations.exception_message_enum import ExceptionEnum


class CancellationJsonParser(JsonParser):
    """Subclass of JsonParer for parsing inputs of get_vaccine_date"""
    DATE_SIGNATURE = AttributeEnum.VACC_CANC_DATE_SIGNATURE.value
    CANCELLATION_TYPE = AttributeEnum.VACC_CANC_TYPE.value
    REASON = AttributeEnum.VACC_CANC_REASON.value
    BAD_DATE_SIGNATURE_LABEL_ERROR = ExceptionEnum.BAD_LABEL_DATE_SIGNATURE.value
    BAD_CANCELLATION_TYPE_LABEL_ERROR = ExceptionEnum.BAD_LABEL_CANC_TYPE.value
    BAD_REASON_LABEL_ERROR = ExceptionEnum.BAD_LABEL_REASON.value

    _JSON_KEYS = [DATE_SIGNATURE, CANCELLATION_TYPE, REASON]
    _ERROR_MESSAGES = [BAD_DATE_SIGNATURE_LABEL_ERROR, BAD_CANCELLATION_TYPE_LABEL_ERROR, BAD_REASON_LABEL_ERROR]
