"""Module for testing request_vaccination_id"""
import unittest
from freezegun import freeze_time

from uc3m_care import VaccineManager
from uc3m_care import VaccineManagementException
from uc3m_care import PatientsJsonStore
from uc3m_care.enumerations.attribute_enum import AttributeEnum
from uc3m_care.enumerations.exception_message_enum import ExceptionEnum

# """
#      import uuid
#       for i in range(10):
#           patient_uuid = uuid.uuid4()
#           print (patient_uuid)
#
#   Lista de uuid v4 valid
#
#   78924cb0-075a-4099-a3ee-f3b562e805b9 test1
#   57c811e5-3f5a-4a89-bbb8-11c0464d53e6  2
#   cde0bc01-5bc7-4c0c-90d6-94c9549e6abd  3
#   a729d963-e0dd-47d0-8bc6-b6c595ad0098  4
#   2b0506db-50de-493b-abf9-1fb44816b628  5
#   e90b6070-3b44-4faa-93ff-9d4d73372d77
#   6071d52e-ab42-452d-837c-0639367db79f
#   7c95ddbf-074c-4c1e-a6f7-c1d663a6f87c
#   2a39433e-f5d7-489c-b263-a68192e4d286
# """


param_list_ok = [("78924cb0-075a-4099-a3ee-f3b562e805b9", "minombre tienelalongitudmaxima", "Regular",
                  "+34123456789", "6", "72b72255619afeed8bd26861a2bc2caf", "test_1"),
                 ("57c811e5-3f5a-4a89-bbb8-11c0464d53e6", "minombre tieneuncharmenosqmax", "Family",
                  "+34333456789", "7", "0d49256644b963208cb8db044a3ebbe7", "test_2"),
                 ("cde0bc01-5bc7-4c0c-90d6-94c9549e6abd", "minombre tiene dosblancos", "Regular",
                  "+34333456789", "125", "7fbd065ae9c274c7ccf30c50c0cd87a3", "test_3"),
                 ("a729d963-e0dd-47d0-8bc6-b6c595ad0098", "m m", "Regular",
                  "+44333456789", "124", "76a1b7346a927ef02ad5098f673ca876", "test_4")
                 ]

param_list_nok = [("bb5dbd6f-d8b4-113f-8eb9-dd262cfc54e0",
                   "minombre tienelalongitudmaxima", "Regular",
                   "+34123456789",
                   "6", ExceptionEnum.BAD_UUID.value, "test_5 , is not uuid v4"),
                  ("zb0506db-50de-493b-abf9-1fb44816b628",
                   "minombre tieneuncharmenosqmax", "Family",
                   "+34333456789", "7", ExceptionEnum.NOT_UUID.value,
                   "test_6, is not hex uuid"),
                  ("2b0506db-50de-493b-abf9-1fb44816b62",
                   "minombre tiene dosblancos", "Regular",
                   "+34333456789", "125", ExceptionEnum.NOT_UUID.value,
                   "test_7, patiend id 34 long"),
                  ("2b0506db-50de-493b-abf9-1fb44816b6289", "m m", "Regular",
                   "+34333456789", "124", ExceptionEnum.NOT_UUID.value,
                   "test_8 , patiend id 36 long"),
                  ("6071d52e-ab42-452d-837c-0639367db79f",
                   "minombre tienelalongitudmaxima",
                   "Regularcito", "+34123456789", "6", ExceptionEnum.BAD_REGISTRATION_TYPE.value,
                   "test_9 registration type not valid"),
                  ("6071d52e-ab42-452d-837c-0639367db79f",
                   "minombre tieneun01", "Family",
                   "+34333456789", "7", ExceptionEnum.BAD_NAME.value,
                   "test_10 name no char"),
                  ("6071d52e-ab42-452d-837c-0639367db79f",
                   "minombre tienelalongitudmaximay", "Regular",
                   "+34333456789", "125", ExceptionEnum.BAD_NAME.value,
                   "test_11, long 31 de name"),
                  ("6071d52e-ab42-452d-837c-0639367db79f",
                   "minombrenotieneblancoentrecha", "Regular",
                   "+34333456789", "124", ExceptionEnum.BAD_NAME.value,
                   "test_12, long 29 y 0 blanco"),
                  ("6071d52e-ab42-452d-837c-0639367db79f",
                   "", "Regular",
                   "+34333456789", "124", ExceptionEnum.BAD_NAME.value,
                   "test_13, 0 char"),
                  ("6071d52e-ab42-452d-837c-0639367db79f",
                   "Pedro Perez", "Regular",
                   "+3433345678a", "124", ExceptionEnum.BAD_PHONE_NUMBER.value,
                   "test_14, phone con char"),
                  ("6071d52e-ab42-452d-837c-0639367db79f",
                   "Pedro Perez", "Regular",
                   "+343334567892", "124", ExceptionEnum.BAD_PHONE_NUMBER.value,
                   "test_15, phone 12 char"),
                  ("6071d52e-ab42-452d-837c-0639367db79f",
                   "Pedro Perez", "Regular",
                   "+3433345678", "124", ExceptionEnum.BAD_PHONE_NUMBER.value,
                   "test_16, phone 10 char"),
                  ("6071d52e-ab42-452d-837c-0639367db79f",
                   "Pedro Perez", "Regular",
                   "+34333456789", "12a", ExceptionEnum.AGE_NOT_VALID.value,
                   "test_17, age no digit"),
                  ("6071d52e-ab42-452d-837c-0639367db79f",
                   "Pedro Perez", "Regular",
                   "+34333456789", "5", ExceptionEnum.AGE_NOT_VALID.value,
                   "test_18, age is 5"),
                  ("6071d52e-ab42-452d-837c-0639367db79f",
                   "Pedro Perez", "Regular",
                   "+34333456789", "126", ExceptionEnum.AGE_NOT_VALID.value,
                   "test_19, age is 126")
                  ]


