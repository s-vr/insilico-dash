import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import io
import uuid
import sample_data

# Page config
st.set_page_config(page_title="Insilicomics Lab Management", page_icon="🧪", layout="wide", initial_sidebar_state="expanded")

# Advanced UI/UX CSS
st.markdown(u"""
<style>
    /* Global Styles */
    .stApp { background-color: var(--background-color); }
    .primary-text { color: #10B981; }
    
    /* Neumorphic Cards */
    .glass-card {
        background: var(--secondary-background-color);
        border-radius: 16px;
        padding: 24px;
        margin-bottom: 24px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
        border: 1px solid rgba(255,255,255,0.1);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    .glass-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
    }
    
    /* Metric styling inside cards */
    .metric-title { font-size: 0.875rem; color: #6B7280; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 0.5rem; }
    .metric-value { font-size: 2.25rem; font-weight: 800; color: var(--text-color); margin: 0; line-height: 1.2; }
    .metric-icon { font-size: 2rem; float: right; opacity: 0.8; }
    
    /* Header gradients */
    .gradient-text {
        background: linear-gradient(90deg, #10B981, #3B82F6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: bold;
    }
    
    /* Custom spacing */
    .stTabs [data-baseweb="tab-list"] { gap: 24px; }
    .stTabs [data-baseweb="tab"] { height: 50px; white-space: pre-wrap; background-color: transparent; border-radius: 4px; padding: 10px 20px;}
    .stTabs [aria-selected="true"] { background-color: rgba(16, 185, 129, 0.1); border-bottom: 3px solid #10B981 !important; color: #10B981; font-weight: bold;}
    
    /* Expander styling for internal project views */
    .streamlit-expanderHeader { background-color: rgba(59, 130, 246, 0.1); border-radius: 8px; font-weight: bold;}
</style>
""", unsafe_allow_html=True)

# User Database
USERS_DB = {
    "admin@insilicomics.com": {"password": "admin", "name": "Admin User"},
    "vishnu@insilicomics.com": {"password": "password123", "name": "Vishnu Raj"},
    "demo@insilicomics.com": {"password": "demo", "name": "Demo User"}
}

# Session State Initialization & Persistent Load
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.current_user = {"name": "", "email": ""}
    st.session_state.current_page = 'Dashboard'
    
    # Load from persistence (CSV files)
    st.session_state.projects_df = sample_data.get_projects_df()
    st.session_state.project_tasks_df = sample_data.get_project_tasks_df()
    st.session_state.students_df = sample_data.get_students_df()
    st.session_state.team_df = sample_data.get_team_df()
    st.session_state.servers_df = sample_data.get_servers_df()

# Helper for saving state
def update_state_and_save(key, df, filename):
    st.session_state[key] = df
    sample_data.save_df(df, filename)

