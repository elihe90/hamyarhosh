from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma

# --- Configuration ---
# ! کلید API و آدرس پایه خود از aval ai را اینجا قرار دهید
AVAL_AI_API_KEY = "aa-sXbTrJMgJUY9bBIJpf5tp3hr2k2iHXRKbBpd1Rz6UmRzO4sm"
AVAL_AI_BASE_URL = "https://api.avalai.ir/v1"

DB_DIR = "./ai_advisor_db_final"
TEST_QUERY = "هوش" # یک سوال تستی که باید نتیجه داشته باشد

print("--- Starting Retriever Test with OpenAI & aval ai Proxy ---")
try:
    print("Initializing embedding model via aval ai...")
    embeddings = OpenAIEmbeddings(
        model="text-embedding-ada-002",
        api_key=AVAL_AI_API_KEY,
        base_url=AVAL_AI_BASE_URL
    )
    
    print(f"Loading vector store from: {DB_DIR}")
    vector_store = Chroma(
        persist_directory=DB_DIR, 
        embedding_function=embeddings
    )
    
    print(f"Performing similarity search for query: '{TEST_QUERY}'")
    results = vector_store.similarity_search(TEST_QUERY, k=3)
    
    print("\n--- TEST RESULTS ---")
    if not results:
        print("❌ No documents found. This could mean:")
        print("1. The vector store is empty or corrupted.")
        print("2. There was a connection issue with the embedding service.")
    else:
        print(f"✅ Found {len(results)} documents:")
        for i, doc in enumerate(results):
            print(f"\n--- Document {i+1} ---")
            print(doc.page_content)
            print("-" * 20)

except Exception as e:
    print(f"\n❌ An error occurred during the test: {e}")