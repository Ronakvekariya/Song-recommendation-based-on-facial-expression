import streamlit as st


if st.session_state.get("username"):
    st.session_state["username"] = ""
    st.session_state["password"] = ""
    st.success("You have successfully logged out.")
else:
    st.info("Login First")
