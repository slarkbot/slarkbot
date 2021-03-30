
CREATE DATABASE :db_name;

\c :db_name

CREATE TABLE bot_users (
    user_id SERIAL PRIMARY KEY,
    telegram_handle TEXT NOT NULL,
    account_id BIGINT NOT NULL,
    chat_id BIGINT NOT NULL
);

CREATE TABLE heroes (
    id INT PRIMARY KEY,
    name TEXT NOT NULL,
    localized_name TEXT NOT NULL,
    primary_attr VARCHAR(3),
    roles TEXT[]
);

CREATE TABLE hero_aliases (
    id SERIAL PRIMARY KEY,
    hero_id INT NOT NULL,
    alias TEXT NOT NULL,
    CONSTRAINT fk_hero
        FOREIGN KEY(hero_id)
        REFERENCES heroes(id)
);
