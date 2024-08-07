create database "NewsBot";

CREATE OR REPLACE FUNCTION check_url_exists(p_url text, p_tablename text)
RETURNS BOOLEAN
AS $$
DECLARE
    url_exists BOOLEAN;
BEGIN
    EXECUTE format('SELECT EXISTS(SELECT 1 FROM %I WHERE url = $1)', p_tablename) INTO url_exists USING p_url;
    RETURN url_exists;
END;
$$ LANGUAGE plpgsql;

CREATE TABLE IF NOT EXISTS public."Second_Visited"
(
    id integer NOT NULL GENERATED BY DEFAULT AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1 ),
    url text COLLATE pg_catalog."default",
    CONSTRAINT "Second_Visited_pkey" PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS public."Test"
(
    id integer NOT NULL GENERATED BY DEFAULT AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1 ),
    url text COLLATE pg_catalog."default",
    CONSTRAINT "Test_pkey" PRIMARY KEY (id)
);