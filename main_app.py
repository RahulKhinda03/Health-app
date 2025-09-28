import streamlit as st
import sqlite3
import hashlib
from app import run_diagnostic_app # Importing your diagnostic app

# --- Database Functions for Users ---
def get_user_connection():
    return sqlite3.connect('users.db', check_same_thread=False)

def create_user(username, password):
    conn = get_user_connection()
    cursor = conn.cursor()
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_password))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False # Username already exists
    finally:
        conn.close()

def check_user(username, password):
    conn = get_user_connection()
    cursor = conn.cursor()
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, hashed_password))
    user = cursor.fetchone()
    conn.close()
    return user

def save_measurements(username, age, height, weight, blood_pressure):
    conn = get_user_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET age=?, height=?, weight=?, blood_pressure=? WHERE username=?",
                   (age, height, weight, blood_pressure, username))
    conn.commit()
    conn.close()

# --- Main App Logic ---
st.set_page_config(page_title="Health App Suite", layout="centered")

# Initialize session state variables
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'page' not in st.session_state:
    st.session_state.page = 'Login'
if 'username' not in st.session_state:
    st.session_state.username = ""

def show_login():
    st.title("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        user = check_user(username, password)
        if user:
            st.session_state.logged_in = True
            st.session_state.username = username
            st.session_state.page = 'Measurements'
            st.rerun()
        else:
            st.error("Invalid username or password")
    if st.button("Go to Register"):
        st.session_state.page = 'Register'
        st.rerun()

def show_register():
    st.title("Register")
    new_username = st.text_input("Choose a Username")
    new_password = st.text_input("Choose a Password", type="password")
    if st.button("Register"):
        if create_user(new_username, new_password):
            st.success("Account created successfully! Please login.")
            st.session_state.page = 'Login'
            st.rerun()
        else:
            st.error("Username already exists.")
    if st.button("Back to Login"):
        st.session_state.page = 'Login'
        st.rerun()

def show_measurements():
    st.title(f"Welcome, {st.session_state.username}!")
    st.header("Please Enter Your Physical Measurements")
    with st.form("measurements_form"):
        age = st.number_input("Age", min_value=1, max_value=120)
        height = st.number_input("Height (cm)", min_value=50.0, max_value=250.0, format="%.1f")
        weight = st.number_input("Weight (kg)", min_value=10.0, max_value=300.0, format="%.1f")
        bp = st.text_input("Blood Pressure (e.g., 120/80)")
        
        submitted = st.form_submit_button("Save and Proceed to Diagnosis")
        if submitted:
            # Save measurements to the database
            save_measurements(st.session_state.username, age, height, weight, bp)
            
            # Also save to session_state so the PDF report can use them
            st.session_state.measurements = {
                "age": age,
                "height": height,
                "weight": weight,
                "blood_pressure": bp
            }
            st.session_state.page = 'Diagnosis'
            st.rerun()

# --- Page Router ---
if not st.session_state.logged_in:
    if st.session_state.page == 'Login':
        show_login()
    elif st.session_state.page == 'Register':
        show_register()
else:
    if st.session_state.page == 'Measurements':
        show_measurements()
    elif st.session_state.page == 'Diagnosis':
        run_diagnostic_app() # Run the original app