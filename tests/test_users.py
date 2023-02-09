import pytest
from app import schemas
from jose import jwt
from app.config import settings

def test_root(client):
    response = client.get('/')
    assert response.json().get('message') == 'Hello World'
    assert response.status_code == 200

def test_create_user(client):
    response = client.post('/users/', json={'email': 'victor@exemplo.com', 'password': 'senha123', 'phone_number': '(37)99999-9999'})
    new_user = schemas.UserOut(**response.json())
    assert new_user.email == 'victor@exemplo.com'
    assert response.status_code == 201

def test_login_user(client, test_user):
    response = client.post('/login', data={'username': test_user['email'], 'password': test_user['password']})
    login_response = schemas.Token(**response.json())
    payload = jwt.decode(login_response.access_token, settings.secret_key, algorithms=[settings.algorithm])
    id = payload.get('user_id')
    assert response.status_code == 200
    assert login_response.token_type == 'bearer'
    assert id == test_user['id']

@pytest.mark.parametrize('email, password, status_code',[
    ('exemplo@exemplo.com', 'senha123', 403),
    ('victor@exemplo.com', 'senhaErrada', 403),
    ('exemplo@exemplo.com', 'senhaErrada', 403),
    (None, 'senha123', 422),
    ('victor@exemplo.com', None, 422),
])
def test_incorrect_login(client, email, password, status_code):
    response = client.post('/login', data={'username': email, 'password': password})
    assert response.status_code == status_code