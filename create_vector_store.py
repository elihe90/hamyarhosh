<<<<<<< HEAD
import sqlite3, json, os, shutil
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document

DB_FILE = "chatbot_data.db"
VECTOR_DB_DIR = "./ai_advisor_db"
AVAL_AI_API_KEY = "aa-sXbTrJMgJUY9bBIJpf5tp3hr2k2iHXRKbBpd1Rz6UmRzO4sm" # ! کلید خود را جایگزین کنید
AVAL_AI_BASE_URL = "https://api.avalai.org/v1"

def load_data_from_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    # ستون جدید 'path' را هم می‌خوانیم
    cursor.execute("SELECT title, description, level, path FROM courses")
    courses = cursor.fetchall()
    cursor.execute("SELECT question, answer FROM faqs")
    faqs = cursor.fetchall()
    conn.close()
    return courses, faqs

try:
    courses_data, qa_data = load_data_from_db()
    all_documents = []
    
    for c in courses_data:
        # اطلاعات مسیر را به محتوای سند اضافه می‌کنیم
        content = f"دوره: {c[0]}. سطح: {c[2]}. مسیر: {c[3]}. توضیحات: {c[1]}."
        all_documents.append(Document(page_content=content, metadata={"source": "course", "title": c[0], "path": c[3]}))
    
    for qa in qa_data:
        content = f"سوال متداول: {qa[0]}\nپاسخ: {qa[1]}"
        all_documents.append(Document(page_content=content, metadata={"source": "faq"}))

    embeddings_model = OpenAIEmbeddings(model="text-embedding-ada-002", api_key=AVAL_AI_API_KEY, base_url=AVAL_AI_BASE_URL)

    if os.path.exists(VECTOR_DB_DIR): shutil.rmtree(VECTOR_DB_DIR)
    
    Chroma.from_documents(documents=all_documents, embedding=embeddings_model, persist_directory=VECTOR_DB_DIR)
    print("✅ Integrated vector store updated successfully with path information.")

except Exception as e:
=======
import sqlite3, json, os, shutil
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document

DB_FILE = "chatbot_data.db"
VECTOR_DB_DIR = "./ai_advisor_db"
AVAL_AI_API_KEY = "aa-sXbTrJMgJUY9bBIJpf5tp3hr2k2iHXRKbBpd1Rz6UmRzO4sm" # ! کلید خود را جایگزین کنید
AVAL_AI_BASE_URL = "https://api.avalai.org/v1"

def load_data_from_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    # ستون جدید 'path' را هم می‌خوانیم
    cursor.execute("SELECT title, description, level, path FROM courses")
    courses = cursor.fetchall()
    cursor.execute("SELECT question, answer FROM faqs")
    faqs = cursor.fetchall()
    conn.close()
    return courses, faqs

try:
    courses_data, qa_data = load_data_from_db()
    all_documents = []
    
    for c in courses_data:
        # اطلاعات مسیر را به محتوای سند اضافه می‌کنیم
        content = f"دوره: {c[0]}. سطح: {c[2]}. مسیر: {c[3]}. توضیحات: {c[1]}."
        all_documents.append(Document(page_content=content, metadata={"source": "course", "title": c[0], "path": c[3]}))
    
    for qa in qa_data:
        content = f"سوال متداول: {qa[0]}\nپاسخ: {qa[1]}"
        all_documents.append(Document(page_content=content, metadata={"source": "faq"}))

    embeddings_model = OpenAIEmbeddings(model="text-embedding-ada-002", api_key=AVAL_AI_API_KEY, base_url=AVAL_AI_BASE_URL)

    if os.path.exists(VECTOR_DB_DIR): shutil.rmtree(VECTOR_DB_DIR)
    
    Chroma.from_documents(documents=all_documents, embedding=embeddings_model, persist_directory=VECTOR_DB_DIR)
    print("✅ Integrated vector store updated successfully with path information.")

except Exception as e:
>>>>>>> 193021b6980fc1f552e28a237a67d4ba76fc1b9f
    print(f"❌ An error occurred: {e}")