"""Tests for get_vaccine_date method"""
from unittest import TestCase
import os
import shutil
from freezegun import freeze_time
from uc3m_care import VaccineManager
from uc3m_care import VaccineManagementException
from uc3m_care import JSON_FILES_PATH, JSON_FILES_RF2_PATH
from uc3m_care import AppointmentsJsonStore
from uc3m_care import PatientsJsonStore
from uc3m_care.enumerations.exception_message_enum import ExceptionEnum

DATE_ISO = "2022-03-18"

param_list_nok = [("test_dup_all.json", ExceptionEnum.WRONG_JSON_FORMAT.value),
                  ("test_dup_char_plus.json", ExceptionEnum.BAD_PHONE_NUMBER.value),
                  ("test_dup_colon.json", ExceptionEnum.WRONG_JSON_FORMAT.value),
                  ("test_dup_comillas.json", ExceptionEnum.WRONG_JSON_FORMAT.value),
                  ("test_dup_comma.json", ExceptionEnum.WRONG_JSON_FORMAT.value),
                  ("test_dup_content.json", ExceptionEnum.WRONG_JSON_FORMAT.value),
                  ("test_dup_data1.json", ExceptionEnum.WRONG_JSON_FORMAT.value),
                  ("test_dup_data1_content.json", ExceptionEnum.BAD_PATIENT_SYS_ID.value),
                  ("test_dup_data2.json", ExceptionEnum.WRONG_JSON_FORMAT.value),
                  ("test_dup_data2_content.json", ExceptionEnum.BAD_PHONE_NUMBER.value),
                  ("test_dup_field1.json", ExceptionEnum.WRONG_JSON_FORMAT.value),
                  ("test_dup_field2.json", ExceptionEnum.WRONG_JSON_FORMAT.value),
                  ("test_dup_final_bracket.json", ExceptionEnum.WRONG_JSON_FORMAT.value),
                  ("test_dup_initial_bracket.json", ExceptionEnum.WRONG_JSON_FORMAT.value),
                  ("test_dup_label1.json", ExceptionEnum.WRONG_JSON_FORMAT.value),
                  ("test_dup_label1_content.json", ExceptionEnum.BAD_LABEL_PATIENT_ID.value),
                  ("test_dup_label2.json", ExceptionEnum.WRONG_JSON_FORMAT.value),
                  ("test_dup_label2_content.json", ExceptionEnum.BAD_LABEL_PHONE.value),
                  ("test_dup_phone.json", ExceptionEnum.BAD_PHONE_NUMBER.value),
                  ("test_empty.json", ExceptionEnum.BAD_LABEL_PATIENT_ID.value),
                  ("test_mod_char_plus.json", ExceptionEnum.BAD_PHONE_NUMBER.value),
                  ("test_mod_data1.json", ExceptionEnum.BAD_PATIENT_SYS_ID.value),
                  ("test_mod_data2.json", ExceptionEnum.BAD_PHONE_NUMBER.value),
                  ("test_mod_label1.json", ExceptionEnum.BAD_LABEL_PATIENT_ID.value),
                  ("test_mod_label2.json", ExceptionEnum.BAD_LABEL_PHONE.value),
                  ("test_mod_phone.json", ExceptionEnum.BAD_PHONE_NUMBER.value),
                  ("test_no_char_plus.json", ExceptionEnum.BAD_PHONE_NUMBER.value),
                  ("test_no_colon.json", ExceptionEnum.WRONG_JSON_FORMAT.value),
                  ("test_no_comillas.json", ExceptionEnum.WRONG_JSON_FORMAT.value),
                  ("test_no_phone.json", ExceptionEnum.BAD_PHONE_NUMBER.value)
                  ]


