import streamlit as st
import mysql.connector



db_connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Ronak@@my1122",
    database="emotion_detection_system"
)


cursor = db_connection.cursor()

# Dictionary to store user information
user_data = {}

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
st.markdown("<h1 >Registration page</h1>", 
unsafe_allow_html=True)


# Text input for username
username = st.text_input('Username')

# Password input for password
password = st.text_input('Password', type='password')

# Button to submit registration
if st.button('Register'):
    if username and password:
        # Store username and password in dictionary
        user_data[username] = password
        

        # Execute a SELECT COUNT(*) query
        query = "SELECT COUNT(*) FROM login_user"
        cursor.execute(query)

            # Fetch the result
        result = cursor.fetchone()

            # Display the number of rows
        num_rows = result[0]
        num_rows = num_rows + 1
            # Execute the query
        query = "INSERT INTO login_user (username, password, id) VALUES (%s, %s, %s)"
        values = (username, password, num_rows)
        cursor.execute(query, values)
            
            # Commit the transaction
        db_connection.commit()
        
        # Set the flag to indicate that the query has been executed
        st.success('Registration successful!')

    else:
        st.warning('Please enter a username and password.')

# # Optional: Display the registered users
# if st.checkbox('Show registered users'):
#     st.write('Registered Users:')
#     for user, pwd in user_data.items():
#         st.write(f'Username: {user}, Password: {pwd}')





# Close the cursor and database connection
cursor.close()
db_connection.close()



