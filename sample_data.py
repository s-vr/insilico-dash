import os
import pandas as pd
import uuid
import random
import streamlit as st
from datetime import datetime, timedelta

# Try to import cloud sync if Supabase secrets are set
try:
    from database_sync import load_data, save_record, delete_record
    # In Streamlit, secrets are accessed via st.secrets
    HAS_SUPABASE = "SUPABASE_URL" in st.secrets and "SUPABASE_KEY" in st.secrets
except:
    HAS_SUPABASE = False

DATA_DIR = "data"
os.makedirs(DATA_DIR, exist_ok=True)

# Schemas - Mapping app columns to DB columns
projects_cols = {'PROJECT_ID': 'str', 'TITLE': 'str', 'CLIENT': 'str', 'TEAM_LEAD': 'str', 'STATUS': 'str', 'PROGRESS': 'int', 'START_DATE': 'object', 'END_DATE': 'object', 'OFFICE': 'str', 'NOTES': 'str', 'PROJECT_TYPE': 'str', 'CLIENT_UNIVERSITY': 'str', 'REFERRED_BY': 'str'}
project_tasks_cols = {'TASK_ID': 'str', 'PROJECT_ID': 'str', 'FILE_NAME': 'str', 'SERVER_USED': 'str', 'STATUS': 'str', 'PROGRESS': 'int', 'LAST_UPDATED': 'object', 'ASSIGNED_TO': 'str', 'DURATION': 'str', 'START_DATE': 'object', 'END_DATE': 'object'}
students_cols = {'STUDENT_ID': 'str', 'NAME': 'str', 'EMAIL': 'str', 'STATUS': 'str', 'SKILLS': 'str', 'OFFICE': 'str'}
team_cols = {'MEMBER_ID': 'str', 'NAME': 'str', 'EMAIL': 'str', 'ROLE': 'str', 'EXPERTISE': 'str'}
servers_cols = {'SERVER_NAME': 'str', 'IP_ADDRESS': 'str', 'GPU_SPECS': 'str', 'CURRENT_USER': 'str', 'STATUS': 'str', 'LOAD_PERCENT': 'int'}
attendance_cols = {'DATE': 'object', 'NAME': 'str', 'ROLE_TYPE': 'str', 'OFFICE': 'str', 'STATUS': 'str'}

def save_df(df, filename):
    # Local Save (Backup)
    filepath = os.path.join(DATA_DIR, f"{filename}.csv")
    df.to_csv(filepath, index=False)
    
    # Cloud Sync
    if HAS_SUPABASE:
        try:
            # Table Map
            table_map = {
                'projects': 'projects', 
                'project_tasks': 'tasks', 
                'students': 'students', 
                'team': 'team', 
                'servers': 'servers',
                'attendance': 'attendance'
            }
            table_name = table_map.get(filename, filename)
            
            # Convert to records and lowercase keys for Postgres
            records = df.to_dict(orient='records')
            for r in records:
                # Filter out NaN and convert to compatible types
                db_record = {}
                for k, v in r.items():
                    val = v
                    if pd.isna(v): val = None
                    db_record[k.lower()] = val
                
                # Push to Supabase
                save_record(table_name, db_record)
        except Exception as e:
            st.error(f"Cloud Sync Error ({table_name}): {e}")

def load_or_create(filename, schema_cols, generator_func):
    if HAS_SUPABASE:
        try:
            table_map = {
                'projects': 'projects', 
                'project_tasks': 'tasks', 
                'students': 'students', 
                'team': 'team', 
                'servers': 'servers',
                'attendance': 'attendance'
            }
            table_name = table_map.get(filename, filename)
            data = load_data(table_name)
            if data and len(data) > 0:
                df = pd.DataFrame(data)
                df.columns = [c.upper() for c in df.columns]
                # Filter to expected columns and ensure types
                existing_cols = [c for c in schema_cols.keys() if c in df.columns]
                df = df[existing_cols]
                return df
        except Exception as e:
            print(f"Cloud load failed ({e}). Falling back to local.")

    filepath = os.path.join(DATA_DIR, f"{filename}.csv")
    if os.path.exists(filepath):
        df = pd.read_csv(filepath)
        for col, dtype in schema_cols.items():
            if col in df.columns:
                if dtype == 'int':
                    df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0).astype(int)
                else:
                    df[col] = df[col].astype(str)
                    df.loc[df[col] == 'nan', col] = ''
        return df
    else:
        df = generator_func()
        save_df(df, filename)
        return df

# Generators
def generate_projects(): return pd.DataFrame(columns=projects_cols.keys())
def generate_servers(): return pd.DataFrame(columns=servers_cols.keys())
def generate_tasks(): return pd.DataFrame(columns=project_tasks_cols.keys())
def generate_students(): return pd.DataFrame(columns=students_cols.keys())
def generate_team(): return pd.DataFrame(columns=team_cols.keys())
def generate_attendance(): return pd.DataFrame(columns=attendance_cols.keys())

# Getters
def get_projects_df(): return load_or_create('projects', projects_cols, generate_projects)
def get_servers_df(): return load_or_create('servers', servers_cols, generate_servers)
def get_project_tasks_df(): return load_or_create('project_tasks', project_tasks_cols, generate_tasks)
def get_students_df(): return load_or_create('students', students_cols, generate_students)
def get_team_df(): return load_or_create('team', team_cols, generate_team)
def get_attendance_df(): return load_or_create('attendance', attendance_cols, generate_attendance)
