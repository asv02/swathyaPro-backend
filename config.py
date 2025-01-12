# import os

# class Config:
#     SECRET_KEY = os.urandom(24)
#     SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:admin@localhost:5432/demo'
#     SQLALCHEMY_TRACK_MODIFICATIONS = False

#     # Email Configuration
#     MAIL_SERVER = 'live.smtp.mailtrap.io'
#     MAIL_PORT = 587
#     MAIL_USE_TLS = True
#     MAIL_USERNAME = 'smtp@mailtrap.io'
#     MAIL_PASSWORD = '11730fd06f2816a9c5098c6c85aee85c'

#     # Celery Configuration
#     CELERY_BROKER_URL = 'redis://localhost:6379/0'
#     CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'

# // Import the functions you need from the SDKs you need
# import { initializeApp } from "firebase/app";
# import { getAnalytics } from "firebase/analytics";
# // TODO: Add SDKs for Firebase products that you want to use
# // https://firebase.google.com/docs/web/setup#available-libraries

# // Your web app's Firebase configuration
# // For Firebase JS SDK v7.20.0 and later, measurementId is optional
# const firebaseConfig = {
#   apiKey: "AIzaSyAKkPYu7TL80K453uL4tKY3zBfZ4jWcE9A",
#   authDomain: "swasthyapro-8ce44.firebaseapp.com",
#   projectId: "swasthyapro-8ce44",
#   storageBucket: "swasthyapro-8ce44.firebasestorage.app",
#   messagingSenderId: "12346077731",
#   appId: "1:12346077731:web:f6925ce21c03cc0c477796",
#   measurementId: "G-0LS3Y4LLKK"
# };

# // Initialize Firebase
# const app = initializeApp(firebaseConfig);
# const analytics = getAnalytics(app);