# register.py
import streamlit as st
import sqlite3
import hashlib

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def register_user(username, password):
    conn = sqlite3.connect("health.db")
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)",
                       (username, hash_password(password)))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def register_page():
    st.subheader("Create a New Account")
    new_user = st.text_input("Username")
    new_password = st.text_input("Password", type='password')
    if st.button("Register"):
        if register_user(new_user, new_password):
            st.success("You have registered successfully! Please go to Login.")
        else:
            st.error("Username already exists. Try a different one.")
