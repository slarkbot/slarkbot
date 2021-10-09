
CREATE DATABASE :db_name;

\c :db_name

CREATE TABLE bot_users (
    user_id SERIAL PRIMARY KEY,
    telegram_handle TEXT NOT NULL UNIQUE,
    account_id BIGINT NOT NULL,
    chat_id BIGINT NOT NULL,
    updated_at TIMESTAMP NOT NULL
);

CREATE TABLE heroes (
    id INT PRIMARY KEY UNIQUE,
    name TEXT NOT NULL UNIQUE,
    localized_name TEXT NOT NULL UNIQUE,
    primary_attr VARCHAR(3),
    roles TEXT[]
);

CREATE TABLE hero_aliases (
    id SERIAL PRIMARY KEY UNIQUE,
    hero_id INT NOT NULL,
    alias TEXT NOT NULL UNIQUE,
    CONSTRAINT fk_hero
        FOREIGN KEY(hero_id)
        REFERENCES heroes(id)
);

CREATE TABLE items (
    id INT PRIMARY KEY,
    item_name TEXT UNIQUE
);
