import streamlit as st
import mysql.connector

from config import DB_CONFIG


db_connection = mysql.connector.connect(**DB_CONFIG)
cursor = db_connection.cursor()

if st.session_state.get("username"):
    cursor.execute(
        "SELECT COUNT(*) FROM song_id WHERE user_password = %s",
        (st.session_state["password"],),
    )
    result = cursor.fetchone()
    num_rows = result[0]

    if num_rows > 0:
        st.markdown(
            "<h1 style='text-align: center; color: #fff; font-family:Montserrat;'>"
            "Your History</h1>",
            unsafe_allow_html=True,
        )

        cursor.execute(
            "SELECT song_id FROM song_id WHERE user_password = %s",
            (st.session_state["password"],),
        )
        unique_list = list({row[0] for row in cursor.fetchall()})

        for track_id in unique_list:
            my_html = (
                '<iframe src="https://open.spotify.com/embed/track/{}" '
                'width="700" height="240" frameborder="0" '
                'allowtransparency="true" allow="encrypted-media" '
                'style="border-radius: 0.75rem;"></iframe>'
            ).format(track_id)
            st.markdown(my_html, unsafe_allow_html=True)
    else:
        st.markdown(
            "<h1 style='text-align: center; color: #fff; font-family:Montserrat;'>"
            "No History</h1><br>"
            "<h2 style='text-align: center; color: #fff; font-family:Montserrat;'>"
            "Use the system for the history</h2>",
            unsafe_allow_html=True,
        )
else:
    st.markdown(
        "<h1 style='text-align: center; color: #fff; font-family:Montserrat;'>"
        "Login First</h1>",
        unsafe_allow_html=True,
    )

cursor.close()
db_connection.close()
