# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /code

# Copy the requirements file into the container
COPY ./requirements.txt /code/requirements.txt

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# Copy the rest of your app's source code from your host to your image filesystem.
COPY . /code/

# Tell Docker that the container listens on port 7860
EXPOSE 7860

# Command to run the app. We use port 7860 as it's standard for Hugging Face Spaces.
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "7860"]