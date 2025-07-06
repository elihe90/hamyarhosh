import sqlite3

DB_FILE = "chatbot_data.db"

def update_course_schema():
    """Adds a 'level' column to the courses table and sets default values."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    try:
        # Add the 'level' column if it doesn't exist
        cursor.execute("ALTER TABLE courses ADD COLUMN level TEXT;")
        print("✅ Column 'level' added to courses table.")
    except sqlite3.OperationalError as e:
        # This error happens if the column already exists, which is fine.
        if "duplicate column name" in str(e):
            print("⚠️ Column 'level' already exists.")
        else:
            raise e

    # --- Set levels for existing courses (you can customize this) ---
    # We will guess the level based on keywords in the title
    updates = {
        "مقدماتی": ["مبانی", "برنامه نویسی برای", "حل مسئله", "ارتباطات"],
        "متوسط": ["یادگیری ماشین", "تحلیل آماری", "تجسم داده", "طراحی الگوریتم"],
        "پیشرفته": ["یادگیری عمیق", "کلان داده", "تحقیقات", "مدل سازی"]
    }

    cursor.execute("SELECT course_id, title FROM courses")
    all_courses = cursor.fetchall()
    
    for course_id, title in all_courses:
        level = "متوسط" # Default level
        if any(keyword in title for keyword in updates["مقدماتی"]):
            level = "مقدماتی"
        elif any(keyword in title for keyword in updates["پیشرفته"]):
            level = "پیشرفته"
        
        cursor.execute("UPDATE courses SET level = ? WHERE course_id = ?", (level, course_id))
        print(f"Set level for '{title}' to '{level}'")

    conn.commit()
    conn.close()
    print("\nDatabase schema updated successfully.")

if __name__ == "__main__":
    update_course_schema()