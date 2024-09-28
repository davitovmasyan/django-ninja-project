from django.db.models import Q
from pydantic import model_validator
from ninja import Schema, ModelSchema
from ninja_jwt.tokens import RefreshToken

from core.errors import invalid_credentials_error
from accounts.models import User

__all__ = (
    'TokenObtainPairPayload',
    'TokenObtainPairResponse',
    'UserSchema',
    'TokenRefreshOutputResponse',
    'TokenRefreshOutputPayload',
)


class UserSchema(Schema):
    id: int
    first_name: str | None
    last_name: str | None
    email: str
    is_verified: bool
    is_superuser: bool


class TokenObtainPairResponse(Schema):
    refresh: str
    access: str
    user: UserSchema


class TokenObtainPairPayload(ModelSchema):
    class Config:
        model = User
        model_fields = ["email", "password"]

    @model_validator(mode='after')
    def validate(self):
        user = User.objects.filter(email=self.email).first()
        if not user:
            raise invalid_credentials_error()
        if not user.check_password(self.password):
            raise invalid_credentials_error()
        return self.get_token(user)

    @staticmethod
    def get_token(user) -> dict:
        values = {}
        refresh = RefreshToken.for_user(user)
        values['refresh'] = str(refresh)
        values['access'] = str(refresh.access_token)
        values['user'] = user
        return values


class TokenObtainPairOtherPayload(Schema):
    user_id: int | None = None
    email: str | None = None

    @model_validator(mode='after')
    def validate(self):
        user = User.objects.filter(Q(email=self.email) | Q(id=self.user_id)).first()
        if not user:
            raise invalid_credentials_error()
        return self.get_token(user)

    @staticmethod
    def get_token(user) -> dict:
        values = {}
        refresh = RefreshToken.for_user(user)
        values['refresh'] = str(refresh)
        values['access'] = str(refresh.access_token)
        values['user'] = user
        return values


class TokenRefreshOutputPayload(Schema):
    refresh: str

    @model_validator(mode="after")
    def validate(cls, values):
        values = values.dict()

        try:
            refresh = RefreshToken(values['refresh'])
        except Exception:
            raise invalid_credentials_error()  # noqa:B904

        data = {"access": str(refresh.access_token)}

        refresh.set_jti()
        refresh.set_exp()
        refresh.set_iat()

        data["refresh"] = str(refresh)
        return data


class TokenRefreshOutputResponse(Schema):
    refresh: str
    access: str
