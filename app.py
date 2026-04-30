import streamlit as st
from agent import ask
from database import init_db

# Page config
st.set_page_config(
    page_title="SQL Agent",
    page_icon="🤖",
    layout="wide"
)

# Initialize DB once
init_db()

# Header
st.title("🤖 LLM-Powered SQL Agent")
st.markdown("Ask any business question in plain English and get instant answers from the database.")
st.divider()

# Sidebar - Schema Info
with st.sidebar:
    st.header("📊 Database Tables")
    st.markdown("""
    - **customers** — name, email, city, signup date
    - **products** — name, category, price, stock
    - **orders** — customer, date, status, amount
    - **order_items** — order, product, quantity, price
    """)

    st.divider()
    st.header("💡 Try These Questions")
    examples = [
        "Show all customers from Delhi",
        "Which product has the highest price?",
        "How many orders were delivered?",
        "What is the total revenue from all orders?",
        "Show me all cancelled orders with customer names",
        "Which city has the most customers?",
        "List all electronics products under 50000",
        "Who placed the most orders?"
    ]
    for ex in examples:
        if st.button(ex, use_container_width=True):
            st.session_state.question = ex

# Main - Question Input
question = st.text_input(
    "💬 Ask your question:",
    value=st.session_state.get("question", ""),
    placeholder="e.g. What is the total revenue from delivered orders?",
    key="input"
)

if st.button("🔍 Run Query", type="primary", use_container_width=True):
    if not question.strip():
        st.warning("Please enter a question first!")
    else:
        with st.spinner("Thinking..."):
            result = ask(question)

        if result["success"]:
            # Summary
            st.success("✅ Answer Ready")
            st.markdown("### 📝 Summary")
            st.info(result["summary"])

            # SQL
            st.markdown("### 🔧 Generated SQL")
            st.code(result["sql"], language="sql")

            # Results Table
            st.markdown("### 📊 Query Results")
            if result["dataframe"] is not None and not result["dataframe"].empty:
                st.dataframe(result["dataframe"], use_container_width=True)
                st.caption(f"Returned {len(result['dataframe'])} row(s)")
            else:
                st.warning("Query returned no results.")
        else:
            st.error("❌ Something went wrong")
            st.code(result["error"])

# Chat history
if "history" not in st.session_state:
    st.session_state.history = []

if st.button("🔍 Run Query", key="run2"):
    pass  # handled above

st.divider()
st.caption("Built with LangChain + Google Gemini + Streamlit | LLM-Powered SQL Agent")