# 1. Start with clean Python container
FROM python:3.9-slim

# 2. Create and cd into /app directory
WORKDIR /app

# 3. Copy requirements.txt first
COPY requirements.txt .

# 4. Create a virtual environment using venv
RUN python -m venv venv

# 5. Activate the virtual environment and install dependencies
RUN . venv/bin/activate && \
    pip install --no-cache-dir -r requirements.txt

# 6. Copy your app folder contents to container's /app folder
COPY . .    

# 7. Make sure Python can find our app
ENV PYTHONPATH=/app

# 8. Set the entry point to use the virtual environment
# This command starts the Uvicorn server to run the FastAPI application.
# It uses the 'uvicorn' executable from the virtual environment 'venv',
# allowing the app to run on all network interfaces (0.0.0.0) and listens
# on the specified PORT (default is 8000 if not set).
CMD ["venv/bin/uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "10000"]
#   │       │    │       │     │         │     └── Default port if PORT not set
#   │       │    │       │     │         └── Use environment variable PORT
#   │       │    │       │     └── Accept connections from anywhere
#   │       │    │       └── Server settings
#   │       │    └── FastAPI file name and app variable (app = FastAPI(...))
#   │       └── main.py path
#   └── ASGI server 