"""Module for testing cancel_appointment"""
import unittest
from freezegun import freeze_time

from uc3m_care import VaccineManager
from uc3m_care import VaccineManagementException
from uc3m_care import PatientsJsonStore
from uc3m_care.cfg.vaccine_manager_config import JSON_FILES_RF4_PATH
from uc3m_care.storage.cancellations_json_store import CancellationsJsonStore


class CancelAppointment(unittest.TestCase):
    """Class for testing cancel_appointment"""

    # pylint: disable=too-many-locals
    @freeze_time("2022-03-08")
    def setUp(self):
        """first prepare the stores"""

        file_store_patient = PatientsJsonStore()
        file_store_date = CancellationsJsonStore()

        file_store_date.delete_json_file()
        file_store_patient.delete_json_file()
        file_test = JSON_FILES_RF4_PATH + "test_ok.json"
        # add patient and date in the store
        my_manager = VaccineManager()

        my_manager.request_vaccination_id("78924cb0-075a-4099-a3ee-f3b562e805b9",
                                          "minombre tienelalongitudmaxima", "Regular",
                                          "+34123456789", "6")

        my_manager.get_vaccine_date(file_test, "2022-03-18")

        my_manager.request_vaccination_id("57c811e5-3f5a-4a89-bbb8-11c0464d53e6",
                                          "minombre tieneuncharmenosqmax", "Family",
                                          "+34333456789", "7")

        file_test = JSON_FILES_RF4_PATH + "test_ok_2.json"

        my_manager.cancel_appointment(file_test)