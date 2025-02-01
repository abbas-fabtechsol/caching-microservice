from fastapi.testclient import TestClient
from main import app
from sqlmodel import Session, select, SQLModel
from models import Payload
from database import engine
from sqlmodel import Session, select
import pytest

# Create a TestClient for the FastAPI app
client = TestClient(app)

# Fixture to set up and tear down the database for each test
@pytest.fixture(scope="function")
def db_session():
    # Create all tables
    SQLModel.metadata.create_all(engine)
    # Create a new session for testing
    with Session(engine) as session:
        yield session
    # Drop all tables after the test
    SQLModel.metadata.drop_all(engine)

# Test POST /payload
def test_create_payload(db_session):
    # Test creating a new payload
    response = client.post(
        "/payload",
        json={"list_1": ["hello", "world"], "list_2": ["foo", "bar"]}
    )
    assert response.status_code == 201
    payload_id = response.json()["id"]
    assert isinstance(payload_id, str)

    # Verify the payload was saved in the database
    with Session(engine) as session:
        payload = session.exec(select(Payload).where(Payload.id == payload_id)).first()
        assert payload is not None
        assert payload.output == "HELLO, FOO, WORLD, BAR"

# Test POST /payload with unequal lists
def test_create_payload_unequal_lists(db_session):
    response = client.post(
        "/payload",
        json={"list_1": ["hello"], "list_2": ["foo", "bar"]}
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "Lists must be of the same length"}

# Test POST /payload with existing output
def test_create_payload_existing_output(db_session):
    # Create a payload with the same output
    existing_payload = Payload(id="123", output="HELLO, FOO, WORLD, BAR")
    with Session(engine) as session:
        session.add(existing_payload)
        session.commit()

    # Test creating a new payload with the same output
    response = client.post(
        "/payload",
        json={"list_1": ["hello", "world"], "list_2": ["foo", "bar"]}
    )
    assert response.status_code == 201
    assert response.json() == {"id": "123"}

# Test GET /payload/{id}
def test_read_payload(db_session):
    # Create a payload to retrieve
    payload_id = "123"
    payload = Payload(id=payload_id, output="HELLO, FOO, WORLD, BAR")
    with Session(engine) as session:
        session.add(payload)
        session.commit()

    # Test retrieving the payload
    response = client.get(f"/payload/{payload_id}")
    assert response.status_code == 200
    assert response.json() == {"output": "HELLO, FOO, WORLD, BAR"}

# Test GET /payload/{id} with non-existent ID
def test_read_payload_not_found(db_session):
    response = client.get("/payload/non-existent-id")
    assert response.status_code == 404
    assert response.json() == {"detail": "Payload not found"}