import sqlite3

DB_FILE = "chatbot_data.db"

# دسته‌بندی دوره‌ها بر اساس شناسه
# شما می‌توانید این دسته‌بندی را به دلخواه تغییر دهید
course_paths = {
    # --- مسیر فنی / تخصصی ---
    "AI-101": "technical",
    "AI-201": "technical",
    "2511200001": "technical",
    "2511200002": "technical",
    "2511200004": "technical",
    "2511200005": "technical",
    "2511200006": "technical",
    "2511200008": "technical",
    "2511200010": "technical",
    "2511200011": "technical",
    "2511200012": "technical",
    "2511200014": "technical",
    "2511200015": "technical",
    "2511200016": "technical",
    "2511200017": "technical",

    # --- مسیر عمومی / کاربردی ---
    "2511200003": "practical",
    "2511200007": "practical",
    "AI-051": "practical",
    "AI-010": "practical",
    "AI-052": "practical",
    "AI-053": "practical",
    "AI-060": "practical",
    "AI-GUIDE": "practical" # راهنمای شروع هم جزو مسیر عمومی است
}

def update_course_paths():
    """Adds a 'path' column to the courses table and sets the path for each course."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    try:
        # افزودن ستون 'path' اگر وجود نداشته باشد
        cursor.execute("ALTER TABLE courses ADD COLUMN path TEXT;")
        print("✅ Column 'path' added to courses table.")
    except sqlite3.OperationalError as e:
        if "duplicate column name" in str(e):
            print("⚠️ Column 'path' already exists.")
        else:
            raise e

    # به‌روزرسانی مسیر برای هر دوره
    updated_count = 0
    for course_id, path in course_paths.items():
        cursor.execute("UPDATE courses SET path = ? WHERE course_id = ?", (path, course_id))
        if cursor.rowcount > 0:
            updated_count += 1
    
    conn.commit()
    conn.close()
    print(f"\n✅ Successfully set paths for {updated_count} courses.")

if __name__ == "__main__":
    update_course_paths()