class TestGetVaccineDate(TestCase):
    """Class for testing get_vaccine_date"""

    @freeze_time("2022-03-08")
    def test_get_vaccine_date_ok(self):
        """test ok"""
        file_test = JSON_FILES_RF2_PATH + "test_ok.json"
        my_manager = VaccineManager()

        # first , prepare my test , remove store patient
        file_store = PatientsJsonStore()
        file_store.delete_json_file()
        file_store_date = AppointmentsJsonStore()
        file_store_date.delete_json_file()

        # add a patient in the store
        my_manager.request_vaccination_id("78924cb0-075a-4099-a3ee-f3b562e805b9",
                                          "minombre tienelalongitudmaxima",
                                          "Regular", "+34123456789", "6")
        # check the method
        value = my_manager.get_vaccine_date(file_test, DATE_ISO)
        self.assertEqual(value, "5a06c7bede3d584e934e2f5bd3861e625cb31937f9f1a5362a51fbbf38486f1c")
        # check store_date
        self.assertIsNotNone(file_store_date.find_item(value))

    @freeze_time("2022-03-08")
    def test_get_vaccine_date_no_ok_parameter(self):
        """tests no ok"""
        my_manager = VaccineManager()
        # first , prepare my test , remove store patient
        file_store = PatientsJsonStore()
        file_store.delete_json_file()
        file_store_date = AppointmentsJsonStore()
        file_store_date.delete_json_file()
        # add a patient in the store
        my_manager.request_vaccination_id("78924cb0-075a-4099-a3ee-f3b562e805b9",
                                          "minombre tienelalongitudmaxima",
                                          "Regular", "+34123456789", "6")
        for file_name, expected_value in param_list_nok:
            with self.subTest(test=file_name):
                file_test = JSON_FILES_RF2_PATH + file_name
                hash_original = file_store_date.data_hash()

                # check the method
                with self.assertRaises(VaccineManagementException) as c_m:
                    my_manager.get_vaccine_date(file_test, DATE_ISO)
                self.assertEqual(c_m.exception.message, expected_value)

                # read the file again to compare
                hash_new = file_store_date.data_hash()

                self.assertEqual(hash_new, hash_original)

    @freeze_time("2022-03-08")
    def test_get_vaccine_date_no_ok(self):
        """# long 32 in patient system id , not valid"""
        file_test = JSON_FILES_RF2_PATH + "test_no_ok.json"
        my_manager = VaccineManager()
        file_store_date = AppointmentsJsonStore()

        # read the file to compare file content before and after method call
        hash_original = file_store_date.data_hash()

        # check the method
        with self.assertRaises(VaccineManagementException) as c_m:
            my_manager.get_vaccine_date(file_test, DATE_ISO)
        self.assertEqual(c_m.exception.message, ExceptionEnum.BAD_PATIENT_SYS_ID.value)

        # read the file again to compare
        hash_new = file_store_date.data_hash()

        self.assertEqual(hash_new, hash_original)

    @freeze_time("2022-03-08")
    def test_get_vaccine_date_no_ok_no_quotes(self):
        """ no quotes , not valid """
        file_test = JSON_FILES_RF2_PATH + "test_nok_no_comillas.json"
        my_manager = VaccineManager()
        file_store_date = AppointmentsJsonStore()

        # read the file to compare file content before and after method call
        hash_original = file_store_date.data_hash()

        # check the method
        with self.assertRaises(VaccineManagementException) as c_m:
            my_manager.get_vaccine_date(file_test, DATE_ISO)
        self.assertEqual(c_m.exception.message, ExceptionEnum.WRONG_JSON_FORMAT.value)

        # read the file again to compare
        hash_new = file_store_date.data_hash()

        self.assertEqual(hash_new, hash_original)

    @freeze_time("2022-03-08")
    def test_get_vaccine_date_no_ok_data_manipulated(self):
        """ no quotes , not valid """
        file_test = JSON_FILES_RF2_PATH + "test_ok.json"
        my_manager = VaccineManager()
        file_store = JSON_FILES_PATH + "store_patient.json"
        file_store_date = JSON_FILES_PATH + "store_date.json"

        if os.path.isfile(JSON_FILES_PATH + "swap.json"):
            os.remove(JSON_FILES_PATH + "swap.json")
        if not os.path.isfile(JSON_FILES_PATH + "store_patient_manipulated.json"):
            shutil.copy(JSON_FILES_RF2_PATH + "store_patient_manipulated.json",
                        JSON_FILES_PATH + "store_patient_manipulated.json")

        # rename the manipulated patient's store
        if os.path.isfile(file_store):
            print(file_store)
            print(JSON_FILES_PATH + "swap.json")
            os.rename(file_store, JSON_FILES_PATH + "swap.json")
        os.rename(JSON_FILES_PATH + "store_patient_manipulated.json", file_store)

        file_store_date = AppointmentsJsonStore()
        # read the file to compare file content before and after method call
        hash_original = file_store_date.data_hash()

        # check the method

        exception_message = "Exception not raised"
        try:
            my_manager.get_vaccine_date(file_test, DATE_ISO)
        # pylint: disable=broad-except
        except Exception as exception_raised:
            exception_message = exception_raised.__str__()

        # restore the original patient's store
        os.rename(file_store, JSON_FILES_PATH + "store_patient_manipulated.json")
        if os.path.isfile(JSON_FILES_PATH + "swap.json"):
            print(JSON_FILES_PATH + "swap.json")
            print(file_store)
            os.rename(JSON_FILES_PATH + "swap.json", file_store)

        # read the file again to compare
        hash_new = file_store_date.data_hash()

        self.assertEqual(exception_message, ExceptionEnum.PAT_DATA_MANIPULATED.value)
        self.assertEqual(hash_new, hash_original)

    @freeze_time("2022-03-08")
    def test_get_vaccine_date_in_past(self):
        """test if the date is in the past"""
        file_test = JSON_FILES_RF2_PATH + "test_ok.json"
        my_manager = VaccineManager()

        # first , prepare my test , remove store patient
        file_store = PatientsJsonStore()
        file_store.delete_json_file()
        file_store_date = AppointmentsJsonStore()
        file_store_date.delete_json_file()

        # add a patient in the store
        my_manager.request_vaccination_id("78924cb0-075a-4099-a3ee-f3b562e805b9",
                                          "minombre tienelalongitudmaxima",
                                          "Regular", "+34123456789", "6")
        # check the method
        try:
            my_manager.get_vaccine_date(file_test, "1969-12-31")
        except VaccineManagementException as exception_raised:
            self.assertEqual(exception_raised.message, ExceptionEnum.APPOINTMENT_EXPIRED.value)

    @freeze_time("2022-03-08")
    def test_get_vaccine_date_is_today(self):
        """test if date is today"""
        file_test = JSON_FILES_RF2_PATH + "test_ok.json"
        my_manager = VaccineManager()

        # first , prepare my test , remove store patient
        file_store = PatientsJsonStore()
        file_store.delete_json_file()
        file_store_date = AppointmentsJsonStore()
        file_store_date.delete_json_file()

        # add a patient in the store
        my_manager.request_vaccination_id("78924cb0-075a-4099-a3ee-f3b562e805b9",
                                          "minombre tienelalongitudmaxima",
                                          "Regular", "+34123456789", "6")
        # check the method
        try:
            my_manager.get_vaccine_date(file_test, "2022-03-08")
        except VaccineManagementException as exception_raised:
            self.assertEqual(exception_raised.message, ExceptionEnum.NOT_APPOINTMENT_THE_SAME_DAY_REQUEST.value)

    def test_get_vaccine_date_date_is_str(self):
        """check if date is a string"""
        file_test = JSON_FILES_RF2_PATH + "test_ok.json"
        my_manager = VaccineManager()
        try:
            my_manager.get_vaccine_date(file_test, int(3))
        except VaccineManagementException as exception_raised:
            self.assertEqual(exception_raised.message, ExceptionEnum.BAD_TYPE_DATE.value)

    def test_get_vaccine_date_date_is_not_iso(self):
        """check if date has iso format"""
        file_test = JSON_FILES_RF2_PATH + "test_ok.json"
        my_manager = VaccineManager()
        try:
            my_manager.get_vaccine_date(file_test, "10")
        except VaccineManagementException as exception_raised:
            self.assertEqual(exception_raised.message, ExceptionEnum.BAD_ISO_FORMAT.value)
