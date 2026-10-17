import streamlit as st
import mysql.connector

from config import DB_CONFIG


if "username" not in st.session_state:
    st.session_state["username"] = ""
if "password" not in st.session_state:
    st.session_state["password"] = ""


st.set_page_config(
    page_title="Song recommendation based on emotion",
    page_icon="👋",
)

db_connection = mysql.connector.connect(**DB_CONFIG)
cursor = db_connection.cursor()
cursor.execute("SELECT * FROM login_user")
results = cursor.fetchall()
cursor.close()
db_connection.close()


css = """
<style>
img {
    border: 2px solid #008080;
    border-radius: 5px;
    padding: 5px;
}
</style>
"""
st.markdown(css, unsafe_allow_html=True)
st.image("logo1.png")

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
st.markdown("<h1>Log In Page</h1>", unsafe_allow_html=True)

username = st.text_input("Username")
password = st.text_input("Password", type="password")
submit = st.button("Login")


if submit:
    authenticated = False

    for row in results:
        if row[0] == username and row[1] == password:
            st.warning("Log In Successfully")
            st.session_state["username"] = username
            st.session_state["password"] = password
            authenticated = True
            break

    if not authenticated:
        st.warning("Incorrect password or username or unregistered user")
