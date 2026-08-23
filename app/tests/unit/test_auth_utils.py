from config.auth_utils import hashing_password, verify_password

def test_hasing_password():
    password = "mysecretpassword"
    hashed_password = hashing_password(password)
    assert hashed_password != password
    password_check = verify_password(password, hashed_password)
    assert password_check is True



def test_jwt_token_generation_and_verification():
    from config.auth_utils import generate_token,verify_token,TokenData
    from uuid import uuid7
    from models import UserRole
    data = TokenData(user_id=uuid7(),role=UserRole.USER)
    
    token = generate_token(data)
    assert token is not None
    verified_data = verify_token(token)
    assert verified_data.user_id == data.user_id
    assert verified_data.role == data.role    