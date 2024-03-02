import psycopg2
from psycopg2 import Error
import config

class BDRequests():

    def __init__(self):
        self.connection = psycopg2.connect(
            host=config.HOST,
            database=config.DATABASE,
            user=config.USER,
            password=config.PASSWORD
        )

    def __del__(self):
        self.connection.close()

    def insert_url(self, url):
        cursor = self.connection.cursor()
        insert_query = 'INSERT INTO public."Visited" (url) VALUES (%s);'
        cursor.execute(insert_query, (url,))
        self.connection.commit()

    def clear_database(self):
        cursor = self.connection.cursor()
        delete_query = 'DELETE FROM public."Visited";'
        cursor.execute(delete_query)
        self.connection.commit()

    def check_url_exist(self, url):
        cursor = self.connection.cursor()
        function_call_query = "SELECT check_url_exists(%s);"
        cursor.execute(function_call_query, (url,))
        result = cursor.fetchone()[0]
        return result
