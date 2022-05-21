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
from uc3m_care.parser.cancellation_json_parser import CancellationJsonParser
from uc3m_care.storage.appointments_json_store import AppointmentsJsonStore
from uc3m_care.parser.appointment_json_parser import AppointmentJsonParser

# pylint: disable=too-many-instance-attributes
from uc3m_care.storage.cancellations_json_store import CancellationsJsonStore


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
    def get_appointment_from_date_signature(cls, date_signature):
        """returns the vaccination appointment object for the date_signature received"""
        appointments_store = AppointmentsJsonStore()
        appointment_record = appointments_store.find_item(DateSignature(date_signature).value)
        if appointment_record is None:
            raise VaccineManagementException("date_signature is not found")
        freezer = freeze_time(
            datetime.fromtimestamp(appointment_record["_VaccinationAppointment__issued_at"]))
        freezer.start()
        appointment = cls(appointment_record["_VaccinationAppointment__patient_sys_id"],
                          appointment_record["_VaccinationAppointment__phone_number"], datetime.fromtimestamp(
                appointment_record["_VaccinationAppointment__appointment_date"]).isoformat())
        freezer.stop()
        return appointment

    @classmethod
    def get_cancellation_from_json_file(cls, json_file):
        cancellation_parser = CancellationJsonParser(json_file)
        cls.is_cancelable(cancellation_parser)
        cancellation = VaccinationCancellationLog(*[i for i in cancellation_parser.json_content.values()])
        if cancellation is None:
            raise VaccineManagementException("cancellation is not found")
        if cancellation.type == "Final":
            raise VaccineManagementException("Appointment cancellation is FINAL")
        return cancellation

    @classmethod
    def is_cancelable(cls, cancellation_parser):
        CancellationType(cancellation_parser.json_content[cancellation_parser.CANCELLATION_TYPE])
        DateSignature(cancellation_parser.json_content[cancellation_parser.DATE_SIGNATURE])
        CancellationReason(cancellation_parser.json_content[cancellation_parser.REASON])

    @classmethod
    def create_appointment_from_json_file(cls, json_file, iso_date):
        """returns the vaccination appointment for the received input json file"""
        appointment_parser = AppointmentJsonParser(json_file)
        cls.is_valid_future(iso_date)
        new_appointment = cls(
            appointment_parser.json_content[appointment_parser.PATIENT_SYSTEM_ID_KEY],
            appointment_parser.json_content[appointment_parser.CONTACT_PHONE_NUMBER_KEY],
            iso_date)
        return new_appointment

    @staticmethod
    def is_valid_future(iso_date: str):
        """checks if the appointment is in the future"""
        ISOFormat(iso_date)
        if datetime.fromisoformat(iso_date) > datetime.now():
            return True
        if datetime.fromisoformat(iso_date) == datetime.now():
            raise VaccineManagementException("The appointment date can't be on the same day of the request")
        raise VaccineManagementException("Date is in the past")

    def is_valid_today(self):
        """returns true if today is the appointment's date"""
        today = datetime.today().date()
        date_patient = datetime.fromtimestamp(self.appointment_date).date()
        if date_patient != today:
            raise VaccineManagementException("Today is not the date")
        return True

    def register_vaccination(self):
        """register the vaccine administration"""
        self.is_valid_today()
        if not self.is_cancelled(self.date_signature):
            vaccination_log_entry = VaccinationLog(self.date_signature)
            vaccination_log_entry.save_log_entry()
        return True

    @staticmethod
    def is_cancelled(date_signature):
        """checks if the appointment is cancelled"""
        cancellations_store = CancellationsJsonStore()
        cancellation_record = cancellations_store.find_item(date_signature, "_VaccinationCancellation__date_signature")
        if cancellation_record is None:
            return False
        if cancellation_record["_VaccinationCancellation__cancellation_type"] == "Final":
            raise VaccineManagementException("Appointment cancellation is FINAL")
        if cancellation_record["_VaccinationCancellation__cancellation_type"] == "Temporal":
            raise VaccineManagementException("Appointment has been cancelled")
        raise VaccineManagementException("Unexpected behaviour")
