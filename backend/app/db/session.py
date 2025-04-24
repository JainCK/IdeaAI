import asyncio
import psycopg2
from psycopg2.extras import RealDictCursor
from supabase import create_client, Client

from app.core.config import settings

class DBSession:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DBSession, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance
    
    def _initialize(self):
        self._pg_conn = None
        self._supabase_client = None
    
    def get_postgres_connection(self):
        if self._pg_conn is None or self._pg_conn.closed:
            self._pg_conn = psycopg2.connect(settings.NEON_DB_URL, cursor_factory=RealDictCursor)
        return self._pg_conn
    
    def get_supabase_client(self) -> Client:
        if self._supabase_client is None:
            self._supabase_client = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)
        return self._supabase_client
    
    def close(self):
        if self._pg_conn and not self._pg_conn.closed:
            self._pg_conn.close()
            self._pg_conn = None

async def initialize_db():
    """Initialize database tables and extensions."""
    db_session = DBSession()
    conn = db_session.get_postgres_connection()
    cursor = conn.cursor()
    
    # Create PostgreSQL tables if they don't exist
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS ideas (
        id SERIAL PRIMARY KEY,
        title TEXT NOT NULL,
        description TEXT NOT NULL,
        topic TEXT NOT NULL,
        keywords TEXT[],
        created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
        avg_rating FLOAT DEFAULT 0,
        feedback_count INT DEFAULT 0
    )
    """)
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS feedback (
        id SERIAL PRIMARY KEY,
        idea_id INTEGER REFERENCES ideas(id) ON DELETE CASCADE,
        rating INTEGER NOT NULL CHECK (rating BETWEEN 1 AND 5),
        feedback TEXT,
        created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
    )
    """)
    
    conn.commit()
    cursor.close()
    
    print("Database initialized")

def get_db():
    db = DBSession()
    try:
        yield db
    finally:
        pass  # We're not closing the connection here to reuse it