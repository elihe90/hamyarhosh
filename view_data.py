import sqlite3
import json

# نام فایل پایگاه داده شما
DB_FILE = "chatbot_data.db"

def view_all_courses():
    """
    Connects to the database, retrieves all courses, and prints them in a readable format.
    """
    try:
        conn = sqlite3.connect(DB_FILE)
        # این خط به ما اجازه می‌دهد تا به ستون‌ها با نام دسترسی داشته باشیم
        conn.row_factory = sqlite3.Row 
        cursor = conn.cursor()

        print("--- Retrieving all courses from the database ---")
        
        cursor.execute("SELECT * FROM courses")
        courses = cursor.fetchall()

        if not courses:
            print("No courses found in the database.")
            return

        print(f"\nFound {len(courses)} courses:\n")

        # نمایش اطلاعات هر دوره به صورت مرتب
        for course in courses:
            print("----------------------------------------")
            print(f"Course ID:   {course['course_id']}")
            print(f"Title:       {course['title']}")
            print(f"Level:       {course['level']}")
            print(f"Description: {course['description']}")
            
            # خواندن مقادیر JSON و نمایش آن‌ها به صورت لیست
            try:
                keywords = json.loads(course['keywords'])
                print(f"Keywords:    {keywords}")
            except (json.JSONDecodeError, TypeError):
                print(f"Keywords:    {course['keywords']}") # نمایش به صورت خام در صورت خطا

            try:
                learning_goals = json.loads(course['learning_goals'])
                print(f"Goals:       {learning_goals}")
            except (json.JSONDecodeError, TypeError):
                print(f"Goals:       {course['learning_goals']}")

            print("----------------------------------------\n")

    except sqlite3.OperationalError as e:
        print(f"❌ Database Error: {e}")
        print("Please make sure the database file 'chatbot_data.db' exists in the same directory.")
    except Exception as e:
        print(f"❌ An unexpected error occurred: {e}")
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    view_all_courses()