import os
import chromadb
import time
import threading
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
# --- ✅ ONLY GEMINI EMBEDDING IMPORT ---
from llama_index.embeddings.gemini import GeminiEmbedding
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.core import StorageContext
# --- ✅ ONLY GEMINI IMPORT ---
from llama_index.llms.gemini import Gemini 
from llama_index.core.settings import Settings

# --- კონფიგურაცია ---
DATA_DIR = "./devops_files"
CHROMA_PATH = "./chroma_db"
COLLECTION_NAME = "devops_project_memory"
MODEL_NAME = "gemini-2.5-flash" 
FILE_EXTENSIONS = [".tf", ".yml", ".yaml", ".sh", ".ini"]

# გლობალური ცვლადი ინდექსისთვის
project_index = None

# --- ✅ გასაღების შემოწმება (მხოლოდ Gemini) ---
if "GEMINI_API_KEY" not in os.environ:
    print("❌ შეცდომა: GEMINI_API_KEY არ არის დაყენებული გარემოს ცვლადებში.")
    print("გთხოვთ, დააყენოთ ცვლადი PowerShell-ში: $env:GEMINI_API_KEY=\"თქვენი_გასაღები\"")
    exit()

# LLM-ის ინიციალიზაცია
Settings.llm = Gemini(model=MODEL_NAME)
Settings.embed_model = GeminiEmbedding()
print(f"✅ AI აგენტი ინიცირებულია {MODEL_NAME} მოდელით.")


# --- 1. ინდექსირება (მეხსიერების შექმნა/განახლება) ---

def initialize_memory():
    """ქმნის ან ანახლებს ვექტორულ მონაცემთა ბაზას."""
    global project_index
    
    if not os.path.exists(DATA_DIR) or not os.listdir(DATA_DIR):
        print(f"⚠️ საქაღალდე {DATA_DIR} ცარიელია ან არ არსებობს.")
        return 

    print("\n... ვიწყებ ინდექსირებას (მეხსიერების შექმნას/განახლებას) ...")
    
    # ChromaDB-ის ინიციალიზაცია
    chroma_client = chromadb.PersistentClient(path=CHROMA_PATH)
    chroma_collection = chroma_client.get_or_create_collection(COLLECTION_NAME)
    
    vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
    storage_context = StorageContext.from_defaults(vector_store=vector_store)
    
    # ფაილების წაკითხვა
    documents = SimpleDirectoryReader(
        DATA_DIR, 
        required_exts=FILE_EXTENSIONS
    ).load_data()

    # ინდექსის შექმნა (განაახლებს ან ქმნის)
    project_index = VectorStoreIndex.from_documents(
        documents,
        storage_context=storage_context,
    )
    print(f"... ინდექსირება დასრულდა. {len(documents)} დოკუმენტი დაიმახსოვრა.")


# --- 2. ავტომატური თრექინგი (Watchdog) ---

class FileChangeHandler(FileSystemEventHandler):
    """ამუშავებს ფაილის შეცვლის ივენთებს და ანახლებს მეხსიერებას."""
    
    def on_modified(self, event):
        if event.is_directory:
            return
        
        # ამოწმებს, არის თუ არა შეცვლილი ფაილი ჩვენი გაფართოების
        if os.path.splitext(event.src_path)[1] in FILE_EXTENSIONS:
            print(f"\n🔔 ფაილი შეიცვალა: {event.src_path}. ავტომატურად ვანახლებ მეხსიერებას...")
            # სრულად განახლება დროებით (შემდეგ ფაზაში იქნება ინკრემენტული)
            initialize_memory()

def start_file_tracker():
    """იწყებს ფაილების მონიტორინგს ცალკე Thread-ში."""
    event_handler = FileChangeHandler()
    observer = Observer()
    observer.schedule(event_handler, DATA_DIR, recursive=True)
    observer.start()
    print(f"\n🔎 ფაილების თრექინგი გააქტიურებულია საქაღალდეში: {DATA_DIR}")
    return observer


# --- 3. მოძიება და გენერაცია (კომუნიკაცია) ---

def query_memory(user_query):
    """ამოწმებს მეხსიერებას, იღებს კონტექსტს და პასუხს სთხოვს LLM-ს."""
    if project_index is None:
        print("მეხსიერება არ არის ინიცირებული.")
        return
        
    query_engine = project_index.as_query_engine()
    response = query_engine.query(user_query)
    
    # --- დებაგინგის ინფორმაცია: გამოყენებული კონტექსტი ---
    print("\n--- AI-ის მიერ გამოყენებული (გახსენებული) კონტექსტი ---")
    retrieved_context = [n.get_text() for n in response.source_nodes]
    
    for i, context in enumerate(retrieved_context[:3]):
        print(f"Node {i+1} (Source): {context[:50]}...") 
    print("----------------------------------------------------------")
    
    print("\n🤖 AI პასუხი:")
    return response

# --- მთავარი გაშვება ---
if __name__ == "__main__":
    
    # 1. მეხსიერების პირველადი ინიცირება
    initialize_memory()
    
    # 2. თრექინგის დაწყება
    tracker = start_file_tracker()
    
    try:
        while True:
            # 3. მომხმარებლის ინტერფეისი
            user_input = input("\nთქვენი შეკითხვა პროექტის შესახებ (ან 'გასვლა'): ")
            
            if user_input.lower() == 'გასვლა':
                break
            
            # 4. პასუხის მიღება
            ai_response = query_memory(user_input)
            print(ai_response)
            
    except KeyboardInterrupt:
        pass
    finally:
        # 5. თრექინგის შეჩერება გასვლისას
        tracker.stop()
        tracker.join()
        print("\n👋 აგენტი გამორთულია. თრექინგი შეჩერდა.")