from datetime import datetime, timedelta, timezone

from app.core.config import config
from app.core.exception import InternalServerException, InvalidTokenException
from app.core.logger import get_logger
from app.middlewares.context import AuthClaims
from jose import ExpiredSignatureError, jwt

logger = get_logger(__name__)


class JWTUtil:
    def create_token(self, claims: AuthClaims, duration: int) -> str:
        try:
            # setup expiration date
            claims.exp = datetime.now(timezone.utc) + timedelta(minutes=duration)

            # create token
            token = jwt.encode(
                claims=claims.model_dump(),
                key=config.AUTH_SECRET_KEY,
            )

            return token
        except Exception as err:
            logger.error(f"[JWT] Failed to create token: {err}")

            raise InternalServerException()

    def parse_token(self, token: str) -> AuthClaims:
        try:
            auth_claims: AuthClaims = jwt.decode(
                token=token,
                key=config.AUTH_SECRET_KEY,
                algorithms="HS256",
            )

            return AuthClaims(**auth_claims)
        except ExpiredSignatureError as err:
            logger.error(f"[JWT] Token expired: {err}")

            raise InvalidTokenException()
        except Exception as err:
            logger.error(f"[JWT] Failed to parse token: {err}")

            raise InvalidTokenException()


jwt_util = JWTUtil()
