from enum import Enum

class ExceptionEnum(Enum):
    NOT_APPOINTMENT_WITH_DATE_SIGNATURE = "There is not an appointment with this date_signature"
    CANCELLATION_NOT_FOUND = "cancellation is not found"
    NOT_APPOINTMENT_THE_SAME_DAY_REQUEST = "The appointment can't be on the same day of the request"
    APPOINTMENT_EXPIRED = "Appointment date is in the past"
    TODAY_NOT_DAY = "Today is not the date"
    APPOINTMENT_IS_FINAL = "Appointment cancellation is FINAL"
    APPOINTMENT_IS_TEMPORAL = "Appointment has been cancelled"
    VACC_CANC_TYPE_NOT_ACCEPT = "Unexpected behaviour"
    APPOINTMENT_ALREADY_CANCEL = "Appointment is already cancelled"
    PAT_SYS_ID_NOT_FOUND = "patient_system_id not found"
    PAT_DATA_MANIPULATED = "Patient's data have been manipulated"
    INVALID_APPOINTMENT_OBJECT = "Invalide appointment object"

    BAD_LABEL_PHONE = "Bad label contact phone"
    BAD_LABEL_PATIENT_ID = "Bad label patient_id"
    BAD_LABEL_DATE_SIGNATURE = "Bad label date_signature"
    BAD_LABEL_CANC_TYPE = "Bad label cancellation_type"
    BAD_LABEL_REASON = "Bad label reason"

    FILE_NOT_FOUND = "File is not found"
    WRONG_JSON_FORMAT = "JSON Decode Error - Wrong JSON Format"
    WRONG_FILE = "Wrong file or file path"

    INVALID_PATIENT_OBJECT = "Invalid patient object"
    PATIENT_ALREADY_REGISTERED = "patien_id is registered in store_patient"
    INVALID_VACC_LOG_OBJECT = "Invalid VaccinationLog object"
