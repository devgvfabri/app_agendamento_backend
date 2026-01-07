from fast_agend.models import User

def test_create_user():
    user = User(
        username='test',
        email='test@test',
        password='test'
    )
    assert user.username == 'test'