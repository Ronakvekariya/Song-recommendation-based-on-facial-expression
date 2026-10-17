import streamlit as st
import requests
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

from config import DB_CONFIG, SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET


client_credentials_manager = SpotifyClientCredentials(
    client_id=SPOTIFY_CLIENT_ID,
    client_secret=SPOTIFY_CLIENT_SECRET,
)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)


def get_track_ids(playlist_id):
    # Get a token using the configured Spotify client credentials
    auth_url = "https://accounts.spotify.com/api/token"
    auth_response = requests.post(
        auth_url,
        {
            "grant_type": "client_credentials",
            "client_id": SPOTIFY_CLIENT_ID,
            "client_secret": SPOTIFY_CLIENT_SECRET,
        },
    )
    auth_response_data = auth_response.json()
    access_token = auth_response_data["access_token"]

    playlist_url = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"
    playlist_response = requests.get(
        playlist_url,
        headers={"Authorization": f"Bearer {access_token}"},
    )
    playlist_data = playlist_response.json()

    return [item["track"]["id"] for item in playlist_data["items"]]


def get_track_data(track_id):
    meta = sp.track(track_id)

    track_details = {
        "name": meta["name"],
        "album": meta["album"]["name"],
        "artist": meta["album"]["artists"][0]["name"],
        "release_date": meta["album"]["release_date"],
        "duration_in_mins": round((meta["duration_ms"] * 0.001) / 60, 2),
    }
    return track_details


def emotion_detection():
    face_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
    )

    video = cv2.VideoCapture(0, cv2.CAP_DSHOW)

    if not video.isOpened():
        raise IOError("Cannot open webcam")

    emo_list = []

    while video.isOpened():
        _, frame = video.read()

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        face = face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
        )

        for x, y, w, h in face:
            image = cv2.rectangle(
                frame,
                (x, y),
                (x + w, y + h),
                (89, 2, 236),
                1,
            )
            try:
                analyze = DeepFace.analyze(frame, actions=["emotion"])
                for face1 in analyze:
                    emo_list.append(face1["dominant_emotion"])
                    cv2.putText(
                        image,
                        str(face1["dominant_emotion"]),
                        (x, y),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1,
                        (224, 77, 176),
                        2,
                    )
            except Exception as error:
                print(error)

        cv2.imshow("video", frame)
        key = cv2.waitKey(1)
        if key == ord("q"):
            break

    result_list = emo_list[-10:]
    print(result_list)

    if not result_list:
        video.release()
        cv2.destroyAllWindows()
        raise RuntimeError("No emotion was detected.")

    counts = Counter(result_list)
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
    else:
        results = "4pUX3ojKN2OxXP7I4Lu9ij"

    track_ids = get_track_ids(results)

    index = []
    num_song = len(track_ids)
    for _ in range(min(6, num_song)):
        index.append(random.randrange(num_song))

    counter = 0
    col_width = 700
    col_height = 200

    db_connection = mysql.connector.connect(**DB_CONFIG)
    cursor = db_connection.cursor()

    user_password = st.session_state["password"]

    for _ in range(3):
        for _ in range(2):
            if counter >= len(track_ids):
                break

            cursor.execute("SELECT COUNT(*) FROM song_id")
            result = cursor.fetchone()
            num_rows = result[0] + 1

            cursor.execute(
                "INSERT INTO song_id (id, song_id, user_password) VALUES (%s, %s, %s)",
                (num_rows, track_ids[counter], user_password),
            )
            db_connection.commit()

            my_html = (
                '<iframe src="https://open.spotify.com/embed/track/{}" '
                'width="{}" height="240px" frameborder="0" '
                'allowtransparency="true" allow="encrypted-media" '
                'style="border-radius: 0.75rem;"></iframe>'
            ).format(track_ids[counter], col_width, col_height)
            st.markdown(my_html, unsafe_allow_html=True)
            counter += 1

    cursor.close()
    db_connection.close()


def main():
    if st.session_state["username"] != "":
        username = st.session_state["username"]
        st.markdown(
            f"<h1 style='text-align: center; color: #fff; font-family:Montserrat;'>"
            f"Hello, {username}!</h1>",
            unsafe_allow_html=True,
        )

        st.markdown(
            "<h1 style='text-align: center; color: #fff; font-family:Montserrat;'>"
            "Emotion Detection</h1>",
            unsafe_allow_html=True,
        )
        st.image("background.png")

        if st.button("Emotion Detection"):
            mood = emotion_detection()
            st.write("Emotion detected successfully")
            recommend_music(mood)
    else:
        st.markdown(
            "<h1 style='text-align: center; color: #fff; font-family:Montserrat;'>"
            "Login First</h1>",
            unsafe_allow_html=True,
        )


if __name__ == "__main__":
    main()
