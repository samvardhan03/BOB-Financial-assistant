from flask import Flask, request, jsonify
import os
import time
from openai import AzureOpenAI

app = Flask(__name__)

client = AzureOpenAI(
    azure_endpoint=os.getenv("https://aienvoysbob.openai.azure.com/"),
    api_key=os.getenv("68fe3fbfff734356a1f3e6019aad87fc"),
    api_version="2024-02-15-preview"
)

assistant = client.beta.assistants.create(
    model="OmniModel",
    instructions="""
    You are a helpful financial assistant bot that helps people with:
    - General Financial Tips: Get practical financial advice tailored to your specific goals, such as saving for a house or planning for retirement.
    - Schedule Appointments: Need to speak with a banker? Easily schedule an appointment at your preferred date and time for personalized assistance.
    - Policy Information: Access detailed information about various banking policies, helping you stay informed and make educated financial decisions.
    - Locate Nearest Branch or ATM: Quickly find the nearest bank branch or ATM based on your current location, ensuring you always have access to essential banking services.
    - Investment Advice: Receive expert investment advice aligned with your financial goals, whether you're planning for retirement or considering new investment opportunities.
    - Loan EMI Calculator: Calculate your monthly loan EMIs by inputting the loan amount, interest rate, and tenure. Make informed decisions with ease.
    - Loan Information: View details about your existing loans, including balances, interest rates, and repayment schedules.
    - Transaction History: Retrieve transaction history for your bank account by specifying your account number and date range, enabling you to track your spending.
    """,
    tools=[
        {"type": "function", "function": {"name": "provide_financial_tips", "description": "Offer general financial tips to help users manage their finances better", "parameters": {"type": "object", "properties": {"financial_goal": {"type": "string", "description": "User's financial goal (e.g., saving for a house, retirement)"}}, "required": ["financial_goal"]}}},
        {"type": "function", "function": {"name": "locate_nearest_branch_atm", "description": "Find the nearest bank branch or ATM based on the user's location", "parameters": {"type": "object", "properties": {"location": {"type": "string", "description": "The user's current location or address"}, "type": {"type": "string", "description": "Specify whether to locate a 'branch' or 'ATM'", "enum": ["branch", "ATM"]}}, "required": ["location", "type"]}}},
        {"type": "function", "function": {"name": "calculate_loan_emi", "description": "Calculate the monthly EMI for a loan", "parameters": {"type": "object", "properties": {"loan_amount": {"type": "number", "description": "The total loan amount"}, "interest_rate": {"type": "number", "description": "The annual interest rate in percentage"}, "tenure_years": {"type": "number", "description": "The loan tenure in years"}}, "required": ["loan_amount", "interest_rate", "tenure_years"]}}},
        {"type": "function", "function": {"name": "get_investment_advice", "description": "Provide investment advice based on user's assets and goals", "parameters": {"type": "object", "properties": {"current_assets": {"type": "number", "description": "The total value of user's current assets"}, "financial_goals": {"type": "string", "description": "User's financial goals (e.g., retirement, buying a house)"}}, "required": ["current_assets", "financial_goals"]}}}
    ]
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
