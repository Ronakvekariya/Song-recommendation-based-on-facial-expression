import streamlit as st



col1, = st.columns([1])
with col1:
    if "username" in st.session_state :
        if st.session_state["username"] != "":
            if "username" in st.session_state:
                del st.session_state["username"]

            if "my_input1" in st.session_state:
                del st.session_state["password"]
            st.markdown("<h1 style='text-align: center; color : #fff; font-family:Montserrat;'>You have Succesfully Loged Out</h1>", unsafe_allow_html=True)
        else :
            st.markdown("<h1 style='text-align: center; color : #fff; font-family:Montserrat;'>Login First</h1>", unsafe_allow_html=True)
            
    else : 
        st.markdown("<h1 style='text-align: center; color : #fff; font-family:Montserrat;'>Login First</h1>", unsafe_allow_html=True)


# Optionally, you can also reset the Streamlit state using this experimental feature:
# st.experimental_rerun()


# Clear session state variables

