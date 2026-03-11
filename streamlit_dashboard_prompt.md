# Streamlit Dashboard Development Prompt

## Project Overview

Create a comprehensive **Lab/Research Project Management Dashboard** for a company called "Insilicomics" (or "BioSimCom") - a Lab Management System for managing research projects, students, servers, and activities across multiple office locations (Ooty and Coimbatore).

---

## System Architecture

### 1. Authentication System (Login Page)

**Design Specifications:**
- Clean, centered login card on white background
- Company logo: Green square with white flask/beaker icon
- Company name: "Insilicomics" in bold dark text
- Tagline: "Lab Management System" in smaller gray text
- Two input fields: Email and Password
- Green "Sign In" button (#10B981)
- Copyright footer: "© 2025 insilicomics. All rights reserved."

---

### 2. Main Dashboard (Home Page)

**Layout:**
- Left sidebar navigation (fixed width ~200px)
- Main content area with responsive grid

**Sidebar Navigation:**
```
- Dashboard (home icon) [active on main page]
- Projects (folder icon)
- Project Types (document icon)
- Clients (user icon)
- Team (users icon)
- Servers (server icon)
- Students (graduation cap icon)
- Attendance (calendar icon)
- Education (book icon)
- Reports (chart icon)
```

**User Profile Section (Bottom of Sidebar):**
- User avatar/name: "Mr. Vishnu Raj"
- Email display
- Logout button
- System status: "System Online" with green dot
- Copyright: "© 2023 Insilicomics"

**Main Content - Office Summary Cards (Top Row):**
Three horizontal cards showing:
1. **All Offices**: "8 Active, 31 projects • 26 students"
2. **Ooty Office**: "5 Active, 43 projects • 14 students" (light green background)
3. **Coimbatore Office**: "3 Active, 8 projects • 12 students" (light blue background)

**Metric Cards (Middle Row - 6 cards):**
| Card | Value | Icon |
|------|-------|------|
| Total Projects | 51 | Document icon |
| Active Projects | 8 | Graph icon |
| Students | 26 | User icon |
| Activities | 368 | Lightning bolt icon |
| Team Members | 9 | People icon |
| Servers | 16 | Server icon |

**Education Metric Card:**
- Education: 13 (book icon)

**Charts Section (Bottom Row):**
1. **Year-wise Overview (Bar Chart):**
   - Compare two years (2025 vs 2026)
   - Y-axis: 0-360 scale
   - Two bar colors: Blue (Projects), Green (Activities)
   - Calendar icon with title

2. **Monthly Trend 2026 (Area Chart):**
   - X-axis: Jan-Dec months
   - Y-axis: 0-180 scale
   - Green filled area with blue outline
   - Wave icon with title

---

### 3. Projects Management Page

**Header:**
- Title: "Projects"
- Subtitle: "Manage research projects and their progress"
- "Add Project" button (dark blue with plus icon)

**Office Summary Cards:**
- Ooty Office: 43 total, 5 active (light green background)
- Coimbatore Office: 8 total, 5 active (light blue background)

**Search & Filter Bar:**
- Search input: "Search projects by title, client, team lead, or status..."
- Office filter dropdown: "Ooty Office" (with green dot indicator)

**Projects Data Table:**
| Column | Description |
|--------|-------------|
| PROJECT ID | Alphanumeric (e.g., PRJ-658C8476) |
| TITLE | Project name/description |
| CLIENT | Client name |
| UNIVERSITY | Institution with building icon |
| TEAM LEAD | Team lead name |
| STATUS | Badge (Completed=green, Active=blue) |
| PROGRESS | Progress bar with percentage (purple gradient) |
| ACTIONS | View, Edit, Delete icons |

**Sample Data:**
```
PRJ-658C8476 | 500 ns Simulation of 3OMC Work | Mr. Sameer Sharma | Biome | Dr. Vivek Chandramohan | Completed | 100%
```

---

### 4. Project Types Page

**Header:**
- Title: "Project Types"
- Subtitle: "Manage research project categories"
- "Add Project Type" button (green with plus icon)

**Search Bar:**
- "Search project types..."

**Grid Layout (3 columns):**
Project type cards with:
- Green folder icon (circular background)
- Project type name
- Edit and Delete action icons

**Sample Project Types:**
- Molecular Dynamics Simulation
- Docking Studies
- Free Energy Calculations
- Protein Structure Analysis
- Virtual Screening
- QSAR Analysis
- ADMET Prediction
- Pharmacophore Modeling
- Machine Learning Applications

---

### 5. Servers Management Page

**Header:**
- Title: "Servers"
- Subtitle: "Manage computational servers and hardware"
- "Add Server" button (green with plus icon)

**Search Bar:**
- "Search servers by name or type..."

**Grid Layout (3 columns):**
Server cards with:
- Green gear icon
- Server name (bold)
- Location/project (lighter text)
- "Available" badge (light green background)
- Edit and Delete icons

**Sample Servers:**
```
MSI - RTX 3070 Ti (Insiliconics)
Insiliconics - RTX 3090 Ti 24GB (Insiliconics)
Zotac - RTX 3070Ti (Insiliconics)
Zotac - RTX 1060 (Insiliconics)
MSI - RTX 4060 (COL-1)
MSI - RTX 4060 (COL-2)
MSI - RTX 3080 (COL-3)
Laptop (Vishnu)
Laptop (Insiliconics)
Laptop (Gilbert)
Laptop (Vivek)
MSI - RTX 4060 (COL-4)
```

---

### 6. Students Management Page

**Header:**
- Title: "Students"
- Subtitle: "Manage student records and information"
- "Add Student" button (blue with plus icon)

**Office Summary Cards:**
- Ooty Office: 14 Total, 5 active students (light green)
- Coimbatore Office: 12 Total, 8 active students (light blue)

**Search & Filter:**
- Search input: "Search students by name, email, or status..."
- Office filter dropdown

**Students Data Table:**
| Column | Description |
|--------|-------------|
| STUDENT | Name with ID in brackets [ISOINT118] |
| EMAIL | Student email |
| STATUS | Badge (Graduated=purple, Active=green) |
| SKILLS | Comma-separated skills (MD Simulation, Molecular Docking) |
| ENROLLMENT | Date (YYYY-MM-DD) |
| ACTIONS | View, Edit, Delete icons |

**Sample Data:**
```
Mr. Deekshith M.M [ISOINT118] | deekdeekshith00@gmail.com | Graduated | MD Simulation, Molecular Docking | 2026-01-01
Mr. Anandharaj S [ISOINT119] | anandha77hari08@gmail.com | Graduated | - | 2026-01-01
```

---

### 7. Attendance Management Page

**Header:**
- Title: "Attendance Management"
- Subtitle: "Mark and manage student attendance records"

**Date Selector:**
- Date picker with calendar icon (default: current date)

**Office Status Cards:**
- Ooty Office: "5 active students" | "0/5 Present Today" (green background)
- Coimbatore Office: "8 active students" | "0/8 Present Today" (blue background)

**Attendance Summary Cards (3 cards):**
| Card | Color | Value |
|------|-------|-------|
| Present | Light green | Count |
| Late | Light yellow | Count |
| Absent | Light red | Count |

**Action Button:**
- "Mark All Present" (green button)

**Notification Banner:**
- Info banner: "5 students have not been marked for attendance today"

**Attendance Table:**
| Column | Description |
|--------|-------------|
| STUDENT | Profile icon + Name with ID |
| EMAIL | Student email |
| STATUS | Badge (Not Marked / Present / Late / Absent) |
| CHECK-IN TIME | Time stamp |
| ACTIONS | Present (✓), Late (○), Absent (✗) buttons |

---

### 8. Education Activities Page

**Header:**
- Title: "Education"
- Subtitle: "Manage education activities and training programs"
- "Add Activity" button (green with plus icon)

**Office Summary Cards:**
- Ooty Office: "Education Hub" | "0 Activities" (green background)
- Coimbatore Office: "Education Hub" | "13 Activities" (white/blue)

**Search & Filter:**
- Search input: "Search activities..."
- Office filter dropdown

**Activities Display:**
- Grid or table of education activities
- Empty state message when no activities: "No education activities found" with book icon

---

### 9. Reports Page

**Header:**
- Title: "Reports"
- Subtitle: "Generate and download monthly reports for projects, students, and attendance"

**Filter Section:**
| Filter | Options |
|--------|---------|
| Report Type | Projects Report, Students Report, Attendance Report |
| Office | All Offices, Ooty Office, Coimbatore Office |
| Month | January - December |
| Year | 2024, 2025, 2026 |

**Summary Metric Cards:**
| Card | Value | Icon |
|------|-------|------|
| Projects | 10 | Folder icon (blue) |
| Students | 0 | User icon (light blue) |
| Attendance Records | 25 | Calendar icon (green) |
| Activities | 144 | Document icon (yellow) |

**Action Buttons:**
- "Download PDF" (red button)
- "Download Excel" (green button)

**Report Preview Table:**
| Column | Description |
|--------|-------------|
| PROJECT ID | Alphanumeric identifier |
| TITLE | Project name |
| CLIENT | Client name |
| OFFICE | Office location |
| STATUS | Completed/Active badge |
| PROGRESS | Progress bar |

---

## Color Scheme & Styling

### Primary Colors:
```css
--primary-green: #10B981;     /* Active states, success, buttons */
--primary-blue: #3B82F6;      /* Secondary elements */
--primary-purple: #8B5CF6;    /* Progress bars, tertiary */
--primary-yellow: #F59E0B;    /* Warnings, activities */
--primary-red: #EF4444;       /* Errors, delete, absent */
```

### Background Colors:
```css
--bg-white: #FFFFFF;          /* Main background */
--bg-light-gray: #F9FAFB;     /* Cards, sidebar */
--bg-light-green: #D1FAE5;    /* Ooty office, present status */
--bg-light-blue: #DBEAFE;     /* Coimbatore office */
--bg-light-yellow: #FEF3C7;   /* Late status */
--bg-light-red: #FEE2E2;      /* Absent status */
```

### Text Colors:
```css
--text-primary: #374151;      /* Headings, main text */
--text-secondary: #6B7280;    /* Subtitles, labels */
--text-muted: #9CA3AF;        /* Placeholder, icons */
```

### Border Colors:
```css
--border-light: #E5E7EB;      /* Card borders, dividers */
--border-medium: #D1D5DB;     /* Input borders */
```

---

## Technical Requirements for Streamlit

### Required Libraries:
```python
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, date
import base64
from io import BytesIO
```

### Page Structure:
```python
# Use st.sidebar for navigation
# Use st.columns for grid layouts
# Use st.dataframe or st.data_editor for tables
# Use plotly for charts
# Use st.session_state for authentication
```

### Session State Management:
```python
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'current_page' not in st.session_state:
    st.session_state.current_page = 'Dashboard'
```

### Key Features to Implement:
1. **Authentication**: Login page with session management
2. **Multi-page navigation**: Sidebar with page routing
3. **CRUD Operations**: Add, View, Edit, Delete for all entities
4. **Data Tables**: Sortable, searchable tables
5. **Charts**: Bar charts, area charts, progress indicators
6. **Export**: PDF and Excel download functionality
7. **Filters**: Office, date, status filters
8. **Responsive Design**: Using st.columns for layouts

---

## Sample Data Structure

### Projects DataFrame:
```python
projects_data = {
    'project_id': ['PRJ-658C8476', 'PRJ-729D9123', ...],
    'title': ['500 ns Simulation of 3OMC Work', ...],
    'client': ['Mr. Sameer Sharma', ...],
    'university': ['Biome', ...],
    'team_lead': ['Dr. Vivek Chandramohan', ...],
    'status': ['Completed', 'Active', ...],
    'progress': [100, 50, ...],
    'office': ['Ooty', 'Coimbatore', ...]
}
```

### Students DataFrame:
```python
students_data = {
    'student_id': ['ISOINT118', 'ISOINT119', ...],
    'name': ['Mr. Deekshith M.M', ...],
    'email': ['deekdeekshith00@gmail.com', ...],
    'status': ['Graduated', 'Active', ...],
    'skills': ['MD Simulation, Molecular Docking', ...],
    'enrollment_date': ['2026-01-01', ...],
    'office': ['Ooty', 'Coimbatore', ...]
}
```

### Servers DataFrame:
```python
servers_data = {
    'server_id': [1, 2, 3, ...],
    'name': ['MSI - RTX 3070 Ti', ...],
    'type': ['GPU Server', 'Laptop', ...],
    'location': ['Insiliconics', 'COL-1', ...],
    'status': ['Available', 'In Use', ...]
}
```

---

## UI Components Reference

### Card Component:
```
┌─────────────────────────────┐
│  📊 Total Projects          │
│  51                         │
└─────────────────────────────┘
```

### Status Badge:
```
┌──────────┐   ┌──────────┐   ┌──────────┐
│ Completed│   │  Active  │   │ Graduated│
│  (green) │   │  (blue)  │   │ (purple) │
└──────────┘   └──────────┘   └──────────┘
```

### Progress Bar:
```
████████████████████████████████ 100%
```

### Action Icons:
```
👁️ View  |  ✏️ Edit  |  🗑️ Delete
```

---

## Implementation Priority

1. **Phase 1**: Authentication + Main Dashboard
2. **Phase 2**: Projects + Project Types pages
3. **Phase 3**: Students + Attendance pages
4. **Phase 4**: Servers + Education pages
5. **Phase 5**: Reports page with export functionality

---

## Notes

- All forms should include validation
- Use st.toast() for success/error notifications
- Implement confirmation dialogs for delete actions
- Add loading spinners for data operations
- Ensure mobile-responsive layouts using column ratios
- Use st.cache_data for data caching
- Implement proper error handling throughout
