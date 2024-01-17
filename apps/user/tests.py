import jwt
from django.test import TestCase


def test_jwt_decoding():
    jwt_options = {
        'verify_signature': True,
        'verify_exp': True,
        'verify_nbf': False,
        'verify_iat': True,
        'verify_aud': False
    }
    token = ('eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9'
             '.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjg5NzQ4ODM3LCJpYXQiOjE2ODcxNTY4MzcsImp0aSI6IjliYzFkNzQ0OWRhYzRhODA4ZDA4NWNjNjk1ZWFlNGNjIiwidXNlcl9pZCI6MX0.IYseiPEM7QDk4RfJQTOiwck9jc-jjWxaLyCB4lupPGc')
    try:
        jwt.decode(
            token,
            'thingsboardDefaultSigningKey',
            algorithms=['HS512'],
            options=jwt_options
        )
        assert True
    except Exception as err:
        print(str(err))
        assert False