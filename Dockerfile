# 1. Start with clean Python container
FROM python:3.9-slim

# 2. Create and cd into /app directory
WORKDIR /app

# 3. Copy requirements.txt from your computer to container's /app folder
COPY requirements.txt .
# Your Computer         Docker Container
# requirements.txt  →   /app/requirements.txt

# 4. Install all packages from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copy your app folder contents to container's /app folder. # Copy everything, not just /app folder
COPY . .    

# 6. Make sure Python can find our app
ENV PYTHONPATH=/app

# 7. Run the FastAPI app using uvicorn
# ${PORT:-8000} means: use the PORT environment variable if it exists, else use 8000
# This makes our app work both locally (8000) and on Render (where PORT is set automatically)
CMD uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}
#   │       │    │       │     │         │     └── Default port if PORT not set
#   │       │    │       │     │         └── Use environment variable PORT
#   │       │    │       │     └── Accept connections from anywhere
#   │       │    │       └── Server settings
#   │       │    └── FastAPI file name and app variable (app = FastAPI(...))
#   │       └── main.py path
#   └── ASGI server 