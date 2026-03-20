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

def save_record(table_name, record, on_conflict=None):
    supabase = get_supabase()
    if on_conflict:
        supabase.table(table_name).upsert(record, on_conflict=on_conflict).execute()
    else:
        supabase.table(table_name).upsert(record).execute()

def delete_record(table_name, id_col, id_val):
    supabase = get_supabase()
    supabase.table(table_name).delete().eq(id_col, id_val).execute()
