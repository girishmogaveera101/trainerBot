from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer
import numpy as np
from pathlib import Path
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv
from groq import Groq
from typing import List





load_dotenv()





# Initialize FastAPI
app = FastAPI(title="Gym RAG Chatbot")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)





class Question(BaseModel):
    question: str





# Global variables
embedder = None
documents = []
doc_embeddings = None
groq_client = None





def chunk_text(text: str, chunk_size: int = 500, overlap: int = 100) -> List[str]:
    chunks = []
    sentences = text.replace('\n', ' ').split('. ')
    current_chunk = []
    current_length = 0
    for sentence in sentences:
        sentence = sentence.strip()
        if not sentence:
            continue 
        sentence_length = len(sentence)
        if current_length + sentence_length > chunk_size and current_chunk:
            chunk_text = '. '.join(current_chunk) + '.'
            chunks.append(chunk_text.strip())
            overlap_sentences = []
            overlap_length = 0
            for sent in reversed(current_chunk):
                if overlap_length + len(sent) < overlap:
                    overlap_sentences.insert(0, sent)
                    overlap_length += len(sent)
                else:
                    break
            current_chunk = overlap_sentences
            current_length = overlap_length
        current_chunk.append(sentence)
        current_length += sentence_length
    if current_chunk:
        chunk_text = '. '.join(current_chunk) + '.'
        chunks.append(chunk_text.strip())
    return chunks







def load_gym_documents():
    docs = []
    data_folder = Path("data")
    if not data_folder.exists():
        print(f"Data folder not found: {data_folder}")
        return docs
    # .txt
    for file_path in data_folder.glob("*.txt"):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                if content.strip():
                    chunks = chunk_text(content, chunk_size=500, overlap=100)
                    docs.extend(chunks)
                    print(f"Loaded: {file_path.name} ({len(chunks)} chunks)")
        except Exception as e:
            print(f"Error reading {file_path.name}: {e}")
    # .pdf
    try:
        import PyPDF2
        for file_path in data_folder.glob("*.pdf"):
            try:
                with open(file_path, 'rb') as f:
                    pdf_reader = PyPDF2.PdfReader(f)
                    full_text = ""
                    for page in pdf_reader.pages:
                        page_text = page.extract_text()
                        if page_text:
                            full_text += page_text + "\n"
                    if full_text.strip():
                        full_text = ' '.join(full_text.split())
                        chunks = chunk_text(full_text, chunk_size=500, overlap=100)
                        chunks = [c for c in chunks if len(c) > 100]
                        docs.extend(chunks)
                        print(f"Loaded: {file_path.name} ({len(chunks)} chunks)")
            except Exception as e:
                print(f"Error reading PDF {file_path.name}: {e}")
    except ImportError:
        print("PyPDF2 not installed. Skipping PDF files.")
    print(f"\nTotal chunks loaded: {len(docs)}")
    return docs




def cosine_similarity(a, b):
    """Calculate cosine similarity between two vectors"""
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))






def retrieve_relevant_docs(query, top_k=3):
    """Retrieve most relevant documents using embeddings"""
    global embedder, documents, doc_embeddings
    if not documents:
        return []
    query_embedding = embedder.encode(query, convert_to_numpy=True)
    similarities = []
    for i, doc_emb in enumerate(doc_embeddings):
        sim = cosine_similarity(query_embedding, doc_emb)
        similarities.append((i, sim))
    similarities.sort(key=lambda x: x[1], reverse=True)
    top_docs = [documents[i] for i, _ in similarities[:top_k]]
    print(f"Top similarities: {[f'{score:.3f}' for _, score in similarities[:top_k]]}")
    return top_docs






def initialize_rag():
    global embedder, documents, doc_embeddings, groq_client
    cache_file = Path("embeddings_cache.npz")
    if cache_file.exists():
        print("Loading cached embeddings...")
        cache = np.load(cache_file, allow_pickle=True)
        documents = cache['documents'].tolist()
        doc_embeddings = cache['embeddings']
        print(f"✅ Loaded {len(documents)} cached documents")
    else:
        documents = load_gym_documents()
        embedder = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
        doc_embeddings = embedder.encode(documents, convert_to_numpy=True, show_progress_bar=True)
        np.savez_compressed('embeddings_cache.npz', documents=documents, embeddings=doc_embeddings)    
    if embedder is None:
        embedder = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
    groq_api_key = os.getenv("GROQ_API_KEY")
    if not groq_api_key:
        print("❌ ERROR: GROQ_API_KEY not found!")
        return    
    try:
        # Initialize Groq without proxies (HF Spaces compatibility)
        import httpx
        # Create a custom HTTP client without proxy
        http_client = httpx.Client(
            timeout=30.0,
            follow_redirects=True
        )
        groq_client = Groq(
            api_key=groq_api_key,
            http_client=http_client
        )
        # Test connection
        test_response = groq_client.chat.completions.create(
            messages=[{"role": "user", "content": "Say 'OK'"}],
            model="llama-3.1-8b-instant",
            max_tokens=5
        )
        print("✅ Groq initialized successfully")
    except Exception as e:
        print(f"❌ Groq initialization failed: {e}")
        print(f"   Error details: {type(e).__name__}")
        groq_client = None





@app.on_event("startup")
async def startup_event():
    initialize_rag()





@app.get("/")
def root():
    return {
        "message": "Gym RAG Chatbot API",
        "status": "running",
        "endpoints": {"/ask": "POST", "/health": "GET"}
    }





@app.post("/ask")
def ask_question(query: Question):
    if embedder is None or groq_client is None:
        raise HTTPException(status_code=500, detail="RAG system not initialized")
    print(f"\n{'='*60}")
    print(f"❓ Question: {query.question}")
    print(f"{'='*60}")
    relevant_docs = retrieve_relevant_docs(query.question, top_k=3)
    context = "\n\n".join(relevant_docs)
    print("Context : ",context)
    try:
        # Call Groq API
        chat_completion = groq_client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful gym and fitness assistant. Answer questions clearly and concisely based on the provided context. Talk like a human when its just a small question and be funny always"
                },
                {
                    "role": "user",
                    "content": f"""Based on this information:
{context}

Question: {query.question}

Provide a clear 2-3 sentence answer in Markdown format with headings, bullet points, and tips only when required or else keep it short funny reply."""
                }
            ],
            model="llama-3.1-8b-instant",
            temperature=0.7,
            max_tokens=200,
            top_p=0.9,
        )
        answer = chat_completion.choices[0].message.content.strip()
        print(f"✅ Groq response received")
        # Create source summaries
        source_summaries = [
            doc[:120] + "..." if len(doc) > 120 else doc 
            for doc in relevant_docs
        ]
        return {
            "question": query.question,
            "answer": answer,
            "sources": source_summaries
        }
    except Exception as e:
        print(f"❌ Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))





@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "rag_initialized": embedder is not None,
        "llm_available": groq_client is not None,
        "num_documents": len(documents) if documents else 0
    }







if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=7860)