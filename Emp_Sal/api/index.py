import os
from fastapi import FastAPI
from main import app as fastapi_app  # Import your main app

# Expose the app for Vercel
app = fastapi_app
