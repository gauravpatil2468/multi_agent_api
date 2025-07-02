
FROM python:3.13.5-slim-bookworm

RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*
# Set the working directory inside the container
WORKDIR /app

# Copy only the requirements file first to leverage Docker caching
# This step will only rerun if requirements.txt changes
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire application code into the container
# The /app directory in the container will now contain your 'app' folder, etc.
COPY . .

# Expose the port that Uvicorn will listen on
# Render will automatically map this to a public port.
EXPOSE 8000

# Command to run your FastAPI application using Uvicorn
# - The 'app' folder is copied to /app, so the entry point is 'app.main:app'
# - --host 0.0.0.0: Binds Uvicorn to all available network interfaces
# - --port 8000: Uvicorn listens on port 8000 (matches EXPOSE)
# - --workers 4: (Optional but recommended for production) Runs multiple Uvicorn worker processes
#                Adjust based on your server's CPU cores.
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "$PORT", "--workers", "4"]