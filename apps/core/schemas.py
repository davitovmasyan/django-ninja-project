from ninja import Schema


class DefaultOKResponse(Schema):
    message: str = 'OK'


class DefaultErrorResponse(Schema):
    message: str = 'Bad Request'
    error_code: int = 400


class DefaultNotFoundResponse(Schema):
    message: str = 'The requested resource was not found.'
    error_code: int = 404
    error_type: str = 'not_found'


class DefaultDeleteResponse(Schema):
    message: str = 'The resource successfully deleted.'
