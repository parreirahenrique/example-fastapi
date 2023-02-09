import pytest
from app import schemas, models

def test_get_all_posts(authorized_client, test_posts):
    response = authorized_client.get('/posts/')

    def validate_posts(post):
        return schemas.ResponseBase(**post)

    posts_map = map(validate_posts, response.json())
    posts_list = list(posts_map)

    assert len(response.json()) == len(test_posts)
    assert response.status_code == 200

    for post_l in posts_list:
        for post_t in test_posts:
            if post_l.id == post_t.id:
                assert post_l.title == post_t.title
                assert post_l.content == post_t.content
                assert post_l.user_id == post_t.user_id
                assert post_l.created_at == post_t.created_at
                assert post_l.votes == post_t.votes

def test_unauthorized_user_get_all_posts(client, test_posts):
    response = client.get('/posts/')
    assert response.status_code == 401

def test_unauthorized_user_get_one_post(client, test_posts):
    for post in test_posts:
        response = client.get(f'/posts/{post.id}')
        assert response.status_code == 401

def test_get_one_post_not_exist(authorized_client, test_posts):
    response = authorized_client.get('/posts/99999')
    assert response.status_code == 404

@pytest.mark.parametrize('id', [
    (1),
    (2),
    (3)
])
def test_get_one_post(authorized_client, test_posts, id):
    response = authorized_client.get(f'/posts/{id}')
    
    for post in test_posts:
        if post.id == id:
            assert response.json().get('title') == post.title
            assert response.json().get('content') == post.content
            assert response.json().get('user_id') == post.user_id
            assert response.json().get('votes') == post.votes

    assert response.status_code == 200

def test_create_post(authorized_client):
    response = authorized_client.post('/posts/', json={'title': 'testing creating post', 'content': 'post created'})
    assert response.json().get('title') == 'testing creating post'
    assert response.json().get('content') == 'post created'
    assert response.status_code == 201

def test_unauthorized_user_create_post(client):
    response = client.post('/posts/', json={'title': 'testing creating post', 'content': 'post created'})
    assert response.status_code == 401

@pytest.mark.parametrize('id', [
    (1),
    (2),
    (3)
])
def test_delete_post(authorized_client, test_posts, id):
    response = authorized_client.delete(f'/posts/{id}')
    assert response.status_code == 204

@pytest.mark.parametrize('id', [
    (1),
    (2),
    (3)
])
def test_unauthorized_user_delete_post(client, test_posts, id):
    response = client.delete(f'/posts/{id}')
    assert response.status_code == 401

def test_delete_post_not_exist(authorized_client, test_posts):
    response = authorized_client.delete('/posts/99999')
    assert response.status_code == 404

def test_delete_other_user_post(authorized_client, test_user, test_posts):
    for post in test_posts:
        if test_user['id'] != post.user_id:
            post_id = post.id
            print(post_id)
            break

    response = authorized_client.delete(f'/posts/{post_id}')
    assert response.status_code == 403
