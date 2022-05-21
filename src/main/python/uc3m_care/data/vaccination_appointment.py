"""Contains the class Vaccination Appointment"""
from datetime import datetime
import hashlib
from freezegun import freeze_time

from uc3m_care.data.attribute.attribute_cancellation_reason import CancellationReason
from uc3m_care.data.attribute.attribute_cancellation_type import CancellationType
from uc3m_care.data.attribute.attribute_iso_date import ISOFormat
from uc3m_care.data.attribute.attribute_phone_number import PhoneNumber
from uc3m_care.data.attribute.attribute_patient_system_id import PatientSystemId
from uc3m_care.data.attribute.attribute_date_signature import DateSignature
from uc3m_care.data.vaccination_cancellation_log import VaccinationCancellationLog
from uc3m_care.data.vaccination_log import VaccinationLog
from uc3m_care.data.vaccine_patient_register import VaccinePatientRegister
from uc3m_care.exception.vaccine_management_exception import VaccineManagementException
from uc3m_care.parser.appointment_json_parser import AppointmentJsonParser
from uc3m_care.parser.cancellation_json_parser import CancellationJsonParser
from uc3m_care.storage.appointments_json_store import AppointmentsJsonStore
from uc3m_care.storage.vaccination_json_store import VaccinationJsonStore
from uc3m_care.storage.cancellations_json_store import CancellationsJsonStore
from uc3m_care.enumerations.exception_message_enum import ExceptionEnum
from uc3m_care.enumerations.attribute_enum import AttributeEnum


