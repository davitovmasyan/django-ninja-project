from enum import Enum

import typing_extensions

from ninja_jwt.tokens import RefreshToken
from pydantic import Field, EmailStr, field_validator
from ninja import ModelSchema, Schema
from pydantic import model_validator
from django.contrib.auth.hashers import check_password

from core.errors import in_use_error, invalid_token_error
from accounts import emails
from accounts.models import User
from accounts.schemas import UserSchema

__all__ = (
    'SignupPayload',
    'ForgotPasswordPayload',
    'ResetPasswordPayload',
    'ChangePasswordPayload',
    'VerifyEmailPayload',
    'ResendVerifyEmailPayload',
    'UserProfileResponse',
    'AccountResponse',
    'UserEmailFilter',
)




class SignupPayload(Schema):
    email: EmailStr
    password: str
    password_confirmation: str | None = Field(None)

    first_name: str | None = Field(None, min_length=2, max_length=150)
    last_name: str | None = Field(None, min_length=2, max_length=150)

    @field_validator('email', mode='after')
    def validate_email(cls, email: EmailStr):
        if User.objects.filter(email=email).exists():
            raise in_use_error('email', email)
        return email

    @model_validator(mode='after')
    def validate_passwords(self) -> typing_extensions.Self:
        if self.password_confirmation is not None and self.password != self.password_confirmation:
            raise ValueError('password do not match')
        return self

    def save(self):
        user = User(
            email=self.email,
            first_name=self.first_name,
            last_name=self.last_name,
            email_confirmation_token=User.generate_token(),
        )

        user.set_password(self.password)
        user.save()

        emails.send_email_address_confirmation(user)

        values = {}
        refresh = RefreshToken.for_user(user)
        values['refresh'] = str(refresh)
        values['access'] = str(refresh.access_token)
        values.update(user=UserSchema.from_orm(user))

        return values


class ForgotPasswordPayload(Schema):
    email: EmailStr

    def save(self):
        user = User.objects.filter(email=self.email).first()
        if user is None:
            # fail silently to avoid getting attacked
            return

        user.reset_password_token = User.generate_token()
        user.generate_password_request_date()
        user.save()

        emails.send_forgot_password_request(user)


class ChangePasswordPayload(Schema):
    old_password: str
    password: str
    password_confirmation: str

    @model_validator(mode='after')
    def validate_passwords(self) -> typing_extensions.Self:
        if self.password != self.password_confirmation:
            raise ValueError('passwords did not match')
        return self

    def save(self, user):
        if not check_password(self.old_password, user.password):
            raise ValueError('current password is incorrect')

        user.set_password(self.password)
        user.save()


class ResetPasswordPayload(Schema):
    token: str
    password: str
    password_confirmation: str | None = None

    @field_validator('token', mode='after')
    def validate_token(cls, token: str):
        user = User.objects.filter(reset_password_token=token).first()
        if user is None or not user.is_password_token_fresh():
            raise invalid_token_error()

        return token

    @model_validator(mode='after')
    def validate_passwords(self) -> typing_extensions.Self:
        if self.password_confirmation is not None and self.password != self.password_confirmation:
            raise ValueError('password do not match')
        return self

    def save(self):
        user = User.objects.filter(reset_password_token=self.token).first()
        user.reset_password_token = None
        user.reset_password_request_date = None
        user.set_password(self.password)
        user.save()


class VerifyEmailPayload(Schema):
    token: str = Field(..., min_length=1)

    def save(self):
        _ = (
            User.objects
                .filter(email_confirmation_token=self.token)
                .update(email_confirmation_token=None)
        )


class UserProfileResponse(ModelSchema):

    class Meta:
        model = User
        fields = [
            'email',
            'first_name',
            'last_name',
            'is_verified',
        ]


class ResendVerifyEmailPayload(Schema):
    @staticmethod
    def save(user):
        user.refresh_from_db()

        emails.send_email_address_confirmation(user)

class AccountResponse(Schema):
    id: int
    email: str
    first_name: str | None = None
    last_name: str | None = None


class UserEmailFilter(Schema):
    email: str | None = None

    def apply_filters(self, queryset):
        if self.email:
            queryset = queryset.filter(email__icontains=self.email)
        return queryset