def login_page():
    st.markdown("<br><br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 1.2, 1])
    with col2:
        st.markdown("<div class='glass-card' style='text-align: center;'>", unsafe_allow_html=True)
        st.markdown("<h1 class='gradient-text' style='font-size: 3rem; margin-bottom:0;'>Insilicomics</h1>", unsafe_allow_html=True)
        st.markdown("<p style='color: #6B7280; font-size: 1.2rem;'>Advanced Lab Management System</p><hr>", unsafe_allow_html=True)
        
        with st.form("login_form"):
            email = st.text_input("Work Email", placeholder="admin@insilicomics.com")
            password = st.text_input("Password", type="password")
            submit = st.form_submit_button("Secure Login", use_container_width=True)
            
            if submit:
                if email in USERS_DB and USERS_DB[email]["password"] == password:
                    st.session_state.logged_in = True
                    st.session_state.current_user = {"name": USERS_DB[email]["name"], "email": email}
                    st.rerun()
                else:
                    st.error("Authentication Failed. Please check credentials.")
        st.markdown("<p style='font-size: 0.8rem; color: #9CA3AF; margin-top: 20px;'>Demo: admin@insilicomics.com / admin</p>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

def render_sidebar():
    with st.sidebar:
        st.markdown(f"<h2 class='gradient-text' style='text-align:center;'>🧪 Insilicomics</h2>", unsafe_allow_html=True)
        st.markdown("<hr style='margin-top:0;'>", unsafe_allow_html=True)
        
        pages = {
            "Dashboard": "🏠", 
            "Projects Center": "🔬", 
            "Server Infrastructure": "🖥️", 
            "Core Team": "👥",
            "Students": "🎓", 
            "Reports": "📊"
        }
        
        for page, icon in pages.items():
            is_active = st.session_state.current_page == page
            btn_type = "primary" if is_active else "secondary"
            if st.button(f"{icon}  {page}", key=f"nav_{page}", use_container_width=True, type=btn_type):
                st.session_state.current_page = page
                st.rerun()
                
        st.markdown("<div style='position: fixed; bottom: 20px; width: 100%;'>", unsafe_allow_html=True)
        st.markdown("<hr>", unsafe_allow_html=True)
        st.markdown(f"<div style='display:flex; align-items:center;'><div style='width:30px; height:30px; border-radius:50%; background:#10B981; color:white; text-align:center; line-height:30px; margin-right:10px;'>{st.session_state.current_user['name'][0]}</div><div><b>{st.session_state.current_user['name']}</b><br><small>{st.session_state.current_user['email']}</small></div></div>", unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.logged_in = False
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

def create_glass_metric(label, value, icon, color="#10B981"):
    return f"""
    <div class="glass-card" style="border-top: 4px solid {color}; padding: 15px 20px;">
        <div class="metric-icon" style="color: {color};">{icon}</div>
        <div class="metric-title">{label}</div>
        <div class="metric-value">{value}</div>
    </div>
    """

def dashboard_page():
    st.markdown("<h1 class='gradient-text'>Global Command Center</h1>", unsafe_allow_html=True)
    
    proj_df = st.session_state.projects_df
    stud_df = st.session_state.students_df
    serv_df = st.session_state.servers_df
    team_df = st.session_state.team_df

    c1, c2, c3, c4 = st.columns(4)
    with c1: st.markdown(create_glass_metric("Total Research Projects", len(proj_df), "🔬", "#3B82F6"), unsafe_allow_html=True)
    with c2: st.markdown(create_glass_metric("Compute Servers", len(serv_df), "🖥️", "#8B5CF6"), unsafe_allow_html=True)
    with c3: st.markdown(create_glass_metric("Core Team", len(team_df), "👥", "#EF4444"), unsafe_allow_html=True)
    with c4: st.markdown(create_glass_metric("Total Students", len(stud_df), "🎓", "#F59E0B"), unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    
    tab_overview, tab_projects, tab_servers = st.tabs(["🌐 Master Overview", "🔬 Projects Analytics", "🖥️ Server Metrics"])
    
    with tab_overview:
        col_plot3, col_plot4 = st.columns(2)
        with col_plot3:
            st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
            st.markdown("### 📍 Location Demographics")
            if not stud_df.empty and 'OFFICE' in stud_df.columns and not proj_df.empty:
                o_p = len(proj_df[proj_df['OFFICE'] == 'Ooty'])
                c_p = len(proj_df[proj_df['OFFICE'] == 'Coimbatore'])
                o_s = len(stud_df[stud_df['OFFICE'] == 'Ooty'])
                c_s = len(stud_df[stud_df['OFFICE'] == 'Coimbatore'])
                
                demo_data = pd.DataFrame({
                    "Office": ["Ooty", "Ooty", "Coimbatore", "Coimbatore"],
                    "Category": ["Projects", "Students", "Projects", "Students"],
                    "Count": [o_p, o_s, c_p, c_s]
                })
                
                fig3 = px.sunburst(demo_data, path=['Office', 'Category'], values='Count',
                                  color='Office', color_discrete_map={'Ooty': '#10B981', 'Coimbatore': '#3B82F6'},
                                  template="plotly_dark" if st.get_option("theme.base") == "dark" else "plotly_white")
                fig3.update_layout(height=350, margin=dict(t=10, b=10, l=10, r=10), paper_bgcolor='rgba(0,0,0,0)')
                st.plotly_chart(fig3, use_container_width=True)
            else:
                st.info("Awaiting demographic data.")
            st.markdown("</div>", unsafe_allow_html=True)

        with col_plot4:
            st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
            st.markdown("### ⚡ Global Execution Task Status")
            tasks_df = st.session_state.project_tasks_df
            if not tasks_df.empty and 'STATUS' in tasks_df.columns:
                fig4 = px.pie(tasks_df, names='STATUS', hole=0.5,
                             color='STATUS', color_discrete_map={'Running': '#3B82F6', 'Queued': '#F59E0B', 'Completed': '#10B981', 'Failed': '#EF4444'},
                             template="plotly_dark" if st.get_option("theme.base") == "dark" else "plotly_white")
                fig4.update_traces(textposition='inside', textinfo='percent+label')
                fig4.update_layout(height=350, margin=dict(t=10, b=10, l=10, r=10), showlegend=False, paper_bgcolor='rgba(0,0,0,0)')
                st.plotly_chart(fig4, use_container_width=True)
            else:
                st.info("Awaiting project task status data.")
            st.markdown("</div>", unsafe_allow_html=True)

    with tab_projects:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.markdown("### 📈 Project Progress Pipeline")
        if not proj_df.empty and 'PROGRESS' in proj_df.columns:
            tasks_df = st.session_state.project_tasks_df
            if not tasks_df.empty:
                active_tasks = tasks_df[tasks_df['STATUS'].isin(['Running', 'Queued'])]
                if not active_tasks.empty:
                    files_agg = active_tasks.groupby('PROJECT_ID')['FILE_NAME'].apply(lambda x: ', '.join(x)).reset_index()
                    plot_df = pd.merge(proj_df, files_agg, on='PROJECT_ID', how='left')
                    plot_df['FILE_NAME'] = plot_df['FILE_NAME'].fillna('None')
                else:
                    plot_df = proj_df.copy()
                    plot_df['FILE_NAME'] = 'None'
            else:
                plot_df = proj_df.copy()
                plot_df['FILE_NAME'] = 'None'

            fig1 = px.bar(plot_df, x='TITLE', y='PROGRESS', color='OFFICE', 
                         color_discrete_map={'Ooty': '#10B981', 'Coimbatore': '#3B82F6'},
                         text='PROGRESS', hover_data=['STATUS', 'FILE_NAME'],
                         template="plotly_dark" if st.get_option("theme.base") == "dark" else "plotly_white")
            fig1.update_traces(texttemplate='%{text}%', textposition='outside', marker_line_width=1.5, opacity=0.8)
            fig1.update_layout(yaxis_range=[0, 110], margin=dict(t=30, b=0, l=0, r=0), height=400, plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig1, use_container_width=True)
        else:
            st.info("Awaiting project data to generate pipeline view.")
        st.markdown("</div>", unsafe_allow_html=True)
        
    with tab_servers:
        col_s1, col_s2 = st.columns(2)
        with col_s1:
            st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
            st.markdown("### 🖥️ Server Load Distribution")
            if not serv_df.empty and 'LOAD_PERCENT' in serv_df.columns:
                fig2 = go.Figure(go.Indicator(
                    mode = "gauge+number",
                    value = serv_df['LOAD_PERCENT'].mean() if not serv_df['LOAD_PERCENT'].empty else 0,
                    title = {'text': "Average Cluster Load"},
                    gauge = {
                        'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': "darkblue"},
                        'bar': {'color': "#8B5CF6"},
                        'bgcolor': "rgba(255,255,255,0.1)",
                        'steps': [
                            {'range': [0, 50], 'color': "rgba(16, 185, 129, 0.2)"},
                            {'range': [50, 80], 'color': "rgba(245, 158, 11, 0.2)"},
                            {'range': [80, 100], 'color': "rgba(239, 68, 68, 0.2)"}],
                    }
                ))
                fig2.update_layout(height=350, margin=dict(t=50, b=0, l=20, r=20), font=dict(color='gray'), paper_bgcolor='rgba(0,0,0,0)')
                st.plotly_chart(fig2, use_container_width=True)
            else:
                st.info("Awaiting server metrics.")
            st.markdown("</div>", unsafe_allow_html=True)
            
        with col_s2:
            st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
            st.markdown("### 📊 Individual Node Load")
            if not serv_df.empty and 'LOAD_PERCENT' in serv_df.columns:
                fig5 = px.bar(serv_df, x='SERVER_NAME', y='LOAD_PERCENT', color='STATUS',
                             color_discrete_map={'Running Workload': '#EF4444', 'Idle': '#10B981', 'Offline': '#6B7280'},
                             template="plotly_dark" if st.get_option("theme.base") == "dark" else "plotly_white")
                fig5.update_layout(yaxis_range=[0, 100], height=350, margin=dict(t=30, b=0, l=0, r=0), plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
                st.plotly_chart(fig5, use_container_width=True)
            else:
                st.info("Awaiting node data.")
            st.markdown("</div>", unsafe_allow_html=True)

def project_detail_view(office_name):
    st.markdown(f"### {office_name} Project Management")
    
    main_df = st.session_state.projects_df
    mask = main_df['OFFICE'] == office_name
    office_df = main_df[mask]
    
    # 1. Add New Project Form
    with st.expander(f"➕ Initialize New Project ({office_name})", expanded=False):
        with st.form(f"add_project_form_{office_name}"):
            c1, c2 = st.columns(2)
            with c1:
                title = st.text_input("Project Title *")
                client = st.text_input("Client / PI")
            with c2:
                team_lead = st.text_input("Assigned Lead")
                status = st.selectbox("Overall Status", ["Active", "Queued", "Completed", "Error", "On Hold"])
            
            c3, c4 = st.columns(2)
            with c3:
                start = st.date_input("Start Date")
                progress = st.slider("Overall Progress (%)", min_value=0, max_value=100, value=0)
            with c4:
                notes = st.text_area("System Notes / Updates")
                
            submitted = st.form_submit_button("Launch Project", use_container_width=True)
            if submitted and title:
                if title in st.session_state.projects_df['TITLE'].values:
                    st.error(f"A project named '{title}' already exists! Please use a unique name.")
                else:
                    new_id = f"PRJ-{uuid.uuid4().hex[:6].upper()}"
                    new_row = pd.DataFrame([{
                        'PROJECT_ID': new_id,
                        'TITLE': title,
                        'CLIENT': client,
                        'TEAM_LEAD': team_lead,
                        'STATUS': status,
                        'PROGRESS': progress,
                        'START_DATE': start.strftime("%Y-%m-%d"),
                        'NOTES': notes,
                        'OFFICE': office_name
                    }])
                    new_df = pd.concat([new_row, st.session_state.projects_df], ignore_index=True)
                    update_state_and_save('projects_df', new_df, 'projects')
                    st.toast(f"Project '{title}' launched successfully!")
                    st.rerun()
            elif submitted and not title:
                st.error("Project Title is required.")

    # 2. View/Edit Existing Projects
    if not office_df.empty:
        st.markdown("#### Top-Level Project Ledger")
        st.caption("Double-click cells to edit. To delete a project, click the far-left checkbox of the row and press the **Delete** or **Backspace** key on your keyboard.")
        
        cols_config = {
            "PROJECT_ID": st.column_config.TextColumn("ID", disabled=True, width="small"),
            "TITLE": st.column_config.TextColumn("Project Title", required=True),
            "PROGRESS": st.column_config.NumberColumn("Overall Completion (%)", min_value=0, max_value=100, step=1, format="%d%%"),
            "STATUS": st.column_config.SelectboxColumn("Status", options=["Active", "Queued", "Completed", "Error", "On Hold"]),
            "OFFICE": None # hidden
        }
        
        st.markdown("<div class='glass-card' style='padding:0; overflow:hidden;'>", unsafe_allow_html=True)
        edited_df = st.data_editor(
            office_df, 
            num_rows="dynamic",
            use_container_width=True,
            column_config=cols_config,
            hide_index=True,
            key=f"editor_proj_{office_name}"
        )
        st.markdown("</div>", unsafe_allow_html=True)
        
        if not edited_df.equals(office_df):
            new_df = pd.concat([main_df[~mask], edited_df], ignore_index=True)
            update_state_and_save('projects_df', new_df, 'projects')
            st.rerun()

        st.markdown("<hr>", unsafe_allow_html=True)
        st.markdown("### 📂 Execution Manager (Sub-Tasks & Running Files)")
        st.markdown("Select a project below to manage its specific running scripts, files, and server assignments.")
        
        project_titles = edited_df['TITLE'].tolist()
        selected_proj_title = st.selectbox("Select Project to manage internals:", ["-- Select Project --"] + project_titles, key=f"sel_proj_{office_name}")
        
        if selected_proj_title != "-- Select Project --":
            proj_id = edited_df[edited_df['TITLE'] == selected_proj_title].iloc[0]['PROJECT_ID']
            
            st.markdown(f"<div class='glass-card'>", unsafe_allow_html=True)
            st.markdown(f"#### ⚙️ Running Files for: {selected_proj_title}")
            
            # Form to add new file/task
            with st.form(f"add_task_form_{proj_id}"):
                c1, c2, c3 = st.columns(3)
                with c1:
                    file_name = st.text_input("File / Script Name *", placeholder="e.g. step1_md.in")
                with c2:
                    available_servers = ["None"] + st.session_state.servers_df['SERVER_NAME'].tolist()
                    server = st.selectbox("Assigned Server", available_servers)
                with c3:
                    task_status = st.selectbox("Status", ["Running", "Queued", "Completed", "Failed"])
                
                add_task = st.form_submit_button("Add File/Task to Project")
                if add_task and file_name:
                    new_task_id = f"TSK-{uuid.uuid4().hex[:5].upper()}"
                    new_task = pd.DataFrame([{
                        'TASK_ID': new_task_id,
                        'PROJECT_ID': proj_id,
                        'FILE_NAME': file_name,
                        'SERVER_USED': server,
                        'STATUS': task_status,
                        'PROGRESS': 0,
                        'LAST_UPDATED': datetime.now().strftime("%Y-%m-%d %H:%M")
                    }])
                    new_df = pd.concat([st.session_state.project_tasks_df, new_task], ignore_index=True)
                    update_state_and_save('project_tasks_df', new_df, 'project_tasks')
                    st.rerun()
            
            # Show existing tasks for this project
            task_mask = st.session_state.project_tasks_df['PROJECT_ID'] == proj_id
            proj_tasks_df = st.session_state.project_tasks_df[task_mask]
            
            if not proj_tasks_df.empty:
                st.markdown("**Active Executions Data:** (Double-click to edit progress/status)")
                
                task_cols_config = {
                    "TASK_ID": st.column_config.TextColumn("Task ID", disabled=True),
                    "PROJECT_ID": None, # hide
                    "FILE_NAME": st.column_config.TextColumn("File / Script", required=True),
                    "SERVER_USED": st.column_config.SelectboxColumn("Server", options=["None"] + st.session_state.servers_df['SERVER_NAME'].tolist()),
                    "STATUS": st.column_config.SelectboxColumn("Status", options=["Running", "Queued", "Completed", "Failed"]),
                    "PROGRESS": st.column_config.NumberColumn("File Progress (%)", min_value=0, max_value=100, step=1, format="%d%%"),
                    "LAST_UPDATED": st.column_config.TextColumn("Last Updated", disabled=True)
                }
                
                edited_tasks = st.data_editor(
                    proj_tasks_df,
                    num_rows="dynamic",
                    use_container_width=True,
                    hide_index=True,
                    column_config=task_cols_config,
                    key=f"task_editor_{proj_id}"
                )
                
                if not edited_tasks.equals(proj_tasks_df):
                    edited_tasks['LAST_UPDATED'] = datetime.now().strftime("%Y-%m-%d %H:%M")
                    main_tasks = st.session_state.project_tasks_df
                    new_df = pd.concat([main_tasks[~task_mask], edited_tasks], ignore_index=True)
                    update_state_and_save('project_tasks_df', new_df, 'project_tasks')
                    st.rerun()
            else:
                st.info("No files/scripts currently tracked under this project.")
                
            st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.info(f"No active projects in {office_name}. Use the form above to initialize one.")

def projects_page():
    st.markdown("<h1 class='gradient-text'>🔬 Projects Center</h1>", unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["📍 Ooty Facility", "📍 Coimbatore Facility"])
    with tab1:
        project_detail_view("Ooty")
    with tab2:
        project_detail_view("Coimbatore")

def team_page():
    st.markdown("<h1 class='gradient-text'>👥 Core Team Members</h1>", unsafe_allow_html=True)
    st.markdown("Global overview of the core leadership and engineering team. This is independent of student offices.")
    
    df = st.session_state.team_df
    
    with st.expander("➕ Onboard New Team Member"):
        with st.form("add_team"):
            c1, c2 = st.columns(2)
            with c1:
                name = st.text_input("Full Name *")
                email = st.text_input("Work Email")
            with c2:
                role = st.selectbox("Role", ["PI / Lead", "Senior Engineer", "System Admin", "Research Scientist"])
                expertise = st.text_input("Area of Expertise (e.g. Molecular Dynamics)")
            if st.form_submit_button("Onboard Member") and name:
                new_id = f"T-{uuid.uuid4().hex[:4].upper()}"
                new_row = pd.DataFrame([{'MEMBER_ID': new_id, 'NAME': name, 'EMAIL': email, 'ROLE': role, 'EXPERTISE': expertise, 'JOIN_DATE': datetime.now().strftime("%Y-%m-%d")}])
                new_df = pd.concat([new_row, st.session_state.team_df], ignore_index=True)
                update_state_and_save('team_df', new_df, 'team')
                st.rerun()

    cols_config = {
        "MEMBER_ID": st.column_config.TextColumn("ID", disabled=True),
        "NAME": st.column_config.TextColumn("Name", required=True),
        "EMAIL": st.column_config.TextColumn("Email"),
        "ROLE": st.column_config.SelectboxColumn("Role", options=["PI / Lead", "Senior Engineer", "System Admin", "Research Scientist"]),
        "EXPERTISE": st.column_config.TextColumn("Expertise")
    }
    
    st.markdown("<div class='glass-card' style='padding:0; overflow:hidden;'>", unsafe_allow_html=True)
    edited_df = st.data_editor(df, num_rows="dynamic", use_container_width=True, column_config=cols_config, hide_index=True, key="team_editor")
    st.markdown("</div>", unsafe_allow_html=True)
    
    if not edited_df.equals(df):
        update_state_and_save('team_df', edited_df, 'team')
        st.rerun()

def students_page():
    st.markdown("<h1 class='gradient-text'>🎓 Student Interns</h1>", unsafe_allow_html=True)
    st.markdown("Manage student interns segmented by their operational facility.")
    
    tab1, tab2 = st.tabs(["📍 Ooty Members", "📍 Coimbatore Members"])
    
    for tab, office_name in zip([tab1, tab2], ["Ooty", "Coimbatore"]):
        with tab:
            main_df = st.session_state.students_df
            mask = main_df['OFFICE'] == office_name
            office_df = main_df[mask].copy()
            
            with st.expander(f"➕ Enroll New Student ({office_name})"):
                with st.form(f"add_student_{office_name}"):
                    name = st.text_input("Student Name *")
                    skills = st.text_input("Skills (e.g. Python, Docking)")
                    if st.form_submit_button("Enroll") and name:
                        new_id = f"ISO-{uuid.uuid4().hex[:4].upper()}"
                        new_row = pd.DataFrame([{'STUDENT_ID': new_id, 'NAME': name, 'SKILLS': skills, 'OFFICE': office_name, 'STATUS': 'Active', 'ENROLLMENT': datetime.now().strftime("%Y-%m-%d"), 'EMAIL': ''}])
                        new_df = pd.concat([new_row, st.session_state.students_df], ignore_index=True)
                        update_state_and_save('students_df', new_df, 'students')
                        st.rerun()

            cols_config = {
                "STUDENT_ID": st.column_config.TextColumn("ID", disabled=True),
                "NAME": st.column_config.TextColumn("Full Name", required=True),
                "STATUS": st.column_config.SelectboxColumn("Status", options=["Active", "Graduated"]),
                "OFFICE": None
            }
            
            st.markdown("<div class='glass-card' style='padding:0; overflow:hidden;'>", unsafe_allow_html=True)
            edited_df = st.data_editor(office_df, num_rows="dynamic", use_container_width=True, column_config=cols_config, hide_index=True, key=f"stud_editor_{office_name}")
            st.markdown("</div>", unsafe_allow_html=True)
            
            if not edited_df.equals(office_df):
                edited_df['OFFICE'] = office_name
                new_df = pd.concat([main_df[~mask], edited_df], ignore_index=True)
                update_state_and_save('students_df', new_df, 'students')
                st.rerun()

def servers_page():
    st.markdown("<h1 class='gradient-text'>🖥️ Global Server Infrastructure</h1>", unsafe_allow_html=True)
    st.markdown("Unified view of all computational hardware across the company. Servers are shared resources.")
    
    df = st.session_state.servers_df
    
    with st.expander("➕ Add Hardware Node"):
        with st.form("add_server"):
            c1, c2 = st.columns(2)
            with c1:
                name = st.text_input("Server Name / Hostname *")
                specs = st.text_input("GPU / CPU Specs")
            with c2:
                ip = st.text_input("IP Address")
                load = st.slider("Initial Load %", 0, 100, 0)
            if st.form_submit_button("Register Server") and name:
                new_row = pd.DataFrame([{'SERVER_NAME': name, 'GPU_SPECS': specs, 'IP_ADDRESS': ip, 'LOAD_PERCENT': load, 'STATUS': 'Idle', 'CURRENT_USER': ''}])
                new_df = pd.concat([new_row, st.session_state.servers_df], ignore_index=True)
                update_state_and_save('servers_df', new_df, 'servers')
                st.rerun()

    cols_config = {
        "SERVER_NAME": st.column_config.TextColumn("Hostname / ID", required=True),
        "IP_ADDRESS": st.column_config.TextColumn("IP / Access"),
        "GPU_SPECS": st.column_config.TextColumn("Hardware Specs"),
        "CURRENT_USER": st.column_config.TextColumn("Reserved By"),
        "STATUS": st.column_config.SelectboxColumn("Status", options=["Idle", "Running Workload", "Maintenance", "Offline"], required=True),
        "LOAD_PERCENT": st.column_config.NumberColumn("Current Load (%)", min_value=0, max_value=100, step=1, format="%d%%")
    }
    
    st.markdown("<div class='glass-card' style='padding:0; overflow:hidden;'>", unsafe_allow_html=True)
    edited_df = st.data_editor(df, num_rows="dynamic", use_container_width=True, column_config=cols_config, hide_index=True, key="editor_servers")
    st.markdown("</div>", unsafe_allow_html=True)
    
    if not edited_df.equals(df):
        update_state_and_save('servers_df', edited_df, 'servers')
        st.rerun()

def reports_page():
    st.markdown("<h1 class='gradient-text'>📊 Analytics & Exports</h1>", unsafe_allow_html=True)
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    report_type = st.selectbox("Select Target Dataset", ["Projects Matrix", "Global Server Grid", "Core Team", "Student Roster"])
    st.markdown("</div>", unsafe_allow_html=True)

    df_map = {
        "Projects Matrix": st.session_state.projects_df,
        "Global Server Grid": st.session_state.servers_df,
        "Core Team": st.session_state.team_df,
        "Student Roster": st.session_state.students_df
    }
    df = df_map[report_type]

    st.dataframe(df, use_container_width=True, hide_index=True)
    
    if not df.empty:
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='Data_Export')
        excel_data = output.getvalue()
        st.download_button("📥 Download Secure Excel Report", data=excel_data, file_name=f"Insilicomics_{report_type.replace(' ', '_')}.xlsx", type="primary", use_container_width=True)

# Application Routing
if not st.session_state.logged_in:
    login_page()
else:
    render_sidebar()
    page = st.session_state.current_page
    
    if page == 'Dashboard': dashboard_page()
    elif page == 'Projects Center': projects_page()
    elif page == 'Server Infrastructure': servers_page()
    elif page == 'Core Team': team_page()
    elif page == 'Students': students_page()
    elif page == 'Reports': reports_page()
    else: st.info(f"Module '{page}' is initializing...")