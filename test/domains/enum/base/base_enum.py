from enum import Enum


class BaseEnum(Enum):
    @classmethod
    def reverse_lookup(cls, val):
        for member in cls:
            if val in member.value:
                return member
        raise ValueError(f"No matching enum member with value: {val}")
