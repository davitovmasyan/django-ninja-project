from accounts.schemas.auth import TokenObtainPairOtherPayload
from ninja import Router, File, UploadedFile, Query
from ninja.errors import ValidationError, HttpError
from ninja.pagination import paginate

from accounts.models import User
from accounts.schemas import (
    SignupPayload,
    ForgotPasswordPayload,
    ResetPasswordPayload,
    ChangePasswordPayload,
    UserProfileResponse,
    VerifyEmailPayload,
    ResendVerifyEmailPayload,
    TokenObtainPairResponse,
    TokenObtainPairPayload,
    TokenRefreshOutputResponse,
    TokenRefreshOutputPayload,
    AccountResponse,
    UserEmailFilter,
)
from core.schemas import DefaultOKResponse, DefaultNotFoundResponse

__all__ = (
    'accounts_router',
)

accounts_router = Router(tags=['Accounts'])


@accounts_router.post(
    'signup/',
    auth=None,
    response={200: TokenObtainPairResponse},
    description='''Signs up a new user without any speciality. 
    `password_confirmation` field is optional.
    If provided, will be compared with the `password` field.''',
)
def signup(request, payload: SignupPayload):
    return 200, payload.save()


@accounts_router.post(
    'auth/pair/',
    auth=None,
    response={200: TokenObtainPairResponse},
    description='''Logs in a user and returns a token pair.''',
)
def auth_pair(request, payload: TokenObtainPairPayload):
    return 200, payload


@accounts_router.post(
    'auth/pair/other/',
    response={200: TokenObtainPairResponse},
    description='''Logs in a user and returns a token pair.''',
)
def auth_pair_other(request, payload: TokenObtainPairOtherPayload):
    if not request.auth.is_superuser:
        raise HttpError(401, 'Unauthorized')

    return 200, payload


@accounts_router.post(
    'auth/refresh/',
    auth=None,
    response={200: TokenRefreshOutputResponse},
    description='''Refreshes an access token.''',
)
def auth_refresh(request, payload: TokenRefreshOutputPayload):
    return 200, payload


@accounts_router.post(
    'forgot-password/',
    auth=None,
    response={200: DefaultOKResponse},
    description='''Sends an email message with a reset password token in it.
    If the provided email address doesn't exist in the database the request won't fail.''',
)
def forgot_password(request, payload: ForgotPasswordPayload):
    payload.save()
    return 200, {}


@accounts_router.post(
    'reset-password/',
    auth=None,
    response={200: DefaultOKResponse},
    description='''Changes unauthorized user's password based on a provided token.
    If the provided token doesn't exist in or is expired request will fail.''',
)
def reset_password(request, payload: ResetPasswordPayload):
    payload.save()
    return 200, {}


@accounts_router.post(
    'verify-email/',
    auth=None,
    response={200: DefaultOKResponse},
    description='''Verifies user's email address based on a provided token.
    If the provided token doesn't exist in the request won't fail.''',
)
def verify_email(request, payload: VerifyEmailPayload):
    payload.save()
    return 200, {}


@accounts_router.post(
    'resend-verify-email/',
    response={200: DefaultOKResponse},
    description='''Sends an email message with an email confirmation token in it.''',
)
def resend_verify_email(request, payload: ResendVerifyEmailPayload):
    payload.save(user=request.auth)
    return 200, {}


@accounts_router.put(
    'change-password/',
    response={200: DefaultOKResponse},
    description='''Changes current user's password.''',
)
def change_password(request, payload: ChangePasswordPayload):
    payload.save(user=request.auth)
    return 200, {}


@accounts_router.get(
    '',
    url_name='user_profile',
    response={200: UserProfileResponse},
)
def user_profile(request):
    user = (
        User.objects
        .filter(id=request.auth.id)
        .select_related('specialist__speciality')
        .first()
    )
    return 200, user


@accounts_router.post(
    'avatar/',
    response={200: UserProfileResponse},
    url_name='avatar',
)
def avatar(request, file: File[UploadedFile]):
    if file.content_type not in ['image/jpg', 'image/jpeg', 'image/png']:
        raise ValidationError([{'type': 'content_type', 'msg': f'content/type - {file.content_type} is not allowed.'}])
    if file.size > 5 * 1024 * 1024:  # 5 MB
        raise ValidationError([{'type': 'size', 'msg': 'file is too large.'}])

    request.auth.avatar.save(file.name, file)
    return 200, request.auth


@accounts_router.get(
    'profile/{user_id}/',
    response={200: UserProfileResponse, 404: DefaultNotFoundResponse},
    url_name='get_user_profile',
)
def get_user_profile(request, user_id: int):
    user = (
        User.objects
        .filter(id=user_id)
        .select_related('specialist__speciality')
        .first()
    )
    if not user:
        return 404, {}
    return 200, user


@accounts_router.get(
    'users/',
    response=list[AccountResponse],
    description='List of all accounts.',
    url_name='get_accounts',
)
@paginate
def get_accounts(request, filters: Query[UserEmailFilter]):
    if not request.user.is_superuser:
        raise HttpError(401, 'Unauthorized')

    return filters.apply_filters(User.objects.filter(is_superuser=False))
