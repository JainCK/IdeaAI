# 💡 Idea AI – Intelligent Idea Generation Platform

**Idea AI** is a modular, scalable, and customizable backend application for AI-assisted idea generation, feedback collection, and semantic search. It leverages **FastAPI**, **PostgreSQL**, **Supabase Vector DB**, and **Hugging Face models** to deliver high-performance and flexible functionality.

---

## 🚀 Live Features

- ✨ Generate creative, tailored ideas using customizable templates
- 🔍 Perform semantic search with embeddings via RAG (Retrieval Augmented Generation)
- 🧠 Store, retrieve, and relate ideas using vector similarity
- 📊 Collect and analyze feedback from users
- 🔧 Tune generation behavior with user-defined parameters

---

## 🧱 Tech Stack

| Layer        | Technology                          |
|-------------|--------------------------------------|
| Backend API | FastAPI (Python)                     |
| Database    | PostgreSQL (via [Neon.tech](https://neon.tech)) |
| Vector DB   | Supabase Vector Store                |
| Embeddings  | Sentence Transformers (Hugging Face) |
| LLM         | Flan-T5 (swappable with any HF model)|
| ORM & Schema| Pydantic + SQLAlchemy                |

----

## 🔑 Core Features

### ✅ FastAPI + PostgreSQL Backend

- Modular API with route grouping: `/ideas`, `/search`, `/feedback`
- Fully RESTful structure with clean separation of concerns
- Rate limiting middleware to avoid abuse

### ✅ Vector-Search-Powered RAG

- **Sentence Transformers** for generating embeddings
- **Supabase Vector DB** for fast semantic similarity search
- **Flan-T5** for controllable idea generation (can swap model as needed)
- RAG pipeline to enrich generated output with similar past ideas

### ✅ Configurability

- Customize creativity, length, and temperature for idea generation
- Add templates with goals, audience, tone, and constraints
- Apply filters and thresholds for similarity search

---

## ⚙️ Performance Optimizations

- `@lru_cache` for model and config caching
- Efficient database reuse via singleton DB client
- Vector index loading optimized for warm starts

---

✨ Future Improvements
 Add Web UI (Next.js frontend)

 Feedback-based ranking of ideas

 Fine-tuning model with custom domain data

 API authentication and usage limits

🙋‍♂️ Author
Made with 🧠 by Your Name

