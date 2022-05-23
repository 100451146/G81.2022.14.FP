"""Subclass of JsonStore for managing the Patients Cancellations store"""

from uc3m_care.storage.json_store import JsonStore
from uc3m_care.cfg.vaccine_manager_config import JSON_FILES_PATH
from uc3m_care.enumerations.attribute_enum import AttributeEnum


class CancellationsJsonStore:
    """Implements the singleton pattern"""

    # pylint: disable=invalid-name
    class __CancellationsJsonStore(JsonStore):
        """Subclass of JsonStore for managing the VaccinationLog"""
        _FILE_PATH = JSON_FILES_PATH + "store_cancellation.json"
        ID_FIELD = AttributeEnum.VACC_CANC_LOG_DATE_SIGNATURE.value

    instance = None

    def __new__(cls):
        if not CancellationsJsonStore.instance:
            CancellationsJsonStore.instance = CancellationsJsonStore.__CancellationsJsonStore()
        return CancellationsJsonStore.instance

    def __getattr__(self, name):
        return getattr(self.instance, name)

    def __setattr__(self, name, value):
        return setattr(self.instance, name, value)
