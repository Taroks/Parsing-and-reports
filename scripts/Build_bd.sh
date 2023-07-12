#!/bin/bash

# Название вашего SQL-скрипта
SQL_SCRIPT="make_bd.sql"

# Настройки подключения к базе данных PostgreSQL
DB_HOST="localhost"
DB_PORT="5432"
DB_NAME="analytics"
DB_USER="postgres"
DB_PASSWORD="123qweasd"

# Команда для выполнения SQL-скрипта
PGPASSWORD="$DB_PASSWORD" psql -h $DB_HOST -p $DB_PORT -U $DB_USER -w -f $SQL_SCRIPT