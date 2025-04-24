FROM pyheart-base

WORKDIR /app
COPY . /app

RUN poetry install

CMD ["./contrib/scripts/db.sh"]
