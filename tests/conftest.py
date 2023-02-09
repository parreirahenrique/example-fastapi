from fastapi.testclient import TestClient
import pytest
from app import models
from app.main import app
from app.database import get_db, Base
from app.oauth2 import create_access_token
from .database import TestingSessionLocal, engine


@pytest.fixture()
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()

    try:
        yield db

    finally:
        db.close()


@pytest.fixture()
def client(session):
    
    def override_get_db():
        db = TestingSessionLocal()

        try:
            yield session

        finally:
            session.close()

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)

@pytest.fixture
def other_test_user(client):
    user_data = {
        'email': 'henrique@exemplo.com',
        'password': 'senha234',
        'phone_number': '(37)99888-8888'
    }

    response = client.post('/users/', json=user_data)
    new_user = response.json()
    new_user['password'] = user_data['password']
    return new_user

@pytest.fixture
def test_user(client):
    user_data = {
        'email': 'victor@exemplo.com',
        'password': 'senha123',
        'phone_number': '(37)99999-9999'
    }

    response = client.post('/users/', json=user_data)
    new_user = response.json()
    new_user['password'] = user_data['password']
    return new_user

@pytest.fixture
def token(test_user):
    return create_access_token({'user_id': test_user['id']})

@pytest.fixture
def authorized_client(client, token):
    client.headers ={
        **client.headers,
        'Authorization': f'Bearer {token}'
    }

    return client

@pytest.fixture
def test_posts(test_user, other_test_user, session):
    posts_data = [
        {
            'title': 'first test post title',
            'content': 'first test post content',
            'votes': 0,
            'user_id': test_user['id']

        },
        {
            'title': 'second test post title',
            'content': 'second test post content',
            'votes': 0,
            'user_id': test_user['id']

        },
        {
            'title': 'third test post title',
            'content': 'third test post content',
            'votes': 0,
            'user_id': test_user['id']

        },
        {
            'title': 'fourth test post title',
            'content': 'fourth test post content',
            'votes': 0,
            'user_id': other_test_user['id']

        }
    ]

    def create_post_model(post):
        return models.Post(**post)

    posts_map = map(create_post_model, posts_data)
    posts = list(posts_map)

    session.add_all(posts)
    session.commit()

    posts = session.query(models.Post).all()
    return posts