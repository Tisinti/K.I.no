# Use an official Python runtime as a parent image
# Matplotlib version requires 3.9 or else error will be thrown ("..rc1 requires Python '>=3.9'..")
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Create a virtual environment
RUN python -m venv venv

# If using project only, not dev: Activate the virtual environment and install dependencies from requirements.lock
# RUN pip install -r requirements.lock

# If working on project: Activate the virtual environment and install dev dependencies from requirements-dev.lock
RUN pip install -r requirements-dev.lock

# Make port 80 available to the world outside this container
EXPOSE 80

# Activate the virtual environment and run main.py when the container launches
CMD ["python", "main.py"]
