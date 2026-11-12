CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TABLE IF NOT EXISTS "publications" (
    "id" uuid NOT NULL DEFAULT uuid_generate_v4(),
    "created_at" timestamp NOT NULL DEFAULT now(),
    "updated_at" timestamp NOT NULL DEFAULT now(),
    "version" bigint NOT NULL DEFAULT 0,
    "topic_id" uuid NOT NULL,
    "name" varchar(255) NOT NULL,
    "status" INTEGER NOT NULL,
    PRIMARY KEY("id")
);

CREATE TABLE IF NOT EXISTS "topics" (
    "id" uuid NOT NULL DEFAULT uuid_generate_v4(),
    "created_at" timestamp NOT NULL DEFAULT now(),
    "updated_at" timestamp NOT NULL DEFAULT now(),
    "version" bigint NOT NULL DEFAULT 0,
    "name" varchar(255) NOT NULL UNIQUE,
    "password_hash" varchar(255) NOT NULL,
    PRIMARY KEY("id")
);