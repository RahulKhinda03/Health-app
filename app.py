import streamlit as st
import pickle
import sqlite3
import pandas as pd
from textblob import TextBlob
from fpdf import FPDF

# --- (All your other functions like analyze_sentiment, load_model, etc. remain the same) ---
def analyze_sentiment(text):
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity
    if polarity < -0.2:
        sentiment = "Negative"
    elif polarity > 0.2:
        sentiment = "Positive"
    else:
        sentiment = "Neutral"
    return sentiment, polarity

def load_model():
    try:
        with open("model.pkl", "rb") as model_file:
            model = pickle.load(model_file)
        with open("vectorizer.pkl", "rb") as vec_file:
            vectorizer = pickle.load(vec_file)
        return model, vectorizer
    except FileNotFoundError:
        return None, None

def get_connection():
    return sqlite3.connect("health.db", check_same_thread=False)

def get_advice(disease):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT advice FROM health_data WHERE disease=?", (disease,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else "No advice available."
# --- End of other functions ---


# -------------------------------
# CORRECTED PDF Report Function
# -------------------------------
def create_pdf_report(report_data):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', size=24)
    pdf.cell(0, 10, txt="Health Diagnosis Report", ln=True, align='C')
    pdf.ln(10)

    pdf.set_font("Arial", size=12)
    pdf.cell(0, 10, txt=f"Date: {pd.Timestamp.now().strftime('%Y-%m-%d')}", ln=True)
    pdf.ln(5)

    for key, value in report_data.items():
        pdf.set_font("Arial", 'B', size=14)
        pdf.cell(0, 10, txt=f"{key}:", ln=True)
        pdf.set_font("Arial", size=12)
        # Using .encode() here to handle potential special characters in user input
        pdf.multi_cell(0, 10, txt=str(value).encode('latin-1', 'replace').decode('latin-1'))
        pdf.ln(5)
    
    # CORRECTED LINE: Convert the output to 'bytes' to ensure compatibility
    return bytes(pdf.output())

# --- (The rest of your run_diagnostic_app function remains the same) ---
def run_diagnostic_app():
    model, vectorizer = load_model()
    st.title("🩺 Health Diagnostics Chatbot")
    user_input = st.text_input("Your symptoms:", placeholder="Describe how you're feeling...")

    if st.button("Diagnose"):
        if not user_input.strip():
            st.warning("⚠️ Please enter your symptoms.")
        else:
            st.session_state['user_symptoms'] = user_input
            sentiment, polarity = analyze_sentiment(user_input)
            st.session_state['sentiment'] = sentiment
            st.session_state['polarity'] = polarity
            
            try:
                X_test = vectorizer.transform([user_input])
                prediction = model.predict(X_test)[0]
                health_advice = get_advice(prediction)
                st.session_state['prediction'] = prediction
                st.session_state['advice'] = health_advice
            except Exception as e:
                st.error(f"An error occurred during diagnosis: {e}")
                for key in ['prediction', 'sentiment', 'polarity', 'advice']:
                    if key in st.session_state:
                        del st.session_state[key]
    
    if 'prediction' in st.session_state:
        st.markdown("---")
        
        sentiment = st.session_state['sentiment']
        polarity = st.session_state['polarity']
        if sentiment == "Negative":
            st.warning(f"Sentiment Analysis: Detected **{sentiment}** sentiment (Score: {polarity:.2f}) 😟")
            st.error("❗ Your description seems to indicate distress. Please consider seeking immediate medical attention if you feel it's an emergency.")
        elif sentiment == "Positive":
            st.success(f"Sentiment Analysis: Detected **{sentiment}** sentiment (Score: {polarity:.2f}) 😊")
        else: # Neutral
            st.info(f"Sentiment Analysis: Detected **{sentiment}** sentiment (Score: {polarity:.2f}) 🙂")
        
        st.markdown("---")
        
        st.success(f"🔎 **Predicted Condition:** {st.session_state['prediction']}")
        st.info(f"💡 **Suggested Advice:** {st.session_state['advice']}")
        
        st.markdown("---")

        st.subheader("📄 Download Your Report")
        report_data = {
            "Patient": st.session_state.get('username', 'N/A'),
            "Age": st.session_state.measurements.get('age', 'N/A'),
            "Height (cm)": st.session_state.measurements.get('height', 'N/A'),
            "Weight (kg)": st.session_state.measurements.get('weight', 'N/A'),
            "Blood Pressure": st.session_state.measurements.get('blood_pressure', 'N/A'),
            "Reported Symptoms": st.session_state.user_symptoms,
            "Detected Sentiment": f"{sentiment} (Score: {polarity:.2f})",
            "AI Predicted Condition": st.session_state.prediction,
            "Suggested Advice": st.session_state.advice
        }
        pdf_bytes = create_pdf_report(report_data)
        
        st.download_button(
            label="Download Health Report (PDF)",
            data=pdf_bytes,
            file_name=f"health_report_{st.session_state.get('username', 'user')}.pdf",
            mime="application/pdf"
        )