import os
import sys
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Load environment variables
load_dotenv()

def setup_postgres_db():
    """Set up the PostgreSQL database tables."""
    db_url = os.getenv("NEON_DB_URL")
    if not db_url:
        print("Error: NEON_DB_URL environment variable not set")
        sys.exit(1)
    
    try:
        conn = psycopg2.connect(db_url, cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        
        # Create ideas table
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
        
        # Create feedback table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS feedback (
            id SERIAL PRIMARY KEY,
            idea_id INTEGER REFERENCES ideas(id) ON DELETE CASCADE,
            rating INTEGER NOT NULL CHECK (rating BETWEEN 1 AND 5),
            feedback TEXT,
            created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
        )
        """)
        
        # Create indexes
        cursor.execute("CREATE INDEX IF NOT EXISTS ideas_topic_idx ON ideas(topic)")
        cursor.execute("CREATE INDEX IF NOT EXISTS ideas_created_at_idx ON ideas(created_at)")
        cursor.execute("CREATE INDEX IF NOT EXISTS feedback_idea_id_idx ON feedback(idea_id)")
        
        conn.commit()
        print("PostgreSQL tables created successfully")
        
    except Exception as e:
        print(f"Error setting up PostgreSQL database: {e}")
        sys.exit(1)
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    setup_postgres_db()
    print("Database setup complete")