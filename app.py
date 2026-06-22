import streamlit as st
import joblib
import pandas as pd

# Page Config
st.set_page_config(
    page_title="Loan Approval Prediction",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS
st.markdown("""
<style>

#MainMenu {visibility:hidden;}
footer {visibility:hidden;}
header {visibility:hidden;}

[data-testid="stToolbar"]{
display:none;
}

.stApp{
background-color:#f8fafc;
}

.main-title{
font-size:42px;
font-weight:700;
color:#0f172a;
text-align:center;
margin-bottom:5px;
}

.sub-title{
font-size:16px;
color:#64748b;
text-align:center;
margin-bottom:30px;
}

.stButton > button{
width:100%;
height:50px;
border-radius:10px;
background-color:#1e40af;
color:white;
font-size:16px;
font-weight:600;
border:none;
}

.stButton > button:hover{
background-color:#1d4ed8;
color:white;
}

</style>
""", unsafe_allow_html=True)

# Load Model
model = joblib.load("loan_model.pkl")

# Header
st.markdown(
    '<div class="main-title">Loan Approval Prediction System</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="sub-title">Enter applicant information to evaluate loan eligibility</div>',
    unsafe_allow_html=True
)

# Form Layout
col1, col2 = st.columns(2)

with col1:

    gender = st.selectbox(
        "Gender",
        ["Male", "Female"]
    )

    married = st.selectbox(
        "Marital Status",
        ["Yes", "No"]
    )

    dependents = st.selectbox(
        "Dependents",
        [0, 1, 2, 3]
    )

    education = st.selectbox(
        "Education",
        ["Graduate", "Not Graduate"]
    )

    self_employed = st.selectbox(
        "Self Employed",
        ["Yes", "No"]
    )

with col2:

    applicant_income = st.number_input(
        "Applicant Income",
        min_value=0.0
    )

    coapplicant_income = st.number_input(
        "Coapplicant Income",
        min_value=0.0
    )

    loan_amount = st.number_input(
        "Loan Amount",
        min_value=0.0
    )

    loan_term = st.number_input(
        "Loan Amount Term",
        min_value=0.0
    )

    credit_history = st.selectbox(
        "Credit History",
        [0, 1]
    )

    property_area = st.selectbox(
        "Property Area",
        ["Rural", "Semiurban", "Urban"]
    )

# Prediction Button
if st.button("Predict Loan Status"):

    total_income = applicant_income + coapplicant_income

    input_data = pd.DataFrame([{
        "Dependents": dependents,
        "LoanAmount": loan_amount,
        "Loan_Amount_Term": loan_term,
        "Credit_History": credit_history,
        "Total_income": total_income,
        "Gender_Male": 1 if gender == "Male" else 0,
        "Married_Yes": 1 if married == "Yes" else 0,
        "Education_Not Graduate": 1 if education == "Not Graduate" else 0,
        "Self_Employed_Yes": 1 if self_employed == "Yes" else 0,
        "Property_Area_Semiurban": 1 if property_area == "Semiurban" else 0,
        "Property_Area_Urban": 1 if property_area == "Urban" else 0
    }])

    prediction = model.predict(input_data)[0]

    st.markdown("---")

    if prediction == 1:

        st.markdown("""
        <div style="
        background:#ecfdf5;
        padding:20px;
        border-radius:12px;
        border-left:6px solid #16a34a;
        font-size:18px;
        font-weight:600;
        color:#14532d;">
        Loan Status: Approved
        </div>
        """, unsafe_allow_html=True)

    else:

        st.markdown("""
        <div style="
        background:#fef2f2;
        padding:20px;
        border-radius:12px;
        border-left:6px solid #dc2626;
        font-size:18px;
        font-weight:600;
        color:#7f1d1d;">
        Loan Status: Rejected
        </div>
        """, unsafe_allow_html=True)