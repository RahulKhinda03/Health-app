# login.py
import streamlit as st
import sqlite3
import hashlib

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def validate_login(username, password):
    conn = sqlite3.connect("health.db")
    cursor = conn.cursor()
    cursor.execute("SELECT password FROM users WHERE username=?", (username,))
    data = cursor.fetchone()
    conn.close()
    if data and data[0] == hash_password(password):
        return True
    return False

def login_page():
    st.subheader("Login to your account")
    username = st.text_input("Username")
    password = st.text_input("Password", type='password')
    if st.button("Login"):
        if validate_login(username, password):
            st.session_state.logged_in = True
            st.session_state.username = username
            st.success(f"Welcome {username}!")
        else:
            st.error("Invalid username or password")
