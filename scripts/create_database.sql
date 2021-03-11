
CREATE DATABASE :db_name;

\c :db_name

CREATE TABLE bot_users (
    user_id serial primary key,
    telegram_handle TEXT NOT NULL,
    account_id BIGINT NOT NULL,
    chat_id BIGINT NOT NULL
);