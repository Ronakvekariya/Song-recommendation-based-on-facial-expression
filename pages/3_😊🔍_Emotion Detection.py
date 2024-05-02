import streamlit as st
import requests
import subprocess
from PIL import Image
from numpy import asarray
import cv2
from deepface import DeepFace
from collections import Counter
from spotipy.oauth2 import SpotifyClientCredentials
import json
import time
import spotipy
import random
import streamlit.components.v1 as components
import mysql.connector

client_id = 'a7e4097b60864b178167f9c287af7f4a'
client_secret = 'f7e3954dbb4c4baba871a42a73e8b953'

client_credentials_manager = SpotifyClientCredentials(client_id, client_secret)
sp = spotipy.Spotify(client_credentials_manager =client_credentials_manager)


def get_track_ids(playlist_id):
    # music_id_list = []
    # playlist = sp.playlist(playlist_id)

    # for item in playlist['tracks']['items']:
    #     music_track = item['track']
    #     music_id_list.append(music_track['id'])
    # return music_id_list


    # Define your Spotify API credentials

    # Get a token using your client ID and client secret
    auth_url = 'https://accounts.spotify.com/api/token'
    auth_response = requests.post(auth_url, {
        'grant_type': 'client_credentials',
        'client_id': client_id,
        'client_secret': client_secret,
    })
    auth_response_data = auth_response.json()
    access_token = auth_response_data['access_token']

    # Use the token to get the playlist tracks
    playlist_url = f'https://api.spotify.com/v1/playlists/{playlist_id}/tracks'
    playlist_response = requests.get(
        playlist_url,
        headers={
            'Authorization': 'Bearer {token}'.format(token=access_token)
        }
    )
    playlist_data = playlist_response.json()

    # Extract track IDs from the playlist data
    track_ids = [item['track']['id'] for item in playlist_data['items']]
    # print(track_ids)
    return track_ids







def get_track_data(track_id):
    meta = sp.track(track_id)

    track_details = {'name':meta['name'], 'album':meta['album']['name'], 
                        'artist':meta['album']['artists'][0]['name'], 'release_date': meta['album']['release_date'],
                        'duration_in_mins':round((meta['duration_ms']*0.001)/60, 2)}
    return track_details





def emotion_detection():
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

    video = cv2.VideoCapture(0, cv2.CAP_DSHOW)

    if not video.isOpened():
        raise IOError("Cannot open webcam")
    
    emoList = []

    while video.isOpened():
        _, frame = video.read()

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        face = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

        for x, y, w, h in face:
            image = cv2.rectangle(frame, (x, y), (x + w, y + h), (89, 2, 236), 1)
            try:
                analyze = DeepFace.analyze(frame, actions=['emotion'])
                for face1 in analyze:
                    # print(face1['dominant_emotion'])
                    emoList.append(face1['dominant_emotion'])
                    
                    cv2.putText(image, str(face1['dominant_emotion']), (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1, (224, 77, 176), 2)
            except Exception as error:
                print(error)

        cv2.imshow('video', frame)
        key = cv2.waitKey(1)
        if key == ord('q'):
            break

    ResultList = emoList[-10:]
    print(ResultList)
    counts = Counter(ResultList)
    max_element = max(counts, key=counts.get)
    st.write("Element repeating the most:", max_element)
    video.release()
    cv2.destroyAllWindows()
    return max_element
     




def recommend_music(mood):
    if mood == "happy":
        results = "0jrlHA5UmxRxJjoykf7qRY"
    elif mood == "sad":
        results = "41sfGuPPtIZHGPMyHN6y2G"
    elif mood == "suprise":
        results = "2WWTTAMQSmAa8gJy10K38a"
    elif mood == "angry":
        results = "0a4Hr64HWlxekayZ8wnWqx"
    elif mood == "neutral":
        results = "4PFwZ4h1LMAOwdwXqvSYHd"
    else :
        results = "4pUX3ojKN2OxXP7I4Lu9ij"

    track_ids = get_track_ids(results) 

    index = []
    num_song = len(track_ids)
    # st.title(num_song)

    for i in range(6):
                index.append(random.randrange(num_song))


    Counter = 0
    col_width = 700
    col_height = 200

    db_connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Ronak@@my1122",
    database="emotion_detection_system"
    )


    cursor = db_connection.cursor()

    user_password = st.session_state["password"]


    for j in range(3):
        for i in range(2):
                    
                    query = "SELECT COUNT(*) FROM song_id"
                    cursor.execute(query)

                        # Fetch the result
                    result = cursor.fetchone()

                        # Display the number of rows
                    num_rows = result[0]
                    num_rows = num_rows + 1
                        # Execute the query
                    query = "INSERT INTO song_id (id, song_id , user_password) VALUES (%s, %s,%s)"
                    values = (num_rows, track_ids[Counter] , user_password)
                    cursor.execute(query, values )
                        
                        # Commit the transaction
                    db_connection.commit()
                    
                    cols = st.columns(1)

                    my_html = '<iframe src="https://open.spotify.com/embed/track/{}" width="{}" height="240px" frameborder="0" allowtransparency="true" allow="encrypted-media" style = "border-radius : 0.75rem; "></iframe>'.format(track_ids[Counter], col_width, col_height)
                    st.markdown(my_html, unsafe_allow_html=True)
                    Counter = Counter + 1
                



def main():
    if st.session_state["username"] != "":
        col1, = st.columns([1])
        with col1:
            username = st.session_state["username"]
            str = f"<h1  style='text-align: center; color : #fff; font-family:Montserrat;'>Hello, {username}!</h1>"
            st.markdown(str , unsafe_allow_html=True )
            

        col1, = st.columns([1])
        flag = 0

        with col1:
            st.markdown("<h1 style='text-align: center; color : #fff; font-family:Montserrat;'>Emotion Detection</h1>", unsafe_allow_html=True)   
        st.image("D://Ronak//SE_PROJECT//Emotion_Detection_Python-master//background.png")
        col1, col2, col3, col4, col5 = st.columns(5)

        # Leave the first two columns empty
        with col1:
            pass

        with col2:
            pass

        # Place the button in the center column
        with col3:       
            if st.button("Emotion Detection"):    
                flag = 1
            
        # Leave the last two columns empty
        with col4:
            pass

        with col5:
            pass

        if flag == 1:
            mood = emotion_detection()
            st.write("emotion detected succesfully")
            recommend_music(mood)
    else :
         st.markdown("<h1 style='text-align: center; color : #fff; font-family:Montserrat;'>Login First</h1>", unsafe_allow_html=True) 


        

if __name__ == "__main__":
    main()
