import os
import pandas as pd
import uuid
import random
from datetime import datetime, timedelta

DATA_DIR = "data"
os.makedirs(DATA_DIR, exist_ok=True)

def get_empty_df(columns):
    return pd.DataFrame({col: pd.Series(dtype=dtype) for col, dtype in columns.items()})

def random_date(start_days_ago=30):
    date = datetime.now() - timedelta(days=random.randint(0, start_days_ago))
    return date.strftime("%Y-%m-%d")

# Schemas
projects_cols = {'PROJECT_ID': 'str', 'TITLE': 'str', 'CLIENT': 'str', 'TEAM_LEAD': 'str', 'STATUS': 'str', 'PROGRESS': 'int', 'START_DATE': 'object', 'END_DATE': 'object', 'COMPUTE_HOURS': 'int', 'OFFICE': 'str', 'NOTES': 'str'}
project_tasks_cols = {'TASK_ID': 'str', 'PROJECT_ID': 'str', 'FILE_NAME': 'str', 'SERVER_USED': 'str', 'STATUS': 'str', 'PROGRESS': 'int', 'LAST_UPDATED': 'object'}
students_cols = {'STUDENT_ID': 'str', 'NAME': 'str', 'EMAIL': 'str', 'STATUS': 'str', 'SKILLS': 'str', 'ENROLLMENT': 'object', 'OFFICE': 'str'}
team_cols = {'MEMBER_ID': 'str', 'NAME': 'str', 'EMAIL': 'str', 'ROLE': 'str', 'EXPERTISE': 'str', 'JOIN_DATE': 'object'}
servers_cols = {'SERVER_NAME': 'str', 'IP_ADDRESS': 'str', 'GPU_SPECS': 'str', 'CURRENT_USER': 'str', 'STATUS': 'str', 'LOAD_PERCENT': 'int'}

def save_df(df, filename):
    filepath = os.path.join(DATA_DIR, f"{filename}.csv")
    df.to_csv(filepath, index=False)

def load_or_create(filename, schema_cols, generator_func):
    filepath = os.path.join(DATA_DIR, f"{filename}.csv")
    if os.path.exists(filepath):
        df = pd.read_csv(filepath)
        # Ensure correct types after loading
        for col, dtype in schema_cols.items():
            if col in df.columns:
                if dtype == 'int':
                    df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0).astype(int)
                else:
                    df[col] = df[col].astype(str)
                    df.loc[df[col] == 'nan', col] = '' # Handle NaN strings
        return df
    else:
        df = generator_func()
        save_df(df, filename)
        return df

# Generators
def generate_projects():
    data = []
    clients = ["Biome", "PharmaTech", "Ooty Univ", "BioSim", "NatureMed", "GenoCorp", "CellTech", "ViroSolve"]
    leads = ["Dr. Vivek C.", "Dr. Priya R.", "Mr. John D.", "Dr. Alice S.", "Dr. Kumar M."]
    offices = ["Ooty", "Coimbatore"]
    statuses = ["Active", "Active", "Active", "Queued", "Completed", "On Hold"]
    titles = [
        "Network Pharmacology, molecular docking and toxicity analysis using SwissADME",
        "TNBC Project",
        "Sumetha-SIET",
        "Dual Dockign and Dynamics [100ns] - MMP9 [4XCT]",
        "Virtual Screening DB", "QSAR Analysis of Flavonoids", "Protein Folding Simulation",
        "Ligand Binding Affinity", "RNA Seq Analysis", "CRISPR Target Prediction"
    ]
    
    # Specific records from screenshot
    screenshot_data = [
        ["PRJ-8E350ED1", "Network Pharmacology, molecular docking and toxicity analysis using SwissADME", "Swetha G", "Dr. Vivek C.", "Completed", 100, "2026-02-01", "2026-02-15", 450, "Coimbatore", "Excellent results"],
        ["PRJ-FA7BCFD8", "TNBC Project", "Dr. George", "Dr. Priya R.", "Active", 75, "2026-02-05", "", 200, "Coimbatore", "In progress"],
        ["PRJ-E477AD12", "Sumetha-SIET", "Ms. Sumnetha", "Dr. Vivek C.", "Completed", 100, "2026-02-10", "2026-02-20", 300, "Coimbatore", "Finalized"],
        ["PRJ-DD5CB96F", "Dual Dockign and Dynamics [100ns] - MMP9 [4XCT]", "Ms. Madhumitha", "Dr. Vivek C.", "Completed", 100, "2026-02-12", "2026-02-25", 600, "Coimbatore", "Simulation stable"]
    ]
    
    for row in screenshot_data:
        data.append(row)

    for i in range(26):
        status = random.choice(statuses)
        progress = 100 if status == "Completed" else (0 if status == "Queued" else random.choice([25, 50, 75]))
        data.append([
            f"PRJ-{uuid.uuid4().hex[:6].upper()}", 
            f"{random.choice(titles)} {i}", 
            random.choice(clients), 
            random.choice(leads), 
            status, 
            progress, 
            random_date(120), 
            random_date(10) if status == "Completed" else "", 
            random.randint(50, 1000), 
            random.choice(offices), 
            "Routine analysis"
        ])
    return pd.DataFrame(data, columns=projects_cols.keys())

