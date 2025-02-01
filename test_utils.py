from utils import transform_string

def test_transform_string():
    # Test basic transformation
    assert transform_string("hello") == "HELLO"
    assert transform_string("world") == "WORLD"