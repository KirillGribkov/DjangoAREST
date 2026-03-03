import os

os.system("pip install -r requirements.txt")
os.system("uvicorn personal_site.asgi:application --host 0.0.0.0 --port 8000")
