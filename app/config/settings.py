import os

DATABASE_URL = os.getenv("DATABASE_URL")

SECRET_KEY = os.getenv("SECRET_KEY", "change-me-in-production")
TIME_EXPIRE_ACCESS_TOKEN = int(os.getenv("TIME_EXPIRE_ACCESS_TOKEN", "3600"))
TIME_EXPIRE_REFRESH_TOKEN = int(os.getenv("TIME_EXPIRE_REFRESH_TOKEN", "604800"))
