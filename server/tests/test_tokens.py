from app.auth.tokens import create_access_token
from jose import jwt

def test_create_access_token():
    token = create_access_token({"sub": "test@example.com"})
    payload = jwt.decode(token, "secret", algorithms=["HS256"])
    assert payload["sub"] == "test@example.com"
