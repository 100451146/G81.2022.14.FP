"""Module """
from uc3m_care.data.vaccine_patient_register import VaccinePatientRegister
from uc3m_care.data.vaccination_appointment import VaccinationAppointment


class VaccineManager:
    """Class for providing the methods for managing the vaccination process"""

    # pylint: disable=invalid-name
    class __VaccineManager:
        def __init__(self):
            pass

        # pylint: disable=too-many-arguments
        # pylint: disable=no-self-use
        def request_vaccination_id(self, patient_id,
                                   name_surname,
                                   registration_type,
                                   phone_number,
                                   age) -> str:
            """Register the patient into the patients file"""
            my_patient = VaccinePatientRegister(patient_id,
                                                name_surname,
                                                registration_type,
                                                phone_number,
                                                age)

            my_patient.save_patient()
            return my_patient.patient_sys_id

        def get_vaccine_date(self, input_file: str, iso_date: str) -> str:
            """Gets an appointment for a registered patient"""
            my_sign = VaccinationAppointment.create_appointment_from_json_file(input_file, iso_date)
            # save the date in store_date.json
            my_sign.save_appointment()
            return my_sign.date_signature

        def vaccine_patient(self, date_signature: str) -> bool:
            """Register the vaccination of the patient"""
            appointment = VaccinationAppointment.get_appointment_from_date_signature(date_signature)
            return appointment.register_vaccination()

        def cancel_appointment(self, input_file: str) -> str:
            """Cancel a vaccination appointment"""
            cancellation = VaccinationAppointment.get_cancellation_from_json_file(input_file)
            appointment = VaccinationAppointment.get_appointment_from_date_signature(cancellation.date_signature)
            VaccinationAppointment.register_cancellation(appointment, cancellation)
            return cancellation.date_signature

    instance = None

    def __new__(cls):
        if not VaccineManager.instance:
            VaccineManager.instance = VaccineManager.__VaccineManager()
        return VaccineManager.instance

    def __getattr__(self, name):
        return getattr(self.instance, name)

    def __setattr__(self, name, value):
        return setattr(self.instance, name, value)
