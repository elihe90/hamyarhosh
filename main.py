import traceback
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List

# LangChain Imports
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnablePassthrough
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
# Make sure langchain-community is installed for ChatMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory

# --- Configuration ---
AVAL_AI_API_KEY = "aa-sXbTrJMgJUY9bBIJpf5tp3hr2k2iHXRKbBpd1Rz6UmRzO4sm" # ! کلید خود را جایگزین کنید
AVAL_AI_BASE_URL = "https://api.avalai.org/v1" # ! آدرس پراکسی شما

# --- FastAPI App ---
app = FastAPI(title="Final AI Advisor with Memory")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

# --- In-Memory Session Storage for Chat History ---
store = {}
def get_session_history(session_id: str) -> ChatMessageHistory:
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
    return store[session_id]

# --- AI Components ---
try:
    print("Initializing AI components via aval ai proxy...")
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.3, api_key=AVAL_AI_API_KEY, base_url=AVAL_AI_BASE_URL)
    embeddings_model = OpenAIEmbeddings(model="text-embedding-ada-002", api_key=AVAL_AI_API_KEY, base_url=AVAL_AI_BASE_URL)
    
    # Load the integrated vector store
    vector_store = Chroma(persist_directory="./ai_advisor_db", embedding_function=embeddings_model)
    retriever = vector_store.as_retriever(search_kwargs={"k": 7})
    print("✅ AI components loaded successfully.")
except Exception as e:
    print(f"❌ Error initializing AI components: {e}")
    raise e

# --- The Final Master Prompt with Multi-step Logic ---
master_prompt = ChatPromptTemplate.from_messages([
    ("system", 
     "You are a friendly and expert AI learning advisor named 'مشاور هوشمند'. Your task is to guide the user step-by-step. "
     "Use the conversation history and the retrieved context to decide your next action.\n\n"
     "**Your Logic:**\n"
     "1. If the user asks a general question about starting (e.g., 'how to start?'), and the context contains the 'راهنمای شروع یادگیری هوش مصنوعی' document, your first response MUST be to introduce the two main learning paths (Technical vs. Practical) and ask the user to choose one.\n"
     "2. If the user has just chosen a path (e.g., 'technical' or 'practical'), your next step is to ask for their skill level: 'مبتدی، متوسط یا پیشرفته؟'.\n"
     "3. If the user has provided both a path and a skill level, use the retrieved context to find and recommend courses that match BOTH the path AND the level.\n"
     "4. For any other specific question, answer it based ONLY on the retrieved context.\n"
     "5. If the context does not contain the answer, say that you don't have information on that topic.\n\n"
     "Answer all questions in clear and helpful Persian."
     "\n\n**Retrieved Context:**\n{context}"
    ),
    MessagesPlaceholder(variable_name="chat_history"),
    ("human", "{question}"),
])

# --- The Final RAG Chain with Memory ---
rag_chain = (
    RunnablePassthrough.assign(context=(lambda x: x["question"]) | retriever)
    | master_prompt
    | llm
    | StrOutputParser()
)

conversational_rag_chain = RunnableWithMessageHistory(
    rag_chain,
    get_session_history,
    input_messages_key="question",
    history_messages_key="chat_history",
)

# --- API ---
class ChatInput(BaseModel):
    message: str
    session_id: str = "default_session"

class ChatOutput(BaseModel):
    response: str

@app.post("/chat", response_model=ChatOutput)
async def chat_with_bot(request: ChatInput):
    try:
        config = {"configurable": {"session_id": request.session_id}}
        response = await conversational_rag_chain.ainvoke({"question": request.message}, config=config)
        return ChatOutput(response=response)
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))
    # --- Add this block at the VERY END of main.py ---
if __name__ == "__main__":
    import uvicorn
    # Render provides the port to run on via the PORT environment variable
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)