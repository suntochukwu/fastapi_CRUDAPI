from fastapi.testclient import TestClient
from app.main import app
from app.main import schemas
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.config import settings
from sqlalchemy.ext.declarative import declarative_base
from app.database import get_db, Base
import pytest
from jose import jwt
sqlalchemy_database_url= f"postgresql://postgres:8938@localhost:5432/FASTAPIdb_test"
#sqlalchemy_database_url= f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}/{settings.database_username}"
engine = create_engine(sqlalchemy_database_url)
testing_sessionlocal= sessionmaker(autocommit=False, autoflush=False, bind= engine)



@pytest.fixture
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = testing_sessionlocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture
def client(session):
    def override_get_db():

        try :
             yield session
        finally:
             session.close()
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)

@pytest.fixture
def test_create_user_fixture(client):
    userslogin= {"email": "donkey@gmail.com", "password":"gioj435"}
    result = clientcall.post("/users/", json=userslogin)
    assert result.status_code == 201
    testuser= result.json()
    testuser["password"]= userslogin["password"]
    print(testuser)
    return testuser



clientcall=TestClient(app)

def test_createuser(client):
    # with pytest.raises(Exception):

    result = clientcall.post("/users/", json={"email":"aobinali@gmail.com","password":"postcard1235"})
    new_user= schemas.UserOut(**result.json())

    assert new_user.email == "aobinali@gmail.com"
    assert result.status_code == 201

def test_get_user(client, test_create_user_fixture):
    result = clientcall.post("/login", data= {"username": test_create_user_fixture["email"], "password": test_create_user_fixture["password"]})
    logintokin= schemas.Token(**result.json())
    payload=jwt.decode(logintokin.access_token, settings.secret_key,algorithms=[settings.algorithm])
    id=  payload.get('user_id')
    assert result.status_code == 200
    assert id == test_create_user_fixture["id"]
    assert logintokin.token_type== 'bearer'

@pytest.mark.parametrize("email, password, statuscode", [
( "donkey@gmail.com", "34355", 403),
( "donke23y@gmail.com", "34dfg5", 403),
( None, "gioj435", 422),
( None, None, 422)

])
def test_wrongpw(client, test_create_user_fixture,email,password,statuscode):
     result = clientcall.post("/login", data= {"username": email, "password":password})
    
     assert result.status_code == statuscode
   #  assert result.json().get('detail') == "invalid credentials"
    