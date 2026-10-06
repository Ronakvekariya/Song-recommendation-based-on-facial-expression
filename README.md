# Emotion-Based Song Recommendation

A Streamlit application that uses facial-expression analysis to infer a user's dominant emotion and recommend songs that match the detected mood.

The project combines computer vision, deep learning inference, a recommendation workflow, a relational database, and the Spotify Web API in one interactive application.

## Demo flow

```
Webcam
  ↓
Face detection (Haar Cascade)
  ↓
Emotion analysis (DeepFace)
  ↓
Dominant emotion
  ↓
Mood-specific Spotify playlist
  ↓
Track retrieval + recommendation
  ↓
Streamlit UI + listening history
```

## Features

- User registration and login backed by MySQL.
- Webcam-based face detection.
- Emotion analysis using DeepFace.
- Mood-to-playlist recommendation logic.
- Spotify track retrieval and embedded playback.
- MySQL-based song history.
- Streamlit multipage interface.

## Technology

**Python · Streamlit · OpenCV · DeepFace · MySQL · Spotipy · Spotify Web API · Requests**

## Project structure

```
.
├── 1_🔒_Login.py
├── pages/
│   ├── 2_📝_register.py
│   ├── 3_😊🔍_Emotion Detection.py
│   ├── 4_ 📜_history.py
│   └── 5_🚪_Logout.py
├── config.py
├── .env.example
└── README.md
```

## Local setup

### 1. Clone the repository

```bash
git clone https://github.com/Ronakvekariya/Song-recommendation-based-on-facial-expression.git
cd Song-recommendation-based-on-facial-expression
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it before installing the dependencies.

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure secrets

Copy `.env.example` to `.env` and fill in your local MySQL and Spotify credentials.

**Never commit `.env`.**

### 5. Prepare the database

The application expects a MySQL database named `emotion_detection_system` with the tables used by the login, registration, and history pages. The original project assumes these tables already exist.

### 6. Run Streamlit

```bash
streamlit run 1_🔒_Login.py
```

The application uses the webcam for emotion detection, so it must be run in an environment with camera access.

## Engineering notes

This is an end-to-end prototype built to connect multiple AI and application components rather than a production recommendation service.

Potential next improvements include:

- hashing application user passwords instead of storing plaintext values;
- moving database access into a dedicated service/module;
- adding schema migrations and validation;
- handling Spotify and webcam failures more explicitly;
- adding tests for recommendation and data-access logic;
- separating UI code from inference and recommendation services;
- containerizing the application for reproducible deployment.

## Security

API credentials and database credentials are loaded from environment variables rather than source code.

When deploying your own copy, create new credentials and keep them outside version control.

## Author

**Ronak Vekariya**

[GitHub](https://github.com/Ronakvekariya)
