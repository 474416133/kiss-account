import logging
from typing import Annotated

from fastapi import Depends
from fastapi import HTTPException
from fastapi import Request
from fastapi import status
from fastapi.security import OAuth2PasswordBearer
from app.engines import Session
from app.schemas.authorize import Client as Client_
from app.managers.user import get_user_by_token



logger = logging.getLogger('kiss-account')
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")
# oauth2_scheme1 = OAuth2PasswordBearer(tokenUrl="/api/oauth2/token", auto_error=False)
Token = Annotated[str, Depends(oauth2_scheme)]


# OptionalToken = Annotated[str, Depends(oauth2_scheme1)]


def get_current_user(request: Request):
    if not hasattr(request, '_current_user'):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Could not validate credentials",
                            headers={"Auth": 'xxxx'},
                            )
    return request._current_user


CurrentUser = Annotated[dict, Depends(get_current_user)]


def get_client(request: Request):
    if hasattr(request, '_client'):
        return request._client
    client_id = request.headers.get('X-KISS-CLIENT-ID')
    ip = request.headers.get('X-Forwarded-For')
    if not ip:
        ip = request.client.host
    client = Client_(client_id=client_id, client_ip=ip)
    request._client = client
    return client


Client = Annotated[Client_, Depends(get_client)]


async def get_conn(request: Request):
    if hasattr(request, '_conn'):
        conn = request._conn
    else:
        conn = Session()
        request._conn = conn
    logger.debug('create a conn')
    try:
        yield conn
    finally:
        await conn.close()
        logger.debug('close a conn')


Conn = Annotated[str, Depends(get_conn)]


async def authenticated(request: Request, token: Token, client:Client, conn: Conn):
    """
    验证
    """
    logger.debug('authenticated ....')
    user_obj = await get_user_by_token(token, client, conn=conn)
    request._current_user = user_obj





