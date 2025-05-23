# -*- coding: utf-8 -*-
# Commented out IPython magic to ensure Python compatibility.
# %%writefile app.py
import streamlit as st
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
# 
# # Load data
insurance_dataset = pd.read_csv('insurance_dataset.csv')
# 
# # Data processing
insurance_processed = insurance_dataset.copy()
insurance_processed['sex'] = insurance_processed['sex'].map({'male': 0, 'female': 1})
insurance_processed['smoker'] = insurance_processed['smoker'].map({'yes': 1, 'no': 0})
insurance_processed = pd.get_dummies(insurance_processed, columns=['region'], drop_first=True)
# 
# # Train model
X = insurance_processed.drop('charges', axis=1)
y = insurance_processed['charges']
rf = RandomForestRegressor(random_state=42)
rf.fit(X, y)
# 
# # Streamlit UI
st.set_page_config(layout="wide")
st.title("💰 Insurance Cost Analyzer")

with st.form("insurance_form"):
    col1, col2, col3 = st.columns(3)

    with col1:
        age = st.number_input("Age", min_value=18, max_value=70, value=30)
        sex = st.radio("Gender", ["male", "female"])

    with col2:
        bmi = st.number_input("BMI", min_value=10.0, max_value=60.0, value=25.0, step=0.1)
        children = st.number_input("Children", min_value=0, max_value=5, value=0, step=1)

    with col3:
        smoker = st.radio("Smoker", ["no", "yes"])
        region = st.selectbox("Region", ["southwest", "southeast", "northwest", "northeast"])

    submitted = st.form_submit_button("Calculate Premium")

if submitted:
    input_data = {
        'age': age,
        'sex': 0 if sex == 'male' else 1,
        'bmi': bmi,
        'children': children,
        'smoker': 1 if smoker == 'yes' else 0,
        'region_northwest': 1 if region == 'northwest' else 0,
        'region_southeast': 1 if region == 'southeast' else 0,
        'region_southwest': 1 if region == 'southwest' else 0
    }

    prediction = rf.predict(pd.DataFrame([input_data]))[0]
    st.success(f"✅ Estimated Annual Premium: **${prediction:,.2f}**")



