import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()


def explain_decision(user_data: dict , prediction: dict) -> str:
    api_key = os.getenv('GROQ_API_KEY')

    if not api_key:
        raise ValueError('GROQ_API_KEY is not configured.')
    
    client = Groq(api_key=api_key)

    prompt =prompt = f"""
You are an experienced credit underwriting analyst for an Indian fintech company.

Customer Information:
- Annual Income: ₹{user_data.get('AMT_INCOME_TOTAL')}
- Requested Loan Amount: ₹{user_data.get('AMT_CREDIT')}
- Age: {user_data.get('DAYS_BIRTH')}
- Employment Duration: {user_data.get('DAYS_EMPLOYED')} years

Prediction:
- Decision: {prediction['decision']}
- Risk Score: {prediction['risk_score']}

Instructions:

1. Use ONLY the information above.
2. Never invent customer information.
3. Never say income is zero unless Annual Income is actually 0.
4. Never assume missing information.
5. Explain the decision in simple language.
6. Keep the explanation under 100 words.
7. Use an Indian banking / fintech context.
"""
    
    response = client.chat.completions.create(
        model = "llama-3.3-70b-versatile",
        messages = [
            {
                "role" : "system",
                "content" : "you are an expert indian credit underwriting analyst."
            },
            {
            "role": "user",
            "content": prompt
            }
        ],
        max_tokens= 150
    )

    return response.choices[0].message.content
