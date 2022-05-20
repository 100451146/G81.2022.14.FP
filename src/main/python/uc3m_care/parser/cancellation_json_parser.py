"""Subclass of JsonParer for parsing inputs of get_vaccine_date"""
from uc3m_care.parser.json_parser import JsonParser


class CancellationJsonParser(JsonParser):
    """Subclass of JsonParer for parsing inputs of get_vaccine_date"""
    DATE_SIGNATURE = "_VaccinationCancellation__date_signature"
    CANCELLATION_TYPE = "_VaccinationCancellation__cancellation_type"
    REASON = "_VaccinationCancellation__reason"
    BAD_DATE_SIGNATURE_LABEL_ERROR = "Bad label date_signature"
    BAD_CANCELLATION_TYPE_LABEL_ERROR = "Bad label cancellation_type"
    BAD_REASON_LABEL_ERROR = "Bad label reason"

    _JSON_KEYS = [DATE_SIGNATURE, CANCELLATION_TYPE, REASON]
    _ERROR_MESSAGES = [BAD_DATE_SIGNATURE_LABEL_ERROR, BAD_CANCELLATION_TYPE_LABEL_ERROR, BAD_REASON_LABEL_ERROR]
