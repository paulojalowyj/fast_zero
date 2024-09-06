from http import HTTPStatus

from fast_zero.schemas import UserPublic


def test_read_root(client):
    response = client.get('/')  # Act
    assert response.status_code == HTTPStatus.OK  # Assert
    assert response.json() == {'message': 'Batatinha Frita 123'}  # Assert


def test_create_user(client):
    response = client.post(
        '/users/',
        json={
            'username': 'alice',
            'email': 'alice@email.com',
            'password': 'secret',
        },
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'username': 'alice',
        'email': 'alice@email.com',
        'id': 1,
    }


def test_create_username_already_exists(client, user):
    response = client.post(
        '/users/',
        json={
            'username': 'test',
            'email': 'test1@test.com',
            'password': 'secret',
        },
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': 'Username already exists'}


def test_create_email_already_exists(client, user):
    response = client.post(
        '/users/',
        json={
            'username': 'test 2',
            'email': 'test@test.com',
            'password': 'secret',
        },
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': 'Email already exists'}


def test_read_users(client):
    response = client.get('/users/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': []}


def test_read_users_with_users(client, user):
    user_schema = UserPublic.model_validate(user).model_dump()

    response = client.get('/users/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': [user_schema]}


def test_update_user(client, user):
    response = client.put(
        '/users/1',
        json={
            'password': 'secret',
            'username': 'testUpdate',
            'email': 'test@test.com',
            'id': 1,
        },
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'username': 'testUpdate',
        'email': 'test@test.com',
        'id': 1,
    }


def test_update_user_not_found(client):
    response = client.put(
        '/users/2',
        json={
            'password': '1',
            'username': 'pedro',
            'email': 'test@test.com',
            'id': 1,
        },
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found'}


def test_read_user_not_found(client):
    response = client.get('/users/1')

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found'}


def test_read_user(client):
    response = client.get('/users/1')

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found'}


def test_delete_user(client, user):
    response = client.delete('/users/1')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'User deleted'}


def test_delete_user_not_found(client):
    response = client.delete('/users/2')

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found'}