def generate_servers():
    data = [
        ["NODE-01-GPU", "192.168.1.101", "2x RTX 3090 24GB", "Auto-scheduler", "Running Workload", 85],
        ["NODE-02-GPU", "192.168.1.102", "4x RTX 4090 24GB", "Dr. Vivek C.", "Running Workload", 92],
        ["NODE-03-CPU", "192.168.1.103", "Threadripper 64-Core", "Idle", "Idle", 5],
        ["MASTER-NODE", "192.168.1.100", "Dual Xeon EPYC", "System", "Running Workload", 40],
        ["NODE-04-GPU", "192.168.1.104", "1x RTX 3070 Ti", "Dr. Priya R.", "Running Workload", 60]
    ]
    return pd.DataFrame(data, columns=servers_cols.keys())

def generate_tasks():
    proj_df = generate_projects()
    serv_df = generate_servers()
    servers = serv_df['SERVER_NAME'].tolist()
    data = []
    for idx, row in proj_df.iterrows():
        if row['STATUS'] == 'Active':
            data.append([f"TSK-{uuid.uuid4().hex[:5].upper()}", row['PROJECT_ID'], f"step1_em.in", random.choice(servers), "Running", random.randint(30, 90), datetime.now().strftime("%Y-%m-%d %H:%M")])
            data.append([f"TSK-{uuid.uuid4().hex[:5].upper()}", row['PROJECT_ID'], f"step2_nvt.in", random.choice(servers), "Queued", 0, datetime.now().strftime("%Y-%m-%d %H:%M")])
        elif row['STATUS'] == 'Completed':
            data.append([f"TSK-{uuid.uuid4().hex[:5].upper()}", row['PROJECT_ID'], f"production.in", random.choice(servers), "Completed", 100, datetime.now().strftime("%Y-%m-%d %H:%M")])
    return pd.DataFrame(data, columns=project_tasks_cols.keys())

def generate_students():
    data = [
        [f"ISO-{uuid.uuid4().hex[:4].upper()}", "Rahul Sharma", "rahul@gmail.com", "Active", "Python, Docking", random_date(100), "Ooty"],
        [f"ISO-{uuid.uuid4().hex[:4].upper()}", "Sneha Patel", "sneha@gmail.com", "Active", "GROMACS, Linux", random_date(80), "Coimbatore"],
        [f"ISO-{uuid.uuid4().hex[:4].upper()}", "Arun Kumar", "arun.k@yahoo.com", "Graduated", "MD Simulations", random_date(300), "Ooty"],
        [f"ISO-{uuid.uuid4().hex[:4].upper()}", "Divya R.", "divya@univ.edu", "Active", "Machine Learning", random_date(40), "Coimbatore"],
        [f"ISO-{uuid.uuid4().hex[:4].upper()}", "Karthik N.", "knarthik@gmail.com", "Active", "Cheminformatics", random_date(10), "Ooty"]
    ]
    return pd.DataFrame(data, columns=students_cols.keys())

def generate_team():
    data = [
        [f"T-{uuid.uuid4().hex[:4].upper()}", "Dr. Vivek Chandramohan", "vivek@insilicomics.com", "PI / Lead", "Molecular Dynamics", random_date(1000)],
        [f"T-{uuid.uuid4().hex[:4].upper()}", "Dr. Priya Raj", "priya@insilicomics.com", "Senior Engineer", "Virtual Screening", random_date(800)],
        [f"T-{uuid.uuid4().hex[:4].upper()}", "Mr. Sameer Sharma", "sameer@insilicomics.com", "System Admin", "Server Infrastructure", random_date(500)],
        [f"T-{uuid.uuid4().hex[:4].upper()}", "Ms. Ananya L.", "ananya@insilicomics.com", "Research Scientist", "QSAR & AI", random_date(200)]
    ]
    return pd.DataFrame(data, columns=team_cols.keys())

# Getters
def get_projects_df(): return load_or_create('projects', projects_cols, generate_projects)
def get_servers_df(): return load_or_create('servers', servers_cols, generate_servers)
def get_project_tasks_df(): return load_or_create('project_tasks', project_tasks_cols, generate_tasks)
def get_students_df(): return load_or_create('students', students_cols, generate_students)
def get_team_df(): return load_or_create('team', team_cols, generate_team)
