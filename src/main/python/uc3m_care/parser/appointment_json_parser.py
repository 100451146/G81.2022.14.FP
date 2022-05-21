"""Subclass of JsonParer for parsing inputs of get_vaccine_date"""
from uc3m_care.parser.json_parser import JsonParser
from uc3m_care.enumerations.exception_message_enum import ExceptionEnum
from uc3m_care.enumerations.attribute_enum import AttributeEnum

class AppointmentJsonParser(JsonParser):
    """Subclass of JsonParer for parsing inputs of get_vaccine_date"""
    BAD_PHONE_NUMBER_LABEL_ERROR = ExceptionEnum.BAD_LABEL_PHONE.value
    BAD_PATIENT_SYS_ID_LABEL_ERROR = ExceptionEnum.BAD_LABEL_PATIENT_ID.value
    PATIENT_SYSTEM_ID_KEY = AttributeEnum.PAT_SYS_ID.value
    CONTACT_PHONE_NUMBER_KEY = AttributeEnum.CONTACT_PHONE.value

    _JSON_KEYS = [PATIENT_SYSTEM_ID_KEY, CONTACT_PHONE_NUMBER_KEY]
    _ERROR_MESSAGES = [BAD_PATIENT_SYS_ID_LABEL_ERROR, BAD_PHONE_NUMBER_LABEL_ERROR]
