import streamlit as st
import joblib
import numpy as np

model = joblib.load('dialogisticprediction.model')

st.title('🩺 DIABETES RISK PREDICTION WEBSITE')

st.markdown("""
<style>
.stApp {
    background-color: #2E7D32;
}
</style>
""", unsafe_allow_html=True)

# Section: Demographics 
st.subheader("👤 Patient Demographics")
col1, col2, col3 = st.columns(3)

age = col1.number_input("Patient Age (years)", min_value=1, max_value=120, step=1)

gender = col2.selectbox("Gender", options=["Female", "Male", "Other"])

smoking_status = col3.selectbox("Smoking Status", options=["Never", "Former", "Current"])

# Section: Lifestyle 
st.subheader("🏃 Lifestyle Factors")
col4, col5, col6 = st.columns(3)

alcohol_consumption_per_week = col4.number_input(
    "Alcohol Consumption (units/week)", min_value=0.0, max_value=50.0, step=0.5
)

physical_activity_minutes_per_week = col5.number_input(
    "Physical Activity (minutes/week)", min_value=0, max_value=900, step=10
)

diet_score = col6.number_input(
    "Diet Score (1–10, higher = healthier)", min_value=1.0, max_value=10.0, step=0.1
)

col7, col8 = st.columns(2)

sleep_hours_per_day = col7.number_input(
    "Sleep Hours per Day", min_value=1.0, max_value=14.0, step=0.5
)

screen_time_hours_per_day = col8.number_input(
    "Screen Time per Day (hours)", min_value=0.0, max_value=20.0, step=0.5
)

# Section: Clinical Measurements
st.subheader("🔬 Clinical Measurements")
col9, col10, col11 = st.columns(3)

bmi = col9.number_input(
    "BMI (kg/m²)", min_value=10.0, max_value=70.0, step=0.1
)

waist_to_hip_ratio = col10.number_input(
    "Waist-to-Hip Ratio", min_value=0.5, max_value=2.0, step=0.01
)

systolic_bp = col11.number_input(
    "Systolic Blood Pressure (mmHg)", min_value=70, max_value=250, step=1
)

col12, col13, col14 = st.columns(3)

diastolic_bp = col12.number_input(
    "Diastolic Blood Pressure (mmHg)", min_value=40, max_value=160, step=1
)

heart_rate = col13.number_input(
    "Resting Heart Rate (bpm)", min_value=30, max_value=200, step=1
)

ldl_cholesterol = col14.number_input(
    "LDL Cholesterol (mg/dL)", min_value=20.0, max_value=400.0, step=1.0
)

col15, col16 = st.columns(2)

cholesterol_total = col15.number_input(
    "Total Cholesterol (mg/dL)", min_value=50.0, max_value=600.0, step=1.0
)

hdl_cholesterol = col16.number_input(
    "HDL Cholesterol (mg/dL)", min_value=10.0, max_value=150.0, step=1.0
)

triglycerides = st.number_input(
    "Triglycerides (mg/dL)", min_value=20.0, max_value=1000.0, step=1.0
)

# Section: Medical History 
st.subheader("🏥 Medical & Family History")
col17, col18, col19 = st.columns(3)

family_history_diabetes = col17.selectbox(
    "Family History of Diabetes?", options=["No", "Yes"]
)

hypertension_history = col18.selectbox(
    "History of Hypertension?", options=["No", "Yes"]
)

cardiovascular_history = col19.selectbox(
    "History of Cardiovascular Disease?", options=["No", "Yes"]
)

#  Encode Categorical Inputs 
gender_encoded = {"Female": 0, "Male": 1, "Other": 2}[gender]
smoking_encoded = {"Current": 0, "Former": 1, "Never": 2}[smoking_status]
family_history_encoded = 1 if family_history_diabetes == "Yes" else 0
hypertension_encoded = 1 if hypertension_history == "Yes" else 0
cardiovascular_encoded = 1 if cardiovascular_history == "Yes" else 0

# Compute Engineered Features 
cholesterol_to_hdl_ratio = cholesterol_total / (hdl_cholesterol + 1e-5)
pulse_pressure = systolic_bp - diastolic_bp
obesity_index = bmi * waist_to_hip_ratio

# Prediction phase
if st.button("🔍 Run Diabetes Risk Diagnosis"):

    input_data = [[
        age,
        alcohol_consumption_per_week,
        physical_activity_minutes_per_week,
        diet_score,
        sleep_hours_per_day,
        screen_time_hours_per_day,
        obesity_index,
        pulse_pressure,
        heart_rate,
        cholesterol_to_hdl_ratio,
        ldl_cholesterol,
        triglycerides,
        gender_encoded,
        smoking_encoded,
        family_history_encoded,
        hypertension_encoded,
        cardiovascular_encoded
    ]]

    prediction = model.predict(input_data)
    probability = model.predict_proba(input_data)[0]

    risk_pct = round(probability[1] * 100, 1)

    if prediction[0] == 1:
        st.warning(
            f"⚠️ **HIGH RISK:** This patient is likely to have diabetes "
            f"(Risk Score: {risk_pct}%). "
            "Please refer the patient for confirmatory blood glucose testing "
            "and initiate appropriate clinical management."
        )
    else:
        st.success(
            f"✅ **LOW RISK:** This patient is unlikely to have diabetes "
            f"(Risk Score: {risk_pct}%). "
            "Patient is advised to maintain a healthy diet, regular physical "
            "activity, and routine annual screening."
        )

#  Footer 
st.markdown("""
<style>
.footer {
    position: fixed;
    left: 0;
    bottom: 0;
    width: 100%;
    background-color: #0E1117;
    color: white;
    text-align: center;
    padding: 10px;
    font-size: 14px;
}
</style>
<div class="footer">
    Website Powered by <strong>LM TECH</strong> 🚀
</div>
""", unsafe_allow_html=True)

#  Watermark 
st.markdown("""
<style>
.watermark {
    position: fixed;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    font-size: 250px;
    opacity: 0.05;
    z-index: 9999;
    pointer-events: none;
    user-select: none;
}
</style>
<div class="watermark">
🩺💉
</div>
""", unsafe_allow_html=True)