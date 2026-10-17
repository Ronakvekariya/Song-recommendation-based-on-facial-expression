import streamlit as st
import mysql.connector

from config import DB_CONFIG


db_connection = mysql.connector.connect(**DB_CONFIG)
cursor = db_connection.cursor()

css = """
<style>
h1 {
    color: #CCCCCC;
    padding-bottom: 5px;
    text-align: center;
}
</style>
"""
st.markdown(css, unsafe_allow_html=True)
st.markdown("<h1>Registration page</h1>", unsafe_allow_html=True)

username = st.text_input("Username")
password = st.text_input("Password", type="password")

if st.button("Register"):
    if username and password:
        cursor.execute("SELECT COUNT(*) FROM login_user")
        result = cursor.fetchone()
        num_rows = result[0] + 1

        cursor.execute(
            "INSERT INTO login_user (username, password, id) VALUES (%s, %s, %s)",
            (username, password, num_rows),
        )
        db_connection.commit()

        st.success("Registration successful!")
    else:
        st.warning("Please enter a username and password.")

cursor.close()
db_connection.close()
