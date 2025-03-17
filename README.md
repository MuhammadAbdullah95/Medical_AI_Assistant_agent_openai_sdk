# 🏥 Medical AI Chatbot

A **medical chatbot** powered by **Langchain, Pinecone, Google Gemini, and OpenAI's Agents SDK**, designed to provide intelligent and up-to-date responses using **RAG (Retrieval-Augmented Generation)** and **Google Search** for dynamic knowledge fetching.

---

## 🚀 Features

- **Medical Query Handling**: Conversational agent for answering medical-related questions.
- **RAG (Retrieval-Augmented Generation)**: Pulls relevant data from embedded medical knowledge base.
- **Google Search Tool**: Retrieves latest online data for up-to-date information.
- **Contextual Memory & Reasoning**: Handles complex conversations with multi-turn context.
- **Agents SDK**: Extends AI behavior with tools for flexible task handling.
- **Fast, Secure, and Scalable Backend** with real-time communication.

---

## 🧐 Tech Stack

- **Langchain** — LLM orchestration and agent logic.
- **Pinecone** — Vector storage for embedding-based retrieval.
- **Google Gemini** — Primary LLM for generating intelligent responses.
- **OpenAI Agents SDK** — Agent-based architecture.
- **Google Search API Tool** — For real-time information updates.
- **Python** (FastAPI/Flask backend).
- **Chainlit** (Optional for Chatbot UI during development).

---

## 📦 Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/MuhammadAbdullah95/Medical_AI_Assistant_agent_openai_sdk.git
cd Medical_AI_Assistant_agent_openai_sdk
```

---

### 2. Set up Environment with UV and Install dependencies

```bash
uv sync
```

---

> ⚙️ If `uv sync` is not working yet, install manually:

```bash
uv add langchain openai pinecone-client google-search-results chainlit
```

---

### 4. Set Up API Keys

Create a `.env` file in the root directory of your project and add the following keys:

```
# .env

# Google Gemini API Key
GEMINI_API_KEY=your_google_gemini_api_key_here

# Pinecone API Key
PINECONE_API_KEY=your_pinecone_api_key_here
PINECONE_ENV=your_pinecone_environment  # (e.g., "us-east1-gcp")

# OpenAI (if required for some tools or fallback)
OPENAI_API_KEY=your_openai_api_key_here

# Google Search API Key (if using Google Search for RAG)
GOOGLE_SEARCH_API_KEY=your_google_search_api_key_here
```

> ⚠️ **Note:** Never commit `.env` to public repositories. It contains sensitive credentials.

---

### 5. Run the Chatbot Application

```bash
python app.py
```

Or if using Chainlit for development UI:

```bash
chainlit run app.py
```

---

## 🛠 Tools Used in Chatbot

| Tool                    | Purpose                                 |
| ----------------------- | --------------------------------------- |
| **Langchain**           | LLM chaining, agents, tool integration  |
| **Pinecone**            | Vector embeddings search & retrieval    |
| **Google Gemini**       | Language model for generating responses |
| **OpenAI Agents SDK**   | Custom AI agent framework               |
| **Google Search API**   | Dynamic data retrieval from the web     |
| **Chainlit (optional)** | Development UI for real-time chat       |

---

## ✅ Usage

- Ask medical-related questions like:
  > "What are the symptoms of diabetes?"
  > "What is the latest treatment for hypertension?"
- Chatbot will answer using its internal RAG system, and when needed, dynamically search up-to-date information using Google Search.
- Supports multi-turn conversations and contextual understanding.

---

## 📂 Project Structure

```
Medical_AI_Assistant_agent_openai_sdk/
├── app.py                  # Main backend application
├── google_search.py       # Google search tool integration
├── retrievel_tool.py      # RAG-based retrieval system
├── src/openai_sdk/        # OpenAI SDK agent components
├── data/                  # Medical datasets (if any)
├── public/                # Static assets (optional)
├── research/              # Research, notes, notebooks (optional)
├── .env                   # Environment variables (API keys)
├── .gitignore             # Files/folders to ignore in Git
└── README.md              # Documentation
```

---

## 📖 Example Query & Response

> **User**: _"What are the causes of high blood pressure?"_

> **Bot**: _"High blood pressure, also known as hypertension, can be caused by several factors such as unhealthy diet, lack of exercise, obesity, genetics, and stress. For more updated research on treatments, would you like me to check the latest studies online?"_

---

## 🤝 Contributing

1. Fork the repo.
2. Create your feature branch: `git checkout -b feature-name`
3. Commit your changes: `git commit -m 'Add feature'`
4. Push to the branch: `git push origin feature-name`
5. Open a Pull Request.

---

## 📧 Contact

For issues, suggestions, or collaborations, reach out to:

> **Email**: ma2404374@gmail.com  
> **GitHub**: MuhammadAbdullah95(https://github.com/muhammadabdullah95)

---
