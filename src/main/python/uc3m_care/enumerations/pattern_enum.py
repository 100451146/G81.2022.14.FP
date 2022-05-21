from enum import Enum

class PatternEnum(Enum):
    CANC_REASON = r"^.{2,100}$"
    CANC_TYPE = r"(Temporal|Final)"
    DATE_SIGNATURE = r"[0-9a-fA-F]{64}$"
    NAME = r"^(?=^.{1,30}$)(([a-zA-Z]+\s)+[a-zA-Z]+)$"
    PATIENT_ID = r"^[0-9A-Fa-f]{8}-[0-9A-Fa-f]{4}-4[0-9A-Fa-f]{3}"\
                 r"-[89ABab][0-9A-Fa-f]{3}-[0-9A-Fa-f]{12}$"
    PATIENT_SYS_ID = r"[0-9a-fA-F]{32}$"
    PHONE_NUMBER = r"^(\+)[0-9]{11}"
    REGISTRATION_TYPE = r"(Regular|Family)"