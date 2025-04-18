# Use the official Python 3.13 image from the Docker Hub
FROM python:3.13

# Set environment variables
ENV POETRY_VERSION=2.1.2

# Install Poetry
RUN apt-get update && \
    apt-get install -y curl && \
    curl -sSL https://install.python-poetry.org | python3 - && \
    ln -s /root/.local/bin/poetry /usr/local/bin/poetry

# Set the working directory
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# # Install dependencies
# RUN poetry install
#
# # Command to run your application
# CMD ["poetry", "run", "python", "your_script.py"]
#
