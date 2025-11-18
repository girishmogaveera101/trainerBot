# server running command
uvicorn app:app --reload --host 0.0.0.0 --port 7860


# server link
https://girizhhh-titantrainerai-api.hf.space/docs

---
title: Gym RAG Chatbot
emoji: 💪
colorFrom: blue
colorTo: purple
sdk: docker
pinned: false
---

# Gym RAG Chatbot 💪

A Retrieval-Augmented Generation (RAG) chatbot for gym and fitness questions.

## Features

- 📚 Semantic search over gym documents
- 🤖 Powered by Groq (Llama 3.1)
- ⚡ Fast responses with embedding caching
- 📄 Supports PDF and TXT files

## API Endpoints

### POST /ask
Ask fitness questions
```json
{
  "question": "How do I build bigger biceps?"
}
```

### GET /health
Check system status

## Setup

Add your `GROQ_API_KEY` to the Space secrets.

Upload your gym documents to the `/data` folder.