import requests
import os
from dotenv import load_dotenv


# Load environment variables from .env file
load_dotenv()


def call_openai_api(prompt):
    headers = {
        'Authorization': f'Bearer {os.getenv("OPENAI_API_KEY")}',  # Use environment variable for API key
        'Content-Type': 'application/json',
    }
    data = {
        'model': 'gpt-3.5-turbo',
        'messages': [{'role': 'user', 'content': prompt}],
    }
    response = requests.post('https://api.openai.com/v1/chat/completions', headers=headers, json=data)
    
    # Check for response status
    if response.status_code == 200:
        return response.json()
    else:
        return {'error': response.text}


# Example usage
result = call_openai_api("What is the capital of France?")
print(result)


knowledge_base = {
    "France": "Paris",
    "Germany": "Berlin",
    "Italy": "Rome"
}


def rag_system(query):
    # Retrieve information from the knowledge base
    answer = knowledge_base.get(query)
    
    if answer:
        return f"The answer is: {answer}"
    else:
        # If not found, generate a response
        response = call_openai_api(f"I don't know the answer to {query}. Can you help?")
        return response.get('choices', [{}])[0].get('message', {}).get('content', 'No response from API.')


# Example usage
print(rag_system("France"))
print(rag_system("Spain"))


class Agent:
    def __init__(self, name):
        self.name = name
        self.memory = []


    def remember(self, information):
        self.memory.append(information)


    def recall(self):
        return self.memory


agent1 = Agent("Agent 1")
agent2 = Agent("Agent 2")


agent1.remember("Paris is the capital of France.")
agent2.remember("Berlin is the capital of Germany.")


print(agent1.recall())
print(agent2.recall())


def agent_communication(agent_from, agent_to, message):
    agent_to.remember(message)
    return f"{agent_from.name} told {agent_to.name}: {message}"


print(agent_communication(agent1, agent2, "Paris is beautiful!"))
