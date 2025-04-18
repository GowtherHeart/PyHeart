FROM base-python

RUN poetry install

CMD ["poetry", "run", "python", "main.py"]
