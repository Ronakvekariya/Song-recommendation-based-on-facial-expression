import streamlit as st
import mysql.connector

db_connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Ronak@@my1122",
    database="emotion_detection_system"
    )


cursor = db_connection.cursor()

if st.session_state["username"] != "":
    # Execute a SELECT query
    

    # Close the cursor and database connection
    

    query = "SELECT COUNT(*) FROM song_id WHERE user_password = %s"
    value = (st.session_state["password"],)
    cursor.execute(query , value)

            # Fetch the result
    result = cursor.fetchone()

            # Display the number of rows
    num_rows = result[0]

    if num_rows > 0:
        st.markdown("<h1 style='text-align: center; color : #fff; font-family:Montserrat;'>Your History</h1>", unsafe_allow_html=True)
        query = "SELECT song_id FROM song_id WHERE user_password = %s"
        value = (st.session_state["password"],)
        cursor.execute(query , value )

        # Fetch the results and store them in a list
        result_list = []
        for row in cursor.fetchall():
            result_list.append(row[0])  # Assuming there is only one column in the query result

        unique_list = list(set(result_list))

        col_width = 700
        col_height = 200
        # cols = st.columns(num_rows)
        counter = 0

        for i in unique_list:                                                        
            col = st.columns(1)
            my_html = '<iframe src="https://open.spotify.com/embed/track/{}" width="{}" height="240px" frameborder="0" allowtransparency="true" allow="encrypted-media" style = "border-radius : 0.75rem; "></iframe>'.format(i, col_width, col_height)
            st.markdown(my_html, unsafe_allow_html=True)
            counter = counter + 1
    else : 
        st.markdown("<h1 style='text-align: center; color : #fff; font-family:Montserrat;'>No History</h1><br><h2 style='text-align: center; color : #fff; font-family:Montserrat;'>Use the system for the history</h2>", unsafe_allow_html=True) 
else : 
    st.markdown("<h1 style='text-align: center; color : #fff; font-family:Montserrat;'>Login First</h1>", unsafe_allow_html=True) 

    cursor.close()
    db_connection.close()
