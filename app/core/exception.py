# --- base ---
class CustomException(Exception):
    def __init__(
        self,
        error_code: str,
        status_code: int = 500,
        message: str = "Internal server error!",
    ):
        self.error_code = error_code
        self.status_code = status_code
        self.message = message


# --- common ---
class InternalServerException(CustomException):
    def __init__(self, message: str = "Internal server error!"):
        super().__init__(
            error_code="INTERNAL_SERVER",
            status_code=500,
            message=message,
        )


class UnauthorizedException(CustomException):
    def __init__(self, message: str = "You're not authenticated!"):
        super().__init__(
            error_code="UNAUTHORIZED",
            status_code=401,
            message=message,
        )


class ValidationErrorException(CustomException):
    def __init__(self, message: str = "Request validation failed!"):
        super().__init__(
            error_code="VALIDATION_ERROR",
            status_code=422,
            message=message,
        )


class ForbiddenAccessException(CustomException):
    def __init__(self, message: str = "You do not have access permissions!"):
        super().__init__(
            error_code="FORBIDDEN_ACCESS",
            status_code=403,
            message=message,
        )


# --- invalid ---
class InvalidTokenException(CustomException):
    def __init__(self, message: str = "Token is invalid!"):
        super().__init__(
            error_code="INVALID_TOKEN",
            status_code=400,
            message=message,
        )


class InvalidOldPasswordException(CustomException):
    def __init__(self, message: str = "Old password is invalid!"):
        super().__init__(
            error_code="INVALID_OLD_PASSWORD",
            status_code=400,
            message=message,
        )


# --- not found ---
class DataNotFoundException(CustomException):
    def __init__(self, message: str = "Data not found!"):
        super().__init__(
            error_code="DATA_NOT_FOUND",
            status_code=400,
            message=message,
        )


# --- exist ---
class UsernameExistException(CustomException):
    def __init__(self, message: str = "Username is already exists!"):
        super().__init__(
            error_code="USERNAME_EXIST",
            status_code=400,
            message=message,
        )
