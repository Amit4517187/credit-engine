from fastapi import FastAPI , HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from src.predict import predict_risk
from src.explain import explain_decision

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_methods=['*'],
    allow_headers=['*']
)

class UserData(BaseModel):
    AMT_INCOME_TOTAL : float = 0
    AMT_CREDIT : float = 0
    AMT_ANNUITY : float = 0
    DAYS_BIRTH : float = 0
    DAYS_EMPLOYED : float = 0 

@app.get("/health")
async def health():
    return{'status': 'ok'}
    
@app.post("/predict")
async def predict(user : UserData):
        try:
            result = predict_risk(user.dict())

            try:
                 result['explanation'] = explain_decision(user.dict(), result)
            except Exception as e:
                 print(f"Explanation service error: {e}")
                 result["explanation"] = (
                      "Explanation service is temporarily unavailable. Please try again later."
                 )

            return result
        except Exception as e:
            raise HTTPException (status_code = 500 , detail=str(e))

