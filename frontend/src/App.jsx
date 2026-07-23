import { useState } from "react";
import LoanInput from "./components/LoanInput"

 
function App() {

  const [income, setIncome] = useState("");
  const [loanAmount, setLoanAmount] = useState("");
  const [age, setAge] = useState("");
  const [employmentYears, setEmploymentYears] = useState("");

  const [prediction, setPrediction] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function handlePredict() {

    setPrediction(null);
    setError("");

    if (!income || !loanAmount || !age || !employmentYears) {
      setError("please fill all the fields before predicting!");
      return;
    }

    setLoading(true);

  try {

    const ageInDays = -(Number(age) * 365)

    const employmentDays = -(Number(employmentYears) * 365)

    const requestData = {
    AMT_INCOME_TOTAL: Number(income),
    AMT_CREDIT: Number(loanAmount),
    DAYS_BIRTH: ageInDays,
    DAYS_EMPLOYED: employmentDays,
    AMT_ANNUITY: 0
    };


    const response = await fetch(
      "http://127.0.0.1:8000/predict",
      {
        method : "POST",
        headers : {
          "Content-Type" : "application/json"
        },
        body : JSON.stringify(requestData)
      }
    );

    if (!response.ok) {
      throw new Error("Prediction request failed.");
    }

    const result = await response.json();

    console.log(result);

    setPrediction(result);

    }  catch (error) {

       console.error(error);

       setError (
        "Unable to connect to the prediction service. Please try again later."
       );

    }  finally {

       setLoading(false);

    }

  }

  return (
    <div>
      <>
        <h1>Credit Underwriting</h1>

      <LoanInput
      label = "Annual Income"
      placeholder = "Enter your annual income"
      value = {income}
      onChange = {setIncome}
      disabled={loading}
      />

      <LoanInput
      label = "Loan Amount"
      placeholder = "Enter required loan amount"
      value = {loanAmount}
      onChange = {setLoanAmount}
      disabled={loading}
      />

      <LoanInput 
      label = "Age"
      placeholder = "Current age"
      value = {age}
      onChange = {setAge}
      disabled={loading}
      />

      <LoanInput
      label = "Employment status"
      placeholder = "Employed years"
      value = {employmentYears}
      onChange = {setEmploymentYears}
      disabled={loading}
    />

    {error && (
      <p 
        style ={{
          color : "red",
          fontWeight : "bold",
          textAlign : "Center"
        }}
      >
        {error}
      </p>
    )}

     <button
          onClick = {handlePredict}
          disabled = {loading}
      >
        { loading ? "Predicting..." : "Predict Risk" }
      </button>

      { prediction && (
        <div className = "prediction-result"
          style= {{
            padding : "20px",
            border : "1px solid #ccc",
            backgroundColor : "#f8f8f8",
            borderRadius : "10px"
          }}
        >

          <h2>Prediction Result</h2>

          <p>
            <strong>Risk score:</strong>{prediction.risk_score}
          </p>

          <p>
            <strong>Decision:</strong>{prediction.decision}
          </p>

          <p>
            <strong>Explanation:</strong>{prediction.explanation}
          </p>
        </div>
      )}
    </>
    </div>
  );
}
export default App
