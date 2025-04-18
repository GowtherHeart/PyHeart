#!/bin/bash

source .env
uuid4_hex() {
	uuidgen | tr -d '-' | tr '[:upper:]' '[:lower:]'
}

MIGRATION_DB_NAME="test_db_$(uuid4_hex)"
echo $MIGRATION_DB_NAME


PGPASSWORD=${PG__PASSWORD} psql -h ${PG__HOST} -p ${PG__PORT} -U ${PG__USERNAME}<<EOF
CREATE DATABASE ${MIGRATION_DB_NAME};
EOF

PG__DB=${MIGRATION_DB_NAME}

GOOSE_DRIVER=postgres GOOSE_MIGRATION_DIR=./contrib/migrations GOOSE_DBSTRING="postgres://${PG__USERNAME}:${PG__PASSWORD}@${PG__HOST}:${PG__PORT}/${MIGRATION_DB_NAME}" goose up


PG__DB=${MIGRATION_DB_NAME} TESTING=true pytest --disable-pytest-warnings tests/


PGPASSWORD=${PG__PASSWORD} psql -h ${PG__HOST} -p ${PG__PORT} -U ${PG__USERNAME}<<EOF
DROP DATABASE ${MIGRATION_DB_NAME};
EOF
