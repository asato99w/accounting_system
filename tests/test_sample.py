from src.main import hello_world

def test_samle():
    result = hello_world()
    expected = "Hello, World."
    assert result == expected