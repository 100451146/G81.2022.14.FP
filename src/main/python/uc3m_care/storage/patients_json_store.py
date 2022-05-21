"""Subclass of JsonStore for managing the Patients store"""
from uc3m_care.storage.json_store import JsonStore
from uc3m_care.cfg.vaccine_manager_config import JSON_FILES_PATH
from uc3m_care.exception.vaccine_management_exception import VaccineManagementException
from uc3m_care.enumerations.attribute_enum import AttributeEnum
from uc3m_care.enumerations.exception_message_enum import ExceptionEnum

class PatientsJsonStore:
    """Implements the singleton pattern"""

    # pylint: disable=invalid-name
    class __PatientsJsonStore(JsonStore):
        """Subclass of JsonStore for managing the VaccinationLog"""
        _FILE_PATH = JSON_FILES_PATH + "store_patient.json"
        _ID_FIELD = AttributeEnum.VACC_PAT_REG_PAT_SYS_ID.value

        def add_item(self, item):
            """Overrides the add_item to verify the item to be stored"""
            # pylint: disable=import-outside-toplevel, cyclic-import
            from uc3m_care.data.vaccine_patient_register import VaccinePatientRegister
            if not isinstance(item, VaccinePatientRegister):
                raise VaccineManagementException(ExceptionEnum.INVALID_PATIENT_OBJECT.value)

            patient_found = False
            patient_records = self.find_items_list \
                (item.patient_id, AttributeEnum.VACC_PAT_REG_PAT_ID.value)
            for patient_recorded in patient_records:
                if (patient_recorded[AttributeEnum.VACC_PAT_REG_REGISTRATION_TYPE.value]
                    == item.vaccine_type) \
                        and \
                        (patient_recorded[AttributeEnum.VACC_PAT_REG_NAME.value]
                         == item.full_name):
                    raise VaccineManagementException(ExceptionEnum.PATIENT_ALREADY_REGISTERED.value)

            if not patient_found:
                super().add_item(item)

    instance = None

    def __new__(cls):
        if not PatientsJsonStore.instance:
            PatientsJsonStore.instance = PatientsJsonStore.__PatientsJsonStore()
        return PatientsJsonStore.instance

    def __getattr__(self, name):
        return getattr(self.instance, name)

    def __setattr__(self, name, value):
        return setattr(self.instance, name, value)
