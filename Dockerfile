FROM python:3.11-slim

# Install PortAudio
RUN apt-get update && apt-get install -y portaudio19-dev

# Set the working directory
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt /app/

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . /app/

# Set the command to run your application
CMD ["python", "your_app.py"]
