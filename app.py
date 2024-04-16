import os
from dataclasses import dataclass

import streamlit as st
import psycopg2
from dotenv import load_dotenv

load_dotenv()

con = psycopg2.connect(os.getenv("DATABASE_URL"))
cur = con.cursor()

cur.execute(
    """
    CREATE TABLE IF NOT EXISTS prompts (
        id SERIAL PRIMARY KEY,
        title TEXT NOT NULL,
        prompt TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """
)

con.commit()

@dataclass
class Prompt:
    title: str
    prompt: str

def prompt_form(prompt=Prompt("","")):
    """
    TODO: Add validation to the form, so that the title and prompt are required.
    """
    with st.form(key="prompt_form", clear_on_submit=True):
        title = st.text_input("Title", value=prompt.title)
        prompt = st.text_area("Prompt", height=200, value=prompt.prompt)
        submitted = st.form_submit_button("Submit")
        # Validation for non-empty fields
        if submitted:
            if title and prompt:  # Validation for non-empty fields
                return Prompt(title, prompt)
            else:
                st.error("Both title and prompt are required.")
                return None        

st.title("Promptbase")
st.subheader("A simple app to store and retrieve prompts")

prompt = prompt_form()
if prompt:
    cur.execute("INSERT INTO prompts (title, prompt) VALUES (%s, %s)", (prompt.title, prompt.prompt,))
    con.commit()
    st.success("Prompt added successfully!")

cur.execute("SELECT * FROM prompts")
prompts = cur.fetchall()

# TODO: Add a search bar
search_query = st.text_input("Search prompts")
sort_order = st.selectbox("Sort by date", ["Newest first", "Oldest first"])

# TODO: Add a sort by date
order_sql = "DESC" if sort_order == "Newest first" else "ASC"
search_sql = f"%{search_query}%"
cur.execute("SELECT * FROM prompts WHERE title LIKE %s OR prompt LIKE %s ORDER BY created_at " + order_sql, (search_sql, search_sql))
prompts = cur.fetchall()

# TODO: Add favorite button
for p in prompts:
    with st.expander(p[1]):
        st.code(p[2])
        # TODO: Add a edit function
        if st.button("Delete", key=p[0]):
            cur.execute("DELETE FROM prompts WHERE id = %s", (p[0],))
            con.commit()
            st.rerun()

            