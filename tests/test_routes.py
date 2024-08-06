# This is to test the signup endpoint
def test_signup(client):
    response = client.post('/api/signup/', json={
        'username': 'testuser',
        'email': 'test@example.com',
        'password': 'password',
        'bio': 'Test bio'
    }, headers={'Content-Type': 'application/json'})
    print(response.data)
    assert response.status_code == 201


# This is to test the signin endpoint
def test_signin(client):
    response = client.post('/api/signin/', json={
        'email': 'test@example.com',
        'password': 'password'
    }, headers={'Content-Type': 'application/json'})
    print(response.data)
    assert response.status_code == 200


# This is to test the get_users endpoint
def test_get_users(client):
    response = client.get('/api/users/')
    assert response.status_code == 200
    assert b'testuser' in response.data


# This is to test the get_user endpoint
def test_get_user(client):
    response = client.get('/api/user/testuser/')
    assert response.status_code == 200
    assert b'testuser' in response.data
    assert b'test@example.com' in response.data
    assert b'Test bio' in response.data
