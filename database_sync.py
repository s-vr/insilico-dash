import streamlit as st
from supabase import create_client

def get_supabase():
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_KEY"]
    return create_client(url, key)

def load_data(table_name):
    supabase = get_supabase()
    response = supabase.table(table_name).select("*").execute()
    return response.data

def save_record(table_name, record):
    supabase = get_supabase()
    supabase.table(table_name).insert(record).execute()

def delete_record(table_name, id_col, id_val):
    supabase = get_supabase()
    supabase.table(table_name).delete().eq(id_col, id_val).execute()
