import pytest
from app import schemas, models

@pytest.fixture()
def test_vote(session, authorized_client):
    authorized_client.post('/vote', json={'post_id': 1, 'dir': 1})
    return session.query(models.Vote)

@pytest.mark.parametrize('id',[
    (1),
    (2),
    (3),
    (4),
])
def test_vote_on_post(session, authorized_client, test_posts, id):
    response = authorized_client.post('/vote', json={'post_id': id, 'dir': 1})

    post = session.query(models.Post).filter(models.Post.id == id).first()
    assert post.votes == 1
    assert response.json().get('message') == 'succesfully added vote'
    assert response.status_code == 201

def test_vote_twice_on_post(authorized_client, test_posts, test_vote):
    response = authorized_client.post('/vote', json={'post_id': 1, 'dir': 1})
    assert response.json().get('detail') == 'User 1 has already voted on post 1'
    assert response.status_code == 409

def test_delete_vote_on_post(session, authorized_client, test_user, test_posts, test_vote):
    response = authorized_client.post('/vote', json={'post_id': 1, 'dir': 0})
    post = session.query(models.Post).filter(models.Post.id == 1).first()
    assert post.votes == 0
    assert response.json().get('message') == 'succesfully deleted vote'
    assert response.status_code == 201

def test_delete_twice_vote_on_post(session, authorized_client, test_posts):
    response = authorized_client.post('/vote', json={'post_id': 1, 'dir': 0})
    post = session.query(models.Post).filter(models.Post.id == 1).first()
    assert post.votes == 0
    assert response.json().get('detail') == 'User 1 did not vote on post 1 previously'
    assert response.status_code == 404

def test_vote_post_not_exist(authorized_client, test_posts):
    response = authorized_client.post('/vote', json={'post_id': 99999, 'dir': 1})
    assert response.json().get('detail') == 'Post with id 99999 does not exist'
    assert response.status_code == 404

def test_delete_vote_post_not_exist(authorized_client, test_posts, test_vote):
    response = authorized_client.post('/vote', json={'post_id': 99999, 'dir': 0})
    assert response.json().get('detail') == 'Post with id 99999 does not exist'
    assert response.status_code == 404

def test_unauthenticated_user_vote_on_post(client, test_posts):
    response = client.post('/vote', json={'post_id': 1, 'dir': 1})
    assert response.status_code == 401