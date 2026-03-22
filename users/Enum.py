from enum import Enum


class RoleEnum(Enum):
    PERSON = "person"
    CLIENT = "client"
    EMPLOYEE = "employee"


class ContractEnum(Enum):
    FULLTIME = "full-time"
    PARTTIME = "part-time"
    B2B = "b2b"
