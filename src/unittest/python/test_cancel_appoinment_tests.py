"""Module for testing cancel_appointment"""
import json
import os
import shutil
import unittest
from freezegun import freeze_time

from uc3m_care import VaccineManager, VaccinationAppointment, PatientsJsonStore, AppointmentsJsonStore, CancellationsJsonStore
from uc3m_care import VaccineManagementException
from uc3m_care.cfg.vaccine_manager_config import JSON_FILES_RF4_PATH, JSON_FILES_PATH, JSON_FILES_RF2_PATH
from uc3m_care.enumerations.exception_message_enum import ExceptionEnum
from uc3m_care.enumerations.attribute_enum import AttributeEnum


class CancelAppointment(unittest.TestCase):
    """Class for testing cancel_appointment"""

    # pylint: disable=too-many-locals
    @freeze_time("2022-03-08")
    def setUp(self):
        """first prepare the stores"""

        file_store_patient = PatientsJsonStore()
        file_store_date = AppointmentsJsonStore()

        cancellation_store = JSON_FILES_PATH + "store_cancellation.json"
        shutil.copy(JSON_FILES_RF4_PATH + "store_cancellation.json",
                    cancellation_store)

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

        my_manager.get_vaccine_date(file_test, "2022-03-18")

    def tearDown(self) -> None:
        file_store_cancellations = CancellationsJsonStore()
        file_store_cancellations.delete_json_file()

    @freeze_time("2022-03-08")
    def test_cancel_appointment_cancellation_ok(self):
        """Try to cancel an appointment that exists and everything is nominal"""
        file_test = JSON_FILES_RF4_PATH + "test_ok_second.json"
        VaccineManager().cancel_appointment(file_test)
        # check if it is added to the cancellation store
        cancellation_type = VaccinationAppointment.is_cancelled("6a8403d8605804cf2534fd7885940f3c3d8ec60ba578bc158b5dc2b9fb68d524")
        self.assertIsNotNone(cancellation_type)

    @freeze_time("2022-03-08")
    def test_cancel_appointment_cancellation_already_cancelled(self):
        """Try to cancel an appointment that has been cancelled already"""
        file_test = JSON_FILES_RF4_PATH + "test_ok_second.json"
        VaccineManager().cancel_appointment(file_test)
        # check if it is added to the cancellation store
        cancellation_type = VaccinationAppointment.is_cancelled(
            "5a06c7bede3d584e934e2f5bd3861e625cb31937f9f1a5362a51fbbf38486f1c")
        self.assertIsNotNone(cancellation_type)

    def test_cancel_appointment_cancellation_input_file_not_found(self):
        """Try to cancel an appointment that exists"""
        file_test = JSON_FILES_RF4_PATH + "test_ok.json" + "random"
        with self.assertRaises(VaccineManagementException) as context:
            VaccineManager().cancel_appointment(file_test)
        self.assertEqual(context.exception.message, ExceptionEnum.FILE_NOT_FOUND.value)

    def test_cancel_appointment_date_signature_not_appointed(self):
        """Test to cancel an appointment that does not exist"""
        file_test = JSON_FILES_RF4_PATH + "test_tnot_appointed.json"
        with self.assertRaises(VaccineManagementException) as context:
            VaccineManager().cancel_appointment(file_test)
        self.assertEqual(context.exception.message, ExceptionEnum.NOT_APPOINTMENT_WITH_DATE_SIGNATURE.value)

    def test_cancel_appointment_reason_not_valid_long(self):
        """Try to cancel an appointment but the reason is too long"""
        file_test = JSON_FILES_RF4_PATH + "test_tnot_valid_reason_long.json"
        with self.assertRaises(VaccineManagementException) as context:
            VaccineManager().cancel_appointment(file_test)
        self.assertEqual(context.exception.message, ExceptionEnum.BAD_CANC_REASON.value)

    def test_cancel_appointment_reason_not_valid_short(self):
        """Try to cancel an appointment but the reason is too short"""
        file_test = JSON_FILES_RF4_PATH + "test_tnot_valid_reason_short.json"
        with self.assertRaises(VaccineManagementException) as context:
            VaccineManager().cancel_appointment(file_test)
        self.assertEqual(context.exception.message, ExceptionEnum.BAD_CANC_REASON.value)

    def test_cancel_appointment_reason_not_valid_empty(self):
        """Try to cancel an appointment but the reason is empty"""
        file_test = JSON_FILES_RF4_PATH + "test_tnot_valid_reason_empty.json"
        with self.assertRaises(VaccineManagementException) as context:
            VaccineManager().cancel_appointment(file_test)
        self.assertEqual(context.exception.message, ExceptionEnum.BAD_CANC_REASON.value)

    def test_cancel_appointment_type_not_string(self):
        """Test to cancel an appointment but the types is not str"""
        file_test = JSON_FILES_RF4_PATH + "test_tnot_valid_type_not_string.json"
        with self.assertRaises(TypeError) as context:
            VaccineManager().cancel_appointment(file_test)
        self.assertEqual(context.exception.__str__(), "expected string or bytes-like object")

    def test_cancel_appointment_type_not_accepted(self):
        """Test to cancel but the type is not a valid one"""
        file_test = JSON_FILES_RF4_PATH + "test_tnot_valid_type.json"
        with self.assertRaises(VaccineManagementException) as context:
            VaccineManager().cancel_appointment(file_test)
        self.assertEqual(context.exception.message, ExceptionEnum.BAD_CANC_TYPE.value)

    def test_cancel_appointment_invalid_signature_length(self):
        """Try to cancel an appointment but the signature format is not valid"""
        file_test = JSON_FILES_RF4_PATH + "test_tnot_valid_signature_length.json"
        with self.assertRaises(VaccineManagementException) as context:
            VaccineManager().cancel_appointment(file_test)
        self.assertEqual(context.exception.message, ExceptionEnum.BAD_DATE_SIGNATURE.value)

    def test_cancel_appointment_invalid_signature_empty(self):
        """Try to cancel an appointment but the signature is empty"""
        file_test = JSON_FILES_RF4_PATH + "test_tnot_valid_signature_empty.json"
        with self.assertRaises(VaccineManagementException) as context:
            VaccineManager().cancel_appointment(file_test)
        self.assertEqual(context.exception.message, ExceptionEnum.BAD_DATE_SIGNATURE.value)

    def test_cancel_appointment_past_appointment_date(self):
        """Try to cancel an appointment that is already expired (same as first test but without freeze time)"""
        file_test = JSON_FILES_RF4_PATH + "test_ok_second.json"
        with self.assertRaises(VaccineManagementException) as context:
            VaccineManager().cancel_appointment(file_test)
        self.assertEqual(context.exception.message, ExceptionEnum.APPOINTMENT_EXPIRED.value)
        # check if it is added to the cancellation store
        cancellation_type = VaccinationAppointment.is_cancelled(
            "6a8403d8605804cf2534fd7885940f3c3d8ec60ba578bc158b5dc2b9fb68d524")
        self.assertIsNotNone(cancellation_type)

    @freeze_time("2022-03-18")
    def test_vaccine_cancelled_temporal(self):
        """Try to vaccinate but the appointment is cancelled with type temporal"""
        with self.assertRaises(VaccineManagementException) as context:
            VaccineManager().vaccine_patient("5a06c7bede3d584e934e2f5bd3861e625cb31937f9f1a5362a51fbbf38486f1c")
        self.assertEqual(context.exception.message, ExceptionEnum.APPOINTMENT_IS_TEMPORAL.value)

    @freeze_time("2022-03-18")
    def test_vaccine_cancelled_final(self):
        """Try to vaccinate but the appointment is cancelled with type Final"""
        cancellation_store = JSON_FILES_PATH + "store_cancellation.json"
        with open(cancellation_store, "r", encoding="utf-8", newline="") as file_cancellations:
            cancels_list = json.load(file_cancellations)
        for cancellation in cancels_list:
            if cancellation[AttributeEnum.VACC_CANC_LOG_DATE_SIGNATURE.value] == "5a06c7bede3d584e934e2f5bd3861e625cb31937f9f1a5362a51fbbf38486f1c":
                cancellation[AttributeEnum.VACC_CANC_LOG_TYPE.value] = "Final"
        with open(cancellation_store, "w", encoding="utf-8", newline="") as file_cancellations:
            json.dump(cancels_list, file_cancellations)

        with self.assertRaises(VaccineManagementException) as context:
            VaccineManager().vaccine_patient("5a06c7bede3d584e934e2f5bd3861e625cb31937f9f1a5362a51fbbf38486f1c")
        self.assertEqual(context.exception.message, ExceptionEnum.APPOINTMENT_IS_FINAL.value)