# pylint: disable=too-many-instance-attributes
class VaccinationAppointment:
    """Class representing an appointment  for the vaccination of a patient"""

    def __init__(self, patient_sys_id, patient_phone_number, iso_date):
        self.__alg = "SHA-256"
        self.__type = "DS"
        self.__patient_sys_id = PatientSystemId(patient_sys_id).value
        patient = VaccinePatientRegister.create_patient_from_patient_system_id(
            self.__patient_sys_id)
        self.__patient_id = patient.patient_id
        self.__phone_number = PhoneNumber(patient_phone_number).value
        justnow = datetime.utcnow()
        self.__issued_at = datetime.timestamp(justnow)
        self.__appointment_date = ISOFormat(iso_date).value

        # if days == 0:
        #     self.__appointment_date = 0
        # else:
        #     # timestamp is represneted in seconds.microseconds
        #     # age must be expressed in senconds to be added to the timestap
        #     self.__appointment_date = self.__issued_at + (days * 24 * 60 * 60)
        self.__date_signature = self.vaccination_signature

    def __signature_string(self):
        """Composes the string to be used for generating the key for the date"""
        return "{alg:" + self.__alg + ",typ:" + self.__type + ",patient_sys_id:" + \
               self.__patient_sys_id + ",issuedate:" + self.__issued_at.__str__() + \
               ",vaccinationtiondate:" + self.__appointment_date.__str__() + "}"

    @property
    def patient_id(self):
        """Property that represents the guid of the patient"""
        return self.__patient_id

    @patient_id.setter
    def patient_id(self, value):
        self.__patient_id = value

    @property
    def patient_sys_id(self):
        """Property that represents the patient_sys_id of the patient"""
        return self.__patient_sys_id

    @patient_sys_id.setter
    def patient_sys_id(self, value):
        self.__patient_sys_id = value

    @property
    def phone_number(self):
        """Property that represents the phone number of the patient"""
        return self.__phone_number

    @phone_number.setter
    def phone_number(self, value):
        self.__phone_number = PhoneNumber(value).value

    @property
    def vaccination_signature(self):
        """Returns the sha256 signature of the date"""
        return hashlib.sha256(self.__signature_string().encode()).hexdigest()

    @property
    def issued_at(self):
        """Returns the issued at value"""
        return self.__issued_at

    @issued_at.setter
    def issued_at(self, value):
        self.__issued_at = value

    @property
    def appointment_date(self):
        """Returns the vaccination date"""
        return self.__appointment_date

    @property
    def date_signature(self):
        """Returns the SHA256 """
        return self.__date_signature

    def save_appointment(self):
        """saves the appointment in the appointments store"""
        appointments_store = AppointmentsJsonStore()
        appointments_store.add_item(self)

    @classmethod
    def create_appointment_from_json_file(cls, json_file, iso_date) -> 'VaccinationAppointment':
        """returns the vaccination appointment for the received input json file"""
        appointment_parser = AppointmentJsonParser(json_file)
        cls.is_valid_future(iso_date)
        new_appointment = cls(
            appointment_parser.json_content[appointment_parser.PATIENT_SYSTEM_ID_KEY],
            appointment_parser.json_content[appointment_parser.CONTACT_PHONE_NUMBER_KEY],
            iso_date)
        return new_appointment

    @classmethod
    def get_appointment_from_date_signature(cls, date_signature: str) -> 'VaccinationAppointment':
        """returns the vaccination appointment object for the date_signature received"""
        appointments_store = AppointmentsJsonStore()
        appointment_record = appointments_store.find_item(DateSignature(date_signature).value)
        if appointment_record is None:
            raise VaccineManagementException(ExceptionEnum.NOT_APPOINTMENT_WITH_DATE_SIGNATURE.value)
        freezer = freeze_time(
            datetime.fromtimestamp(appointment_record[AttributeEnum.VACC_APP_ISSUED.value]))
        freezer.start()
        appointment = cls(appointment_record[AttributeEnum.VACC_APP_PAT_SYS_ID.value],
                          appointment_record[AttributeEnum.VACC_APP_PHONE_NUMBER.value], datetime.fromtimestamp(
                appointment_record[AttributeEnum.VACC_APP_DATE.value]).isoformat())
        freezer.stop()
        return appointment

    @classmethod
    def get_cancellation_from_json_file(cls, json_file: str) -> VaccinationCancellationLog:
        """Obtain a cancellation object using the data from the json file"""
        cancellation_parser = CancellationJsonParser(json_file)
        cls.is_cancellation(cancellation_parser)
        cancellation = VaccinationCancellationLog(*list(cancellation_parser.json_content.values()))
        if cancellation is None:
            raise VaccineManagementException(ExceptionEnum.CANCELLATION_NOT_FOUND.value)
        return cancellation

    @classmethod
    def is_cancellation(cls, cancellation_parser: CancellationJsonParser) -> None:
        """Checks if the received json file is a cancellation"""
        CancellationType(cancellation_parser.json_content[cancellation_parser.CANCELLATION_TYPE])
        DateSignature(cancellation_parser.json_content[cancellation_parser.DATE_SIGNATURE])
        CancellationReason(cancellation_parser.json_content[cancellation_parser.REASON])

    @staticmethod
    def is_valid_future(iso_date: str) -> bool:
        """checks if the appointment is in the future"""
        ISOFormat(iso_date)
        if datetime.fromisoformat(iso_date) > datetime.now():
            return True
        if datetime.fromisoformat(iso_date) == datetime.now():
            raise VaccineManagementException(ExceptionEnum.NOT_APPOINTMENT_THE_SAME_DAY_REQUEST.value)
        raise VaccineManagementException(ExceptionEnum.APPOINTMENT_EXPIRED.value)

    def is_valid_today(self) -> bool:
        """returns true if today is the appointment's date"""
        today = datetime.today().date()
        date_patient = datetime.fromtimestamp(self.appointment_date).date()
        if date_patient != today:
            raise VaccineManagementException(ExceptionEnum.TODAY_NOT_DAY.value)
        return True

    @staticmethod
    def is_cancelled(date_signature: str):
        """checks if the appointment is cancelled"""
        cancellation = CancellationsJsonStore().find_item(date_signature, AttributeEnum.VACC_CANC_LOG_DATE_SIGNATURE.value)
        if cancellation is None:
            return False
        return cancellation[AttributeEnum.VACC_CANC_LOG_TYPE.value]

    @staticmethod
    def is_vaccinated(date_signature: str) -> bool:
        """checks if the patient is vaccinated"""
        vaccination = VaccinationJsonStore().find_item(date_signature)#, "_VaccinationLog__date_signature")
        if vaccination is None:
            return False
        return True

    def register_vaccination(self) -> bool:
        """register the vaccine administration"""
        self.is_valid_today()
        if not (c_type := self.is_cancelled(self.date_signature)):
            if self.is_vaccinated(self.date_signature):
                raise VaccineManagementException("Patient is already vaccinated")
            vaccination_log_entry = VaccinationLog(self.date_signature)
            vaccination_log_entry.save_log_entry()
        elif c_type == "Final":
            raise VaccineManagementException(ExceptionEnum.APPOINTMENT_IS_FINAL.value)
        elif c_type == "Temporal":
            raise VaccineManagementException(ExceptionEnum.APPOINTMENT_IS_TEMPORAL.value)
        else:
            raise VaccineManagementException(ExceptionEnum.VACC_CANC_TYPE_NOT_ACCEPT.value)
        return True

    @staticmethod
    def register_cancellation(appointment: 'VaccinationAppointment', cancellation: VaccinationCancellationLog) -> None:
        """Check if the appointment is in the future, if it is not already cancelled, and then register the cancellation"""
        VaccinationAppointment.is_valid_future(datetime.fromtimestamp(appointment.appointment_date).isoformat())
        if VaccinationAppointment.is_cancelled(cancellation.date_signature):
            raise VaccineManagementException(ExceptionEnum.APPOINTMENT_ALREADY_CANCEL.value)
        CancellationsJsonStore().add_item(cancellation)
