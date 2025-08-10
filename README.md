# 💰 Salary Predictor App

A **Streamlit** web application that predicts salary based on years of experience using trained machine learning models.

---

## 🚀 Project Overview

This application predicts salary based on **years of experience** using machine learning models.  
It provides an intuitive interface with real-time predictions and interactive visualizations.

### ✨ Key Features
- 📊 **Interactive slider** for years of experience input
- ⚡ **Real-time salary prediction**
- 📈 **Salary trend visualization** with Plotly charts
- 📝 **Prediction history** with CSV download option
- 🔄 **Model selection** between Linear Regression & Random Forest

---

## 🛠️ Steps Followed
1. **Data Collection** → Used `Salary_Data.csv`
2. **Data Preprocessing** → Handled missing values, outliers, and feature scaling
3. **Model Training** → Trained Linear Regression & Random Forest
4. **Model Selection** → Chose best model via R² score and saved as `best_salary_model.joblib`
5. **App Development** → Built with Streamlit & Plotly
6. **Deployment** → Hosted on **Streamlit Community Cloud**

---

## 📦 How to Run Locally

### Prerequisites
- Python 3.8+
- Git

### Installation
```bash
# Clone the repository
git clone https://github.com/aqsa-isha/Salary-Prediction-using-Traditional-ML-Techniques.git
cd Salary-Prediction-using-Traditional-ML-Techniques

# Create and activate virtual environment
python -m venv venv
# On Mac/Linux
source venv/bin/activate
# On Windows
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the application
streamlit run app.py


---

## 🌐 Live App
🔗 **Try it here:** [Salary Predictor on Streamlit](https://salary-prediction-using-traditional-ml-techniques-tgzlcuftltxy.streamlit.app/)

---

## 📜 License
This project is licensed under the **MIT License** — feel free to use and modify.