class TestRequestVacID(unittest.TestCase):
    """Class for testing request_vaccination_id"""

    # pylint: disable=too-many-locals
    @freeze_time("2022-03-08")
    def test_parametrized_valid_request_vaccination(self):
        """Parametrized tests: valid cases"""
        file_store = PatientsJsonStore()
        file_store.delete_json_file()

        my_request = VaccineManager()

        for patient_id, name_surname, registration_type, phone_number, \
            age, expected_result, comment in param_list_ok:
            with self.subTest(test=comment):
                value = my_request.request_vaccination_id(patient_id, name_surname,
                                                          registration_type, phone_number, age)
                self.assertEqual(value, expected_result)
                self.assertIsNotNone(file_store.find_item(value))

    def test_parametrized_not_valid_request_vaccination(self):
        """Method for testing request_vaccination_id: invalid cases"""
        file_store = PatientsJsonStore()
        file_store.empty_json_file()
        my_request = VaccineManager()

        for patient_id, name_surname, registration_type, phone_number, age, \
            expected_result, comment in param_list_nok:
            with self.subTest(test=comment):
                with self.assertRaises(VaccineManagementException) as context_manager:
                    my_request.request_vaccination_id \
                        (patient_id, name_surname, registration_type, phone_number, age)
                self.assertEqual(context_manager.exception.message, expected_result)
                self.assertIsNone \
                    (file_store.find_item(patient_id, AttributeEnum.VACC_PAT_REG_PAT_ID.value))

    def test__duplicate_valid_request_vaccination(self):
        """ Test 20 , patient id is registered in store"""
        file_store = PatientsJsonStore()
        file_store.delete_json_file()
        my_request = VaccineManager()
        value = my_request.request_vaccination_id("a729d963-e0dd-47d0-8bc6-b6c595ad0098",
                                                  "Pedro Perez", "Regular", "+34333456789", "124")

        with self.assertRaises(VaccineManagementException) as context_manager:
            value = my_request.request_vaccination_id("a729d963-e0dd-47d0-8bc6-b6c595ad0098",
                                                      "Pedro Perez", "Regular", "+34333456789", "124")
        self.assertEqual(context_manager.exception.message,
                         ExceptionEnum.PATIENT_ALREADY_REGISTERED.value)

        self.assertIsNotNone(file_store.find_item(value))

    @freeze_time("2022-03-08")
    def test__add_family_valid_request_vaccination(self):
        """ Test 21 , patient Regular and family registered in store"""
        file_store = PatientsJsonStore()
        file_store.empty_json_file()
        my_request = VaccineManager()
        my_request.request_vaccination_id("a729d963-e0dd-47d0-8bc6-b6c595ad0098",
                                                  "Pedro Perez", "Regular", "+34333456789", "124")
        value = my_request.request_vaccination_id("a729d963-e0dd-47d0-8bc6-b6c595ad0098",
                                                  "Pedro Perez", "Family", "+34333456789", "124")
        self.assertEqual(value, "f498f09220649fce1e2e8e523d16d212")
        patients_found = file_store.find_items_list("a729d963-e0dd-47d0-8bc6-b6c595ad0098",
                                                    AttributeEnum.VACC_PAT_REG_PAT_ID.value)
        self.assertEqual(len(patients_found), 2)

    @freeze_time("2022-03-08")
    def test_request_vaccination_id_ok(self):
        """Test OK"""
        file_store = PatientsJsonStore()
        file_store.delete_json_file()
        my_request = VaccineManager()

        value = my_request.request_vaccination_id("bb5dbd6f-d8b4-413f-8eb9-dd262cfc54e0",
                                                  "Pedro Hernandez", "Regular", "+34123456789", "22")
        self.assertEqual("9bc3dcae6701f7f54d71e36e0df12a59", value)
        self.assertIsNotNone(
            file_store.find_item(value))

    def test_request_vaccination_id_nok_uuid(self):
        """UUID is not v4 version"""
        my_request = VaccineManager()

        with self.assertRaises(VaccineManagementException) as context_manager:
            my_request.request_vaccination_id("bb5dbd6f-d8b4-113f-8eb9-dd262cfc54e0",
                                              "Pedro Hernandez", "Regular",
                                              "+34123456789", "22")
        self.assertEqual(ExceptionEnum.BAD_UUID.value, context_manager.exception.message)

    def test_request_vaccination_id_nok_uuid_2(self):
        """UUID is not hexadecimal"""
        my_request = VaccineManager()
        with self.assertRaises(VaccineManagementException) as context_manager:
            my_request.request_vaccination_id("zb5dbd6f-d8b4-113f-8eb9-dd262cfc54e0",
                                              "Pedro Hernandez", "Regular",
                                              "+34123456789", "22")
        self.assertEqual(ExceptionEnum.NOT_UUID.value, context_manager.exception.message)

    def test_request_registration_type_nok(self):
        """registration type is not ok"""
        file_store = PatientsJsonStore()
        hash_original = file_store.data_hash()

        my_request = VaccineManager()
        with self.assertRaises(VaccineManagementException) as context_manager:
            my_request.request_vaccination_id("bb5dbd6f-d8b4-413f-8eb9-dd262cfc54e0",
                                              "Pedro Hernandez", "Regularito",
                                              "+34123456789", "22")
        hash_new = file_store.data_hash()

        self.assertEqual(ExceptionEnum.BAD_REGISTRATION_TYPE.value, context_manager.exception.message)
        self.assertEqual(hash_new, hash_original)


if __name__ == '__main__':
    unittest.main()
