from http import HTTPStatus

from fastapi.testclient import TestClient

from fast_zero.app import app

# Segir o padrão Arrange > Act > Assert para definir testes;


def test_read_root_deve_retornar_ok_e_ola_mundo():
    client = TestClient(app)  # Arrange
    response = client.get('/')  # Act
    assert response.status_code == HTTPStatus.OK  # Assert
    assert response.json() == {'message': 'Batatinha Frita 123'}  # Assert
