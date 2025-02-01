from sqlmodel import Session, create_engine
from models import CachedResult, Payload

def test_cached_result_model():
    # Test CachedResult model
    cached_result = CachedResult(original_string="hello", transformed_string="HELLO")
    assert cached_result.original_string == "hello"
    assert cached_result.transformed_string == "HELLO"

def test_payload_model():
    # Test Payload model
    payload = Payload(id="550e8400-e29b-41d4-a716-446655440000", output="HELLO, WORLD")
    assert payload.id == "550e8400-e29b-41d4-a716-446655440000"
    assert payload.output == "HELLO, WORLD"