import sqlite3
import json

# Define the database file name
DB_FILE = "chatbot_data.db"

# --- Create Tables ---
def create_tables(conn):
    cursor = conn.cursor()
    # Create courses table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS courses (
        course_id TEXT PRIMARY KEY,
        title TEXT NOT NULL,
        description TEXT,
        keywords TEXT,
        learning_goals TEXT,
        target_audience TEXT,
        prerequisites TEXT,
        career_path TEXT
    );
    """)
    # Create faqs table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS faqs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        question TEXT NOT NULL UNIQUE,
        answer TEXT NOT NULL
    );
    """)
    conn.commit()
    print("Tables created successfully (if they didn't exist).")

def migrate_data(conn):
    cursor = conn.cursor()
    try:
        with open('courses.json', 'r', encoding='utf-8') as f:
            courses_data = json.load(f)
        for course in courses_data:
            cursor.execute("""
            INSERT OR IGNORE INTO courses (course_id, title, description, keywords, learning_goals, target_audience, prerequisites, career_path)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?);
            """, (
                course.get('course_id'),
                course.get('title'),
                course.get('description'),
                json.dumps(course.get('keywords', []), ensure_ascii=False), # <--- تغییر
                json.dumps(course.get('learning_goals', []), ensure_ascii=False), # <--- تغییر
                json.dumps(course.get('target_audience', []), ensure_ascii=False), # <--- تغییر
                json.dumps(course.get('prerequisites', []), ensure_ascii=False), # <--- تغییر
                json.dumps(course.get('career_path', []), ensure_ascii=False)  # <--- تغییر
            ))
        print(f"{len(courses_data)} courses migrated successfully.")
    except FileNotFoundError:
        print("courses.json not found. Skipping course migration.")
    
    # ... (بخش مربوط به FAQ بدون تغییر باقی می‌ماند) ...
    try:
        with open('qa.json', 'r', encoding='utf-8') as f:
            qa_data = json.load(f)
        for qa in qa_data:
            cursor.execute("INSERT OR IGNORE INTO faqs (question, answer) VALUES (?, ?);", (qa.get('question'), qa.get('answer')))
        print(f"{len(qa_data)} FAQs migrated successfully.")
    except FileNotFoundError:
        print("qa.json not found. Skipping FAQ migration.")

    conn.commit()

if __name__ == "__main__":
    # Connect to the database (it will be created if it doesn't exist)
    connection = sqlite3.connect(DB_FILE)
    
    # Create tables
    create_tables(connection)
    
    # Migrate existing data
    migrate_data(connection)
    
    # Close the connection
    connection.close()
    
    print("\nDatabase setup complete!")