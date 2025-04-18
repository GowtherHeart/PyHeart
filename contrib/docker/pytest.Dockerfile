# Используем образ из migration.Dockerfile
FROM migration

FROM base-python

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем содержимое из образа base
COPY --from=base-python /app /app

# Устанавливаем зависимости
RUN poetry install


# Копируем содержимое из образа migration
COPY --from=migration /go/bin/goose /usr/local/bin/goose
COPY --from=migration /usr/bin/uuidgen /usr/local/bin/uuidgen
COPY --from=migration /usr/bin/psql /usr/local/bin/psql


# Команда для запуска приложения
CMD ["./contrib/scripts/db.sh"]
