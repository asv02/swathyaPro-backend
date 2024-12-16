import os

class Config:
    MAIL_SERVER = 'smtp.gmail.com'  # or your mail server
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.getenv("MAIL_USERNAME", "your-email@example.com")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD", "your-email-password")
    CELERY_BROKER_URL = "redis://localhost:6379/0"
    CELERY_RESULT_BACKEND = "redis://localhost:6379/0"
