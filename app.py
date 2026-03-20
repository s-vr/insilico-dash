import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from datetime import datetime
import io
import uuid
import os
import sample_data

# Page config
st.set_page_config(page_title="Insilicomics Lab Management", page_icon="🧪", layout="wide", initial_sidebar_state="expanded")

# Advanced UI/UX CSS & Heavy Graphics Enhancements
st.markdown(u"""

<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;800&display=swap');
    
    /* Global Styles */
    .stApp { 
        background-color: #05070a; 
        background-image: 
            radial-gradient(circle at 20% 20%, rgba(16, 185, 129, 0.05) 0%, transparent 40%),
            radial-gradient(circle at 80% 80%, rgba(59, 130, 246, 0.05) 0%, transparent 40%),
            radial-gradient(circle at 50% 50%, #0a0e17 0%, #05070a 100%); 
        color: #f1f5f9; 
        font-family: 'Inter', sans-serif !important;
    }
    
    /* Typography Refresh */
    h1, h2, h3, h4 { font-family: 'Inter', sans-serif !important; font-weight: 800 !important; letter-spacing: -0.03em !important; }
    p, label, .streamlit-expanderHeader { font-size: 1.05rem !important; color: #94a3b8; }
    h1 { font-size: 3.5rem !important; margin-bottom: 0.5rem !important; }
    
    /* The Ultimate Glass Card */
    .glass-card {
        background: rgba(15, 23, 42, 0.6);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border-radius: 24px;
        padding: 28px;
        margin-bottom: 24px;
        border: 1px solid rgba(255, 255, 255, 0.08);
        box-shadow: 0 20px 50px rgba(0, 0, 0, 0.5);
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    }
    .glass-card:hover {
        transform: translateY(-8px) scale(1.02);
        border-color: rgba(16, 185, 129, 0.3);
        box-shadow: 0 30px 60px rgba(0, 0, 0, 0.6), 0 0 20px rgba(16, 185, 129, 0.1);
    }
    
    /* Metric Typography */
    .metric-title { font-size: 0.75rem; color: #64748b; text-transform: uppercase; letter-spacing: 0.15em; font-weight: 700; margin-bottom: 4px; }
    .metric-value { font-size: 2.8rem; font-weight: 800; color: #ffffff; margin: 0; filter: drop-shadow(0 0 10px rgba(255,255,255,0.1)); }
    .metric-icon { font-size: 2.5rem; float: right; filter: drop-shadow(0 0 12px currentColor); margin-top: -5px; }
    
    /* Animated Gradient Headers */
    .gradient-text {
        background: linear-gradient(90deg, #10B981, #3B82F6, #8B5CF6, #10B981);
        background-size: 200% auto;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: shine 5s linear infinite;
    }
    @keyframes shine { to { background-position: 200% center; } }
    
    /* Tab Styling Refinement */
    .stTabs [data-baseweb="tab-list"] { background: rgba(15, 23, 42, 0.4); padding: 8px; border-radius: 16px; border: 1px solid rgba(255,255,255,0.05); }
    .stTabs [data-baseweb="tab"] { color: #64748b; font-weight: 600; border-radius: 10px; transition: all 0.3s; }
    .stTabs [aria-selected="true"] { background: #10B981 !important; color: #ffffff !important; box-shadow: 0 4px 15px rgba(16, 185, 129, 0.4); }
    
    /* Sidebar Overhaul */
    [data-testid="stSidebar"] { background-color: #0a0e17; border-right: 1px solid rgba(255,255,255,0.05); }
    [data-testid="stSidebarNav"] { padding-top: 2rem; }
    .stSidebar [data-testid="stMarkdownContainer"] p { font-size: 0.95rem !important; }
    
    /* Custom Button Aesthetics */
    div[data-testid="stButton"] > button {
        border-radius: 14px !important;
        padding: 12px 24px !important;
        font-weight: 600 !important;
        letter-spacing: 0.02em !important;
        border: 1px solid rgba(255,255,255,0.1) !important;
        background: rgba(255,255,255,0.03) !important;
        transition: all 0.3s ease !important;
    }
    div[data-testid="stButton"] > button:hover {
        background: rgba(255,255,255,0.08) !important;
        border-color: rgba(255,255,255,0.2) !important;
        transform: translateY(-2px);
    }
    div[data-testid="stButton"] > button[kind="primary"] {
        background: linear-gradient(135deg, #10B981 0%, #059669 100%) !important;
        color: white !important;
        border: none !important;
        box-shadow: 0 10px 20px rgba(16, 185, 129, 0.2) !important;
    }
    div[data-testid="stButton"] > button[kind="primary"]:hover {
        box-shadow: 0 15px 25px rgba(16, 185, 129, 0.4) !important;
    }

    /* Input Fields */
    .stTextInput input, .stSelectbox div[data-baseweb="select"] {
        background-color: rgba(15, 23, 42, 0.5) !important;
        border-radius: 12px !important;
        border: 1px solid rgba(255,255,255,0.1) !important;
        color: white !important;
    }
    
    /* Progress Bars */
    .stProgress > div > div > div > div { background-color: #10B981 !important; }

    /* Custom Scrollbar */
    ::-webkit-scrollbar { width: 8px; }
    ::-webkit-scrollbar-track { background: #05070a; }
    ::-webkit-scrollbar-thumb { background: #1e293b; border-radius: 10px; }
    ::-webkit-scrollbar-thumb:hover { background: #334155; }


    /* Interactive Hover Glows */
    .glass-card:hover {
        border-color: rgba(16, 185, 129, 0.4) !important;
        box-shadow: 0 0 30px rgba(16, 185, 129, 0.15) !important;
    }
    
    /* Login Page Refresh */
    .login-container {
        padding: 50px;
        border-radius: 30px;
        background: rgba(15, 23, 42, 0.8);
        border: 1px solid rgba(255, 255, 255, 0.1);
        box-shadow: 0 50px 100px rgba(0,0,0,0.8);
    }
    
    /* Better Charts Layout */
    .chart-container {
        padding: 10px;
        border-radius: 20px;
        background: rgba(0, 0, 0, 0.2);
        border: 1px solid rgba(255, 255, 255, 0.03);
    }
    
    /* Entry Animations */
    @keyframes fadeInUp {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    .glass-card { animation: fadeInUp 0.6s ease-out backwards; }
    .glass-card:nth-child(1) { animation-delay: 0.1s; }
    .glass-card:nth-child(2) { animation-delay: 0.2s; }
    .glass-card:nth-child(3) { animation-delay: 0.3s; }


    .stSidebar [data-testid="stButton"] button[kind="primary"] {
        background: linear-gradient(135deg, #10B981 0%, #059669 100%) !important;
        box-shadow: 0 0 20px rgba(16, 185, 129, 0.4) !important;
        border: none !important;
    }
    .stSidebar [data-testid="stButton"] button[kind="secondary"] {
        background: rgba(255,255,255,0.03) !important;
        border: 1px solid rgba(255,255,255,0.05) !important;
    }
    .stSidebar [data-testid="stButton"] button:hover {
        background: rgba(255,255,255,0.1) !important;
        transform: translateX(5px) !important;
    }

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
    st.session_state.current_page = 'Bio-Games Hub'
    
    # Load from persistence (CSV files)
    st.session_state.projects_df = sample_data.get_projects_df()
    st.session_state.project_tasks_df = sample_data.get_project_tasks_df()
    st.session_state.students_df = sample_data.get_students_df()
    st.session_state.team_df = sample_data.get_team_df()
    st.session_state.servers_df = sample_data.get_servers_df()
    if 'attendance_df' not in st.session_state:
        # Load from persistence if exists, else create empty
        if os.path.exists("data/attendance.csv"):
            st.session_state.attendance_df = pd.read_csv("data/attendance.csv")
        else:
            st.session_state.attendance_df = pd.DataFrame(columns=['DATE', 'NAME', 'ROLE_TYPE', 'OFFICE', 'STATUS'])

# Helper for saving state

def delete_row(table_key, id_col, id_val, filename):
    df = st.session_state[table_key]
    new_df = df[df[id_col] != id_val].reset_index(drop=True)
    update_state_and_save(table_key, new_df, filename)
    st.toast(f"Deleted successfully!")
    st.rerun()

def update_state_and_save(key, df, filename):
    st.session_state[key] = df
    sample_data.save_df(df, filename)

def login_page():
    st.markdown("<br><br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 1.2, 1])
    with col2:
        st.markdown("<div class='glass-card login-container' style='text-align: center;'>", unsafe_allow_html=True)
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
        st.markdown(f"<h1 class='gradient-text' style='text-align:center; font-size: 2.2rem !important; text-shadow: 0 0 20px rgba(16,185,129,0.3);'>🧪 INSILICOMICS</h1>", unsafe_allow_html=True)
        st.markdown("<hr style='margin-top:0;'>", unsafe_allow_html=True)

        # Connection Status Indicator
        import sample_data
        is_cloud = getattr(sample_data, 'HAS_SUPABASE', False)
        status_color = "#10B981" if is_cloud else "#94a3b8"
        status_text = "☁️ CLOUD SYNC: ACTIVE" if is_cloud else "📂 LOCAL STORAGE"
        st.markdown(f"""
            <div style='text-align:center; padding:5px; border-radius:10px; background:rgba(255,255,255,0.03); border:1px solid rgba(255,255,255,0.05); margin-bottom:20px;'>
                <small style='color:{status_color}; font-weight:800; letter-spacing:0.1em;'>{status_text}</small>
            </div>
        """, unsafe_allow_html=True)

        
        pages = {
            "Bio-Games Hub": "🎮",
            "Dashboard": "🏠", 
            "Projects Center": "🔬", 
            "Server Infrastructure": "🖥️", 
            "Core Team": "👥",
            "Students": "🎓", 
            "Attendance": "📅",
            "Project Types": "🏷️",
            "Clients": "🏢",
            "Education": "📚",
            "Reports": "📊"
        }
        
        for page, icon in pages.items():
            is_active = st.session_state.current_page == page
            btn_type = "primary" if is_active else "secondary"
            if st.button(f"{icon}  {page}", key=f"nav_{page}", use_container_width=True, type=btn_type):
                st.session_state.current_page = page
                st.rerun()
                
        
        st.markdown("<hr>", unsafe_allow_html=True)
        page = st.session_state.current_page
        
        if page == 'Projects Center':
            st.markdown("### 🏗️ Project Management")
            if st.button("➕ Add New Project", use_container_width=True):
                st.session_state['show_proj_form_Ooty'] = True # Default to Ooty or just trigger
                st.rerun()
            
            all_prjs = st.session_state.projects_df['TITLE'].tolist() if not st.session_state.projects_df.empty else []
            if all_prjs:
                sel_p = st.selectbox("Select Project to Manage", ["-- Select --"] + all_prjs, key="side_sel_p")
                if sel_p != "-- Select --":
                    p_id = st.session_state.projects_df[st.session_state.projects_df['TITLE'] == sel_p]['PROJECT_ID'].values[0]
                    sc1, sc2, sc3 = st.columns(3)
                    if sc1.button("👁️", key="side_view_p", help="View Workspace"):
                        st.session_state.active_project_id = p_id
                        st.session_state.current_page = 'Project Workspace'
                        st.rerun()
                    if sc2.button("✏️", key="side_edit_p", help="Edit Project"):
                        st.session_state[f'editing_prj_{p_id}'] = True
                        st.rerun()
                    if sc3.button("🗑️", key="side_del_p", help="Delete Project"):
                        delete_row('projects_df', 'PROJECT_ID', p_id, 'projects')
        
        elif page == 'Core Team':
            st.markdown("### 👥 Team Management")
            all_m = st.session_state.team_df['NAME'].tolist() if not st.session_state.team_df.empty else []
            if all_m:
                sel_m = st.selectbox("Select Member", ["-- Select --"] + all_m, key="side_sel_m")
                if sel_m != "-- Select --":
                    m_id = st.session_state.team_df[st.session_state.team_df['NAME'] == sel_m]['MEMBER_ID'].values[0]
                    sc1, sc2 = st.columns(2)
                    if sc1.button("✏️ Edit", key="side_edit_m", use_container_width=True):
                        st.session_state[f"editing_team_{m_id}"] = True
                        st.rerun()
                    if sc2.button("🗑️ Remove", key="side_del_m", use_container_width=True):
                        delete_row('team_df', 'MEMBER_ID', m_id, 'team')
        
        elif page == 'Students':
            st.markdown("### 🎓 Student Management")
            all_s = st.session_state.students_df['NAME'].tolist() if not st.session_state.students_df.empty else []
            if all_s:
                sel_s = st.selectbox("Select Student", ["-- Select --"] + all_s, key="side_sel_s")
                if sel_s != "-- Select --":
                    s_id = st.session_state.students_df[st.session_state.students_df['NAME'] == sel_s]['STUDENT_ID'].values[0]
                    sc1, sc2 = st.columns(2)
                    if sc1.button("✏️ Edit", key="side_edit_s", use_container_width=True):
                        st.session_state[f"editing_stud_{s_id}"] = True
                        st.rerun()
                    if sc2.button("🗑️ Discharge", key="side_del_s", use_container_width=True):
                        delete_row('students_df', 'STUDENT_ID', s_id, 'students')

        
        elif page == 'Project Workspace':
            st.markdown("### ⚙️ Workspace Actions")
            p_id = st.session_state.get('active_project_id')
            if p_id:
                if st.button("➕ Add Activity", use_container_width=True):
                    st.session_state[f'show_act_form_{p_id}'] = True
                    st.rerun()
                
                # List project tasks in sidebar
                p_tasks = st.session_state.project_tasks_df[st.session_state.project_tasks_df['PROJECT_ID'] == p_id]
                if not p_tasks.empty:
                    task_names = p_tasks['FILE_NAME'].tolist()
                    sel_t = st.selectbox("Select Activity", ["-- Select --"] + task_names, key="side_sel_t")
                    if sel_t != "-- Select --":
                        t_id = p_tasks[p_tasks['FILE_NAME'] == sel_t]['TASK_ID'].values[0]
                        sc1, sc2 = st.columns(2)
                        if sc1.button("✏️ Edit", key="side_edit_t", use_container_width=True):
                            st.session_state[f"editing_task_{t_id}"] = True
                            st.rerun()
                        if sc2.button("🗑️ Delete", key="side_del_t", use_container_width=True):
                            delete_row('project_tasks_df', 'TASK_ID', t_id, 'project_tasks')

        elif page == 'Server Infrastructure':
            st.markdown("### 🖥️ Server Management")
            all_sv = st.session_state.servers_df['SERVER_NAME'].tolist() if not st.session_state.servers_df.empty else []
            if all_sv:
                sel_sv = st.selectbox("Select Server", ["-- Select --"] + all_sv, key="side_sel_sv")
                if sel_sv != "-- Select --":
                    sc1, sc2 = st.columns(2)
                    if sc1.button("✏️ Edit", key="side_edit_sv", use_container_width=True):
                        st.session_state[f"editing_serv_{sel_sv}"] = True
                        st.rerun()
                    if sc2.button("🗑️ Delete", key="side_del_sv", use_container_width=True):
                        delete_row('servers_df', 'SERVER_NAME', sel_sv, 'servers')

        st.markdown("<div style='height: 100px;'></div>", unsafe_allow_html=True)

        st.markdown("<div style='position: fixed; bottom: 20px; width: 100%;'>", unsafe_allow_html=True)
        st.markdown("<hr>", unsafe_allow_html=True)
        st.markdown(f"<div style='display:flex; align-items:center;'><div style='width:30px; height:30px; border-radius:50%; background:#10B981; color:white; text-align:center; line-height:30px; margin-right:10px;'>{st.session_state.current_user['name'][0]}</div><div><b>{st.session_state.current_user['name']}</b><br><small>{st.session_state.current_user['email']}</small></div></div>", unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        
        if st.button("🚪 Logout", use_container_width=True, key="logout_btn", type="secondary"):
            st.session_state.logged_in = False
            st.rerun()

            st.session_state.logged_in = False
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)


def create_glass_metric(label, value, icon, color="#10B981"):
    return f"""
    <div class="glass-card" style="border-left: 5px solid {color}; overflow: hidden;">
        <div style="position: absolute; top: -20px; right: -20px; font-size: 8rem; opacity: 0.05; color: {color}; pointer-events: none;">{icon}</div>
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
    tasks_df = st.session_state.project_tasks_df

    if 'dashboard_view' not in st.session_state:
        st.session_state.dashboard_view = 'Overview'

    st.markdown("### 👆 Touch a metric to view detailed analytics:")
    c1, c2, c3, c4, c5, c6 = st.columns(6)
    with c1: 
        if st.button("🌐 Overview", use_container_width=True, type="primary" if st.session_state.dashboard_view=='Overview' else "secondary"):
            st.session_state.dashboard_view = 'Overview'
            st.rerun()
    with c2: 
        if st.button("🔬 Projects", use_container_width=True, type="primary" if st.session_state.dashboard_view=='Projects' else "secondary"):
            st.session_state.dashboard_view = 'Projects'
            st.rerun()
    with c3: 
        if st.button("🖥️ Servers", use_container_width=True, type="primary" if st.session_state.dashboard_view=='Servers' else "secondary"):
            st.session_state.dashboard_view = 'Servers'
            st.rerun()
    with c4: 
        if st.button("📅 Timeline", use_container_width=True, type="primary" if st.session_state.dashboard_view=='Timeline' else "secondary"):
            st.session_state.dashboard_view = 'Timeline'
            st.rerun()
    with c5: 
        if st.button("📅 Attendance", use_container_width=True, type="primary" if st.session_state.dashboard_view=='Attendance' else "secondary"):
            st.session_state.dashboard_view = 'Attendance'
            st.rerun()
    with c6: 
        if st.button("🎓 People", use_container_width=True, type="primary" if st.session_state.dashboard_view=='People' else "secondary"):
            st.session_state.dashboard_view = 'People'
            st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)
    view = st.session_state.dashboard_view
    
    if view == 'Overview':
        col_o1, col_o2 = st.columns(2)
        with col_o1:
            st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
            st.markdown(f"<h3 style='color:#10B981; text-align:center;'>Total Projects: {len(proj_df)}</h3>", unsafe_allow_html=True)
            if not proj_df.empty and 'STATUS' in proj_df.columns:
                fig_stat = px.pie(proj_df, names='STATUS', template="plotly_dark", hole=0.5, )
                fig_stat.update_layout(height=250, margin=dict(t=0, b=0, l=0, r=0), font_family='Inter', font_color='#94a3b8', title_font_family='Inter', title_font_color='#f1f5f9', title_font_size=20, showlegend=False, paper_bgcolor='rgba(0,0,0,0)')
                st.plotly_chart(fig_stat, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)
        with col_o2:
            st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
            st.markdown(f"<h3 style='color:#3B82F6; text-align:center;'>Compute Servers: {len(serv_df)}</h3>", unsafe_allow_html=True)
            if not serv_df.empty and 'LOAD_PERCENT' in serv_df.columns:
                fig2 = go.Figure(go.Indicator(mode="gauge+number", value=serv_df['LOAD_PERCENT'].mean(), title={'text':"Avg Load"}, gauge={'axis': {'range': [None, 100]}, 'bar': {'color': "#8B5CF6"}}))
                fig2.update_layout(height=250, margin=dict(t=30, b=0, l=20, r=20), paper_bgcolor='rgba(0,0,0,0)')
                st.plotly_chart(fig2, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)

    elif view == 'Projects':
        col_adv1, col_adv2 = st.columns(2)
        with col_adv1:
            st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
            st.markdown("### 🌐 Project Resource Constellation (3D)")
            if not proj_df.empty:
                plot_df = proj_df.copy()
                plot_df['COMPLEXITY'] = np.random.randint(10, 100, size=len(plot_df))
                plot_df['BUDGET_UTILIZATION'] = np.random.randint(20, 100, size=len(plot_df))
                plot_df['TEAM_SIZE'] = np.random.randint(2, 10, size=len(plot_df))
                fig_3d_scatter = px.scatter_3d(plot_df, x='PROGRESS', y='COMPLEXITY', z='BUDGET_UTILIZATION', color='STATUS', size='TEAM_SIZE', hover_name='TITLE',
                                             color_discrete_map={'Active': '#10B981', 'Queued': '#F59E0B', 'Completed': '#3B82F6', 'Error': '#EF4444', 'On Hold': '#9CA3AF'},
                                             template="plotly_dark")
                fig_3d_scatter.update_layout(margin=dict(l=0, r=0, b=0, t=0), font_family='Inter', font_color='#94a3b8', title_font_family='Inter', title_font_color='#f1f5f9', title_font_size=20, showlegend=False, height=350, paper_bgcolor='rgba(0,0,0,0)')
                st.plotly_chart(fig_3d_scatter, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)

        with col_adv2:
            st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
            st.markdown("### 🧬 Protein-Ligand Interaction Frequency")
            st.caption("Aggregated predicted binding site interactions across all active pipelines.")
            residues = [f"Res_{i}" for i in range(1, 16)]
            ligands = [f"Lig_{chr(65+i)}" for i in range(10)]
            interaction_data = np.random.poisson(lam=5, size=(len(residues), len(ligands)))
            fig_bio_heat = px.imshow(interaction_data, x=ligands, y=residues, color_continuous_scale="Viridis", aspect="auto", template="plotly_dark")
            fig_bio_heat.update_layout(height=350, margin=dict(t=10, b=10, l=10, r=10), font_family='Inter', font_color='#94a3b8', title_font_family='Inter', title_font_color='#f1f5f9', title_font_size=20, showlegend=False, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig_bio_heat, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)

    elif view == 'Timeline':
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.markdown("### 📅 Monthly Project Start Timeline")
        if not proj_df.empty and 'START_DATE' in proj_df.columns:
            temp_df = proj_df.copy()
            temp_df['START_DATE'] = pd.to_datetime(temp_df['START_DATE'], errors='coerce')
            temp_df = temp_df.dropna(subset=['START_DATE'])
            if not temp_df.empty:
                temp_df['Month-Year'] = temp_df['START_DATE'].dt.to_period('M').astype(str)
                timeline_df = temp_df.groupby('Month-Year').size().reset_index(name='Projects Started')
                timeline_df = timeline_df.sort_values('Month-Year')
                fig_time = px.area(timeline_df, x='Month-Year', y='Projects Started', template="plotly_dark")
                fig_time.update_layout(height=400, margin=dict(t=10, b=10, l=10, r=10), font_family='Inter', font_color='#94a3b8', title_font_family='Inter', title_font_color='#f1f5f9', title_font_size=20, showlegend=False, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
                st.plotly_chart(fig_time, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    elif view == 'Servers':
        col_s1, col_s2 = st.columns(2)
        with col_s1:
            st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
            st.markdown("### 📊 Individual Node Load")
            if not serv_df.empty and 'LOAD_PERCENT' in serv_df.columns:
                fig_load = px.bar(serv_df, x='SERVER_NAME', y='LOAD_PERCENT', color='STATUS', template="plotly_dark", color_discrete_map={'Running Workload': '#EF4444', 'Idle': '#10B981', 'Offline': '#6B7280'})
                fig_load.update_layout(yaxis_range=[0, 100], height=350, margin=dict(t=30, b=0, l=0, r=0), font_family='Inter', font_color='#94a3b8', title_font_family='Inter', title_font_color='#f1f5f9', title_font_size=20, showlegend=False, plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
                st.plotly_chart(fig_load, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)
            
        with col_s2:
            st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
            st.markdown("### 🌌 Compute Cluster Heatmap (3D)")
            # Fix 3D Heatmap meshgrid so it definitely shows
            x_vals = np.linspace(-5, 5, 50)
            y_vals = np.linspace(-5, 5, 50)
            xGrid, yGrid = np.meshgrid(x_vals, y_vals)
            base_load = serv_df['LOAD_PERCENT'].mean() if not serv_df.empty else 50
            R = np.sqrt(xGrid**2 + yGrid**2)
            z_vals = np.sin(R) + (base_load / 100.0) * np.cos(xGrid) * np.sin(yGrid) + np.random.rand(50, 50) * 0.2
            
            fig_surf = go.Figure(data=[go.Surface(z=z_vals, x=x_vals, y=y_vals, colorscale='Viridis')])
            fig_surf.update_layout(height=350, margin=dict(l=0, r=0, b=0, t=0), font_family='Inter', font_color='#94a3b8', title_font_family='Inter', title_font_color='#f1f5f9', title_font_size=20, showlegend=False, paper_bgcolor='rgba(0,0,0,0)', template="plotly_dark", scene=dict(xaxis_title='X Node', yaxis_title='Y Node', zaxis_title='Heat'))
            st.plotly_chart(fig_surf, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)

    elif view == 'People':
        c_p1, c_p2 = st.columns(2)
        with c_p1:
            st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
            st.markdown("### 🧠 Team Roles")
            if not team_df.empty and 'ROLE' in team_df.columns:
                fig_roles = px.pie(team_df, names='ROLE', template="plotly_dark", hole=0.3)
                fig_roles.update_layout(height=350, margin=dict(t=10, b=10, l=10, r=10), font_family='Inter', font_color='#94a3b8', title_font_family='Inter', title_font_color='#f1f5f9', title_font_size=20, showlegend=False, paper_bgcolor='rgba(0,0,0,0)')
                st.plotly_chart(fig_roles, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)
        with c_p2:
            st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
            st.markdown("### 📍 Student Location Demographics")
            if not stud_df.empty and 'OFFICE' in stud_df.columns:
                fig_loc = px.pie(stud_df, names='OFFICE', template="plotly_dark", color_discrete_map={'Ooty': '#10B981', 'Coimbatore': '#3B82F6'})
                fig_loc.update_layout(height=350, margin=dict(t=10, b=10, l=10, r=10), font_family='Inter', font_color='#94a3b8', title_font_family='Inter', title_font_color='#f1f5f9', title_font_size=20, showlegend=False, paper_bgcolor='rgba(0,0,0,0)')
                st.plotly_chart(fig_loc, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)

    elif view == 'Attendance':
        if 'attendance_df' in st.session_state and not st.session_state.attendance_df.empty:
            df_att = st.session_state.attendance_df
            c_att1, c_att2 = st.columns(2)
            with c_att1:
                st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
                st.markdown("#### Historical Trends by Group")
                hist_df = df_att.groupby(['DATE', 'ROLE_TYPE', 'STATUS']).size().reset_index(name='Count')
                fig_hist = px.bar(hist_df, x='DATE', y='Count', color='STATUS', facet_col='ROLE_TYPE', color_discrete_map={'Present': '#10B981', 'Absent': '#EF4444', 'Leave': '#F59E0B', 'Work From Home': '#3B82F6'}, template="plotly_dark")
                fig_hist.update_layout(height=300, margin=dict(t=30, b=10, l=10, r=10), font_family='Inter', font_color='#94a3b8', title_font_family='Inter', title_font_color='#f1f5f9', title_font_size=20, showlegend=False, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
                st.plotly_chart(fig_hist, use_container_width=True)
                st.markdown("</div>", unsafe_allow_html=True)
            with c_att2:
                st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
                st.markdown("#### 📅 Individual Attendance Heatmap")
                pivot_df = df_att.pivot_table(index='NAME', columns='DATE', values='STATUS', aggfunc=lambda x: 1 if x.iloc[0]=='Present' else (0.5 if x.iloc[0]=='Work From Home' else 0)).fillna(0)
                if not pivot_df.empty:
                    fig_heat = px.imshow(pivot_df, text_auto=False, aspect="auto", color_continuous_scale=[[0, '#EF4444'], [0.5, '#3B82F6'], [1, '#10B981']], labels=dict(color="Presence"), template="plotly_dark")
                    fig_heat.update_xaxes(side="top")
                    fig_heat.update_layout(height=300, margin=dict(t=10, b=10, l=10, r=10), font_family='Inter', font_color='#94a3b8', title_font_family='Inter', title_font_color='#f1f5f9', title_font_size=20, showlegend=False, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
                    st.plotly_chart(fig_heat, use_container_width=True)
                st.markdown("</div>", unsafe_allow_html=True)
        else:
            st.info("No attendance data to visualize.")


def create_project_form(office_name):
    c1, c2, c3 = st.columns(3)
    with c1:
        title = st.text_input("Project Title *")
    with c2:
        if 'project_types_list' not in st.session_state:
            st.session_state.project_types_list = ["Molecular Dynamics", "Virtual Screening", "QSAR", "Homology Modeling"]
        project_type = st.selectbox("Project Type *", st.session_state.project_types_list)
    with c3:
        office = st.selectbox("Office *", ["Coimbatore Office", "Ooty Office"], index=0 if office_name=="Coimbatore" else 1)
        
    c4, c5 = st.columns(2)
    with c4:
        if 'clients_list' not in st.session_state:
            st.session_state.clients_list = ["Biome", "PharmaTech", "Ooty Univ", "BioSim", "NatureMed"]
        client = st.selectbox("Select Client *", st.session_state.clients_list)
    with c5:
        client_university = st.text_input("Client University", placeholder="Auto-filled from client", disabled=True)
        
    referred_by = st.text_input("Referred By *")
    description = st.text_area("Description *")
    
    c6, c7, c8 = st.columns(3)
    with c6:
        status = st.selectbox("Status *", ["Active", "Queued", "Completed", "Error", "On Hold"])
    with c7:
        if 'team_df' in st.session_state and not st.session_state.team_df.empty:
            leads = st.session_state.team_df['NAME'].tolist()
        else:
            leads = ["Choose team lead"]
        team_lead = st.selectbox("Team Lead *", leads)
    with c8:
        progress_str = st.selectbox("Progress *", ["0% - Not Started", "25%", "50%", "75%", "100%"])
        
    c9, c10 = st.columns(2)
    with c9:
        start_date = st.date_input("Start Date *")
    with c10:
        end_date = st.date_input("End Date (Optional)", value=None)
        
    col_empty, col_btn1, col_btn2 = st.columns([6, 1, 1])
    with col_btn1:
        if st.button("Cancel", use_container_width=True):
            st.rerun()
    with col_btn2:
        if st.button("Create", type="primary", use_container_width=True):
            if not title:
                st.error("Project Title is required")
                return
            progress_val = int(progress_str.split('%')[0]) if '%' in progress_str else 0
            new_id = f"PRJ-{uuid.uuid4().hex[:6].upper()}"
            new_row = pd.DataFrame([{
                'PROJECT_ID': new_id,
                'TITLE': title,
                'PROJECT_TYPE': project_type,
                'CLIENT': client,
                'CLIENT_UNIVERSITY': client_university,
                'REFERRED_BY': referred_by,
                'TEAM_LEAD': team_lead,
                'STATUS': status,
                'PROGRESS': progress_val,
                'START_DATE': start_date.strftime("%Y-%m-%d"),
                'END_DATE': end_date.strftime("%Y-%m-%d") if end_date else "",
                'NOTES': description,
                'OFFICE': office.split()[0]
            }])
            new_df = pd.concat([new_row, st.session_state.projects_df], ignore_index=True)
            update_state_and_save('projects_df', new_df, 'projects')
            st.toast(f"Project '{title}' created successfully!")
            st.rerun()

def add_activity_form(proj_id):
    activity_name = st.text_input("Activity Name *", placeholder="e.g., Data preprocessing, Model training")
    
    c1, c2 = st.columns(2)
    with c1:
        if 'team_df' in st.session_state and not st.session_state.team_df.empty:
            members = ["Select team member"] + st.session_state.team_df['NAME'].tolist()
        else:
            members = ["Select team member"]
        assigned_to = st.selectbox("Assigned To *", members)
    with c2:
        available_servers = ["Select server"] + st.session_state.servers_df['SERVER_NAME'].tolist()
        server = st.selectbox("Server *", available_servers)
        
    c3, c4 = st.columns(2)
    with c3:
        duration = st.selectbox("Duration (nanoseconds)", ["Select duration", "10 ns", "50 ns", "100 ns", "500 ns", "1000 ns"])
        st.markdown("<small style='color: orange;'>Duration is only applicable for MD Simulation projects</small>", unsafe_allow_html=True)
    with c4:
        progress = st.selectbox("Progress (%) *", ["0%", "25%", "50%", "75%", "100%"])
        
    c5, c6 = st.columns(2)
    with c5:
        start_date = st.date_input("Start Date")
    with c6:
        end_date = st.date_input("End Date")
        
    status = st.selectbox("Status *", ["Pending", "Running", "Queued", "Completed", "Failed"])
    
    col_empty, col_btn1, col_btn2 = st.columns([6, 1, 1])
    with col_btn1:
        if st.button("Cancel", use_container_width=True):
            st.rerun()
    with col_btn2:
        if st.button("Create", type="primary", use_container_width=True):
            if not activity_name:
                st.error("Activity Name is required")
                return
            progress_val = int(progress.replace("%", "")) if progress != "0%" else 0
            new_task_id = f"TSK-{uuid.uuid4().hex[:5].upper()}"
            new_task = pd.DataFrame([{
                'TASK_ID': new_task_id,
                'PROJECT_ID': proj_id,
                'FILE_NAME': activity_name,
                'SERVER_USED': server if server != "Select server" else "None",
                'ASSIGNED_TO': assigned_to,
                'DURATION': duration,
                'START_DATE': start_date.strftime("%Y-%m-%d"),
                'END_DATE': end_date.strftime("%Y-%m-%d"),
                'STATUS': status,
                'PROGRESS': progress_val,
                'LAST_UPDATED': datetime.now().strftime("%Y-%m-%d %H:%M")
            }])
            new_df = pd.concat([st.session_state.project_tasks_df, new_task], ignore_index=True)
            update_state_and_save('project_tasks_df', new_df, 'project_tasks')
            st.toast(f"Activity '{activity_name}' created successfully!")
            st.rerun()


def create_project_form(office_name):
    with st.container(border=True):
        st.markdown("### Create New Project")
        c1, c2, c3 = st.columns(3)
        with c1:
            title = st.text_input("Project Title *", key=f"title_in_{office_name}")
        with c2:
            if 'project_types_list' not in st.session_state:
                st.session_state.project_types_list = ["Molecular Dynamics", "Virtual Screening", "QSAR", "Homology Modeling"]
            project_type = st.selectbox("Project Type *", st.session_state.project_types_list, key=f"type_in_{office_name}")
        with c3:
            office = st.selectbox("Office *", ["Coimbatore Office", "Ooty Office"], index=0 if office_name=="Coimbatore" else 1, key=f"office_in_{office_name}")
            
        c4, c5 = st.columns(2)
        with c4:
            if 'clients_list' not in st.session_state:
                st.session_state.clients_list = ["Biome", "PharmaTech", "Ooty Univ", "BioSim", "NatureMed"]
            client = st.selectbox("Select Client *", st.session_state.clients_list, key=f"client_in_{office_name}")
        with c5:
            client_university = st.text_input("Client University", placeholder="Auto-filled from client", disabled=True, key=f"univ_in_{office_name}")
            
        referred_by = st.text_input("Referred By *", key=f"ref_in_{office_name}")
        description = st.text_area("Description *", key=f"desc_in_{office_name}")
        
        c6, c7, c8 = st.columns(3)
        with c6:
            status = st.selectbox("Status *", ["Active", "Queued", "Completed", "Error", "On Hold"], key=f"status_in_{office_name}")
        with c7:
            if 'team_df' in st.session_state and not st.session_state.team_df.empty:
                leads = st.session_state.team_df['NAME'].tolist()
            else:
                leads = ["Choose team lead"]
            team_lead = st.selectbox("Team Lead *", leads, key=f"lead_in_{office_name}")
        with c8:
            progress_str = st.selectbox("Progress *", ["0% - Not Started", "25%", "50%", "75%", "100%"], key=f"prog_in_{office_name}")
            
        c9, c10 = st.columns(2)
        with c9:
            start_date = st.date_input("Start Date *", key=f"start_in_{office_name}")
        with c10:
            end_date = st.date_input("End Date (Optional)", value=None, key=f"end_in_{office_name}")
            
        col_empty, col_btn1, col_btn2 = st.columns([6, 1, 1])
        with col_btn1:
            if st.button("Cancel", use_container_width=True, key=f"cancel_proj_{office_name}"):
                st.session_state[f'show_proj_form_{office_name}'] = False
                st.rerun()
        with col_btn2:
            if st.button("Create", type="primary", use_container_width=True, key=f"create_proj_{office_name}"):
                if not title:
                    st.error("Project Title is required")
                    return
                progress_val = int(progress_str.split('%')[0]) if '%' in progress_str else 0
                new_id = f"PRJ-{uuid.uuid4().hex[:6].upper()}"
                new_row = pd.DataFrame([{
                    'PROJECT_ID': new_id,
                    'TITLE': title,
                    'PROJECT_TYPE': project_type,
                    'CLIENT': client,
                    'CLIENT_UNIVERSITY': client_university,
                    'REFERRED_BY': referred_by,
                    'TEAM_LEAD': team_lead,
                    'STATUS': status,
                    'PROGRESS': progress_val,
                    'START_DATE': start_date.strftime("%Y-%m-%d"),
                    'END_DATE': end_date.strftime("%Y-%m-%d") if end_date else "",
                    'NOTES': description,
                    'OFFICE': office.split()[0]
                }])
                new_df = pd.concat([new_row, st.session_state.projects_df], ignore_index=True)
                update_state_and_save('projects_df', new_df, 'projects')
                st.session_state[f'show_proj_form_{office_name}'] = False
                st.toast(f"Project '{title}' created successfully!")
                st.rerun()

def add_activity_form(proj_id):
    with st.container(border=True):
        st.markdown("### Add New Activity")
        activity_name = st.text_input("Activity Name *", placeholder="e.g., Data preprocessing, Model training", key=f"act_name_in_{proj_id}")
        
        c1, c2 = st.columns(2)
        with c1:
            if 'team_df' in st.session_state and not st.session_state.team_df.empty:
                members = ["Select team member"] + st.session_state.team_df['NAME'].tolist()
            else:
                members = ["Select team member"]
            assigned_to = st.selectbox("Assigned To *", members, key=f"act_assigned_{proj_id}")
        with c2:
            available_servers = ["Select server"] + st.session_state.servers_df['SERVER_NAME'].tolist()
            server = st.selectbox("Server *", available_servers, key=f"act_server_{proj_id}")
            
        c3, c4 = st.columns(2)
        with c3:
            duration = st.selectbox("Duration (nanoseconds)", ["Select duration", "10 ns", "50 ns", "100 ns", "500 ns", "1000 ns"], key=f"act_dur_{proj_id}")
            st.markdown("<small style='color: orange;'>Duration is only applicable for MD Simulation projects</small>", unsafe_allow_html=True)
        with c4:
            progress = st.selectbox("Progress (%) *", ["0%", "25%", "50%", "75%", "100%"], key=f"act_prog_{proj_id}")
            
        c5, c6 = st.columns(2)
        with c5:
            start_date = st.date_input("Start Date", key=f"act_start_{proj_id}")
        with c6:
            end_date = st.date_input("End Date", key=f"act_end_{proj_id}")
            
        status = st.selectbox("Status *", ["Pending", "Running", "Queued", "Completed", "Failed"], key=f"act_status_{proj_id}")
        
        col_empty, col_btn1, col_btn2 = st.columns([6, 1, 1])
        with col_btn1:
            if st.button("Cancel", use_container_width=True, key=f"cancel_act_{proj_id}"):
                st.session_state[f'show_act_form_{proj_id}'] = False
                st.rerun()
        with col_btn2:
            if st.button("Create", type="primary", use_container_width=True, key=f"create_act_{proj_id}"):
                if not activity_name:
                    st.error("Activity Name is required")
                    return
                progress_val = int(progress.replace("%", "")) if progress != "0%" else 0
                new_task_id = f"TSK-{uuid.uuid4().hex[:5].upper()}"
                new_task = pd.DataFrame([{
                    'TASK_ID': new_task_id,
                    'PROJECT_ID': proj_id,
                    'FILE_NAME': activity_name,
                    'SERVER_USED': server if server != "Select server" else "None",
                    'ASSIGNED_TO': assigned_to,
                    'DURATION': duration,
                    'START_DATE': start_date.strftime("%Y-%m-%d"),
                    'END_DATE': end_date.strftime("%Y-%m-%d"),
                    'STATUS': status,
                    'PROGRESS': progress_val,
                    'LAST_UPDATED': datetime.now().strftime("%Y-%m-%d %H:%M")
                }])
                new_df = pd.concat([st.session_state.project_tasks_df, new_task], ignore_index=True)
                update_state_and_save('project_tasks_df', new_df, 'project_tasks')
                st.session_state[f'show_act_form_{proj_id}'] = False
                st.toast(f"Activity '{activity_name}' created successfully!")
                st.rerun()

def project_detail_view(office_name):
    st.markdown(f"### {office_name} Project Management")
    
    main_df = st.session_state.projects_df
    mask = main_df['OFFICE'] == office_name
    office_df = main_df[mask]
    
    if f'show_proj_form_{office_name}' not in st.session_state:
        st.session_state[f'show_proj_form_{office_name}'] = False

    if st.session_state[f'show_proj_form_{office_name}']:
        create_project_form(office_name)

    # 1. Add New Project Form (Trigger)
    col1, col2 = st.columns([8, 2])
    with col2:
        if st.button("➕ Add Project", use_container_width=True, key=f"add_proj_btn_{office_name}"):
            st.session_state[f'show_proj_form_{office_name}'] = True
            st.rerun()

    # 2. View/Edit Existing Projects
    if not office_df.empty:
        st.markdown("<hr>", unsafe_allow_html=True)
        st.markdown("### 📂 Project Workspaces")
        st.markdown("Touch a project below to open its dedicated workspace and manage activities.")
        
        cols = st.columns(3)
        for i, (idx, row) in enumerate(office_df.iterrows()):
            with cols[i % 3]:
                st.markdown(f'''<div class='glass-card' style='padding: 24px;'>
                    <div style='display:flex; justify-content:space-between; align-items:flex-start; margin-bottom:15px;'>
                        <h4 style='margin:0; font-size:1.3rem; line-height:1.2; color:#fff;'>{row['TITLE']}</h4>
                        <span style='background:rgba(16,185,129,0.1); color:#10B981; padding:4px 10px; border-radius:8px; font-size:0.75rem; font-weight:700;'>{row['STATUS']}</span>
                    </div>
                    <div style='background:rgba(255,255,255,0.03); border-radius:12px; padding:12px; margin-bottom:15px;'>
                        <p style='margin:0; font-size:0.85rem; color:#94a3b8;'>Client: <b style='color:#e2e8f0;'>{row['CLIENT']}</b></p>
                        <p style='margin:0; font-size:0.85rem; color:#94a3b8;'>Lead: <b style='color:#e2e8f0;'>{row['TEAM_LEAD']}</b></p>
                    </div>
                    <div style='display:flex; justify-content:space-between; align-items:center;'>
                        <span style='font-size:0.8rem; color:#64748b;'>{row['START_DATE']}</span>
                        <span style='font-size:1.1rem; font-weight:800; color:#10B981;'>{row['PROGRESS']}%</span>
                    </div>
                </div>''', unsafe_allow_html=True)
                st.markdown("<div style='margin-top:-20px;'>", unsafe_allow_html=True) # Adjust for the action buttons
                
                act_c1, act_c2, act_c3 = st.columns(3)
                with act_c1:
                    if st.button("👁️ View", key=f"view_prj_{row['PROJECT_ID']}", help="View Details", use_container_width=True):
                        st.session_state.current_page = 'Project Workspace'
                        st.session_state.active_project_id = row['PROJECT_ID']
                        st.rerun()
                with act_c2:
                    if st.button("✏️ Edit", key=f"edit_prj_{row['PROJECT_ID']}", help="Edit Project", use_container_width=True):
                        st.session_state[f'editing_prj_{row["PROJECT_ID"]}'] = True
                with act_c3:
                    if st.button("🗑️ Del", key=f"del_prj_{row['PROJECT_ID']}", help="Delete Project", use_container_width=True):
                        delete_row('projects_df', 'PROJECT_ID', row['PROJECT_ID'], 'projects')

                if st.session_state.get(f'editing_prj_{row["PROJECT_ID"]}'):
                    with st.container(border=True):
                        st.markdown(f"### Edit Project: {row['TITLE']}")
                        new_status = st.selectbox("Update Status", ["Active", "Queued", "Completed", "Error", "On Hold"], index=["Active", "Queued", "Completed", "Error", "On Hold"].index(row['STATUS']) if row['STATUS'] in ["Active", "Queued", "Completed", "Error", "On Hold"] else 0, key=f"edit_stat_{row['PROJECT_ID']}")
                        new_progress = st.select_slider("Update Progress (%)", options=[0, 25, 50, 75, 100], value=int(row['PROGRESS']), key=f"edit_prog_{row['PROJECT_ID']}")
                        if st.button("Save Changes", key=f"save_prj_{row['PROJECT_ID']}"):
                            df = st.session_state.projects_df
                            df.loc[df['PROJECT_ID'] == row['PROJECT_ID'], 'STATUS'] = new_status
                            df.loc[df['PROJECT_ID'] == row['PROJECT_ID'], 'PROGRESS'] = new_progress
                            update_state_and_save('projects_df', df, 'projects')
                            st.session_state[f'editing_prj_{row["PROJECT_ID"]}'] = False
                            st.rerun()
                        if st.button("Cancel", key=f"cancel_edit_prj_{row['PROJECT_ID']}"):
                            st.session_state[f'editing_prj_{row["PROJECT_ID"]}'] = False
                            st.rerun()
                st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.info(f"No active projects in {office_name}. Use the form above to initialize one.")

def project_workspace_page():
    if 'active_project_id' not in st.session_state:
        st.warning("No project selected.")
        if st.button("Return to Projects Center"):
            st.session_state.current_page = 'Projects Center'
            st.rerun()
        return

    proj_id = st.session_state.active_project_id
    proj_mask = st.session_state.projects_df['PROJECT_ID'] == proj_id
    if not proj_mask.any():
        st.error("Project not found.")
        return
        
    proj_data = st.session_state.projects_df[proj_mask].iloc[0]
    
    col_back, col_title = st.columns([1, 4])
    with col_back:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("⬅️ Back to Projects", use_container_width=True):
            st.session_state.current_page = 'Projects Center'
            st.rerun()
    with col_title:
        st.markdown(f"<h1 class='gradient-text' style='margin-top:0; padding-top:0;'>Workspace: {proj_data['TITLE']}</h1>", unsafe_allow_html=True)
        
    st.markdown(f"**Client:** {proj_data['CLIENT']} | **Lead:** {proj_data['TEAM_LEAD']} | **Status:** {proj_data['STATUS']} | **Progress:** {proj_data['PROGRESS']}%")
    st.markdown("<hr>", unsafe_allow_html=True)
    
    st.markdown(f"<div class='glass-card'>", unsafe_allow_html=True)
    if f'show_act_form_{proj_id}' not in st.session_state:
        st.session_state[f'show_act_form_{proj_id}'] = False
    
    if st.session_state[f'show_act_form_{proj_id}']:
        add_activity_form(proj_id)

    col1, col2 = st.columns([8, 2])
    with col1:
        st.markdown(f"#### ⚙️ Project Activities  <span style='color: gray; font-size: 0.8em;'>(Active)</span>", unsafe_allow_html=True)
    with col2:
        if st.button("➕ Add Activity", use_container_width=True, key=f"add_act_btn_{proj_id}"):
            st.session_state[f'show_act_form_{proj_id}'] = True
            st.rerun()
            
    task_mask = st.session_state.project_tasks_df['PROJECT_ID'] == proj_id
    proj_tasks_df = st.session_state.project_tasks_df[task_mask]
    
    if not proj_tasks_df.empty:
        st.markdown("### 📊 Active Sub-Tasks / Activities")
        cols = st.columns(3)
        for i, (idx, row) in enumerate(proj_tasks_df.iterrows()):
            with cols[i % 3]:
                st.markdown(f'''<div class='glass-card' style='padding: 20px; border-left: 4px solid #3B82F6;'>
                    <h4 style='margin:0 0 10px 0; color:#3B82F6; font-size:1.2rem;'>{row['FILE_NAME']}</h4>
                    <div style='font-size:0.9rem; margin-bottom:15px;'>
                        <span style='color:#94a3b8;'>Server:</span> <b style='color:#f1f5f9;'>{row['SERVER_USED']}</b><br>
                        <span style='color:#94a3b8;'>Status:</span> <b style='color:#f1f5f9;'>{row['STATUS']}</b>
                    </div>
                    <div style='display:flex; justify-content:space-between; align-items:center;'>
                        <span style='font-size:0.75rem; color:#64748b;'>{row['LAST_UPDATED']}</span>
                        <span style='font-size:1.1rem; font-weight:800; color:#3B82F6;'>{row['PROGRESS']}%</span>
                    </div>
                </div>''', unsafe_allow_html=True)
                st.markdown("<div style='margin-top:-20px;'>", unsafe_allow_html=True)
                t_c1, t_c2 = st.columns(2)
                with t_c1:
                    if st.button("✏️ Edit", key=f"edit_task_{row['TASK_ID']}", use_container_width=True):
                        st.session_state[f'editing_task_{row["TASK_ID"]}'] = True
                with t_c2:
                    if st.button("🗑️ Del", key=f"del_task_{row['TASK_ID']}", use_container_width=True):
                        delete_row('project_tasks_df', 'TASK_ID', row['TASK_ID'], 'project_tasks')

                if st.session_state.get(f'editing_task_{row["TASK_ID"]}'):
                    with st.container(border=True):
                        new_t_status = st.selectbox("Status", ["Running", "Queued", "Completed", "Failed"], index=["Running", "Queued", "Completed", "Failed"].index(row['STATUS']), key=f"ts_{row['TASK_ID']}")
                        new_t_prog = st.selectbox("Progress", [0, 25, 50, 75, 100], index=[0, 25, 50, 75, 100].index(int(row['PROGRESS'])), key=f"tp_{row['TASK_ID']}")
                        if st.button("Update", key=f"upd_task_{row['TASK_ID']}"):
                            df = st.session_state.project_tasks_df
                            df.loc[df['TASK_ID'] == row['TASK_ID'], 'STATUS'] = new_t_status
                            df.loc[df['TASK_ID'] == row['TASK_ID'], 'PROGRESS'] = new_t_prog
                            df.loc[df['TASK_ID'] == row['TASK_ID'], 'LAST_UPDATED'] = datetime.now().strftime("%Y-%m-%d %H:%M")
                            update_state_and_save('project_tasks_df', df, 'project_tasks')
                            st.session_state[f'editing_task_{row["TASK_ID"]}'] = False
                            st.rerun()
                st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.info("No activities currently tracked under this project.")
    st.markdown("</div>", unsafe_allow_html=True)

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

    if not df.empty:
        st.markdown("<hr>", unsafe_allow_html=True)
        cols = st.columns(3)
        for i, (idx, row) in enumerate(df.iterrows()):
            with cols[i % 3]:
                st.markdown(f'''<div class='glass-card' style='text-align:center; padding:30px;'>
                    <div style='width:80px; height:80px; background:rgba(16,185,129,0.1); border-radius:50%; display:flex; align-items:center; justify-content:center; margin:0 auto 20px auto; font-size:2.5rem; border:1px solid rgba(16,185,129,0.2);'>🧑‍🔬</div>
                    <h3 style='margin:0 0 5px 0; color:#fff;'>{row['NAME']}</h3>
                    <p style='color:#10B981; font-weight:700; margin:0 0 10px 0; font-size:0.9rem; text-transform:uppercase; letter-spacing:0.05em;'>{row['ROLE']}</p>
                    <div style='background:rgba(255,255,255,0.03); border-radius:12px; padding:10px; margin-bottom:20px;'>
                        <p style='margin:0; font-size:0.85rem; color:#94a3b8;'>{row['EXPERTISE']}</p>
                        <p style='margin:5px 0 0 0; font-size:0.75rem; color:#64748b;'>{row['EMAIL']}</p>
                    </div>
                </div>''', unsafe_allow_html=True)
                st.markdown("<div style='margin-top:-30px;'>", unsafe_allow_html=True)
                tc1, tc2 = st.columns(2)
                with tc1:
                    if st.button("✏️ Edit", key=f"edit_team_{row['MEMBER_ID']}", use_container_width=True):
                        st.session_state[f"editing_team_{row['MEMBER_ID']}"] = True
                with tc2:
                    if st.button("🗑️ Remove", key=f"del_team_{row['MEMBER_ID']}", use_container_width=True):
                        delete_row('team_df', 'MEMBER_ID', row['MEMBER_ID'], 'team')
                
                if st.session_state.get(f"editing_team_{row['MEMBER_ID']}"):
                    with st.container(border=True):
                        new_role = st.selectbox("Role", ["PI / Lead", "Senior Engineer", "System Admin", "Research Scientist"], index=["PI / Lead", "Senior Engineer", "System Admin", "Research Scientist"].index(row['ROLE']), key=f"erole_{row['MEMBER_ID']}")
                        new_exp = st.text_input("Expertise", value=row['EXPERTISE'], key=f"eexp_{row['MEMBER_ID']}")
                        if st.button("Update Team", key=f"upd_team_{row['MEMBER_ID']}"):
                            df = st.session_state.team_df
                            df.loc[df['MEMBER_ID'] == row['MEMBER_ID'], 'ROLE'] = new_role
                            df.loc[df['MEMBER_ID'] == row['MEMBER_ID'], 'EXPERTISE'] = new_exp
                            update_state_and_save('team_df', df, 'team')
                            st.session_state[f"editing_team_{row['MEMBER_ID']}"] = False
                            st.rerun()
                st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.info("No team members found.")

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

            if not office_df.empty:
                st.markdown("<hr>", unsafe_allow_html=True)
                cols = st.columns(3)
                for i, (idx, row) in enumerate(office_df.iterrows()):
                    with cols[i % 3]:
                        st.markdown(f'''<div class='glass-card' style='text-align:center; padding:30px;'>
                            <div style='width:80px; height:80px; background:rgba(59,130,246,0.1); border-radius:50%; display:flex; align-items:center; justify-content:center; margin:0 auto 20px auto; font-size:2.5rem; border:1px solid rgba(59,130,246,0.2);'>🎓</div>
                            <h3 style='margin:0 0 5px 0; color:#fff;'>{row['NAME']}</h3>
                            <span style='background:rgba(16,185,129,0.1); color:#10B981; padding:4px 12px; border-radius:20px; font-size:0.75rem; font-weight:700;'>{row['STATUS']}</span>
                            <p style='margin:20px 0 20px 0; font-size:0.9rem; color:#94a3b8; line-height:1.4;'>Skills: <b style='color:#e2e8f0;'>{row['SKILLS']}</b></p>
                        </div>''', unsafe_allow_html=True)
                        st.markdown("<div style='margin-top:-30px;'>", unsafe_allow_html=True)
                        sc1, sc2 = st.columns(2)
                        with sc1:
                            if st.button("✏️ Edit", key=f"edit_stud_{row['STUDENT_ID']}", use_container_width=True):
                                st.session_state[f"editing_stud_{row['STUDENT_ID']}"] = True
                        with sc2:
                            if st.button("🗑️ Discharge", key=f"del_stud_{row['STUDENT_ID']}", use_container_width=True):
                                delete_row('students_df', 'STUDENT_ID', row['STUDENT_ID'], 'students')
                        
                        if st.session_state.get(f"editing_stud_{row['STUDENT_ID']}"):
                            with st.container(border=True):
                                new_skills = st.text_input("Skills", value=row['SKILLS'], key=f"eskills_{row['STUDENT_ID']}")
                                new_stat = st.selectbox("Status", ["Active", "Graduated"], index=["Active", "Graduated"].index(row['STATUS']), key=f"estat_{row['STUDENT_ID']}")
                                if st.button("Update Student", key=f"upd_stud_{row['STUDENT_ID']}"):
                                    df = st.session_state.students_df
                                    df.loc[df['STUDENT_ID'] == row['STUDENT_ID'], 'SKILLS'] = new_skills
                                    df.loc[df['STUDENT_ID'] == row['STUDENT_ID'], 'STATUS'] = new_stat
                                    update_state_and_save('students_df', df, 'students')
                                    st.session_state[f"editing_stud_{row['STUDENT_ID']}"] = False
                                    st.rerun()
                        st.markdown("</div>", unsafe_allow_html=True)
            else:
                st.info("No students found.")

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

    if not df.empty:
        st.markdown("<hr>", unsafe_allow_html=True)
        cols = st.columns(3)
        for i, (idx, row) in enumerate(df.iterrows()):
            with cols[i % 3]:
                status_colors = {"Idle": "#10B981", "Running Workload": "#EF4444", "Maintenance": "#F59E0B", "Offline": "#6B7280"}
                scolor = status_colors.get(row['STATUS'], "#9CA3AF")
                st.markdown(f'''<div class='glass-card' style='padding:25px; border-top: 4px solid {scolor};'>
                    <div style='display:flex; justify-content:space-between; align-items:center; margin-bottom:15px;'>
                        <h3 style='margin:0; color:#3B82F6; font-size:1.4rem;'>🖥️ {row['SERVER_NAME']}</h3>
                        <span style='color:{scolor}; font-size:0.8rem; font-weight:800; text-transform:uppercase;'>{row['STATUS']}</span>
                    </div>
                    <div style='margin-bottom:15px;'>
                        <div style='display:flex; justify-content:space-between; font-size:0.85rem; color:#94a3b8; margin-bottom:5px;'>
                            <span>System Load</span>
                            <span>{row['LOAD_PERCENT']}%</span>
                        </div>
                        <div style='height:8px; background:rgba(255,255,255,0.05); border-radius:4px; overflow:hidden;'>
                            <div style='height:100%; width:{row['LOAD_PERCENT']}%; background:{scolor}; box-shadow:0 0 10px {scolor}66;'></div>
                        </div>
                    </div>
                    <div style='font-size:0.85rem; color:#94a3b8;'>
                        <p style='margin:0;'>Specs: <b style='color:#e2e8f0;'>{row['GPU_SPECS']}</b></p>
                        <p style='margin:2px 0 0 0;'>IP: <b style='color:#e2e8f0;'>{row['IP_ADDRESS']}</b></p>
                    </div>
                </div>''', unsafe_allow_html=True)
                st.markdown("<div style='margin-top:-30px;'>", unsafe_allow_html=True)
                svc1, svc2 = st.columns(2)
                with svc1:
                    if st.button("✏️ Edit", key=f"edit_serv_{row['SERVER_NAME']}", use_container_width=True):
                        st.session_state[f"editing_serv_{row['SERVER_NAME']}"] = True
                with svc2:
                    if st.button("🗑️ Decommission", key=f"del_serv_{row['SERVER_NAME']}", use_container_width=True):
                        delete_row('servers_df', 'SERVER_NAME', row['SERVER_NAME'], 'servers')
                
                if st.session_state.get(f"editing_serv_{row['SERVER_NAME']}"):
                    with st.container(border=True):
                        new_serv_status = st.selectbox("Status", ["Idle", "Running Workload", "Maintenance", "Offline"], index=["Idle", "Running Workload", "Maintenance", "Offline"].index(row['STATUS']), key=f"ess_{row['SERVER_NAME']}")
                        new_serv_load = st.slider("Load", 0, 100, int(row['LOAD_PERCENT']), key=f"esl_{row['SERVER_NAME']}")
                        if st.button("Update Server", key=f"upd_serv_{row['SERVER_NAME']}"):
                            df = st.session_state.servers_df
                            df.loc[df['SERVER_NAME'] == row['SERVER_NAME'], 'STATUS'] = new_serv_status
                            df.loc[df['SERVER_NAME'] == row['SERVER_NAME'], 'LOAD_PERCENT'] = new_serv_load
                            update_state_and_save('servers_df', df, 'servers')
                            st.session_state[f"editing_serv_{row['SERVER_NAME']}"] = False
                            st.rerun()
                st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.info("No servers available.")

def attendance_page():
    st.markdown("<h1 class='gradient-text'>📅 Quick Attendance</h1>", unsafe_allow_html=True)
    st.markdown("Mark presence for today.")
    
    if 'attendance_df' not in st.session_state:
        st.session_state.attendance_df = pd.DataFrame(columns=['DATE', 'NAME', 'ROLE_TYPE', 'OFFICE', 'STATUS'])
        
    today_str = datetime.now().strftime("%Y-%m-%d")
    
    # Get all names
    students = st.session_state.students_df['NAME'].tolist() if not st.session_state.students_df.empty else []
    team = st.session_state.team_df['NAME'].tolist() if not st.session_state.team_df.empty else []
    
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    st.markdown(f"### 📋 Roster for {today_str}")
    
    with st.form("quick_attendance"):
        st.markdown("#### Students")
        student_status = {}
        for i, s in enumerate(students):
            col1, col2 = st.columns([1, 3])
            with col1:
                st.write(f"**{s}**")
            with col2:
                student_status[s] = st.radio("Status", ["Present", "Absent", "Leave", "WFH"], key=f"s_{s}", horizontal=True, label_visibility="collapsed")
                
        st.markdown("#### Core Team")
        team_status = {}
        for i, t in enumerate(team):
            col1, col2 = st.columns([1, 3])
            with col1:
                st.write(f"**{t}**")
            with col2:
                team_status[t] = st.radio("Status", ["Present", "Absent", "Leave", "WFH"], key=f"t_{t}", horizontal=True, label_visibility="collapsed")
        
        if st.form_submit_button("💾 Save Today's Attendance", use_container_width=True):
            new_records = []
            for s, stat in student_status.items():
                new_records.append({'DATE': today_str, 'NAME': s, 'ROLE_TYPE': 'Student', 'OFFICE': 'Global', 'STATUS': 'Work From Home' if stat == 'WFH' else stat})
            for t, stat in team_status.items():
                new_records.append({'DATE': today_str, 'NAME': t, 'ROLE_TYPE': 'Core Team', 'OFFICE': 'Global', 'STATUS': 'Work From Home' if stat == 'WFH' else stat})
            
            new_df = pd.DataFrame(new_records)
            st.session_state.attendance_df = pd.concat([new_df, st.session_state.attendance_df], ignore_index=True)
            update_state_and_save('attendance_df', st.session_state.attendance_df, 'attendance')
            st.success("Attendance successfully saved! View analytics in the Dashboard.")
            st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("### 📜 Recent Attendance Logs")
    if not st.session_state.attendance_df.empty:
        recent_df = st.session_state.attendance_df.head(20)
        for i, row in recent_df.iterrows():
            with st.container(border=True):
                c1, c2, c3, c4 = st.columns([2, 3, 2, 1])
                c1.markdown(f"**{row['DATE']}**")
                c2.write(row['NAME'])
                c3.write(row['STATUS'])
                if c4.button("🗑️", key=f"del_att_{i}_{row['NAME']}", use_container_width=True):
                    df = st.session_state.attendance_df
                    df = df.drop(i).reset_index(drop=True)
                    update_state_and_save('attendance_df', df, 'attendance')
                    st.rerun()

def reports_page():
    st.markdown("<h1 class='gradient-text'>Reports</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color: #94a3b8;'>Generate and download monthly reports for projects, students, and attendance</p>", unsafe_allow_html=True)

    # 🏺 Report Filters
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    st.markdown("### 🏺 Report Filters")
    cf1, cf2, cf3, cf4 = st.columns(4)
    with cf1:
        report_type = st.selectbox("Report Type", ["Projects Report", "Students Report", "Attendance Report"])
    with cf2:
        office_filter = st.selectbox("Office", ["All Offices", "Ooty Office", "Coimbatore Office"])
    with cf3:
        month_filter = st.selectbox("Month", ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"])
    with cf4:
        year_filter = st.selectbox("Year", ["2025", "2026", "2027"])
    st.markdown("</div>", unsafe_allow_html=True)

    # Filtering Logic
    month_num = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"].index(month_filter) + 1
    year_val = int(year_filter)
    
    if report_type == "Projects Report":
        df = st.session_state.projects_df.copy()
        date_col = 'START_DATE'
    elif report_type == "Students Report":
        df = st.session_state.students_df.copy()
        date_col = 'ENROLLMENT'
    else:
        df = st.session_state.attendance_df.copy()
        date_col = 'DATE'

    if not df.empty and date_col in df.columns:
        df[date_col] = pd.to_datetime(df[date_col], errors='coerce')
        # Apply office filter
        if office_filter != "All Offices":
            office_name = office_filter.split(" ")[0]
            df = df[df['OFFICE'] == office_name]
        
        # Filter by month and year
        # For preview, we show the filtered data. But for metrics we might want to show globals or filtered.
        # Screenshot shows 112 attendance records, so it's likely filtered or cumulative.
        filtered_df = df[(df[date_col].dt.month == month_num) & (df[date_col].dt.year == year_val)].copy()
    else:
        filtered_df = df.copy()

    # Metrics Row
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        num_projects = len(st.session_state.projects_df)
        st.markdown(create_glass_metric("Projects", num_projects, "📁", "#3B82F6"), unsafe_allow_html=True)
    with m2:
        num_students = len(st.session_state.students_df)
        st.markdown(create_glass_metric("Students", num_students, "👥", "#10B981"), unsafe_allow_html=True)
    with m3:
        num_attendance = len(st.session_state.attendance_df)
        st.markdown(create_glass_metric("Attendance Records", num_attendance, "📅", "#8B5CF6"), unsafe_allow_html=True)
    with m4:
        num_activities = len(st.session_state.project_tasks_df)
        st.markdown(create_glass_metric("Activities", num_activities, "📝", "#F59E0B"), unsafe_allow_html=True)

    # Download Report Section
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    st.markdown("### Download Report")
    d1, d2, d3 = st.columns([1, 1, 1])
    
    # Data Preparation for export
    export_df = filtered_df.copy()
    if not export_df.empty and date_col in export_df.columns:
        export_df[date_col] = export_df[date_col].dt.strftime('%Y-%m-%d')

    # Excel Export
    output_excel = io.BytesIO()
    with pd.ExcelWriter(output_excel, engine='openpyxl') as writer:
        export_df.to_excel(writer, index=False, sheet_name='Report')
    excel_data = output_excel.getvalue()

    # CSV Export
    csv_data = export_df.to_csv(index=False).encode('utf-8')

    # PDF Export (using fpdf2)
    try:
        from fpdf import FPDF
        class PDF(FPDF):
            def header(self):
                self.set_font('helvetica', 'B', 15)
                self.cell(0, 10, f'Insilicomics - {report_type}', 0, 1, 'C')
                self.ln(5)
            def footer(self):
                self.set_y(-15)
                self.set_font('helvetica', 'I', 8)
                self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

        pdf = PDF()
        pdf.add_page()
        pdf.set_font("helvetica", size=10)
        # Add basic info
        pdf.cell(0, 10, f"Filter: {office_filter} | {month_filter} {year_filter}", 0, 1, 'L')
        pdf.ln(5)
        
        # Simple Table
        if not export_df.empty:
            cols = export_df.columns.tolist()[:6] # Limit columns for PDF layout
            page_width = pdf.w - 2 * pdf.l_margin
            c_width = page_width / len(cols)
            
            # Header
            pdf.set_fill_color(200, 220, 255)
            pdf.set_font("helvetica", 'B', 8)
            for col in cols:
                pdf.cell(c_width, 8, str(col), 1, 0, 'C', 1)
            pdf.ln()
            
            # Data
            pdf.set_font("helvetica", size=7)
            for _, row in export_df.head(50).iterrows():
                for col in cols:
                    pdf.cell(c_width, 7, str(row[col])[:20], 1)
                pdf.ln()
        
        # FIX: Ensure output is bytes for Streamlit
        pdf_output = pdf.output()
        if isinstance(pdf_output, str):
            pdf_data = pdf_output.encode('latin-1')
        else:
            pdf_data = bytes(pdf_output)
            
    except Exception as e:
        pdf_data = f"PDF Generation Error: {str(e)}".encode('utf-8')

    # Filename format
    file_prefix = f"insilicomics_{report_type.lower().replace(' ', '_')}_{month_filter}_{year_filter}"

    with d1:
        st.markdown('<div class="pdf-download">', unsafe_allow_html=True)
        st.download_button("📥 Download PDF", data=pdf_data, file_name=f"{file_prefix}.pdf", use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    with d2:
        st.markdown('<div class="excel-download">', unsafe_allow_html=True)
        st.download_button("📥 Download Excel", data=excel_data, file_name=f"{file_prefix}.xlsx", use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    with d3:
        st.markdown('<div class="csv-download">', unsafe_allow_html=True)
        st.download_button("📥 Download CSV", data=csv_data, file_name=f"{file_prefix}.csv", use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

    # Report Preview Table
    st.markdown(f"### Report Preview - {report_type}")
    st.markdown(f"<p style='color: #94a3b8;'>{month_filter} {year_filter} | {office_filter}</p>", unsafe_allow_html=True)
    
    if not filtered_df.empty:
        # Display nicely formatted table like the screenshot
        display_df = filtered_df.copy()
        if report_type == "Projects Report":
            # Select specific columns to match screenshot
            display_df = display_df[['PROJECT_ID', 'TITLE', 'CLIENT', 'OFFICE', 'STATUS', 'PROGRESS']]
            # Format Progress with %
            display_df['PROGRESS'] = display_df['PROGRESS'].astype(str) + "%"
        
        st.dataframe(display_df, use_container_width=True, hide_index=True)
    else:
        st.info("No records found for the selected filters.")

def bio_games_page():
    st.markdown("<h1 class='gradient-text'>🎮 Bio-Games Hub</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color: #94a3b8;'>Interactive training modules & bioinformatics challenges. Touch a module to expand!</p>", unsafe_allow_html=True)
    
    with st.expander("🧬 Challenge 1: DNA Complement Matcher", expanded=True):
        st.markdown("#### Find the matching DNA strand for the sequence.")
        
        sequence = st.session_state.get('dna_seq', ''.join(np.random.choice(['A', 'T', 'G', 'C'], 10)))
        if 'dna_seq' not in st.session_state:
            st.session_state.dna_seq = sequence
            
        st.markdown(f"<h2 style='letter-spacing: 10px; color: #10B981; text-align: center; background: rgba(0,0,0,0.3); padding: 20px; border-radius: 10px;'>{st.session_state.dna_seq}</h2>", unsafe_allow_html=True)
        
        col1, col2 = st.columns([3, 1])
        with col1:
            user_match = st.text_input("Enter complement (A-T, G-C):", key="dna_input", placeholder="e.g., TACG...").upper()
        with col2:
            st.markdown("<br>", unsafe_allow_html=True)
            check_dna = st.button("Check Match", use_container_width=True)
            
        if check_dna:
            complement = ''.join([{'A':'T', 'T':'A', 'G':'C', 'C':'G'}[b] for b in st.session_state.dna_seq])
            if user_match == complement:
                st.success("🎉 Perfect Match! Sequence translated successfully.")
                st.balloons()
            else:
                st.error(f"Mismatch. Keep trying! (Hint: Starts with {complement[0]})")
                
        if st.button("↻ Generate New Sequence", use_container_width=True):
            st.session_state.dna_seq = ''.join(np.random.choice(['A', 'T', 'G', 'C'], 10))
            st.rerun()

    with st.expander("🔬 Challenge 2: Codon to Amino Acid Translator", expanded=False):
        st.markdown("#### Translate the RNA codon into its 1-letter Amino Acid code.")
        
        codons = {"AUG": "M", "UUU": "F", "GCU": "A", "GCA": "A", "UAA": "Stop", "UAG": "Stop", "UGG": "W", "GGC": "G"}
        if 'current_codon' not in st.session_state:
            st.session_state.current_codon = np.random.choice(list(codons.keys()))
            
        st.markdown(f"<h2 style='letter-spacing: 10px; color: #3B82F6; text-align: center; background: rgba(0,0,0,0.3); padding: 20px; border-radius: 10px;'>{st.session_state.current_codon}</h2>", unsafe_allow_html=True)
        
        col3, col4 = st.columns([3, 1])
        with col3:
            aa_guess = st.text_input("Enter Amino Acid (1-letter or 'Stop'):", key="aa_input", placeholder="e.g., M").title()
        with col4:
            st.markdown("<br>", unsafe_allow_html=True)
            check_aa = st.button("Translate", use_container_width=True)
            
        if check_aa:
            correct_aa = codons[st.session_state.current_codon]
            if aa_guess == correct_aa.split(' ')[0]:
                st.success(f"✅ Correct Translation! It is {correct_aa}")
                st.snow()
            else:
                st.error(f"Incorrect. Try again!")
                
        if st.button("↻ Next Codon", use_container_width=True):
            st.session_state.current_codon = np.random.choice(list(codons.keys()))
            st.rerun()

    with st.expander("🧩 Challenge 3: Molecular Docking Setup Match", expanded=False):
        st.markdown("#### Match the Docking Term to its Definition.")
        
        docking_terms = {
            "Ligand": "The small molecule that binds to the receptor.",
            "Receptor": "The target macromolecule (usually a protein).",
            "Active Site": "The specific region where binding occurs.",
            "Binding Affinity": "Strength of interaction between molecules.",
            "Pose": "A specific 3D orientation of the ligand in the pocket."
        }
        
        if 'docking_term' not in st.session_state:
            st.session_state.docking_term = np.random.choice(list(docking_terms.keys()))
            st.session_state.docking_options = np.random.permutation(list(docking_terms.values()))

        st.markdown(f"**Term to identify:**")
        st.markdown(f"<h3 style='color: #F59E0B; text-align: center; background: rgba(0,0,0,0.3); padding: 10px; border-radius: 10px;'>{st.session_state.docking_term}</h3>", unsafe_allow_html=True)
        
        user_choice = st.radio("Select the correct definition:", st.session_state.docking_options, index=None, key="docking_radio")
        
        if st.button("Check Answer", key="btn_docking"):
            if user_choice:
                if user_choice == docking_terms[st.session_state.docking_term]:
                    st.success("🎯 Spot on! That is correct.")
                    st.balloons()
                else:
                    st.error("Incorrect. Review your docking concepts!")
            else:
                st.warning("Please select an option.")
                
        if st.button("↻ Next Term", use_container_width=True, key="btn_next_docking"):
            st.session_state.docking_term = np.random.choice(list(docking_terms.keys()))
            st.session_state.docking_options = np.random.permutation(list(docking_terms.values()))
            st.rerun()

    with st.expander("🌊 Challenge 4: MD Simulation Pipeline", expanded=False):
        st.markdown("#### Order the steps of a standard Molecular Dynamics Simulation.")
        
        correct_order = ["1. Topology Generation", "2. Solvation", "3. Adding Ions", "4. Energy Minimization", "5. Equilibration (NVT/NPT)", "6. Production Run"]
        
        st.markdown("Here are the steps shuffled. Can you identify the correct sequential order?")
        
        shuffled = np.random.RandomState(seed=42).permutation(correct_order).tolist()
        
        user_order = []
        for i in range(len(correct_order)):
            choice = st.selectbox(f"Step {i+1}:", ["-- Select --"] + shuffled, key=f"md_step_{i}")
            user_order.append(choice)
            
        if st.button("Validate Pipeline", key="btn_md"):
            if "-- Select --" in user_order:
                st.warning("Please select all steps.")
            elif user_order == correct_order:
                st.success("🏆 Perfect! Your simulation will run flawlessly.")
                st.snow()
            else:
                st.error("Simulation crashed! Check the fundamental order of operations.")



def project_types_page():
    st.markdown("<h1 class='gradient-text'>🏷️ Project Types</h1>", unsafe_allow_html=True)
    st.markdown("Configure and manage project classifications (e.g., Molecular Dynamics, Docking, QSAR).")
    
    if 'project_types_list' not in st.session_state:
        st.session_state.project_types_list = ["Molecular Dynamics", "Virtual Screening", "QSAR", "Homology Modeling"]
        
    with st.form("add_proj_type"):
        new_type = st.text_input("New Project Type / Category")
        if st.form_submit_button("Add Category") and new_type:
            if new_type not in st.session_state.project_types_list:
                st.session_state.project_types_list.append(new_type)
                st.success(f"Added {new_type}!")
                st.rerun()
            else:
                st.warning("Category already exists.")
                
    st.markdown("### 📋 Active Categories")
    cols = st.columns(4)
    for i, p_type in enumerate(st.session_state.project_types_list):
        with cols[i % 4]:
            st.markdown(f"<div class='glass-card' style='padding:15px; text-align:center;'><b>{p_type}</b></div>", unsafe_allow_html=True)

def clients_page():
    st.markdown("<h1 class='gradient-text'>🏢 Client Directory</h1>", unsafe_allow_html=True)
    st.markdown("Manage external clients and institutional partners.")
    
    if 'clients_list' not in st.session_state:
        st.session_state.clients_list = ["Biome", "PharmaTech", "Ooty Univ", "BioSim", "NatureMed"]
        
    with st.form("add_client"):
        c1, c2 = st.columns(2)
        with c1:
            new_client = st.text_input("Client / Institution Name *")
        with c2:
            contact = st.text_input("Primary Contact / Email")
        if st.form_submit_button("Onboard Client") and new_client:
            if new_client not in st.session_state.clients_list:
                st.session_state.clients_list.append(new_client)
                st.success(f"Onboarded client: {new_client}!")
                st.rerun()
            else:
                st.warning("Client already exists.")

    st.markdown("### 🤝 Registered Partners")
    cols = st.columns(3)
    for i, client in enumerate(st.session_state.clients_list):
        with cols[i % 3]:
            st.markdown(f"<div class='glass-card' style='padding:15px; text-align:center;'><h3 style='margin:0; color:#10B981;'>{client}</h3><small>Active Partner</small></div>", unsafe_allow_html=True)

def education_page():
    st.markdown("<h1 class='gradient-text'>📚 Education & Activities</h1>", unsafe_allow_html=True)
    st.markdown("<div class='glass-card'>Add workshops, training courses, and seminars for students and staff.</div>", unsafe_allow_html=True)
    
    with st.form("add_edu"):
        col1, col2 = st.columns(2)
        with col1:
            st.text_input("Activity Name")
            st.selectbox("Type", ["Workshop", "Course", "Seminar", "Training"])
        with col2:
            st.date_input("Date")
            st.text_input("Instructor/Lead")
        if st.form_submit_button("Add Activity"):
            st.success("Activity added successfully.")

# Application Routing

if not st.session_state.logged_in:
    login_page()
else:
    render_sidebar()
    page = st.session_state.current_page
    
    if page == 'Bio-Games Hub': bio_games_page()
    elif page == 'Dashboard': dashboard_page()
    elif page == 'Projects Center': projects_page()
    elif page == 'Project Workspace': project_workspace_page()
    elif page == 'Server Infrastructure': servers_page()
    elif page == 'Core Team': team_page()
    elif page == 'Students': students_page()
    elif page == 'Attendance': attendance_page()
    elif page == 'Project Types': project_types_page()
    elif page == 'Clients': clients_page()
    elif page == 'Education': education_page()
    elif page == 'Reports': reports_page()
    else: st.info(f"Module '{page}' is initializing...")
