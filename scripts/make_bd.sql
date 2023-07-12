-- Создание базы данных
CREATE DATABASE analytics;

-- Использование созданной базы данных
\c analytics;

-- Создание таблицы
CREATE TABLE analytic (
    id SERIAL PRIMARY KEY,
    data VARCHAR,
    data_of_check VARCHAR,
    link VARCHAR(255),
    name VARCHAR(100),
    first_month INTEGER,
    percentage_1 FLOAT,
    second_month INTEGER,
    percentage_2 FLOAT,
    third_month INTEGER,
    percentage_3 FLOAT,
    fourth_month INTEGER,
    percentage_4 FLOAT,
    fifth_month INTEGER,
    percentage_5 FLOAT,
    sixth_month INTEGER,
    percentage_6 FLOAT
);