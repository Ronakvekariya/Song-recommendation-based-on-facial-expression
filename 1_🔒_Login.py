import streamlit as st
import mysql.connector


# Initialize session state variables
if "username" not in st.session_state:
    st.session_state["username"] = ""
if "password" not in st.session_state:
    st.session_state["password"] = ""

user_data = {
    'Ronak': 'Ronak@123',
    'Vraj': 'Vraj@123',
    'Jay': 'Jay@123'
}

st.set_page_config(
    page_title="Song recommendation based on emotion",
    page_icon="👋",
)
db_connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Ronak@@my1122",
    database="emotion_detection_system"
)

# Create a cursor object
cursor = db_connection.cursor()

# Execute a SELECT query
query = "SELECT * FROM login_user"
cursor.execute(query)

# Fetch the results
results = cursor.fetchall()


# Close the cursor and database connection
cursor.close()
db_connection.close()

# st.markdown("<h1 style='text-align: center; color : #CCCCCC; font-family:Montserrat;'>Song Recommendation System Based On facial Expression</h1>", unsafe_allow_html=True)

css = """
<style>
img {
    border: 2px solid #008080; /* Red border */
    border-radius: 5px; /* Rounded corners */
    padding: 5px; /* Padding around the image */
}
</style>
"""

# Display the CSS style
st.markdown(css, unsafe_allow_html=True)

st.image("logo1.png")

css = """
<style>
h1 {
    color: #CCCCCC; /* Red color */
    padding-bottom: 5px; /* Padding below the heading */
    text-align : center;
}
</style>
"""

# Display the CSS style
st.markdown(css, unsafe_allow_html=True)
st.markdown("<h1 >Log In Page</h1>", 
unsafe_allow_html=True)
# st.sidebar.success("Select a page above.")

username = st.text_input("Username")
password = st.text_input("Password" , type='password')
submit = st.button("Login")



if submit:
    flag = 0
    for row in results:
        # Check if the entered password matches the stored password
        if row[0] == username and row[1] == password:
            st.warning('Log In Successfully')
            # st.markdown("<h1 style='text-align: center; color : #fff; font-family:Montserrat;'>Log In Successfully</h1>", unsafe_allow_html=True) 
            st.session_state["username"] = username
            st.session_state["password"] = password
            
            flag = 1
            break
    if flag == 0 :
        st.warning('Incorrect password or username or unregistered')
        # st.markdown("<h1 style='text-align: center; color : #fff; font-family:Montserrat;'>Incorrect password or username or unregistered user</h1>", unsafe_allow_html=True)  
        
