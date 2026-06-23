import streamlit as st
import joblib
import pandas as pd

st.set_page_config(
    page_title="Loan Approval Prediction",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>

#MainMenu {visibility:hidden;}
footer {visibility:hidden;}
header {visibility:hidden;}

[data-testid="stToolbar"]{
display:none;
}

.stApp{
background: linear-gradient(
135deg,
#e0f2fe 0%,
#f8fafc 50%,
#eef4ff 100%
);
}

/* Main Title */
.main-title{
font-size:48px;
font-weight:700;
color:#1e3a8a;
text-align:center;
margin-bottom:5px;
}

/* Subtitle */
.sub-title{
font-size:18px;
color:#475569;
text-align:center;
margin-bottom:35px;
}

/* Section Heading */
.section-title{
font-size:24px;
font-weight:600;
color:#0f172a;
margin-top:20px;
margin-bottom:15px;
padding-bottom:5px;
border-bottom:2px solid #cbd5e1;
}

/* Labels */
label{
font-weight:600 !important;
color:#334155 !important;
}

/* Button */
.stButton > button{
width:100%;
height:55px;
border-radius:12px;
background:#2563eb;
color:white;
font-size:17px;
font-weight:600;
border:none;
}

.stButton > button:hover{
background:#1d4ed8;
color:white;
}

</style>
""", unsafe_allow_html=True)


model = joblib.load("loan_model.pkl")


st.markdown(
    '<div class="main-title">Loan Approval Prediction System</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="sub-title">Enter applicant information to evaluate loan eligibility</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="section-title">Personal Information</div>',
    unsafe_allow_html=True
)

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

with col2:

    education = st.selectbox(
        "Education",
        ["Graduate", "Not Graduate"]
    )

    self_employed = st.selectbox(
        "Self Employed",
        ["Yes", "No"]
    )

st.markdown(
    '<div class="section-title">Financial Information</div>',
    unsafe_allow_html=True
)

col3, col4 = st.columns(2)

with col3:

    applicant_income = st.number_input(
        "Applicant Income",
        min_value=0.0,
        value=0.0
    )

    coapplicant_income = st.number_input(
        "Co-applicant Income",
        min_value=0.0,
        value=0.0
    )

with col4:

    loan_amount = st.number_input(
        "Loan Amount",
        min_value=0.0,
        value=0.0
    )

    loan_term = st.number_input(
        "Loan Amount Term",
        min_value=0.0,
        value=360.0
    )


st.markdown(
    '<div class="section-title">Credit Information</div>',
    unsafe_allow_html=True
)

col5, col6 = st.columns(2)

with col5:

    credit_history = st.selectbox(
        "Credit History",
        [0, 1],
        help="1 = Good Credit History, 0 = Poor Credit History"
    )

with col6:

    property_area = st.selectbox(
        "Property Area",
        ["Rural", "Semiurban", "Urban"]
    )

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

        st.success(
            "Loan Approved - Applicant satisfies the eligibility criteria."
        )

    else:

        st.error(
            "Loan Rejected - Applicant does not satisfy the eligibility criteria."
        )
