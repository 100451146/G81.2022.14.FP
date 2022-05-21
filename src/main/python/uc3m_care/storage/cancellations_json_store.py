"""Subclass of JsonStore for managing the Patients store"""
from uc3m_care.storage.json_store import JsonStore
from uc3m_care.cfg.vaccine_manager_config import JSON_FILES_PATH
from uc3m_care.exception.vaccine_management_exception import VaccineManagementException


class CancellationsJsonStore:
    """Implements the singleton pattern"""

    # pylint: disable=invalid-name
    class __CancellationsJsonStore(JsonStore):
        """Subclass of JsonStore for managing the VaccinationLog"""
        _FILE_PATH = JSON_FILES_PATH + "store_cancellation.json"
        ID_FIELD = "_VaccinationCancellationLog__date_signature"

        # def add_item(self, item):
        #     """Overrides the add_item to verify the item to be stored"""
        #     # pylint: disable=import-outside-toplevel, cyclic-import
        #     from uc3m_care.data.vaccine_patient_register import VaccinePatientRegister
        #     if not isinstance(item, VaccinePatientRegister):
        #         raise VaccineManagementException("Invalid patient object")
        #
        #     patient_found = False
        #     patient_records = self.find_items_list \
        #         (item.patient_id, "_VaccinePatientRegister__patient_id")
        #     for patient_recorded in patient_records:
        #         if (patient_recorded["_VaccinePatientRegister__registration_type"]
        #             == item.vaccine_type) \
        #                 and \
        #                 (patient_recorded["_VaccinePatientRegister__full_name"]
        #                  == item.full_name):
        #             raise VaccineManagementException("patien_id is registered in store_patient")
        #
        #     if not patient_found:
        #         super().add_item(item)

        # def search(self, json_cancellation):
        #     cancellation_found = False

    instance = None

    def __new__(cls):
        if not CancellationsJsonStore.instance:
            CancellationsJsonStore.instance = CancellationsJsonStore.__CancellationsJsonStore()
        return CancellationsJsonStore.instance

    def __getattr__(self, name):
        return getattr(self.instance, name)

    def __setattr__(self, name, value):
        return setattr(self.instance, name, value)

    def delete():
        """Delete the store"""
        CancellationsJsonStore.instance = None
