import os
from dotenv import load_dotenv
import requests
from unittest.mock import patch

# Load environment variables
load_dotenv()

def call_openai_api(prompt):
    headers = {
        'Authorization': f'Bearer {os.getenv("OPENAI_API_KEY")}',
        'Content-Type': 'application/json',
    }
    response = requests.post('https://api.openai.com/v1/engines/davinci/completions', headers=headers, json={'prompt': prompt})
    return response.json()

@patch('requests.post')
def test_call_openai_api(mock_post):
    # Define the mock response data
    mock_response = {
        'choices': [
            {'text': 'Paris is the capital of France.'}
        ]
    }
    # Set the mock to return a response with the desired data
    mock_post.return_value.json.return_value = mock_response

    # Call your function
    result = call_openai_api("What is the capital of France?")
    
    # Assert the expected output
    assert result == mock_response
    print("Test passed:", result)

# Run the test
test_call_openai_api()
