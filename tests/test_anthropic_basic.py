import os
import pytest
from anthropic import Anthropic
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

@pytest.fixture
def anthropic_client():
    """Create an Anthropic client using API key from environment"""
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        pytest.skip("ANTHROPIC_API_KEY not found in environment")
    return Anthropic(api_key=api_key)

def test_anthropic_api_connection(anthropic_client):
    """Test basic API connectivity with a simple message"""
    message = anthropic_client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=100,
        messages=[
            {"role": "user", "content": "Say hello in exactly 3 words"}
        ]
    )
    
    # Verify we got a response
    assert message.content is not None
    assert len(message.content) > 0
    
    # Get the text response
    response_text = message.content[0].text
    
    # Verify it's a string and not empty
    assert isinstance(response_text, str)
    assert len(response_text) > 0
    
    print(f"\nClaude's response: {response_text}")

def test_anthropic_model_response_format(anthropic_client):
    """Test that the API returns expected response structure"""
    message = anthropic_client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=50,
        messages=[
            {"role": "user", "content": "What is 2+2?"}
        ]
    )
    
    # Check response structure
    assert hasattr(message, 'content')
    assert hasattr(message, 'model')
    assert hasattr(message, 'role')
    assert message.role == 'assistant'
    
    print(f"\nModel used: {message.model}")