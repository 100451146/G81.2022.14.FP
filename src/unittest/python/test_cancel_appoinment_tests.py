"""Module for testing cancel_appointment"""
import json
import os
import shutil
import unittest
from freezegun import freeze_time

from uc3m_care import VaccineManager, AppointmentsJsonStore
from uc3m_care import VaccineManagementException
from uc3m_care import PatientsJsonStore
from uc3m_care.cfg.vaccine_manager_config import JSON_FILES_RF4_PATH, JSON_FILES_PATH, JSON_FILES_RF2_PATH
from uc3m_care.storage.cancellations_json_store import CancellationsJsonStore

DATE_ISO = "2022-03-18"


class CancelAppointment(unittest.TestCase):
    """Class for testing cancel_appointment"""

    # pylint: disable=too-many-locals
    @freeze_time("2022-03-08")
    def setUp(self):
        """first prepare the stores"""

        file_store_patient = PatientsJsonStore()
        file_store_date = AppointmentsJsonStore()
        if os.path.isfile(JSON_FILES_PATH + "store_cancellation.json"):
            os.remove(JSON_FILES_PATH + "store_cancellation.json")

        file_store_date.delete_json_file()
        file_store_patient.delete_json_file()
        file_test = JSON_FILES_RF2_PATH + "test_ok.json"
        # add patient and date in the store
        my_manager = VaccineManager()

        my_manager.request_vaccination_id("78924cb0-075a-4099-a3ee-f3b562e805b9",
                                          "minombre tienelalongitudmaxima", "Regular",
                                          "+34123456789", "6")

        my_manager.get_vaccine_date(file_test, "2022-03-18")

        my_manager.request_vaccination_id("57c811e5-3f5a-4a89-bbb8-11c0464d53e6",
                                          "minombre tieneuncharmenosqmax", "Family",
                                          "+34333456789", "7")

        file_test = JSON_FILES_RF2_PATH + "test_ok_2.json"

        my_manager.get_vaccine_date(file_test, DATE_ISO)

    def tearDown(self) -> None:
        file_store_cancellations = CancellationsJsonStore()
        file_store_cancellations.delete_json_file()

    @freeze_time("2022-03-08")
    def test_cancel_appointment_cancellation(self):
        """Try to cancel an appointment that exists"""
        cancellation_store = JSON_FILES_PATH + "store_cancellation.json"
        shutil.copy(JSON_FILES_RF4_PATH + "store_cancellation.json",
                    cancellation_store)
        file_test = JSON_FILES_RF4_PATH + "test_ok.json"
        VaccineManager().cancel_appointment(file_test)
    # check if it is added to cancellation store

    def test_cancel_appointment_cancellation_input_not_found(self):
        """Try to cancel an appointment that exists"""
        cancellation_store = JSON_FILES_PATH + "store_cancellation.json"
        shutil.copy(JSON_FILES_RF4_PATH + "store_cancellation.json",
                    cancellation_store)
        file_test = JSON_FILES_RF4_PATH + "test_ok.json" + "random"
        with self.assertRaises(VaccineManagementException) as context:
            VaccineManager().cancel_appointment(file_test)
        self.assertEqual(context.exception.message, "File is not found")

    def test_cancel_appointment_date_signature_not_appointed(self):
        pass

    def test_cancel_appointment_reason_not_valid(self):
        pass

    def test_cancel_appointment_type_not_valid(self):
        pass

    def test_cancel_appointment_not_appointed(self):
        pass

    def test_cancel_appointment_past_appointment_date(self):
        pass

    @freeze_time("2022-03-18")
    def test_vaccine_cancelled_temporal(self):
        """Try to vaccinate but the appointment is cancelled with type Final"""
        cancellation_store = JSON_FILES_PATH + "store_cancellation.json"
        shutil.copy(JSON_FILES_RF4_PATH + "store_cancellation.json",
                    cancellation_store)

        with self.assertRaises(VaccineManagementException) as context:
            VaccineManager().vaccine_patient("5a06c7bede3d584e934e2f5bd3861e625cb31937f9f1a5362a51fbbf38486f1c")
        self.assertEqual(context.exception.message, "Appointment has been cancelled")

    @freeze_time("2022-03-18")
    def test_vaccine_cancelled_Final(self):
        """Try to vaccinate but the appointment is cancelled with type Final"""
        cancellation_store = JSON_FILES_PATH + "store_cancellation.json"

        shutil.copy(JSON_FILES_RF4_PATH + "store_cancellation.json", cancellation_store)
        with open(cancellation_store, "r", encoding="utf-8", newline="") as file_cancellations:
            cancellation_list = json.load(file_cancellations)
        for cancellation in cancellation_list:
            if cancellation["_VaccinationCancellation__date_signature"] == "5a06c7bede3d584e934e2f5bd3861e625cb31937f9f1a5362a51fbbf38486f1c":
                cancellation["_VaccinationCancellation__cancellation_type"] = "Final"
        with open(cancellation_store, "w", encoding="utf-8", newline="") as file_cancellations:
            json.dump(cancellation_list, file_cancellations)

        with self.assertRaises(VaccineManagementException) as context:
            VaccineManager().vaccine_patient("5a06c7bede3d584e934e2f5bd3861e625cb31937f9f1a5362a51fbbf38486f1c")
        self.assertEqual(context.exception.message, "Appointment cancellation is FINAL")
