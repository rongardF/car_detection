# from uuid import UUID

# from fastapi import FastAPI, Request, status
# from fastapi.responses import JSONResponse
# from fastapi.security import OAuth2PasswordBearer, APIKeyHeader
# from jose import JWTError, jwt

# from starlette.types import Receive, Scope, Send

# # local imports
# from ..exception.repository_exception import NotFoundException

# # --- Authentication Setup ---
# SECRET_KEY = "my_key"
# ALGORITHM = "HS256"
# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token", auto_error=False)
# api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)
# VALID_API_KEYS = {'103a8ac0-e082-4d2c-859d-22d1a9026649', '8bb65040-f59a-49e9-bf7f-74809335fc9b'}


# class AuthenticationMiddleware:
#     # more info about middlewares: https://www.starlette.io/middleware/ 
#     def __init__(self, app: FastAPI):
#         self.app = app

#     def _parse_uuid(self, value: str) -> UUID:
#         try:
#             return UUID(value) 
#         except ValueError:
#             raise ValueError("invalid_uuid_string")

#     async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
#         # Skip middleware if non-HTTP request (e.g., WebSocket, lifespan event)
#         if scope["type"] != "http":  # for non-HTTP requests (e.g., WebSocket)
#             return await self.app(scope, receive, send)
        
#         # Create a Request object
#         request = Request(scope=scope, receive=receive)

#         # Skip middleware
#         if request.url.path.startswith("/docs"):  # for docs endpoints
#             return await self.app(scope, receive, send)
#         elif request.url.path.startswith("/health"):  # for health endpoint
#             return await self.app(scope, receive, send)
        
#         # logger: Logger = scope["state"]["logger"]

#         # JWT authentication
#         token = request.headers.get("Authorization", None)
#         if token and token.startswith("Bearer "):
#             try:
#                 jwt_token = token.split(" ")[1]
#                 payload = jwt.decode(jwt_token, SECRET_KEY, algorithms=[ALGORITHM])
#                 user_id = payload.get("sub")  # get user ID
#                 scope["state"]["user_id"] = self._parse_uuid(user_id)
#                 await self.app(scope, receive, send)
#             except JWTError:
#                 pass  # continue

#         # API key authentication
#         api_key = request.headers.get("X-API-Key", None)
#         if api_key:
#             api_key_repository = scope["state"]["api_key_repository"]
#             try:
#                 api_key_entity = api_key_repository.get_one(entity_id=api_key)
#             except NotFoundException:
#                 pass  # continue
#             scope["state"]["user_id"] = api_key_entity.user_id
#             await self.app(scope, receive, send)

#         response = JSONResponse(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             content={"detail": "unauthorized"},
#         )
#         await response(scope, receive, send)
