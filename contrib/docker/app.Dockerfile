FROM pyheart-base

WORKDIR /app
COPY . /app

RUN poetry install --only main

CMD ["poetry", "run", "python", "main.py"]
