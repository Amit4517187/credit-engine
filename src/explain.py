import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()


def explain_decision(user_data: dict , prediction: dict) -> str:
    api_key = os.getenv('GROQ_API_KEY')

    if not api_key:
        raise ValueError('GROQ_API_KEY is not configured.')
    
    client = Groq(api_key=api_key)

    prompt =f"""
you are a credit risk analyst. explain this loan decision to a user in simple terms.

customer:
- Income: {user_data.get('AMT_INCOME_TOTAL' , 0)}
- loan_amount: {user_data.get('AMT_CREDIT' , 0)}

Decision: {prediction['decision']}
Risk score: {prediction['risk_score']} (higher = more risky)

Explain the decision in 2-3 simple sentance. why this decision was made.
Map the explaination to a indian fintech context.
"""
    
    response = client.chat.completions.create(
        model = "llama-3.3-70b-versatile",
        messages = [
            {
            "role": "user",
            "content": prompt
            }
        ],
        max_tokens= 150
    )

    return response.choices[0].message.content
