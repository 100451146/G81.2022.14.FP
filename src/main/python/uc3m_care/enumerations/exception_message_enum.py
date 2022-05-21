from enum import Enum

class ExceptionEnum(Enum):
    # Invalid Object
    INVALID_APPOINTMENT_OBJECT = "Invalide appointment object"
    INVALID_VACC_LOG_OBJECT = "Invalid VaccinationLog object"
    INVALID_PATIENT_OBJECT = "Invalid patient object"

    # Vaccination Cancellation
    CANCELLATION_NOT_FOUND = "cancellation is not found"
    APPOINTMENT_IS_FINAL = "Appointment cancellation is FINAL"
    APPOINTMENT_IS_TEMPORAL = "Appointment has been cancelled"
    APPOINTMENT_ALREADY_CANCEL = "Appointment is already cancelled"
    VACC_CANC_TYPE_NOT_ACCEPT = "Unexpected behaviour"

    # Vaccination Date
    NOT_APPOINTMENT_WITH_DATE_SIGNATURE = "There is not an appointment with this date_signature"
    NOT_APPOINTMENT_THE_SAME_DAY_REQUEST = "The appointment can't be on the same day of the request"
    APPOINTMENT_EXPIRED = "Appointment date is in the past"
    TODAY_NOT_DAY = "Today is not the date"

    # Searchs failures
    PAT_SYS_ID_NOT_FOUND = "patient_system_id not found"
    PAT_DATA_MANIPULATED = "Patient's data have been manipulated"
    FILE_NOT_FOUND = "File is not found"
    WRONG_JSON_FORMAT = "JSON Decode Error - Wrong JSON Format"
    WRONG_FILE = "Wrong file or file path"
    PATIENT_ALREADY_REGISTERED = "patien_id is registered in store_patient"

    # Bad label
    BAD_LABEL_PHONE = "Bad label contact phone"
    BAD_LABEL_PATIENT_ID = "Bad label patient_id"
    BAD_LABEL_DATE_SIGNATURE = "Bad label date_signature"
    BAD_LABEL_CANC_TYPE = "Bad label cancellation_type"
    BAD_LABEL_REASON = "Bad label reason"

    # Attributes
    AGE_NOT_VALID = "age is not valid"
    BAD_CANC_REASON = "Reason for cancellation length is not between 2 and 100"
    BAD_CANC_TYPE = "Cancellation type is not valid"
    BAD_DATE_SIGNATURE = "date_signature format is not valid"
    BAD_NAME = "name surname is not valid"
    BAD_ISO_FORMAT = "Date is not ISO format"
    BAD_TYPE_DATE = "Date is not a string"
    BAD_UUID = "UUID invalid"
    NOT_UUID = "Id received is not a UUID"
    BAD_PATIENT_SYS_ID = "patient system id is not valid"
    BAD_PHONE_NUMBER = "phone number is not valid"
    BAD_REGISTRATION_TYPE = "Registration type is nor valid"





