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
