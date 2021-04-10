
\c :db_name

DROP TABLE heroes, hero_aliases, items;

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
