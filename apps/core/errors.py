from typing import Any

from pydantic_core import PydanticCustomError


def in_use_error(field_name: str, wrong_value: Any):
    return PydanticCustomError(
        'in_use',
        f'{field_name}[{wrong_value}] is already used',
        dict(field_name=field_name, wrong_value=wrong_value),
    )


def invalid_token_error():
    return PydanticCustomError(
        'invalid_token',
        'provided token is not valid or expired',
    )


def invalid_credentials_error():
    return PydanticCustomError(
        'invalid_credentials',
        'provided credentials are not valid',
    )

def limit_exceeded():
    return PydanticCustomError(
        'limit_exceeded',
        'limit exceeded',
    )
