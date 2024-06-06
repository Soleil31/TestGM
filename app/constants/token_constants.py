TOKEN_API_PREFIX = "/token"

ALGORITHM = "HS256"

ACCESS_TOKEN_EXPIRE_MINUTES = 60

REFRESH_TOKEN_EXPIRE_DAYS = 7

TOKEN_HEADERS = {
    "headers": {"WWW-Authenticate": "Bearer"},
}

OAUTH2_URL = "/api/v1/user/login"
