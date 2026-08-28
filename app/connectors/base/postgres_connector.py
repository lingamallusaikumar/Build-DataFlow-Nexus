from app.connectors.base.connector_interface import BaseConnector
import psycopg2
from psycopg2.extras import RealDictCursor

class PostgresConnector(BaseConnector):
    def connect(self):
        return psycopg2.connect(
            host=self.config.get('host'),
            database=self.config.get('database'),
            user=self.config.get('user'),
            password=self.config.get('password'),
            port=self.config.get('port', 5432)
        )

    def test_connection(self):
        try:
            conn = self.connect()
            conn.close()
            return True
        except Exception:
            return False

    def fetch_data(self, query):
        conn = self.connect()
        try:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(query)
                return cur.fetchall()
        finally:
            conn.close()

    def push_data(self, data):
        pass # Implemented in specific destinations
