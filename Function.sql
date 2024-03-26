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