import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import os
import joblib
import time
from streamlit_lottie import st_lottie
import requests

# Load Lottie animation
def load_lottie_url(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

# Set page config
st.set_page_config(
    page_title="Salary Predictor",
    page_icon="💰",
    layout="centered"
)

# Load model
@st.cache_resource
def load_model():
    try:
        return joblib.load("best_salary_model.joblib")
    except Exception as e:
        st.error(f"Model load error: {str(e)}")
        return None

model = load_model()

# Session state
if 'predictions_log' not in st.session_state:
    st.session_state.predictions_log = []

# Inject custom CSS for styling and animations
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
    * {
        font-family: 'Inter', sans-serif;
    }
    .stApp {
        max-width: 1200px;
        margin: 0 auto;
        padding: 2rem 1rem;
    }
    .header-container {
        text-align: center;
        margin-bottom: 2.5rem;
    }
    .header-container h1 {
        font-size: 2.5rem;
        margin-bottom: 0.5rem;
    }
    .header-container p {
        font-size: 1.1rem;
        color: #718096;
        max-width: 600px;
        margin: auto;
    }
    .prediction-card {
        background: linear-gradient(135deg, #4299e1, #3182ce);
        border-radius: 12px;
        padding: 2rem;
        text-align: center;
        color: white;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin: 1.5rem 0;
    }
    .prediction-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 15px rgba(0, 0, 0, 0.1);
    }
    .stButton > button {
        background: linear-gradient(135deg, #4299e1, #3182ce);
        color: white !important;
        border: none;
        border-radius: 8px;
        padding: 0.75rem 1.5rem;
        font-weight: 600;
        width: 100%;
        font-size: 1rem;
    }
    .stButton > button:active {
        transform: scale(0.97);
        transition: all 0.1s ease;
    }
    .stButton > button:hover {
        background: linear-gradient(135deg, #3182ce, #2c5282);
    }
    .section-title {
        color: #2d3748;
        font-weight: 600;
        font-size: 1.25rem;
        margin-bottom: 1rem;
        position: relative;
        display: inline-block;
    }
    .section-title::after {
        content: "";
        position: absolute;
        bottom: -5px;
        left: 0;
        width: 40px;
        height: 3px;
        background: linear-gradient(to right, #4299e1, #3182ce);
        border-radius: 3px;
    }
    .dataframe {
        border-radius: 8px;
        overflow: hidden;
    }
    .stDownloadButton {
        background: linear-gradient(135deg, #4299e1, #3182ce) !important;
        color: white !important;
        border-radius: 8px;
        padding: 0.75rem 1.5rem !important;
        font-weight: 600;
        margin-top: 1.5rem;
        font-size: 1rem;
    }
    .footer {
        text-align: center;
        margin-top: 3rem;
        padding: 1.5rem;
        background-color: #f7fafc;
        border-radius: 12px;
        color: #2d3748; /* Added for light mode */
    }
    
    /* Dark mode fixes */
    @media (prefers-color-scheme: dark) {
        .footer {
            background-color: #2d3748;
            color: #e2e8f0; /* Light color for dark mode */
        }
        .section-title {
            color: #e2e8f0;
        }
        .section-title::after {
            background: linear-gradient(to right, #63b3ed, #4299e1);
        }
    }
    
    /* Animations */
    .fade-in {
        animation: fadeIn ease 1.5s;
    }
    .bounce-in {
        animation: bounceIn 0.8s ease;
    }
    .pulse {
        animation: pulse 2s infinite;
    }
    .float {
        animation: float 3s ease-in-out infinite;
    }
    @keyframes fadeIn {
        0% { opacity: 0; transform: translateY(20px); }
        100% { opacity: 1; transform: translateY(0); }
    }
    @keyframes bounceIn {
        0% { opacity: 0; transform: scale(0.3); }
        50% { opacity: 1; transform: scale(1.05); }
        70% { transform: scale(0.9); }
        100% { transform: scale(1); }
    }
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.05); }
        100% { transform: scale(1); }
    }
    @keyframes float {
        0% { transform: translateY(0px); }
        50% { transform: translateY(-10px); }
        100% { transform: translateY(0px); }
    }
    /* Remove blue outlines */
    *:focus {
        outline: none !important;
        box-shadow: none !important;
    }
</style>
""", unsafe_allow_html=True)

# Header + Lottie
st.markdown("""
<div class="header-container fade-in">
    <h1>💼 Salary Prediction App</h1>
    <p>Predict your salary based on years of experience using advanced machine learning models</p>
</div>
""", unsafe_allow_html=True)

lottie_header = load_lottie_url("https://assets10.lottiefiles.com/packages/lf20_cgfdhxgx.json")
if lottie_header:
    st_lottie(lottie_header, height=180, key="header_anim")

# Input
col1, col2 = st.columns([1, 2])
with col1:
    st.markdown("<h3 class='section-title fade-in'>📊 Enter Experience</h3>", unsafe_allow_html=True)
    experience = st.slider("Years of Experience", 0.0, 20.0, 5.0, 0.5)
    if st.button("🔮 Predict Salary"):
        if model is not None:
            input_data = np.array([[experience]])
            with st.spinner("Calculating salary prediction..."):
                prediction = model.predict(input_data)[0]
                time.sleep(1)
            st.session_state.prediction = prediction
            st.session_state.predictions_log.append({
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "experience": experience,
                "prediction": prediction
            })
            log_df = pd.DataFrame(st.session_state.predictions_log)
            os.makedirs("logs", exist_ok=True)
            log_df.to_csv("logs/predictions_log.csv", index=False)
            
            # Lottie success animation
            lottie_success = load_lottie_url("https://assets2.lottiefiles.com/packages/lf20_mkcnmyyj.json")
            if lottie_success:
                st_lottie(lottie_success, height=120, key="success_anim")
            st.success("Prediction complete! 🎉")
        else:
            st.error("Model could not be loaded. ⚠️")

with col2:
    st.markdown("<h3 class='section-title fade-in'>💰 Predicted Salary</h3>", unsafe_allow_html=True)
    if 'prediction' in st.session_state:
        st.markdown(f"""
        <div class="prediction-card bounce-in">
            <div style="font-size: 2rem; margin-bottom: 1rem; animation: float 3s ease-in-out infinite;">💰</div>
            <h3>Predicted Salary</h3>
            <p style="font-size: 2.5rem; font-weight: bold;">Rs. {st.session_state.prediction:,.2f}</p>
            <p>for {experience} years of experience</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="prediction-card" style="background: linear-gradient(135deg, #718096, #4a5568);">
            <div style="font-size: 2rem; margin-bottom: 1rem;">💰</div>
            <h3>Predicted Salary</h3>
            <p style="font-size: 2.5rem; font-weight: bold;">Rs. 0.00</p>
            <p>Enter experience to predict</p>
        </div>
        """, unsafe_allow_html=True)

# Visualization
st.markdown("<h3 class='section-title fade-in'>📈 Salary Trend Visualization</h3>", unsafe_allow_html=True)

# Add chart animation
lottie_chart = load_lottie_url("https://assets9.lottiefiles.com/packages/lf20_1pxqjqps.json")
if lottie_chart:
    st_lottie(lottie_chart, height=150, key="chart_anim")

exp_range = np.linspace(0, 20, 100)
salaries = [model.predict([[exp]])[0] if model else 0 for exp in exp_range]
viz_df = pd.DataFrame({
    'YearsExperience': exp_range,
    'PredictedSalary': salaries
})

fig = px.line(
    viz_df,
    x='YearsExperience',
    y='PredictedSalary',
    title='Salary vs Experience',
    labels={'YearsExperience': 'Years of Experience', 'PredictedSalary': 'Predicted Salary (Rs.)'},
    line_shape="spline",
    color_discrete_sequence=['#4299e1']
)

if 'prediction' in st.session_state:
    fig.add_trace(
        go.Scatter(
            x=[experience],
            y=[st.session_state.prediction],
            mode='markers+text',
            marker=dict(size=12, color='#e53e3e'),
            name='Your Prediction',
            text=["📍"],
            textposition="top center"
        )
    )

fig.update_layout(
    hovermode='x unified',
    font=dict(family="Inter", size=12),
    title_font=dict(family="Inter", size=16)
)

st.plotly_chart(fig, use_container_width=True)

# History
st.markdown("<h3 class='section-title fade-in'>📋 Prediction History</h3>", unsafe_allow_html=True)

# Add history animation
lottie_history = load_lottie_url("https://assets5.lottiefiles.com/packages/lf20_DMgKk1.json")
if lottie_history:
    st_lottie(lottie_history, height=150, key="history_anim")

if st.session_state.predictions_log:
    log_df = pd.DataFrame(st.session_state.predictions_log)
    log_df['prediction'] = log_df['prediction'].map('Rs. {:,.2f}'.format)
    st.dataframe(log_df, use_container_width=True)
    csv = log_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download Prediction History",
        data=csv,
        file_name='salary_predictions_log.csv',
        mime='text/csv',
        key='download_csv'
    )
else:
    st.info("No predictions yet. Try using the slider to predict salary. 🤔")

# Footer with animations
st.markdown("""
<div class="footer fade-in">
    <p>© 2025 Salary Predictor | Built by Aqsa using Streamlit</p> 
    <p style="margin-top: 0.5rem; font-size: 0.9rem;">
        <span class="pulse">💻</span> Machine Learning 
        <span style="margin: 0 0.5rem;">•</span> 
        <span class="pulse">📊</span> Data Visualization 
        <span style="margin: 0 0.5rem;">•</span> 
        <span class="pulse">🚀</span> Modern UI
    </p>
</div>
""", unsafe_allow_html=True)