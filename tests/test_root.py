from fastapi import status


def test_get_root(client):
    response = client.get('/')
    assert response.status_code == status.HTTP_200_OK, response.text
    assert response.json == {"hello": "Hello, world!"}, response.json


def test_get_robots_txt(client):
    response = client.get('/robots.txt')
    assert response.status_code == status.HTTP_200_OK, response.text 
