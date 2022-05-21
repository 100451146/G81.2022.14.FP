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