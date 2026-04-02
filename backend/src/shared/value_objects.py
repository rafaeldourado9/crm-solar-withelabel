import re

from pydantic import field_validator

from src.shared.exceptions import ValidationError


def validate_cpf(value: str) -> str:
    digits = re.sub(r"\D", "", value)
    if len(digits) != 11:
        raise ValidationError("CPF deve ter 11 digitos")
    return digits


def validate_cnpj(value: str) -> str:
    digits = re.sub(r"\D", "", value)
    if len(digits) != 14:
        raise ValidationError("CNPJ deve ter 14 digitos")
    return digits


def validate_cpf_cnpj(value: str) -> str:
    digits = re.sub(r"\D", "", value)
    if len(digits) == 11:
        return validate_cpf(value)
    if len(digits) == 14:
        return validate_cnpj(value)
    raise ValidationError("CPF/CNPJ invalido")
