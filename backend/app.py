from flask import Flask, request, jsonify
import os
import time
from openai import AzureOpenAI

app = Flask(__name__)

client = AzureOpenAI(
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    api_version="2024-02-15-preview"
)

assistant = client.beta.assistants.create(
    model="OmniModel",
    instructions="you are a helpful financial assistant bot that helps people with...",
    tools=[{"type":"function","function":{"name":"provide_financial_tips",...}},...]
)

def handle_message(user_message):
    thread = client.beta.threads.create()
    client.beta.threads.messages.create(thread_id=thread.id, role="user", content=user_message)
    run = client.beta.threads.runs.create(thread_id=thread.id, assistant_id=assistant.id)

    while run.status in ['queued', 'in_progress', 'cancelling']:
        time.sleep(1)
        run = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)

    if run.status == 'completed':
        messages = client.beta.threads.messages.list(thread_id=thread.id)
        return messages[-1].content
    else:
        return "There was an error processing your request."

@app.route('/api/message', methods=['POST'])
def message():
    user_message = request.json.get('content')
    if not user_message:
        return jsonify({'reply': 'Invalid message'}), 400

    response_message = handle_message(user_message)
    return jsonify({'reply': response_message})

if __name__ == '__main__':
    app.run(debug=True)

