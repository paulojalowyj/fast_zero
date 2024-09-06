from jwt import decode

from fast_zero.security import create_access_token
from fast_zero.settings import Settings


def test_jwt():
    data = {'sub': 'test@test.com'}
    token = create_access_token(data)

    decoded = decode(
        token, Settings().JWT_SECRET, algorithms=Settings().JWT_ALGORITHM
    )

    assert decoded['sub'] == data['sub']
    assert decoded['exp']
