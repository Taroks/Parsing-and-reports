#!/bin/bash

# Установка PostgreSQL с использованием Homebrew
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
brew install postgresql

# Запуск службы PostgreSQL
brew services start postgresql

# Настройка пароля для суперпользователя "postgres"
sudo -u _postgres psql -c "ALTER USER postgres WITH PASSWORD 'Joker171';"

# Изменение метода аутентификации на "md5" в файле pg_hba.conf
sudo sed -i '' 's/peer/md5/g' /usr/local/var/postgres/pg_hba.conf

# Перезапуск службы PostgreSQL для применения изменений
brew services restart postgresql

echo "Установка и настройка PostgreSQL завершена."