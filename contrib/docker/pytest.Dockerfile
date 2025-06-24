FROM pyheart-app

RUN uv sync --frozen

CMD ["./contrib/scripts/db.sh"]
