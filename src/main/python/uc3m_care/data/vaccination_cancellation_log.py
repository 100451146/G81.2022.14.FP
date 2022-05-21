"""Class representing an entry of the vaccine administration log"""
from uc3m_care.storage.vaccination_json_store import VaccinationJsonStore


# pylint: disable=too-few-public-methods
class VaccinationCancellationLog:
    """Class representing an entry of the Vaccine administration log"""

    def __init__(self, date_signature, cancellation_type: str, reason: str):
        self.__date_signature = date_signature
        self.__type = cancellation_type
        self.__reason = reason

    def save_log_entry(self):
        """saves the entry in the vaccine administration log"""
        vaccination_log = VaccinationJsonStore()
        vaccination_log.add_item(self)

    @property
    def date_signature(self):
        """returns the value of the date_signature"""
        return self.__date_signature

    @property
    def type(self):
        """returns the value of the type"""
        return self.__type

    @property
    def reason(self):
        """returns the timestamp corresponding to the date of administration """
        return self.__reason
