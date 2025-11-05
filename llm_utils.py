# llm_utils.py
import google.generativeai as genai
import os
import sqlite3
import pandas as pd
import re
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
DB_PATH = "inventory.db"

def fix_window_function_sql(query: str) -> str:
    # If window functions are used in WHERE, wrap into CTE
    if "lag(" in query.lower() and "where" in query.lower():
        core = re.sub(r"(?is)^select", "SELECT", query)
        return f"WITH base AS ({core}) SELECT * FROM base;"
    return query

def run_safe_sql(query: str) -> pd.DataFrame:
    """Safely execute read-only SQL queries (supports WITH, SELECT, window functions)."""
    q_lower = query.lower().strip()

    # Basic safety rules
    forbidden = ["update", "delete", "insert", "drop", "alter", "create", 
                 "replace", "attach", "detach", "pragma", "vacuum"]
    if any(word in q_lower for word in forbidden):
        raise ValueError("❌ Query blocked: write operations are not allowed.")

    # Must begin with SELECT or WITH
    if not (q_lower.startswith("select") or q_lower.startswith("with")):
        raise ValueError("❌ Only SELECT or WITH queries are allowed.")

    # Connect and run
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

def call_gemini(user_query: str) -> str:

    sql_prompt = f"""
    You are an expert SQL analyst for an inventory management system.
    Database schema:
    - inventory_current(item_name TEXT, stock_count INTEGER, last_updated TEXT)
    - inventory_log(id INTEGER, timestamp TEXT, image_id TEXT, item_name TEXT, count INTEGER)

    User question: "{user_query}"

    Generate the most relevant SQL SELECT query to retrieve the data needed to answer it.
    Return ONLY the SQL query. Do not include explanations.
    """

    try:
        model = genai.GenerativeModel("gemini-2.5-flash")
        sql_response = model.generate_content(sql_prompt)
        sql_query = sql_response.text.strip().strip("```sql").strip("```").strip()

        sql_query = re.sub(r"```.*?```", "", sql_query).strip()
        sql_query = sql_query.split(";")[0] + ";" if ";" not in sql_query else sql_query
        sql_query = fix_window_function_sql(sql_query)
        print(f"[DEBUG] Generated SQL: {sql_query}")

        try:
            df = run_safe_sql(sql_query)
        except Exception as e:
            return f"⚠️ Gemini generated invalid SQL:\n```\n{sql_query}\n```\nError: {str(e)}"

        if df.empty:
            data_summary = "No rows found for this query."
        else:
            data_summary = df.head(10).to_markdown(index=False)

        answer_prompt = f"""
        You are an inventory analyst assistant.
        The following table is the SQL query result:

        {data_summary}

        Based on this, answer the original user question:
        "{user_query}"

        Give a short, clear explanation with insights.
        """
        answer_response = model.generate_content(answer_prompt)
        return answer_response.text.strip()

    except Exception as e:
        return f"❌ Error communicating with Gemini: {e}"
