# 🤖 LLM-Powered SQL Agent

A natural language interface for querying SQL databases using Google Gemini + LangChain + Streamlit.
Ask business questions in plain English and get instant SQL queries, results, and AI-generated summaries.

---

## 🚀 Demo

> "Show me all cancelled orders with customer names"
> "Which city has the most customers?"
> "What is the total revenue from delivered orders?"

The agent understands your question → writes SQL → runs it → explains the result in plain English.

---

## 🧠 How It Works

User Question (Natural Language)
↓
Google Gemini LLM (Text-to-SQL)
↓
SQL Query Executed on SQLite Database
↓
Results + AI Business Summary
↓
Streamlit UI (Interactive Dashboard)

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| LLM | Google Gemini 2.5 Flash |
| Orchestration | LangChain |
| Database | SQLite via SQLAlchemy |
| Frontend | Streamlit |
| Language | Python 3.x |

---

## 📊 Database Schema

The project uses a sample e-commerce database with 4 tables:

- **customers** — customer details, city, signup date
- **products** — name, category, price, stock
- **orders** — order date, status, total amount
- **order_items** — product, quantity, unit price

---

## ⚙️ Setup & Installation

### 1. Clone the repository
```bash
git clone https://github.com/LakshayHasija/SQL-Agent.git
cd SQL-Agent
```

### 2. Create virtual environment
```bash
python -m venv venv
venv\Scripts\activate  # Windows
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Set up environment variables
Create a `.env` file in the root directory:

GOOGLE_API_KEY=your_gemini_api_key_here

Get your free API key at [aistudio.google.com](https://aistudio.google.com)

### 5. Initialize the database
```bash
python database.py
```

### 6. Run the app
```bash
streamlit run app.py
```

---

## 💡 Example Questions You Can Ask

- What is the total revenue from all orders?
- Show me all customers from Delhi
- Which product has the highest price?
- How many orders were delivered vs cancelled?
- Who placed the most orders?
- List all electronics products under ₹50,000

---

## 🔑 Key Features

- **Natural Language to SQL** — No SQL knowledge needed
- **AI Business Summaries** — Results explained in plain English
- **Query Validation** — Prevents harmful queries (DROP, DELETE etc.)
- **Interactive UI** — Clean Streamlit dashboard with example questions
- **Modular Architecture** — Easily swap database or LLM provider

---

## 📁 Project Structure

sql-agent/
├── app.py          # Streamlit UI
├── agent.py        # LLM + SQL orchestration logic
├── database.py     # DB schema, sample data, query runner
├── requirements.txt
└── .gitignore

---

## 🔮 Future Improvements

- Support for PostgreSQL / MySQL databases
- Multi-turn conversational memory
- Chart generation from query results
- Authentication for multi-user access