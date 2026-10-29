import asyncio

from app.core.config import config
from app.core.exception import (
    CustomException,
    InternalServerException,
    UnauthorizedException,
    ValidationErrorException,
)
from app.core.logger import get_logger
from app.integrations.telegram import TelegramClient
from app.middlewares.context import AuthClaims, RequestContext, TokenTypeEnum
from app.middlewares.jwt.main import jwt_util
from app.utils.common import get_current_datetime
from fastapi import Depends, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer

logger = get_logger(__name__)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=config.AUTH_TOKEN_URL, auto_error=False)


class Middleware:
    def __init__(self):
        self._telegram_client = TelegramClient()

    def get_auth_user(self, token: str = Depends(oauth2_scheme)) -> AuthClaims:
        if not token:
            raise UnauthorizedException()

        try:
            auth_claims = jwt_util.parse_token(token)
            if auth_claims.type != TokenTypeEnum.ACCESS.value:
                raise UnauthorizedException()

            return auth_claims
        except Exception as err:
            logger.error(f"[Middleware] Failed to get auth user: {err}")

            raise UnauthorizedException()

    async def notify_internal_server_error(
        self, context: RequestContext, message: str
    ) -> None:
        formatted_message = "<b>🔊DANGER</b>‼️‼️\n"
        formatted_message += (
            f"<b>{config.SERVICE_NAME.upper()} INTERNAL SERVER ERROR 🔥🔥</b>\n\n"
        )
        formatted_message += f"🗓️*{get_current_datetime().replace(microsecond=0)}*\n\n"

        if context.ip:
            formatted_message += f"<b>IP ADDRESS:</b>\n{context.ip}\n\n"

        if context.port:
            formatted_message += f"<b>PORT:</b>\n{context.port}\n\n"

        if context.url:
            formatted_message += f"<b>URL:</b>\n{context.url}\n\n"

        if context.method:
            formatted_message += f"<b>METHOD:</b>\n{context.method}\n\n"

        formatted_message += f"<b>ERROR MESSAGE:</b>\n{message}\n\n"

        await self._telegram_client.send_message(
            chat_id=config.TELEGRAM_CHAT_ID,
            text=formatted_message,
            message_thread_id=config.TELEGRAM_MESSAGE_THREAD_ID,
        )

    async def unhandled_exception_handler(self, request: Request, exc: Exception):
        context = RequestContext(
            ip=request.client.host if request.client else None,
            port=request.client.port if request.client else None,
            url=str(request.url),
            method=request.method,
        )
        asyncio.create_task(self.notify_internal_server_error(context, str(exc)))

        return JSONResponse(
            status_code=InternalServerException().status_code,
            content={
                "err_code": InternalServerException().error_code,
                "message": InternalServerException().message,
            },
        )

    async def request_validation_exception_handler(
        self, request: Request, exc: RequestValidationError
    ):
        return JSONResponse(
            status_code=ValidationErrorException().status_code,
            content={
                "err_code": ValidationErrorException().error_code,
                "message": exc.errors(),
            },
        )

    async def custom_exception_handler(self, request: Request, exc: CustomException):
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "err_code": exc.error_code,
                "message": exc.message,
            },
        )


middleware = Middleware()
