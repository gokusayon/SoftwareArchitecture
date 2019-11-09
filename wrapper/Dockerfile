# Use an official Python runtime as a parent image
FROM python:3.7-slim
#RUN apt-get install python-pip

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

RUN pip install -r requirements.txt

# Make port 8081 available to the world outside this container
#EXPOSE 8081

# Define environment variable
#ENV NAME App

# Run app.py when the container launches
CMD ["python", "wrapper.py"]
