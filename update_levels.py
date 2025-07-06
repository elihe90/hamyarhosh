import sqlite3

DB_FILE = "chatbot_data.db"

# در اینجا سطح هر دوره را بر اساس شناسه آن مشخص می‌کنیم
# شما می‌توانید این سطوح را به دلخواه تغییر دهید
course_levels_to_update = {
    "2511200001": "پیشرفته",  # بکارگیری ریاضیات پیشرفته
    "2511200002": "متوسط",     # طراحی الگوریتم
    "2511200003": "مقدماتی",  # ارتباطات و همکاری
    "2511200004": "پیشرفته",  # انجام تحقیق جامع
    "2511200005": "متوسط",     # حل مسئله و تفکر تحلیلی
    "2511200006": "متوسط",     # تحلیل آماری
    "2511200007": "مقدماتی",  # بکارگیری اخلاق و مسئولیت
    "2511200008": "پیشرفته",  # یادگیری ماشین با TensorFlow و PyTorch
    "2511200010": "پیشرفته",  # تجزیه و تحلیل کلان داده
    "2511200011": "مقدماتی",  # برنامه نویسی برای هوش مصنوعی با پایتون و R
    "2511200012": "پیشرفته",  # یادگیری عمیق
    "2511200014": "متوسط",     # تجسم داده ها
    "2511200015": "پیشرفته",  # مدل سازی و الگوریتم های پیش بینی کننده
    "2511200016": "مقدماتی",  # برنامه نویسی و علوم کامپیوتر برای مهندسین
    "2511200017": "متوسط"      # ارزیابی و تنظیم مدل
}

def update_levels():
    """Updates the 'level' for existing courses in the database."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    try:
        updated_count = 0
        for course_id, level in course_levels_to_update.items():
            cursor.execute("UPDATE courses SET level = ? WHERE course_id = ?", (level, course_id))
            if cursor.rowcount > 0:
                updated_count += 1
        
        conn.commit()
        print(f"✅ Successfully updated levels for {updated_count} courses.")

    except Exception as e:
        print(f"❌ An error occurred: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    update_levels()