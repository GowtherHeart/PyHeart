#!/bin/bash

GOOSE_DRIVER=postgres GOOSE_MIGRATION_DIR=./contrib/migrations GOOSE_DBSTRING="postgres://${PG__USERNAME}:${PG__PASSWORD}@${PG__HOST}:${PG__PORT}/${PG__DB}" goose up
