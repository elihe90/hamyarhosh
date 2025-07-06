import sqlite3
import json

# نام فایل پایگاه داده که باید با اسکریپت‌های دیگر یکسان باشد
DB_FILE = "chatbot_data.db"

def add_course(course_id: str, title: str, level: str, description: str, keywords: list, learning_goals: list, target_audience: list, prerequisites: list, career_path: list):
    """
    یک دوره جدید به جدول 'courses' اضافه می‌کند.
    لیست‌ها به صورت رشته JSON ذخیره می‌شوند.
    """
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    try:
        cursor.execute("""
        INSERT OR IGNORE INTO courses (course_id, title, level, description, keywords, learning_goals, target_audience, prerequisites, career_path)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);
        """, (
            course_id, 
            title, 
            level, 
            description,
            json.dumps(keywords, ensure_ascii=False),
            json.dumps(learning_goals, ensure_ascii=False),
            json.dumps(target_audience, ensure_ascii=False),
            json.dumps(prerequisites, ensure_ascii=False),
            json.dumps(career_path, ensure_ascii=False)
        ))
        if cursor.rowcount > 0:
            print(f"✅ Course added: {title}")
        else:
            print(f"⚠️ Course with ID '{course_id}' already exists. Skipping.")
    except Exception as e:
        print(f"❌ An error occurred while adding course: {e}")
    finally:
        conn.commit()
        conn.close()

def add_faq(question: str, answer: str):
    """
    یک سوال و جواب جدید به جدول 'faqs' اضافه می‌کند.
    """
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT OR IGNORE INTO faqs (question, answer) VALUES (?, ?);", (question, answer))
        if cursor.rowcount > 0:
            print(f"✅ FAQ added: {question}")
        else:
            print(f"⚠️ FAQ already exists, skipping: {question}")
    except Exception as e:
        print(f"❌ An error occurred while adding FAQ: {e}")
    finally:
        conn.commit()
        conn.close()

if __name__ == '__main__':
    # --- برای اضافه کردن داده جدید، بخش مربوطه را از حالت کامنت خارج کرده و ویرایش کنید ---

    print("--- Starting data addition process ---")

    # 1. افزودن «سند راهنما» برای فلو جدید مکالمه
    add_course(
        course_id="AI-GUIDE",
        title="راهنمای شروع یادگیری هوش مصنوعی",
        level="مقدماتی",
        description="برای یادگیری هوش مصنوعی دو مسیر اصلی وجود دارد. مسیر اول، مسیر تخصصی و فنی است که در آن فرد با برنامه‌نویسی و ریاضیات، نحوه ساخت مدل‌های هوش مصنوعی را یاد می‌گیرد. مسیر دوم، مسیر عمومی و کاربردی است که در آن فرد نحوه استفاده از ابزارهای آماده AI را بدون نیاز به کدنویسی فرا می‌گیرد.",
        keywords=["شروع", "راهنما", "چگونه شروع کنم", "مسیر یادگیری", "مشاوره"],
        learning_goals=["انتخاب مسیر صحیح یادگیری بین فنی و کاربردی"],
        target_audience=["تمام افراد علاقه‌مند به شروع یادگیری هوش مصنوعی"],
        prerequisites=[],
        career_path=[]
    )
    
    # 2. مثال برای اضافه کردن یک دوره جدید (در صورت نیاز از کامنت خارج کنید)
    # add_course(
    #     course_id="AI-501",
    #     title="بینایی کامپیوتر پیشرفته",
    #     level="پیشرفته",
    #     description="در این دوره به مباحث عمیق بینایی ماشین مانند شبکه‌های GAN و مدل‌های تشخیص سه بعدی می‌پردازیم.",
    #     keywords=["بینایی ماشین", "پردازش تصویر", "GAN", "سه بعدی"],
    #     learning_goals=["پیاده‌سازی GAN", "درک مدل‌های 3D"],
    #     target_audience=["متخصصان یادگیری ماشین"],
    #     prerequisites=["AI-301"],
    #     career_path=["مهندس بینایی ماشین"]
    # )

    # 3. مثال برای اضافه کردن یک سوال متداول جدید (در صورت نیاز از کامنت خارج کنید)
    # add_faq(
    #     question="آیا دوره‌ها پروژه محور هستند؟",
    #     answer="بله، تمام دوره‌های تخصصی ما شامل پروژه‌های عملی و واقعی هستند تا شما مهارت‌های خود را در عمل به کار بگیرید."
    # )
    
    print("\n--- Data addition process complete ---")