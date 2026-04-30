import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from database import get_schema, run_query
import re

load_dotenv()

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=os.getenv("GOOGLE_API_KEY"),
    temperature=0
)

SQL_PROMPT = PromptTemplate(
    input_variables=["schema", "question"],
    template="""
You are an expert SQL assistant. Given the database schema below, write a valid SQLite SQL query to answer the user's question.

SCHEMA:
{schema}

RULES:
- Return ONLY the raw SQL query
- No explanations, no markdown, no backticks, no code blocks
- Use only tables and columns that exist in the schema above
- Always use proper JOINs when data spans multiple tables
- Never use DELETE, DROP, INSERT, or UPDATE statements

USER QUESTION:
{question}

SQL QUERY:
"""
)

SUMMARY_PROMPT = PromptTemplate(
    input_variables=["question", "sql", "results"],
    template="""
You are a helpful data analyst assistant.

The user asked: {question}
The SQL query run was: {sql}
The results were: {results}

Write a clear, concise business-friendly answer in 2-3 lines based on the results.
Do not repeat the SQL. Just explain what the data shows.
"""
)

def clean_sql(raw: str) -> str:
    cleaned = re.sub(r"```(?:sql)?", "", raw, flags=re.IGNORECASE)
    cleaned = cleaned.replace("```", "").strip()
    return cleaned

def ask(question: str) -> dict:
    try:
        schema = get_schema()

        # Step 1: Generate SQL
        sql_chain = SQL_PROMPT | llm
        raw_sql = sql_chain.invoke({
            "schema": schema,
            "question": question
        }).content

        sql = clean_sql(raw_sql)

        # Step 2: Run SQL
        df = run_query(sql)

        # Step 3: Generate Summary
        summary_chain = SUMMARY_PROMPT | llm
        summary = summary_chain.invoke({
            "question": question,
            "sql": sql,
            "results": df.to_string()
        }).content

        return {
            "success": True,
            "sql": sql,
            "dataframe": df,
            "summary": summary
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "sql": None,
            "dataframe": None,
            "summary": None
        }