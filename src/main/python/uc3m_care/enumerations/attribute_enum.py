from enum import Enum

class AttributeEnum(Enum):
    VACC_APP_ISSUED = "_VaccinationAppointment__issued_at"
    VACC_APP_PAT_SYS_ID = "_VaccinationAppointment__patient_sys_id"
    VACC_APP_PHONE_NUMBER = "_VaccinationAppointment__phone_number"
    VACC_APP_DATE = "_VaccinationAppointment__appointment_date"

    VACC_CANC_LOG_DATE_SIGNATURE = "_VaccinationCancellationLog__date_signature"
    VACC_CANC_LOG_TYPE = "_VaccinationCancellationLog__type"

    VACC_CANC_DATE_SIGNATURE = "_VaccinationCancellation__date_signature"
    VACC_CANC_TYPE = "_VaccinationCancellation__cancellation_type"
    VACC_CANC_REASON = "_VaccinationCancellation__reason"

    VACC_PAT_REG_TIME_STAMP = "_VaccinePatientRegister__time_stamp"
    VACC_PAT_REG_PAT_ID = "_VaccinePatientRegister__patient_id"
    VACC_PAT_REG_NAME = "_VaccinePatientRegister__full_name"
    VACC_PAT_REG_PHONE = "_VaccinePatientRegister__phone_number"
    VACC_PAT_REG_REGISTRATION_TYPE = "_VaccinePatientRegister__registration_type"
    VACC_PAT_REG_AGE = "_VaccinePatientRegister__age"

    PAT_SYS_ID = "PatientSystemID"
    CONTACT_PHONE = "ContactPhoneNumber"