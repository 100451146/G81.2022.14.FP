from enum import Enum

class AttributeEnum(Enum):
    VACC_APP_ISSUED = "_VaccinationAppointment__issued_at"
    VACC_APP_PAT_SYS_ID = "_VaccinationAppointment__patient_sys_id"
    VACC_APP_PHONE_NUMBER = "_VaccinationAppointment__phone_number"
    VACC_APP_DATE = "_VaccinationAppointment__appointment_date"

    VACC_CANC_DATE_SIGNATURE = "_VaccinationCancellationLog__date_signature"
    VACC_CANC_TYPE = "_VaccinationCancellationLog__type"
