"""Subclass of JsonStore for managing the Appointments"""

from uc3m_care.storage.json_store import JsonStore
from uc3m_care.cfg.vaccine_manager_config import JSON_FILES_PATH
from uc3m_care.exception.vaccine_management_exception import VaccineManagementException
from uc3m_care.enumerations.exception_message_enum import ExceptionEnum
from uc3m_care.enumerations.attribute_enum import AttributeEnum

class AppointmentsJsonStore:
    """Implements the singleton pattern"""

    # pylint: disable=invalid-name
    class __AppointmentsJsonStore(JsonStore):
        """Subclass of JsonStore for managing the Appointments"""
        _FILE_PATH = JSON_FILES_PATH + "store_date.json"
        _ID_FIELD = AttributeEnum.VACC_APP_DATE_SIGNATURE.value
        ERROR_INVALID_APPOINTMENT_OBJECT = ExceptionEnum.INVALID_APPOINTMENT_OBJECT.value

        def add_item(self, item):
            """Overrides the add_item method to verify the item to be stored"""
            # pylint: disable=import-outside-toplevel, cyclic-import
            from uc3m_care.data.vaccination_appointment import VaccinationAppointment
            if not isinstance(item, VaccinationAppointment):
                raise VaccineManagementException(self.ERROR_INVALID_APPOINTMENT_OBJECT)
            super().add_item(item)

    instance = None

    def __new__(cls):
        if not AppointmentsJsonStore.instance:
            AppointmentsJsonStore.instance = AppointmentsJsonStore.__AppointmentsJsonStore()
        return AppointmentsJsonStore.instance

    def __getattr__(self, name):
        return getattr(self.instance, name)

    def __setattr__(self, name, value):
        return setattr(self.instance, name, value)
