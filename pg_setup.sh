#!/bin/bash

# Export environmental variables.
set -a
source .env
set +a

# Create the postgresql databases.
psql -d postgres -c "CREATE DATABASE ${DB_NAME};"
psql -d ${DB_NAME} -c "CREATE USER ${DB_USER} WITH PASSWORD '${DB_PASSWORD}';"
