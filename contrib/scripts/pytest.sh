#!/bin/bash

source container.env

uuid4_hex() {
	uuidgen | tr -d '-' | tr '[:upper:]' '[:lower:]'
}

# Generate a unique database name for testing
MIGRATION_DB_NAME="test_db_$(uuid4_hex)"
echo "Creating database: $MIGRATION_DB_NAME"

# Create the test database
PGPASSWORD=${PG__PASSWORD} psql -h ${PG__HOST} -p ${PG__PORT} -U ${PG__USERNAME} -c "CREATE DATABASE ${MIGRATION_DB_NAME};"
if [ $? -ne 0 ]; then
    echo "Failed to create database ${MIGRATION_DB_NAME}"
    exit 1
fi

# Set the database name for the session
export PG__DB=${MIGRATION_DB_NAME}

# Run migrations
GOOSE_DRIVER=postgres GOOSE_MIGRATION_DIR=./contrib/migrations GOOSE_DBSTRING="postgres://${PG__USERNAME}:${PG__PASSWORD}@${PG__HOST}:${PG__PORT}/${MIGRATION_DB_NAME}" goose up
if [ $? -ne 0 ]; then
    echo "Failed to run migrations on ${MIGRATION_DB_NAME}"
    exit 1
fi

# Run tests
PG__DB=${MIGRATION_DB_NAME} TESTING=true poetry run pytest --disable-pytest-warnings tests/
if [ $? -ne 0 ]; then
    echo "Tests failed"
    # Drop the database even if tests fail
    PGPASSWORD=${PG__PASSWORD} psql -h ${PG__HOST} -p ${PG__PORT} -U ${PG__USERNAME} -c "DROP DATABASE ${MIGRATION_DB_NAME};"
    exit 1
fi

# Drop the test database
PGPASSWORD=${PG__PASSWORD} psql -h ${PG__HOST} -p ${PG__PORT} -U ${PG__USERNAME} -c "DROP DATABASE ${MIGRATION_DB_NAME};"
if [ $? -ne 0 ]; then
    echo "Failed to drop database ${MIGRATION_DB_NAME}"
    exit 1
fi
