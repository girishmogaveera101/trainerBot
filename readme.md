# 💪 Gym RAG Chatbot

A Retrieval-Augmented Generation (RAG) chatbot for gym and fitness questions, powered by Groq's Llama 3.1 and semantic search.

![Python](https://img.shields.io/badge/Python-3.10-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104-green)
![Next.js](https://img.shields.io/badge/Next.js-14-black)
![Groq](https://img.shields.io/badge/Groq-Llama--3.1-orange)

## 🌟 Features

- 🤖 **AI-Powered Responses** - Uses Groq's Llama 3.1-8B for fast, accurate answers
- 📚 **RAG Architecture** - Semantic search over gym documents for context-aware responses
- ⚡ **Lightning Fast** - Sub-2 second response times with Groq API
- 💬 **ChatGPT-Style UI** - Beautiful dark mode interface with message history
- 📱 **Fully Responsive** - Works seamlessly on desktop, tablet, and mobile
- 🔍 **Smart Document Chunking** - Efficiently processes PDFs and text files

## 🚀 Live Demo

- **Frontend (Vercel)**: [trainerBot.vercel.app](https://trainerbot.vercel.app)
- **Backend API (HuggingFace)**: [girizhhh-trainerBot.hf.space](https://girizhhh-titantrainerai-api.hf.space)

## 🏗️ Architecture

```
┌─────────────────┐      HTTP      ┌──────────────────┐
│   Next.js UI    │ ────────────► │   FastAPI        │
│   (Vercel)      │                │   (HF Spaces)    │
└─────────────────┘                └──────────────────┘
                                            │
                                            ▼
                         ┌──────────────────────────────┐
                         │  RAG Pipeline                │
                         │  1. Semantic Search          │
                         │  2. Document Retrieval       │
                         │  3. Groq LLM Generation      │
                         └──────────────────────────────┘
```

## 📦 Tech Stack

### Backend
- **FastAPI** - High-performance Python API framework
- **Sentence Transformers** - Document embeddings (`all-MiniLM-L6-v2`)
- **Groq API** - Ultra-fast LLM inference (Llama 3.1-8B)
- **NumPy** - Vector similarity calculations
- **PyPDF2** - PDF document processing

### Frontend
- **Next.js 14** - React framework with App Router
- **TypeScript** - Type-safe React components
- **Tailwind CSS** - Utility-first styling
- **React Markdown** - Markdown rendering for responses

## 🛠️ Installation

### Prerequisites
- Python 3.10+
- Node.js 18+
- Groq API Key

### Backend Setup

```bash
# Clone the repository
git clone 
cd gym-rag-chatbot/backend

# Install dependencies
pip install -r requirements.txt

# Create .env file
echo "GROQ_API_KEY=your_groq_api_key_here" > .env

# Add your gym documents to the data/ folder
mkdir data
# Copy your .txt or .pdf files to data/

# Run the server
uvicorn app:app --host 0.0.0.0 --port 7860
```

### Frontend Setup

```bash
cd ../frontend

# Install dependencies
npm install

# Update API endpoint in page.tsx
# Change: http://localhost:7860/ask
# To: https://your-space.hf.space/ask

# Run development server
npm run dev
```

## 📁 Project Structure

```
gym-rag-chatbot/
├── backend/
│   ├── app.py                 # FastAPI application
│   ├── requirements.txt       # Python dependencies
│   ├── Dockerfile            # Docker configuration
│   ├── data/                 # Gym documents (.txt, .pdf)
│   └── embeddings_cache.npz  # Cached embeddings (auto-generated)
│
├── frontend/
│   ├── app/
│   │   └── page.tsx          # Main chat interface
│   ├── package.json          # Node dependencies
│   └── tailwind.config.ts    # Tailwind configuration
│
└── README.md
```

## 🌐 Deployment

### Backend (HuggingFace Spaces)

1. Create a new Space on [HuggingFace](https://huggingface.co/spaces)
2. Choose **Docker** as SDK
3. Upload backend files:
   - `app.py`
   - `Dockerfile`
   - `requirements.txt`
   - `README.md`
   - `data/` folder
4. Add `GROQ_API_KEY` in Space Settings → Secrets
5. Space will auto-deploy!

## 📝 Adding Your Own Documents

1. Add `.txt` or `.pdf` files to `backend/data/` folder
2. Restart the server (embeddings will auto-regenerate)
3. Documents are automatically chunked and indexed

**Supported formats:**
- Plain text (`.txt`)
- PDF documents (`.pdf`)

## 🙏 Acknowledgments

- [Groq](https://groq.com) - Ultra-fast LLM inference
- [HuggingFace](https://huggingface.co) - Model hosting and embeddings
- [Sentence Transformers](https://www.sbert.net/) - Semantic search
- [FastAPI](https://fastapi.tiangolo.com/) - Modern Python API framework
- [Next.js](https://nextjs.org/) - React framework


**⭐ If you found this helpful, please give it a star!**