CREATE OR REPLACE FUNCTION check_url_exists(p_url text)
RETURNS BOOLEAN
AS $$
BEGIN
    RETURN EXISTS(SELECT 1 FROM public."Visited" WHERE url = p_url);
END;
$$ LANGUAGE plpgsql;