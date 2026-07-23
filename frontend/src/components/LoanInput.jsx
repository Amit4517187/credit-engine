function LoanInput({
    label,
    placeholder,
    value,
    onChange,
    disabled
}) {
    return  (
        <div style= {{marginBottom: "15px"}}>
             <label>{label}</label>

            <br/>

             <input
             type = "number"
             placeholder = {placeholder}
             value = {value}
             disabled = {disabled}
             onChange={(event) => onChange(event.target.value)}
             />
        </div>
    );
}

export default LoanInput;