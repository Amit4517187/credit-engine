import joblib
import pandas as pd

def predict_risk(user_data: dict) -> dict:
    model = joblib.load('models/credit_model.pkl')
    features = joblib.load('models/features_name.pkl')

    df = pd.DataFrame([user_data])
    for col in features:
        if col not in df.columns:
            df[col] = 0
    df = df[features]

    risk_score = float(model.predict_proba(df)[0][1])
    decision = 'REJECT' if risk_score > 0.5 else 'APPROVE'

    return{
        'risk_score': round(risk_score, 4),
        'decision': decision
    }
if __name__ == "__main__":
  result = predict_risk({'AMT_INCOME_TOTAL': 150000 , 'AMT_CREDIT': 500000})
  print(result)

