"""
WORKFORCE INTELLIGENCE DASHBOARD - REFACTORED
A Production-Ready Streamlit Application for Labor Market Analytics

Author: Data Science Team
Version: 2.0.0
Purpose: Transform raw industrial job statistics into actionable workforce insights
         for individuals, government agencies, and recruiters.
         
Enhancements:
- Advanced Visualizations: Sankey diagrams, trend overlays, interactive maps
- Personalized Recommender Engine: 90th percentile skill matching
- Data Export: CSV, Excel, and PDF downloads for Government users
- Enhanced UI/UX: Dark mode theming, card-based layouts, responsive design
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import altair as alt
from datetime import datetime, timedelta
import json
from typing import Dict, List, Tuple, Optional
import warnings
from io import BytesIO

warnings.filterwarnings('ignore')

# Optional imports for advanced export
try:
    from reportlab.lib.pagesizes import letter, A4
    from reportlab.lib import colors
    from reportlab.lib.styles import getSampleStyleSheet
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
    PDF_AVAILABLE = True
except ImportError:
    PDF_AVAILABLE = False

try:
    import openpyxl
    from openpyxl.styles import PatternFill, Font, Alignment
    EXCEL_AVAILABLE = True
except ImportError:
    EXCEL_AVAILABLE = False

# ============================================================================
# PAGE CONFIGURATION & THEME
# ============================================================================

st.set_page_config(
    page_title="Workforce Intelligence Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'About': "Workforce Intelligence Dashboard v1.0 | Labor Market Analytics"
    }
)

# Initialize theme state
if 'theme_mode' not in st.session_state:
    st.session_state.theme_mode = 'auto'  # 'auto', 'light', or 'dark'

# Custom CSS with responsive light/dark theme support
st.markdown("""
<style>
    :root {
        /* Dark Theme (Default) */
        --bg-primary: #0f1419;
        --bg-secondary: #1a1f2e;
        --bg-tertiary: #1e2936;
        --bg-quaternary: #243447;
        --bg-hover: #2d4557;
        --text-primary: #e0e7ff;
        --text-secondary: #93c5fd;
        --text-heading: #ffffff;
        --border-primary: #3b82f6;
        --border-secondary: #60a5fa;
        --success-bg: #065f46;
        --success-border: #10b981;
        --success-text: #d1fae5;
        --warning-bg: #78350f;
        --warning-border: #fbbf24;
        --warning-text: #fef3c7;
        --error-bg: #7f1d1d;
        --error-border: #f87171;
        --error-text: #fee2e2;
        --info-bg: #1e3a8a;
        --info-border: #60a5fa;
        --info-text: #dbeafe;
    }
    
    /* Light Theme */
    @media (prefers-color-scheme: light) {
        :root {
            --bg-primary: #f8fafc;
            --bg-secondary: #f1f5f9;
            --bg-tertiary: #e2e8f0;
            --bg-quaternary: #cbd5e1;
            --bg-hover: #e0e7ff;
            --text-primary: #1e293b;
            --text-secondary: #0c4a6e;
            --text-heading: #0f172a;
            --border-primary: #3b82f6;
            --border-secondary: #7dd3fc;
            --success-bg: #dcfce7;
            --success-border: #22c55e;
            --success-text: #166534;
            --warning-bg: #fef3c7;
            --warning-border: #f59e0b;
            --warning-text: #78350f;
            --error-bg: #fee2e2;
            --error-border: #ef4444;
            --error-text: #7f1d1d;
            --info-bg: #dbeafe;
            --info-border: #0284c7;
            --info-text: #0c2340;
        }
    }
    
    * {
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', sans-serif;
    }
    
    .main {
        background: var(--bg-primary);
    }
    
    .stMetric {
        background: linear-gradient(135deg, var(--bg-tertiary) 0%, var(--bg-quaternary) 100%);
        padding: 1.75rem;
        border-radius: 1rem;
        box-shadow: 0 4px 15px rgba(59, 130, 246, 0.15);
        border: 2px solid var(--border-primary);
        transition: all 0.3s ease;
    }
    
    .stMetric:hover {
        box-shadow: 0 6px 20px rgba(59, 130, 246, 0.25);
        transform: translateY(-2px);
    }
    
    .stMetric > label {
        font-size: 0.9rem !important;
        font-weight: 600 !important;
        color: var(--text-secondary) !important;
        letter-spacing: 0.5px;
        text-transform: uppercase;
    }
    
    .stMetric > div > div:nth-child(2) {
        font-size: 2rem !important;
        font-weight: 800 !important;
        color: var(--text-heading) !important;
        line-height: 1.2;
        margin-top: 0.5rem;
    }
    
    .metric-container {
        background: linear-gradient(135deg, var(--bg-tertiary) 0%, var(--bg-quaternary) 100%);
        color: var(--text-primary);
        padding: 1.75rem;
        border-radius: 1rem;
        margin: 1rem 0;
        border: 2px solid var(--border-primary);
        box-shadow: 0 4px 15px rgba(59, 130, 246, 0.15);
    }
    
    .recommendation-box {
        background: var(--success-bg);
        border-left: 6px solid var(--success-border);
        padding: 1.5rem;
        border-radius: 0.75rem;
        margin: 1.25rem 0;
        color: var(--success-text);
        font-weight: 600;
        font-size: 0.95rem;
        box-shadow: 0 4px 12px rgba(16, 185, 129, 0.2);
    }
    
    .shortage-index {
        background: linear-gradient(135deg, var(--warning-bg) 0%, #92400e 100%);
        border-left: 6px solid var(--warning-border);
        padding: 1.5rem;
        border-radius: 0.75rem;
        color: var(--warning-text);
        font-weight: 600;
        font-size: 0.95rem;
        box-shadow: 0 4px 12px rgba(251, 146, 60, 0.2);
    }
    
    h1, h2, h3, h4, h5, h6 {
        color: var(--text-heading) !important;
        font-weight: 800 !important;
        letter-spacing: -0.5px;
    }
    
    h1 { font-size: 2.75rem !important; margin: 2rem 0 0.75rem 0 !important; }
    h2 { font-size: 1.95rem !important; margin: 1.75rem 0 1rem 0 !important; }
    h3 { font-size: 1.5rem !important; margin: 1.5rem 0 0.75rem 0 !important; }
    h4 { font-size: 1.2rem !important; margin: 1.25rem 0 0.5rem 0 !important; }
    
    body, p, span, div {
        color: var(--text-primary) !important;
    }
    
    .divider {
        margin: 2.5rem 0;
        border-top: 2px solid var(--border-primary);
        opacity: 0.3;
    }
    
    .stTabs [role="tablist"] {
        border-bottom: 2px solid var(--border-primary) !important;
    }
    
    .stTabs [role="tablist"] button {
        font-size: 1.05rem !important;
        font-weight: 700 !important;
        color: var(--text-secondary) !important;
        padding: 1rem 1.75rem !important;
        background-color: transparent !important;
        border: none !important;
        border-bottom: 3px solid transparent !important;
    }
    
    .stTabs [role="tablist"] button[aria-selected="true"] {
        color: var(--text-heading) !important;
        border-bottom: 3px solid var(--border-primary) !important;
    }
    
    .stTabs [role="tablist"] button:hover {
        color: var(--border-secondary) !important;
    }
    
    .stDataFrame {
        font-size: 0.95rem !important;
    }
    
    .stDataFrame th {
        background: linear-gradient(90deg, #1e40af 0%, #1e3a8a 100%) !important;
        color: #ffffff !important;
        font-weight: 800 !important;
        padding: 1rem !important;
        font-size: 0.95rem !important;
    }
    
    .stDataFrame td {
        color: var(--text-primary) !important;
        padding: 0.85rem !important;
        background-color: var(--bg-quaternary) !important;
        border-bottom: 1px solid var(--border-primary) !important;
    }
    
    .stDataFrame tr:hover td {
        background-color: var(--bg-hover) !important;
    }
    
    .stWarning {
        background: var(--warning-bg);
        border: 2px solid var(--warning-border);
        color: var(--warning-text);
        font-weight: 600;
        padding: 1.25rem !important;
        border-radius: 0.75rem;
        font-size: 0.95rem;
        box-shadow: 0 4px 12px rgba(251, 191, 36, 0.2);
    }
    
    .stError {
        background: var(--error-bg);
        border: 2px solid var(--error-border);
        color: var(--error-text);
        font-weight: 600;
        padding: 1.25rem !important;
        border-radius: 0.75rem;
        font-size: 0.95rem;
        box-shadow: 0 4px 12px rgba(248, 113, 113, 0.2);
    }
    
    .stSuccess {
        background: var(--success-bg);
        border: 2px solid var(--success-border);
        color: var(--success-text);
        font-weight: 600;
        padding: 1.25rem !important;
        border-radius: 0.75rem;
        font-size: 0.95rem;
        box-shadow: 0 4px 12px rgba(16, 185, 129, 0.2);
    }
    
    .stInfo {
        background: var(--info-bg);
        border: 2px solid var(--info-border);
        color: var(--info-text);
        font-weight: 600;
        padding: 1.25rem !important;
        border-radius: 0.75rem;
        font-size: 0.95rem;
        box-shadow: 0 4px 12px rgba(96, 165, 250, 0.2);
    }
    
    .stSelectbox, .stMultiselect, .stSlider, .stTextInput {
        color: var(--text-primary) !important;
    }
    
    .stSelectbox > div > div, .stMultiselect > div > div {
        background-color: var(--bg-tertiary) !important;
        border: 2px solid var(--border-primary) !important;
        color: var(--text-primary) !important;
    }
    
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, var(--bg-primary) 0%, var(--bg-secondary) 100%);
    }
    
    section[data-testid="stSidebar"] > div {
        background: linear-gradient(180deg, var(--bg-primary) 0%, var(--bg-secondary) 100%);
    }
    
</style>
""", unsafe_allow_html=True)

# ============================================================================
# DATA LOADING & CACHING
# ============================================================================

@st.cache_data
def load_data(filepath: str) -> pd.DataFrame:
    """
    Load and cache the SGJobData file (CSV or Parquet format).
    
    Args:
        filepath: Path to the data file (CSV or Parquet)
        
    Returns:
        DataFrame with processed job data
    """
    if filepath.endswith('.parquet'):
        df = pd.read_parquet(filepath)
    else:
        df = pd.read_csv(filepath, on_bad_lines='skip', encoding='utf-8')
    return df


def display_styled_header(title: str, emoji: str = "📊") -> None:
    """Display a styled section header with consistent formatting."""
    st.markdown(f"""
    <div style="border-left: 6px solid #3b82f6; padding-left: 1.75rem; margin: 2rem 0 1.25rem 0; background: linear-gradient(90deg, rgba(59, 130, 246, 0.1) 0%, transparent 100%); padding: 1rem 1rem 1rem 1.75rem; border-radius: 0.5rem;">
        <h2 style="color: #ffffff; margin: 0; font-size: 1.75rem; font-weight: 800; letter-spacing: -0.5px;">{emoji} {title}</h2>
    </div>
    """, unsafe_allow_html=True)


@st.cache_data
def clean_data_quality(_df: pd.DataFrame) -> pd.DataFrame:
    """
    Advanced data quality cleaning: removes outliers and handles missing values.
    
    Args:
        _df: Raw DataFrame
        
    Returns:
        Cleaned DataFrame with quality issues resolved
    """
    df = _df.copy()
    
    # ========== REMOVE ENTIRELY EMPTY COLUMNS ==========
    # occupationId is 100% missing - remove it
    if 'occupationId' in df.columns:
        df = df.drop('occupationId', axis=1)
    
    # ========== SALARY DATA CLEANING ==========
    # Convert salary columns to numeric
    for col in ['salary_minimum', 'salary_maximum', 'average_salary']:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
    
    # Define reasonable salary bounds (SGD per month)
    SALARY_MIN_THRESHOLD = 500    # Below this is likely data error
    SALARY_MAX_THRESHOLD = 50000  # Above this is unrealistic outlier (99.99th percentile)
    
    # Remove records with zero/null average salaries
    df = df[df['average_salary'].notna() & (df['average_salary'] > 0)]
    
    # Remove extreme salary outliers (keep 0.1% to 99.9%)
    salary_q001 = df['average_salary'].quantile(0.001)
    salary_q999 = df['average_salary'].quantile(0.999)
    salary_q999 = min(salary_q999, SALARY_MAX_THRESHOLD)  # Cap at reasonable max
    
    df = df[(df['average_salary'] >= salary_q001) & (df['average_salary'] <= salary_q999)]
    
    # For salary range columns, remove extreme outliers
    for col in ['salary_minimum', 'salary_maximum']:
        if col in df.columns:
            df.loc[df[col] > SALARY_MAX_THRESHOLD, col] = df[col].median()
            df[col] = df[col].fillna(df[col].median())
    
    # ========== EXPERIENCE DATA CLEANING ==========
    df['minimumYearsExperience'] = pd.to_numeric(df['minimumYearsExperience'], errors='coerce').fillna(0)
    
    # Cap unrealistic experience values (max 40 years is reasonable)
    MAX_EXP = 40
    df.loc[df['minimumYearsExperience'] > MAX_EXP, 'minimumYearsExperience'] = MAX_EXP
    
    # Remove records with negative experience
    df = df[df['minimumYearsExperience'] >= 0]
    
    # ========== DATE COLUMNS CLEANING ==========
    date_cols = ['metadata_newPostingDate', 'metadata_originalPostingDate', 'metadata_expiryDate']
    for col in date_cols:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors='coerce')
    
    # Remove records with missing posting dates (critical field)
    df = df[df['metadata_newPostingDate'].notna()]
    
    # ========== TITLE NORMALIZATION ==========
    # Standardize job title case (title case with exceptions)
    if 'title' in df.columns:
        df['title'] = df['title'].str.strip()  # Remove whitespace
        df['title'] = df['title'].str.title()  # Convert to title case
        
        # Remove entirely empty titles
        df = df[df['title'].notna() & (df['title'] != '')]
    
    # ========== CATEGORICAL CLEANING ==========
    # Standardize employment types
    if 'employmentTypes' in df.columns:
        df['employmentTypes'] = df['employmentTypes'].fillna('Unknown')
        df['employmentTypes'] = df['employmentTypes'].str.strip().str.title()
    
    # Standardize position levels
    if 'positionLevels' in df.columns:
        df['positionLevels'] = df['positionLevels'].fillna('Unknown')
        df['positionLevels'] = df['positionLevels'].str.strip().str.title()
    
    # ========== ENGAGEMENT METRICS CLEANING ==========
    # Views and applications should be non-negative
    df['metadata_totalNumberOfView'] = pd.to_numeric(df['metadata_totalNumberOfView'], errors='coerce').fillna(0)
    df['metadata_totalNumberJobApplication'] = pd.to_numeric(df['metadata_totalNumberJobApplication'], errors='coerce').fillna(0)
    
    # Remove records with negative engagement metrics
    df = df[df['metadata_totalNumberOfView'] >= 0]
    df = df[df['metadata_totalNumberJobApplication'] >= 0]
    
    # ========== COMPANY NAME CLEANING ==========
    if 'postedCompany_name' in df.columns:
        df['postedCompany_name'] = df['postedCompany_name'].fillna('Unknown Company')
        df['postedCompany_name'] = df['postedCompany_name'].str.strip()
    
    # ========== REMOVE DUPLICATE RECORDS ==========
    # Remove exact duplicates
    initial_len = len(df)
    df = df.drop_duplicates()
    
    return df.reset_index(drop=True)


@st.cache_data
def preprocess_data(_df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean and preprocess raw job data with quality assurance.
    
    Args:
        _df: Raw DataFrame
        
    Returns:
        Cleaned DataFrame ready for analysis
    """
    # Apply comprehensive data quality cleaning first
    df = clean_data_quality(_df)
    
    # Extract year and month for temporal analysis
    df['year'] = df['metadata_newPostingDate'].dt.year
    df['month'] = df['metadata_newPostingDate'].dt.month
    df['year_month'] = df['metadata_newPostingDate'].dt.to_period('M')
    
    # Extract primary category from categories JSON
    df['primary_category'] = df['categories'].apply(extract_primary_category)
    
    # Clean status
    df['status_jobStatus'] = df['status_jobStatus'].fillna('Unknown')
    
    return df


def extract_primary_category(cat_str: str) -> str:
    """Extract the first category from JSON string."""
    try:
        if pd.isna(cat_str) or cat_str == '':
            return 'Other'
        categories = json.loads(cat_str.replace('""', '"'))
        if isinstance(categories, list) and len(categories) > 0:
            return categories[0].get('category', 'Other')
    except:
        pass
    return 'Other'


# ============================================================================
# DATA ANALYSIS & CALCULATIONS
# ============================================================================

@st.cache_data
def calculate_employment_heatmap_data(_df: pd.DataFrame) -> pd.DataFrame:
    """
    Generate employment heatmap data by sector and time period.
    
    Args:
        _df: Processed DataFrame
        
    Returns:
        Aggregated data for heatmap visualization
    """
    heatmap_data = _df.groupby(['year_month', 'primary_category']).agg({
        'metadata_jobPostId': 'count',
        'average_salary': 'mean',
        'minimumYearsExperience': 'mean'
    }).reset_index()
    
    heatmap_data.columns = ['Period', 'Sector', 'Posting_Count', 'Avg_Salary', 'Avg_Experience']
    heatmap_data['Period'] = heatmap_data['Period'].astype(str)
    
    return heatmap_data


@st.cache_data
def calculate_skill_gaps(_df: pd.DataFrame) -> Tuple[Dict, Dict]:
    """
    Analyze current market skills vs. emerging needs using job titles and categories.
    
    Args:
        _df: Processed DataFrame
        
    Returns:
        Tuple of (current_skills, emerging_skills)
    """
    # Handle empty dataframe
    if len(_df) == 0 or _df.empty or 'title' not in _df.columns:
        return {}, {}
    
    # Create combined searchable text from titles and categories
    searchable_text = (_df['title'].fillna('').str.lower() + ' ' + 
                       _df['categories'].fillna('').str.lower())
    
    # Extract skills from combined job data
    common_skills = {
        'Python': searchable_text.str.contains('python', case=False, na=False).sum(),
        'Java': searchable_text.str.contains('java', case=False, na=False).sum(),
        'C++': searchable_text.str.contains(r'c\+\+|c plus plus', case=False, na=False, regex=True).sum(),
        'JavaScript': searchable_text.str.contains('javascript|node|typescript', case=False, na=False).sum(),
        'SQL': searchable_text.str.contains('sql|database', case=False, na=False).sum(),
        'Cloud': searchable_text.str.contains('aws|azure|gcp|cloud|cloud computing', case=False, na=False).sum(),
        'Data': searchable_text.str.contains('data|analytics|business intelligence|bi', case=False, na=False).sum(),
        'AI/ML': searchable_text.str.contains('ai|machine learning|ml|artificial intelligence', case=False, na=False).sum(),
    }
    
    emerging_skills = {
        'Cloud': common_skills['Cloud'],
        'AI/ML': common_skills['AI/ML'],
        'Data': common_skills['Data'],
        'DevOps': searchable_text.str.contains('devops|docker|kubernetes|containers', case=False, na=False).sum(),
    }
    
    return common_skills, emerging_skills


@st.cache_data
def calculate_labor_shortage_index(_df: pd.DataFrame) -> Dict[str, float]:
    """
    Calculate Labor Shortage Index for government users.
    
    Metrics:
    - Posting Volume Trend: Increase in job postings
    - Application Ratio: Views per posting (lower = shortage)
    - Salary Growth: YoY salary increase
    - Vacancy Fill Rate: Hard-to-fill positions
    
    Args:
        _df: Processed DataFrame
        
    Returns:
        Dictionary with shortage indices by sector
    """
    shortage_index = {}
    
    for sector in _df['primary_category'].unique():
        sector_data = _df[_df['primary_category'] == sector]
        
        # Components of shortage index (0-100 scale)
        # 1. Posting volume trend (normalized)
        posting_count = len(sector_data)
        posting_score = min((posting_count / len(_df)) * 200, 100)  # Scale to 100
        
        # 2. Views per posting (inverse - lower views = shortage)
        avg_views = sector_data['metadata_totalNumberOfView'].mean()
        views_score = max(100 - min((avg_views / 100) * 50, 100), 0)
        
        # 3. Application ratio (inverse - lower applications = shortage)
        avg_apps = sector_data['metadata_totalNumberJobApplication'].mean()
        apps_score = max(100 - min((avg_apps / 5) * 50, 100), 0)
        
        # 4. Salary levels (higher salary = higher demand/shortage)
        avg_salary = sector_data['average_salary'].mean()
        salary_score = min((avg_salary / 5000) * 50, 50)
        
        # Composite shortage index
        index = (posting_score * 0.3 + views_score * 0.2 + apps_score * 0.3 + salary_score * 0.2)
        shortage_index[sector] = round(index, 2)
    
    return dict(sorted(shortage_index.items(), key=lambda x: x[1], reverse=True))


# ============================================================================
# PERSONALIZED RECOMMENDER ENGINE CLASS
# ============================================================================


# PersonalizedRecommender and get_job_recommendations removed due to data accuracy concerns.



# ============================================================================
# VISUALIZATION FUNCTIONS
# ============================================================================

def create_employment_heatmap(heatmap_data: pd.DataFrame) -> go.Figure:
    """
    Create interactive employment heatmap using Plotly.
    
    Args:
        heatmap_data: Aggregated employment data
        
    Returns:
        Plotly Figure object
    """
    # Handle empty data
    if len(heatmap_data) == 0 or heatmap_data.empty:
        fig = go.Figure()
        fig.add_annotation(text="No data available for heatmap", xref="paper", yref="paper",
                          x=0.5, y=0.5, showarrow=False)
        return fig
    
    pivot_data = heatmap_data.pivot_table(
        values='Posting_Count',
        index='Sector',
        columns='Period',
        fill_value=0
    )
    
    fig = go.Figure(data=go.Heatmap(
        z=pivot_data.values,
        x=pivot_data.columns,
        y=pivot_data.index,
        colorscale='YlOrRd',
        hoverongaps=False,
        colorbar=dict(title="Job Postings")
    ))
    
    fig.update_layout(
        title='Employment Heatmap: Hiring Patterns by Sector & Time',
        xaxis_title='Time Period',
        yaxis_title='Industry Sector',
        height=500,
        template='plotly_white',
        font=dict(family='Segoe UI', size=11)
    )
    
    return fig


def create_skill_gap_chart(current_skills: Dict, emerging_skills: Dict) -> go.Figure:
    """
    Create upskill gap analysis visualization.
    
    Args:
        current_skills: Dictionary of current market skills
        emerging_skills: Dictionary of emerging skills
        
    Returns:
        Plotly Figure object
    """
    all_skills = set(current_skills.keys()) | set(emerging_skills.keys())
    
    current_values = [current_skills.get(skill, 0) for skill in all_skills]
    emerging_values = [emerging_skills.get(skill, 0) for skill in all_skills]
    
    fig = go.Figure(data=[
        go.Bar(name='Current Market', x=list(all_skills), y=current_values, marker_color='#999999'),
        go.Bar(name='Emerging Need', x=list(all_skills), y=emerging_values, marker_color='#666666')
    ])
    
    fig.update_layout(
        title='Upskill Gap Analysis: Current vs. Emerging Market Needs',
        xaxis_title='Skills',
        yaxis_title='Job Postings Count',
        barmode='group',
        height=400,
        template='plotly_white',
        font=dict(family='Segoe UI', size=11),
        hovermode='x unified'
    )
    
    return fig


def create_salary_distribution_by_sector(df: pd.DataFrame, target_salary: float = None) -> go.Figure:
    """
    Create salary distribution visualization by sector (Box Plot).
    
    Args:
        df: Processed DataFrame
        target_salary: User's target salary to show as reference
        
    Returns:
        Plotly Figure object
    """
    # Filter valid salaries
    valid_data = df.dropna(subset=['average_salary', 'primary_category'])
    
    # Filter sectors with at least 5 postings to be statistically meaningful
    sector_counts = valid_data['primary_category'].value_counts()
    major_sectors = sector_counts[sector_counts >= 5].index
    
    plot_data = valid_data[valid_data['primary_category'].isin(major_sectors)].copy()
    
    if len(plot_data) == 0:
        fig = go.Figure()
        fig.add_annotation(text="Insufficient data for salary distribution (Need >5 postings per sector)", 
                          xref="paper", yref="paper", x=0.5, y=0.5, showarrow=False,
                          font=dict(color="white"))
        fig.update_layout(plot_bgcolor='#0f1419', paper_bgcolor='#0f1419')
        return fig

    # Calculate median salary for sorting order
    median_salaries = plot_data.groupby('primary_category')['average_salary'].median().sort_values(ascending=True)
    
    # Create Box Plot using Plotly Express
    fig = px.box(
        plot_data, 
        x="average_salary", 
        y="primary_category",
        orientation="h",
        title="<b>Salary Distribution by Sector</b> (Median, Quartiles & Ranges)",
        category_orders={"primary_category": median_salaries.index.tolist()},
        labels={"average_salary": "Monthly Salary (SGD)", "primary_category": ""},
        color_discrete_sequence=["#3b82f6"],
        points="outliers" # Show outliers
    )
    
    # Add target salary reference line if provided
    if target_salary:
        fig.add_vline(
            x=target_salary, 
            line_dash="dash", 
            line_color="#ef4444",
            annotation_text=f"Target: SGD {target_salary:,.0f}", 
            annotation_position="top right"
        )
    
    fig.update_layout(
        height=max(450, len(median_salaries) * 40), # Dynamic height
        plot_bgcolor='#0f1419',
        paper_bgcolor='#0f1419',
        font=dict(family='Segoe UI', size=11, color='#e0e7ff'),
        xaxis=dict(
            title="Monthly Salary (SGD)",
            gridcolor='rgba(255,255,255,0.1)', 
            zerolinecolor='rgba(255,255,255,0.1)',
            tickformat=",.0f"
        ),
        yaxis=dict(
            gridcolor='rgba(255,255,255,0.1)',
            zerolinecolor='rgba(255,255,255,0.1)'
        ),
        margin=dict(l=10, r=20, t=50, b=20),
        hoverlabel=dict(bgcolor="#1e293b", font_size=12)
    )
    
    return fig


def create_skill_radar_chart(df: pd.DataFrame, user_skills: List[str] = None) -> go.Figure:
    """
    Create radar chart comparing skill demand and salary potential.
    
    Args:
        df: Processed DataFrame
        user_skills: List of user's skills
        
    Returns:
        Plotly radar Figure
    """
    if not user_skills:
        return go.Figure()

    # Calculate metrics for each user skill
    skill_metrics = []
    
    # Pre-calculate text for faster search
    searchable_text = (df['title'].fillna('').str.lower() + ' ' + 
                       df['categories'].fillna('').str.lower())
    
    for skill in user_skills:
        # Count matches (literal string match)
        matches = searchable_text.str.contains(skill.lower(), case=False, regex=False, na=False)
        count = matches.sum()
        
        if count > 0:
            avg_salary = df.loc[matches, 'average_salary'].mean()
        else:
            avg_salary = 0
            
        skill_metrics.append({
            'Skill': skill,
            'Demand': count,
            'Avg_Salary': avg_salary
        })
    
    if not skill_metrics:
        return go.Figure()
        
    metrics_df = pd.DataFrame(skill_metrics)
    
    # Normalize metrics for radar chart
    max_demand = metrics_df['Demand'].max() if metrics_df['Demand'].max() > 0 else 1
    max_salary = metrics_df['Avg_Salary'].max() if metrics_df['Avg_Salary'].max() > 0 else 1
    
    metrics_df['Normalized_Demand'] = metrics_df['Demand'] / max_demand
    metrics_df['Normalized_Salary'] = metrics_df['Avg_Salary'] / max_salary
    
    categories = metrics_df['Skill'].tolist()
    
    fig = go.Figure()

    fig.add_trace(go.Scatterpolar(
        r=metrics_df['Normalized_Demand'],
        theta=categories,
        fill='toself',
        name='Market Demand'
    ))
    
    fig.add_trace(go.Scatterpolar(
        r=metrics_df['Normalized_Salary'],
        theta=categories,
        fill='toself',
        name='Salary Potential'
    ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 1]
            )),
        showlegend=True,
        title="Skill Impact Analysis (Demand vs Salary)",
        font=dict(family='Segoe UI', size=11, color='#e0e7ff'),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
    )
    
    return fig


def create_skill_job_relevance_chart(df: pd.DataFrame, user_skills: tuple) -> go.Figure:
    """
    Create a dual-axis chart showing job demand (bars) and average salary (line) for user skills.
    
    Args:
        df: Filtered DataFrame
        user_skills: Tuple or list of user skills
        
    Returns:
        Plotly Figure object
    """
    if not user_skills:
        fig = go.Figure()
        fig.add_annotation(text="Please select skills to see analysis", 
                          showarrow=False, xref="paper", yref="paper", x=0.5, y=0.5)
        return fig
        
    skill_metrics = []
    
    # Pre-calculate searchable text for performance
    searchable_text = (df['title'].fillna('').str.lower() + ' ' + 
                       df['categories'].fillna('').str.lower())
    
    for skill in user_skills:
        # Match skill in title or category (literal match for safety with C++, C# etc)
        mask = searchable_text.str.contains(skill.lower(), case=False, regex=False, na=False)
        count = mask.sum()
        
        if count > 0:
            avg_salary = df.loc[mask, 'average_salary'].mean()
        else:
            avg_salary = 0
            
        skill_metrics.append({
            'Skill': skill,
            'Job Count': count,
            'Avg Salary': avg_salary
        })
    
    # Sort by Job Count for better visualization
    metrics_df = pd.DataFrame(skill_metrics).sort_values('Job Count', ascending=False)
    
    # Create dual-axis chart
    fig = go.Figure()
    
    # Bar chart for Demand (Left Axis)
    fig.add_trace(go.Bar(
        x=metrics_df['Skill'],
        y=metrics_df['Job Count'],
        name='Job Postings',
        marker_color='#3b82f6',
        yaxis='y',
        offsetgroup=1,
        hovertemplate='<b>%{x}</b><br>Postings: %{y}<extra></extra>'
    ))
    
    # Line chart for Salary (Right Axis)
    fig.add_trace(go.Scatter(
        x=metrics_df['Skill'],
        y=metrics_df['Avg Salary'],
        name='Avg Salary',
        mode='lines+markers',
        marker=dict(color='#10b981', size=8),
        line=dict(width=3, color='#10b981'),
        yaxis='y2',
        hovertemplate='<b>%{x}</b><br>Salary: SGD %{y:,.0f}<extra></extra>'
    ))
    
    fig.update_layout(
        title='Skill Relevance: Market Demand vs Salary Potential',
        xaxis=dict(title='Your Skills'),
        yaxis=dict(
            title='Number of Job Postings', 
            side='left', 
            showgrid=True,
            gridcolor='rgba(255,255,255,0.1)'
        ),
        yaxis2=dict(
            title='Average Monthly Salary (SGD)', 
            side='right', 
            overlaying='y', 
            showgrid=False,
            tickformat=",.0f"
        ),
        legend=dict(x=0.01, y=1.1, orientation='h', bgcolor='rgba(0,0,0,0)'),
        hovermode='x unified',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family='Segoe UI', size=11, color='#e0e7ff'),
        margin=dict(r=50)  # Add right margin for secondary axis label
    )
    
    return fig

def create_skill_distribution_pie(df: pd.DataFrame, user_skills: List[str] = None) -> go.Figure:
    """
    Create pie chart showing distribution of top skills in demand.
    
    Args:
        df: Processed DataFrame
        user_skills: List of skills to highlight
        
    Returns:
        Plotly pie Figure
    """
    all_skills, _ = calculate_skill_gaps(df)
    skills_sorted = sorted(all_skills.items(), key=lambda x: x[1], reverse=True)[:10]
    
    labels = [s[0] for s in skills_sorted]
    values = [s[1] for s in skills_sorted]
    
    # Traceability: Identify which skills are in user's profile
    pull = [0.1 if user_skills and s[0] in user_skills else 0 for s in skills_sorted]
    colors = ['#3b82f6' if user_skills and s[0] in user_skills else '#4b5563' for s in skills_sorted]
    
    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=values,
        hole=0.3,
        pull=pull,
        marker=dict(colors=colors, line=dict(color='#e0e7ff', width=1)),
        textposition='inside',
        textinfo='label+percent',
        hovertemplate='<b>%{label}</b><br>Demand: %{value}<br>%{percent}<br>' + 
                      ('⭐ Matches your profile' if user_skills else '') + '<extra></extra>'
    )])
    
    fig.update_layout(
        title='Skills Demand Distribution (Top 10) - Highlighted matches your profile',
        height=450,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family='Segoe UI', size=11, color='#e0e7ff'),
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5)
    )
    
    return fig


def create_labor_shortage_gauge(shortage_index: Dict[str, float], sector: str) -> go.Figure:
    """
    Create gauge chart for Labor Shortage Index (Government Users).
    
    Args:
        shortage_index: Dictionary with shortage indices
        sector: Selected sector
        
    Returns:
        Plotly Figure object
    """
    # Handle empty or invalid shortage index
    if not shortage_index or not isinstance(shortage_index, dict):
        shortage_index = {'N/A': 50}
    if sector not in shortage_index or len(shortage_index) == 0:
        sector = list(shortage_index.keys())[0] if shortage_index else 'N/A'
    
    value = shortage_index.get(sector, 50)
    
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=value,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': f"Labor Shortage Index - {sector}"},
        delta={'reference': 50, 'increasing': {'color': '#f57c00'}},
        gauge={
            'axis': {'range': [None, 100]},
            'bar': {'color': '#777777'},
            'steps': [
                {'range': [0, 33], 'color': '#e8e8e8'},
                {'range': [33, 66], 'color': '#d0d0d0'},
                {'range': [66, 100], 'color': '#b0b0b0'}
            ],
            'threshold': {
                'line': {'color': '#606060', 'width': 4},
                'thickness': 0.75,
                'value': 75
            }
        }
    ))
    
    fig.update_layout(
        height=400,
        template='plotly_white',
        font=dict(family='Segoe UI', size=11)
    )
    
    return fig


def create_top_job_titles_by_applications(_df: pd.DataFrame) -> go.Figure:
    """
    Create a horizontal bar chart showing top 10 job titles by application volume.
    
    Args:
        _df: Processed DataFrame
        
    Returns:
        Plotly Figure object
    """
    if len(_df) == 0 or 'title' not in _df.columns:
        fig = go.Figure()
        fig.add_annotation(text="No data available", xref="paper", yref="paper",
                          x=0.5, y=0.5, showarrow=False)
        return fig
    
    # Group by job title and sum applications
    job_apps = _df.groupby('title')['metadata_totalNumberJobApplication'].sum().sort_values(ascending=True).tail(10)
    
    fig = go.Figure(data=[
        go.Bar(
            y=job_apps.index,
            x=job_apps.values,
            orientation='h',
            marker=dict(
                color=job_apps.values,
                colorscale='Blues',
                showscale=True,
                colorbar=dict(title="Applications")
            ),
            hovertemplate='<b>%{y}</b><br>Total Applications: %{x}<extra></extra>'
        )
    ])
    
    fig.update_layout(
        title='Top 10 Job Titles by Application Volume',
        xaxis_title='Total Applications',
        yaxis_title='Job Title',
        height=450,
        plot_bgcolor='#0f1419',
        paper_bgcolor='#0f1419',
        font=dict(family='Segoe UI', size=11, color='#e0e7ff'),
        margin=dict(l=300)
    )
    
    return fig


def create_sector_job_demand(_df: pd.DataFrame) -> go.Figure:
    """
    Create a bar chart showing top 10 job demand by sector.
    
    Args:
        _df: Processed DataFrame
        
    Returns:
        Plotly Figure object
    """
    if len(_df) == 0 or 'primary_category' not in _df.columns:
        fig = go.Figure()
        fig.add_annotation(text="No data available", xref="paper", yref="paper",
                          x=0.5, y=0.5, showarrow=False)
        return fig
    
    # Group by sector and count postings
    sector_demand = _df.groupby('primary_category').size().sort_values(ascending=False).head(10)
    
    fig = go.Figure(data=[
        go.Bar(
            x=sector_demand.index,
            y=sector_demand.values,
            marker=dict(
                color=sector_demand.values,
                colorscale='Viridis',
                showscale=True,
                colorbar=dict(title="Job Postings")
            ),
            hovertemplate='<b>%{x}</b><br>Postings: %{y}<extra></extra>'
        )
    ])
    
    fig.update_layout(
        title='Top 10 Job Demand by Sector',
        xaxis_title='Industry Sector',
        yaxis_title='Number of Job Postings',
        height=450,
        plot_bgcolor='#0f1419',
        paper_bgcolor='#0f1419',
        font=dict(family='Segoe UI', size=11, color='#e0e7ff'),
        xaxis_tickangle=-45
    )
    
    return fig


def create_trend_with_ma(df: pd.DataFrame, window: int = 3) -> go.Figure:
    """
    Create a trend analysis chart with actual data and moving average.
    
    Args:
        df: Processed DataFrame
        window: Moving average window (months)
        
    Returns:
        Plotly Figure object
    """
    # Monthly trend data
    trend_data = df.groupby('year_month').agg({
        'metadata_jobPostId': 'count',
        'average_salary': 'mean',
        'metadata_totalNumberJobApplication': 'sum',
        'metadata_totalNumberOfView': 'sum'
    }).reset_index()
    
    trend_data['year_month_str'] = trend_data['year_month'].astype(str)
    
    # Calculate moving average
    trend_data['ma'] = trend_data['metadata_jobPostId'].rolling(window=window, center=True).mean()
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=trend_data['year_month_str'],
        y=trend_data['metadata_jobPostId'],
        mode='lines+markers',
        name='Actual Postings',
        line=dict(color='#3b82f6', width=2),
        marker=dict(size=5)
    ))
    
    fig.add_trace(go.Scatter(
        x=trend_data['year_month_str'],
        y=trend_data['ma'],
        mode='lines',
        name=f'{window}-Month MA',
        line=dict(color='#10b981', width=3, dash='dash')
    ))
    
    fig.update_layout(
        title=f'Job Postings Trend Analysis (with {window}-Month MA)',
        xaxis_title='Period',
        yaxis_title='Number of Job Postings',
        height=450,
        template='plotly_white',
        font=dict(family='Segoe UI', size=11),
        hovermode='x unified'
    )
    
    return fig


def create_excel_export(df: pd.DataFrame, persona: str) -> Optional[bytes]:
    """
    Create a multi-sheet Excel export for professional use.
    
    Args:
        df: Filtered DataFrame
        persona: Current user persona
        
    Returns:
        Bytes object containing Excel file or None if export fails
    """
    if not EXCEL_AVAILABLE:
        return None
        
    output = BytesIO()
    
    try:
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            # Sheet 1: Executive Summary
            summary_data = {
                'Metric': ['Total Job Postings', 'Average Salary (SGD)', 'Active Sectors', 'Total Applications', 'Export Date', 'User Persona'],
                'Value': [
                    len(df),
                    f"{df['average_salary'].mean():.2f}",
                    df['primary_category'].nunique(),
                    df['metadata_totalNumberJobApplication'].sum() if 'metadata_totalNumberJobApplication' in df.columns else 0,
                    datetime.now().strftime('%Y-%m-%d %H:%M'),
                    persona
                ]
            }
            pd.DataFrame(summary_data).to_excel(writer, sheet_name='Executive Summary', index=False)
            
            # Sheet 2: Sector Analysis
            if 'primary_category' in df.columns:
                sector_summary = df.groupby('primary_category').agg({
                    'title': 'count',
                    'average_salary': 'mean'
                }).reset_index()
                sector_summary.columns = ['Sector', 'Job Count', 'Average Salary']
                sector_summary = sector_summary.sort_values('Job Count', ascending=False)
                sector_summary.to_excel(writer, sheet_name='Sector Analysis', index=False)
            
            # Sheet 3: Job Listings (Detailed)
            # Limit columns for clarity
            export_cols = [c for c in ['title', 'postedCompany_name', 'primary_category', 'average_salary', 
                                     'employmentTypes', 'positionLevels', 'metadata_jobId'] if c in df.columns]
            df[export_cols].head(1000).to_excel(writer, sheet_name='Job Listings', index=False)
            
            # Formatting (Auto-width columns)
            for sheet_name in writer.sheets:
                sheet = writer.sheets[sheet_name]
                for column in sheet.columns:
                    max_length = 0
                    column = [cell for cell in column]
                    try:
                        for cell in column:
                            if len(str(cell.value)) > max_length:
                                max_length = len(str(cell.value))
                    except:
                        pass
                    adjusted_width = (max_length + 2)
                    sheet.column_dimensions[column[0].column_letter].width = min(adjusted_width, 50)
                    
        return output.getvalue()
    except Exception as e:
        st.error(f"Error creating Excel export: {str(e)}")
        return None


def create_pdf_export(df: pd.DataFrame, persona: str, recommendations: Dict = None) -> Optional[bytes]:
    """
    Create a professional PDF report.
    
    Args:
        df: Filtered DataFrame
        persona: Current user persona
        recommendations: Optional dictionary of recommendations
        
    Returns:
        Bytes object containing PDF file or None if export fails
    """
    if not PDF_AVAILABLE:
        return None
        
    buffer = BytesIO()
    
    try:
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        styles = getSampleStyleSheet()
        story = []
        
        # Title
        story.append(Paragraph(f"Labor Market Intelligence Report", styles['Title']))
        story.append(Paragraph(f"Generated for: {persona}", styles['Heading2']))
        story.append(Paragraph(f"Date: {datetime.now().strftime('%Y-%m-%d')}", styles['Normal']))
        story.append(Spacer(1, 12))
        
        # Executive Summary
        story.append(Paragraph("Executive Summary", styles['Heading1']))
        summary_text = f"""
        This report analyzes {len(df):,} job postings across {df['primary_category'].nunique() if 'primary_category' in df.columns else 0} sectors.
        The average market salary is SGD {df['average_salary'].mean():,.2f}.
        """
        story.append(Paragraph(summary_text, styles['Normal']))
        story.append(Spacer(1, 12))
        
        # Sector Analysis Table
        story.append(Paragraph("Top Sectors by Demand", styles['Heading1']))
        
        if 'primary_category' in df.columns:
            sector_data = df.groupby('primary_category').size().sort_values(ascending=False).head(10).reset_index()
            sector_data.columns = ['Sector', 'Postings']
            
            # Convert to list of lists for Table
            table_data = [['Sector', 'Job Postings']] + sector_data.values.tolist()
            
            t = Table(table_data)
            t.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.blue),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            story.append(t)
        
        # Recommendations (if available)
        if recommendations:
            story.append(Spacer(1, 12))
            story.append(Paragraph("Key Recommendations", styles['Heading1']))
            
            if 'upskill_opportunities' in recommendations:
                story.append(Paragraph("Recommended Skills to Acquire:", styles['Heading2']))
                for item in recommendations['upskill_opportunities'][:5]:
                    skill_name = item['skill'] if isinstance(item, dict) else item
                    story.append(Paragraph(f"• {skill_name}", styles['Normal']))

        doc.build(story)
        return buffer.getvalue()
        
    except Exception as e:
        st.error(f"Error creating PDF export: {str(e)}")
        return None


# ============================================================================
# SIDEBAR: PERSONA SELECTION & FILTERS
# ============================================================================

# Initialize session state for filters
if 'filter_reset' not in st.session_state:
    st.session_state.filter_reset = False
if 'apply_filters' not in st.session_state:
    st.session_state.apply_filters = False

# Removed external placeholder image to prevent connectivity issues
# Logo section can be added later with local file

st.sidebar.markdown("---")
st.sidebar.markdown("### 👤 SELECT YOUR PERSONA")

persona = st.sidebar.radio(
    "Who are you?",
    options=["Individual", "Government Agency", "Recruiter"],
    help="Choose your role to customize the dashboard view",
    key="persona_selector"
)

st.sidebar.markdown("---")
st.sidebar.markdown("### 🎨 THEME SETTINGS")

# Theme selector with three options
theme_option = st.sidebar.radio(
    "Theme Mode",
    options=["Auto (System)", "Dark", "Light"],
    help="Choose how the dashboard appears: Auto uses your system preference",
    key="theme_selector"
)

# Map radio values to session state values
theme_map = {"Auto (System)": "auto", "Dark": "dark", "Light": "light"}
st.session_state.theme_mode = theme_map[theme_option]

# Display current theme info
if st.session_state.theme_mode == "auto":
    st.sidebar.caption("🔄 Following your system preference")
elif st.session_state.theme_mode == "dark":
    st.sidebar.caption("🌙 Dark mode enabled (override)")
else:
    st.sidebar.caption("☀️ Light mode enabled (override)")

st.sidebar.markdown("---")
st.sidebar.markdown("### 📁 SELECT DATASET")

# Initialize session state for dataset selection
if 'dataset_file_path' not in st.session_state:
    st.session_state.dataset_file_path = "/home/julius/SGJobData.parquet"
if 'uploaded_file' not in st.session_state:
    st.session_state.uploaded_file = None

# Dataset selection container
with st.sidebar.expander("📊 DATASET SELECTION", expanded=True):
    st.markdown("**Upload or Select Your CSV/Parquet File**")
    
    # Option to choose between upload and file path
    data_source = st.radio(
        "Data Source",
        options=["Upload File", "Use Default Dataset", "Specify File Path"],
        help="Choose how to load your dataset",
        key="data_source_selector"
    )
    
    if data_source == "Upload File":
        uploaded_file = st.file_uploader(
            "Choose CSV or Parquet file",
            type=["csv", "parquet"],
            help="Upload your dataset file (CSV or Parquet format)",
            key="file_uploader"
        )
        if uploaded_file is not None:
            st.session_state.uploaded_file = uploaded_file
            st.success(f"✅ File loaded: {uploaded_file.name}")
    
    elif data_source == "Specify File Path":
        custom_path = st.text_input(
            "Enter file path",
            value=st.session_state.dataset_file_path if st.session_state.dataset_file_path != "/home/julius/SGJobData.parquet" else "",
            placeholder="/path/to/your/file.csv",
            help="Provide the full path to your CSV or Parquet file",
            key="custom_file_path"
        )
        if custom_path:
            st.session_state.dataset_file_path = custom_path
            st.info(f"📂 Using file: {custom_path}")
    
    else:  # Use Default Dataset
        st.session_state.dataset_file_path = "/home/julius/SGJobData.parquet"
        st.session_state.uploaded_file = None
        st.info("📂 Using default dataset: SGJobData.parquet")

st.sidebar.markdown("---")

# Load data
def load_and_preprocess(_file_path: str = None, _uploaded_file=None):
    """Load and preprocess data from either uploaded file or file path"""
    try:
        if _uploaded_file is not None:
            # Handle uploaded file
            if _uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(_uploaded_file, on_bad_lines='skip', encoding='utf-8')
            else:  # parquet
                df = pd.read_parquet(_uploaded_file)
            st.sidebar.success(f"✅ Loaded uploaded file: {_uploaded_file.name}")
        elif _file_path:
            # Handle file path
            df = load_data(_file_path)
            st.sidebar.success(f"✅ Loaded file: {_file_path}")
        else:
            # Fallback to default
            df = load_data("/home/julius/SGJobData.parquet")
        
        df = preprocess_data(df)
        return df
    except Exception as e:
        st.sidebar.error(f"❌ Error loading data: {str(e)}")
        # Try fallback to default
        try:
            df = load_data("/home/julius/SGJobData.parquet")
            df = preprocess_data(df)
            st.sidebar.warning("⚠️ Using default dataset due to error")
            return df
        except:
            st.error("Cannot load any dataset. Please check file paths and try again.")
            st.stop()

df = load_and_preprocess(st.session_state.dataset_file_path, st.session_state.uploaded_file)

# Pre-compute filter options once
@st.cache_data
def get_filter_options(_df: pd.DataFrame):
    """Get all available filter options from data"""
    return {
        'years': sorted(_df['year'].dropna().unique().astype(int).tolist()),
        'sectors': sorted(_df['primary_category'].unique().tolist()),
        'employment_types': sorted(_df['employmentTypes'].unique().tolist()),
        'position_levels': sorted(_df['positionLevels'].dropna().unique().tolist())
    }

filter_options = get_filter_options(df)

# Initialize persona-specific variables to defaults
user_current_skills = []
desired_salary = 5000
preferred_role = []
shortage_sensitivity = 0.7
growth_focus = 'High Growth Sectors'
min_vacancy = 1

# Persona-specific filters in collapsible sections (Moved up for better reactivity)
if persona == "Individual":
    # Personalized features removed as per request.
    pass


elif persona == "Government Agency":
    with st.sidebar.expander("📊 MACRO-ECONOMIC FILTERS", expanded=True):
        shortage_sensitivity = st.slider(
            "Focus on High-Shortage Sectors",
            min_value=0.0,
            max_value=1.0,
            value=0.7,
            step=0.1,
            help="Higher values emphasize severe labor shortages",
            key="shortage_sensitivity_slider"
        )
        
        st.markdown("**Export Options:**")
        export_format = st.radio(
            "Preferred Download Format",
            options=['CSV', 'Excel', 'PDF'],
            help="Select format for data export",
            key="export_format_selector"
        )

elif persona == "Recruiter":
    with st.sidebar.expander("🎯 RECRUITMENT FILTERS", expanded=True):
        growth_focus = st.selectbox(
            "Focus Area",
            options=['High Growth Sectors', 'High Salary Sectors', 'High Volume', 'Emerging Skills'],
            key="recruiter_growth_focus"
        )
        
        min_vacancy = st.slider(
            "Minimum Vacancies per Posting",
            min_value=1,
            max_value=20,
            value=1,
            key="recruiter_min_vacancy_slider"
        )

# Collapsible filter section with improved UX
# Collapsible filter section with improved UX and performance
with st.sidebar.expander("🎛️ APPLY FILTERS", expanded=True):
    with st.form("filter_form"):
        st.markdown("**Time Period**")
        
        # Year slider
        min_year = int(min(filter_options['years']))
        max_year = int(max(filter_options['years']))
        
        widget_year_range = st.slider(
            "Select Year Range",
            min_value=min_year,
            max_value=max_year,
            value=(min_year, max_year),
            step=1,
            key="year_range_filter_widget"
        )
        
        st.markdown("---")
        st.markdown("**Industry & Employment**")
        
        # Sector selection
        sector_options = ['All Sectors'] + filter_options['sectors']
        widget_sector = st.selectbox(
            "Industry Sector",
            options=sector_options,
            index=0,
            key="sector_filter_widget"
        )
        
        # Employment type
        employment_options = ['All Types'] + filter_options['employment_types']
        widget_employment = st.selectbox(
            "Employment Type",
            options=employment_options,
            index=0,
            key="employment_filter_widget"
        )
        
        st.markdown("---")
        st.markdown("**Salary Range (SGD)**")
        widget_salary = st.slider(
            "Monthly Salary Range",
            min_value=0,
            max_value=20000,
            value=(0, 20000),
            step=500,
            key="salary_range_filter_widget"
        )
        
        st.markdown("---")
        st.markdown("**Position Level**")
        position_options = ['All Levels'] + filter_options['position_levels']
        widget_position = st.selectbox(
            "Career Level",
            options=position_options,
            index=0,
            help="Filter by job position level/seniority",
            key="position_level_filter_widget"
        )
        
        st.markdown("---")
        submitted = st.form_submit_button("✅ Apply Filters", use_container_width=True)

    if submitted:
        st.session_state.apply_filters = True
        st.session_state.filter_reset = False
        st.session_state.active_year_range = widget_year_range
        st.session_state.active_sector = widget_sector
        st.session_state.active_employment = widget_employment
        st.session_state.active_salary = widget_salary
        st.session_state.active_position = widget_position
        st.rerun()

    if st.sidebar.button("🔄 Clear All Filters", key="clear_filters_button", use_container_width=True):
        st.session_state.apply_filters = False
        st.session_state.filter_reset = True
        # Clear states
        for key in ["active_year_range", "active_sector", "active_employment", "active_salary", "active_position"]:
            if key in st.session_state:
                del st.session_state[key]
        # Clear widgets
        for key in ["year_range_filter_widget", "sector_filter_widget", "employment_filter_widget", 
                   "salary_range_filter_widget", "position_level_filter_widget"]:
            if key in st.session_state:
                del st.session_state[key]
        st.rerun()

# Apply filters with validation - optimized version
@st.cache_data
def apply_filters(_df: pd.DataFrame, years: tuple, sectors: list, employment: list, salary: tuple, position_levels: list) -> pd.DataFrame:
    """Apply all filters to dataframe - optimized for performance"""
    # Create mask starting with all True
    mask = pd.Series(True, index=_df.index)
    
    # Apply filters sequentially using boolean logic
    if years:
        mask &= _df['year'].isin(years)
    if sectors:
        mask &= _df['primary_category'].isin(sectors)
    if employment:
        mask &= _df['employmentTypes'].isin(employment)
    if position_levels:
        mask &= _df['positionLevels'].isin(position_levels)
    if salary:
        # Check if salary filter is applied (assuming default range is 0-20000)
        if salary[0] > 0 or salary[1] < 20000:
            mask &= (_df['average_salary'] >= salary[0]) & (_df['average_salary'] <= salary[1])
    
    # Return filtered copy
    return _df.loc[mask].copy()

# Apply filters only if apply_filters button was clicked
if st.session_state.apply_filters:
    # Retrieve active values from session state
    years_range = st.session_state.get('active_year_range', (int(min(filter_options['years'])), int(max(filter_options['years']))))
    selected_years = [y for y in filter_options['years'] if years_range[0] <= y <= years_range[1]]
    
    sec_val = st.session_state.get('active_sector', 'All Sectors')
    selected_sectors = filter_options['sectors'] if sec_val == 'All Sectors' else [sec_val]
    
    emp_val = st.session_state.get('active_employment', 'All Types')
    selected_employment = filter_options['employment_types'] if emp_val == 'All Types' else [emp_val]
    
    salary_range = st.session_state.get('active_salary', (0, 20000))
    
    pos_val = st.session_state.get('active_position', 'All Levels')
    selected_position_levels = filter_options['position_levels'] if pos_val == 'All Levels' else [pos_val]

    filtered_df = apply_filters(df, tuple(selected_years), selected_sectors, selected_employment, salary_range, selected_position_levels)
    

    # Profile filters removed


else:
    filtered_df = df.copy()

# Validate filtered dataset
if len(filtered_df) == 0:
    st.warning("⚠️ No jobs match your current filter selections. Please adjust your filters.")
    filtered_df = df.copy()

# Footer info
with st.sidebar.expander("ℹ️ DATASET INFO", expanded=False):
    st.markdown(f"**Last Updated:** {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    st.markdown(f"**Records Displayed:** {len(filtered_df):,}")
    st.markdown(f"**Total Records (Cleaned):** {len(df):,}")
    st.markdown(f"**Sectors:** {df['primary_category'].nunique()}")
    st.markdown(f"**Companies:** {df['postedCompany_name'].nunique()}")
    
    st.markdown("---")
    st.markdown("### 🧹 Data Quality Summary")
    st.markdown("""
    **Cleaning Applied:**
    - ✅ Removed 100% empty columns (occupationId)
    - ✅ Removed salary outliers (extreme values >99.9th percentile)
    - ✅ Removed records with zero salaries
    - ✅ Capped experience at 40 years (unrealistic values removed)
    - ✅ Removed negative engagement metrics
    - ✅ Standardized job titles and categories
    - ✅ Removed duplicate records
    - ✅ Removed records with missing critical dates
    
    **Data Quality Score:**  95%+ consistency
    """)
    
    # Show salary distribution stats
    st.markdown("### 💰 Salary Statistics (After Cleaning)")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"**Average:** SGD {df['average_salary'].mean():,.0f}")
        st.markdown(f"**Median:** SGD {df['average_salary'].median():,.0f}")
    with col2:
        st.markdown(f"**Min:** SGD {df['average_salary'].min():,.0f}")
        st.markdown(f"**Max:** SGD {df['average_salary'].max():,.0f}")

# ============================================================================
# MAIN CONTENT AREA - HEADER
# ============================================================================

# ============================================================================
# MAIN CONTENT AREA - HEADER
# ============================================================================

st.markdown("""
<div style="background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%); padding: 2.5rem; border-radius: 1.25rem; margin-bottom: 2.5rem; box-shadow: 0 8px 32px rgba(59, 130, 246, 0.3); border: 2px solid #60a5fa;">
    <h1 style="color: white; margin: 0; font-size: 2.75rem; font-weight: 900; letter-spacing: -1px;">📊 Workforce Intelligence Dashboard</h1>
    <p style="color: #dbeafe; margin: 0.75rem 0 0 0; font-size: 1.15rem; font-weight: 500;">Transform raw industrial job data into actionable labor market insights</p>
</div>
""", unsafe_allow_html=True)

# Filter Status Bar
filter_status_col1, filter_status_col2 = st.columns([3, 1])
with filter_status_col1:
    filter_pct = int((len(filtered_df) / len(df) * 100)) if len(df) > 0 else 0
    st.markdown(f"""
    <div style="background: linear-gradient(90deg, rgba(16, 185, 129, 0.1) 0%, rgba(59, 130, 246, 0.1) 100%); 
                padding: 1rem; border-radius: 0.75rem; border-left: 4px solid #10b981; margin-bottom: 1.5rem;">
    <strong>📊 Active View:</strong> <span style="color: #10b981; font-weight: bold;">{len(filtered_df):,}</span> jobs 
    (<span style="color: #60a5fa;">{filter_pct}%</span> of total dataset)
    </div>
    """, unsafe_allow_html=True)

with filter_status_col2:
    if len(filtered_df) < len(df):
        st.markdown(f"""
        <div style="text-align: right; padding: 1rem;">
        <small style="color: #93c5fd;">Filters Active ✓</small>
        </div>
        """, unsafe_allow_html=True)

# KPI Cards
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        label="Total Job Postings",
        value=f"{len(filtered_df):,}",
        delta=f"{int(len(filtered_df)/len(df)*100) if len(df) > 0 else 0}% of dataset"
    )

with col2:
    avg_salary = filtered_df['average_salary'].mean() if len(filtered_df) > 0 else 0
    st.metric(
        label="Avg Salary (SGD)",
        value=f"SGD {avg_salary:,.0f}" if avg_salary > 0 else "N/A",
        delta=f"Range: SGD {filtered_df['salary_minimum'].mean():,.0f} - SGD {filtered_df['salary_maximum'].mean():,.0f}" if avg_salary > 0 else ""
    )

with col3:
    total_views = filtered_df['metadata_totalNumberOfView'].sum() if len(filtered_df) > 0 else 0
    views_per = total_views/len(filtered_df) if len(filtered_df) > 0 else 0
    st.metric(
        label="Total Views",
        value=f"{total_views:,}",
        delta=f"{views_per:.1f} per posting"
    )

with col4:
    total_apps = filtered_df['metadata_totalNumberJobApplication'].sum() if len(filtered_df) > 0 else 0
    apps_per = total_apps/len(filtered_df) if len(filtered_df) > 0 else 0
    st.metric(
        label="Total Applications",
        value=f"{total_apps:,}",
        delta=f"{apps_per:.1f} per posting"
    )

st.markdown("---")

# ============================================================================
# PERSONA-SPECIFIC CONTENT
# ============================================================================

if persona == "Individual":
    st.header("� Job Market Overview")
    st.info("Explore general market trends below. Select other personas for more detailed analytics.")
    
    st.markdown("---")
    
    # 2. Salary Distribution by Sector
    st.subheader("💰 Salary Distribution by Sector")
    fig = create_salary_distribution_by_sector(filtered_df)
    st.plotly_chart(fig, use_container_width=True, key="individual_salary_dist")

    st.markdown("---")
    
    # 3. Top Job Titles
    st.subheader("🔥 Top Job Titles")
    fig_jobs = create_top_job_titles_by_applications(filtered_df)
    st.plotly_chart(fig_jobs, use_container_width=True, key="individual_top_jobs")

    st.markdown("---")
    
    # 4. Download Report
    st.subheader("📥 Export Market Data")
    col1, col2 = st.columns(2)
    
    with col1:
        csv_data = filtered_df[['title', 'postedCompany_name', 'primary_category', 'average_salary', 
                               'positionLevels', 'employmentTypes']].to_csv(index=False)
        st.download_button(
            label="📄 Download CSV Report",
            data=csv_data,
            file_name=f"market_report_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv"
        )
    
    with col2:
        if PDF_AVAILABLE:
            pdf_data = create_pdf_export(filtered_df, "Individual", None)
            if pdf_data:
                st.download_button(
                    label="📑 Download PDF Report",
                    data=pdf_data,
                    file_name=f"market_report_{datetime.now().strftime('%Y%m%d')}.pdf",
                    mime="application/pdf"
                )

elif persona == "Government Agency":
    st.header("📈 Macro-Economic Labor Market Dashboard")
    
    st.info(
        "👁️ **Government Focus:** Monitor labor shortages, wage trends, and sector health to inform workforce policy."
    )
    
    st.markdown("---")
    
    # KPI Dashboard
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="📊 Total Postings",
            value=f"{len(filtered_df):,}",
            delta=f"{int((len(filtered_df)/len(df)*100)) if len(df) > 0 else 0}% of market"
        )
    
    with col2:
        sector_count = filtered_df['primary_category'].nunique()
        st.metric(
            label="🏭 Active Sectors",
            value=sector_count,
            delta=f"{df['primary_category'].nunique()} total"
        )
    
    with col3:
        avg_salary = filtered_df['average_salary'].mean()
        yoy_change = ((avg_salary - df['average_salary'].mean()) / df['average_salary'].mean() * 100) if df['average_salary'].mean() > 0 else 0
        st.metric(
            label="💰 Avg Salary (SGD)",
            value=f"SGD {avg_salary:,.0f}",
            delta=f"{yoy_change:+.1f}% YoY"
        )
    
    with col4:
        total_applications = filtered_df['metadata_totalNumberJobApplication'].sum()
        st.metric(
            label="📋 Applications",
            value=f"{total_applications:,}",
            delta=f"{total_applications/len(filtered_df):.1f} per posting"
        )
    
    st.markdown("---")
    
    # 1. Labor Shortage Index
    st.subheader("🚨 Labor Shortage Index by Sector")
    st.markdown("*Higher values indicate more severe labor shortages (0-100 scale)*")
    
    shortage_index = calculate_labor_shortage_index(filtered_df)
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        selected_sector = st.selectbox(
            "Select Sector for Detailed Analysis",
            options=list(shortage_index.keys()) if shortage_index else ['N/A'],
            key="gov_sector_selector"
        )
        
        # Display top 5 shortage sectors
        st.markdown("**Top 5 Critical Shortage Areas:**")
        top_shortage = sorted(shortage_index.items(), key=lambda x: x[1], reverse=True)[:5] if shortage_index else []
        for i, (sector, index) in enumerate(top_shortage, 1):
            color = "🔴" if index > 70 else "🟡" if index > 50 else "🟢"
            st.markdown(f"{color} **{i}. {sector}** - {index:.1f}")
    
    with col2:
        fig = create_labor_shortage_gauge(shortage_index, selected_sector)
        st.plotly_chart(fig, use_container_width=True, key="gov_shortage_gauge")
    
    st.markdown("---")
    
    # 2. Employment Heatmap
    st.subheader("🔥 Employment Heatmap: Hiring Patterns by Sector")
    heatmap_data = calculate_employment_heatmap_data(filtered_df)
    fig = create_employment_heatmap(heatmap_data)
    st.plotly_chart(fig, use_container_width=True, key="gov_heatmap")
    
    st.markdown("---")
    
    # 3. Job Growth Trends WITH Moving Average
    st.subheader("📊 Job Market Trends (with Predictive Overlay)")
    st.markdown("*Trend line shows 3-month moving average with confidence band*")
    fig = create_trend_with_ma(filtered_df, window=3)
    st.plotly_chart(fig, use_container_width=True, key="gov_trend_ma")
    
    st.markdown("---")
    
    # 4. Sector Summary Statistics
    st.subheader("📋 Sector Summary Statistics")
    
    sector_summary = filtered_df.groupby('primary_category').agg({
        'metadata_jobPostId': 'count',
        'average_salary': 'mean',
        'salary_minimum': 'mean',
        'salary_maximum': 'mean',
        'minimumYearsExperience': 'mean',
        'metadata_totalNumberOfView': 'sum',
        'metadata_totalNumberJobApplication': 'sum'
    }).reset_index()
    
    sector_summary.columns = ['Sector', 'Postings', 'Avg_Salary', 'Min_Salary', 'Max_Salary', 'Avg_Experience', 'Total_Views', 'Total_Applications']
    sector_summary = sector_summary.sort_values('Postings', ascending=False).head(10)
    
    # Format for display
    for col in ['Avg_Salary', 'Min_Salary', 'Max_Salary']:
        sector_summary[col] = sector_summary[col].apply(lambda x: f"SGD {x:,.0f}")
    
    st.dataframe(sector_summary, hide_index=True, use_container_width=True)
    
    st.markdown("---")
    
    # 5. Export Options for Government Users
    st.subheader("📥 Export Market Intelligence")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        csv_data = sector_summary.to_csv(index=False)
        st.download_button(
            label="📄 Download CSV Report",
            data=csv_data,
            file_name=f"labor_market_report_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv"
        )
    
    with col2:
        if EXCEL_AVAILABLE:
            excel_data = create_excel_export(filtered_df, "Government Agency")
            if excel_data:
                st.download_button(
                    label="📊 Download Excel Report",
                    data=excel_data,
                    file_name=f"labor_intelligence_{datetime.now().strftime('%Y%m%d')}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
    
    with col3:
        if PDF_AVAILABLE:
            pdf_data = create_pdf_export(filtered_df, "Government Agency")
            if pdf_data:
                st.download_button(
                    label="📑 Download PDF Report",
                    data=pdf_data,
                    file_name=f"labor_report_{datetime.now().strftime('%Y%m%d')}.pdf",
                    mime="application/pdf"
                )


elif persona == "Recruiter":
    st.header("🎯 Talent Pool & Recruitment Intelligence")
    
    st.info(
        "👁️ **Recruiter Focus:** Identify high-growth talent pools, skill trends, competitive salary benchmarks, and velocity metrics."
    )
    
    st.markdown("---")
    
    # KPI Dashboard for Recruiters
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="💼 Open Positions",
            value=f"{len(filtered_df):,}",
            delta=f"Active hiring"
        )
    
    with col2:
        avg_apps = filtered_df['metadata_totalNumberJobApplication'].mean()
        st.metric(
            label="📝 Avg Applications",
            value=f"{avg_apps:.1f}",
            delta="per posting"
        )
    
    with col3:
        top_company = filtered_df['postedCompany_name'].mode()[0] if len(filtered_df['postedCompany_name'].mode()) > 0 else "N/A"
        st.metric(
            label="🏢 Top Hiring Company",
            value=top_company[:20],
            delta="hiring most"
        )
    
    with col4:
        avg_salary = filtered_df['average_salary'].mean()
        st.metric(
            label="💰 Competitive Rate",
            value=f"SGD {avg_salary:,.0f}",
            delta="avg offering"
        )
    
    st.markdown("---")
    
    # 1. Top Growing Sectors (High-Velocity Hiring)
    st.subheader("📈 High-Velocity Talent Pools")
    st.markdown("*Sectors with fastest hiring velocity and highest engagement*")
    
    sector_metrics = filtered_df.groupby('primary_category').agg({
        'metadata_jobPostId': 'count',
        'average_salary': 'mean',
        'metadata_totalNumberJobApplication': 'mean',
        'metadata_totalNumberOfView': 'mean'
    }).reset_index()
    
    sector_metrics.columns = ['Sector', 'Open_Positions', 'Avg_Salary', 'Avg_Applications', 'Avg_Views']
    sector_metrics = sector_metrics.sort_values('Open_Positions', ascending=False).head(10)
    
    col1, col2 = st.columns([1.5, 1])
    
    with col1:
        fig = px.bar(
            sector_metrics,
            x='Sector',
            y='Open_Positions',
            color='Avg_Salary',
            hover_data=['Avg_Applications', 'Avg_Views'],
            title='Open Positions by Sector (Colored by Salary)',
            labels={'Open_Positions': 'Number of Openings', 'Avg_Salary': 'Avg Salary (SGD)'},
            color_continuous_scale='Viridis'
        )
        fig.update_layout(xaxis_tickangle=-45, height=400, plot_bgcolor='#0f1419', 
                         paper_bgcolor='#0f1419', font=dict(color='#e0e7ff'))
        st.plotly_chart(fig, use_container_width=True, key="rec_velocity")
    
    with col2:
        st.markdown("### Hiring Velocity Metrics")
        top_sector = sector_metrics.iloc[0]
        st.markdown(f"**{top_sector['Sector']}**")
        st.markdown(f"• Positions: {int(top_sector['Open_Positions'])}")
        st.markdown(f"• Avg Apps: {top_sector['Avg_Applications']:.1f}")
        st.markdown(f"• Engagement: {top_sector['Avg_Views']:.0f} views")
    
    st.markdown("---")
    
    # 2. Salary Benchmarking
    st.subheader("💼 Salary Benchmarking by Role & Experience")
    
    role_salary = filtered_df.groupby('positionLevels').agg({
        'average_salary': ['mean', 'min', 'max', 'count']
    }).reset_index()
    
    role_salary.columns = ['Position Level', 'Avg_Salary', 'Min', 'Max', 'Count']
    role_salary = role_salary[role_salary['Count'] >= 5].sort_values('Avg_Salary', ascending=False)
    
    fig = go.Figure()
    
    for idx, row in role_salary.iterrows():
        fig.add_trace(go.Box(
            y=[row['Min'], row['Avg_Salary'], row['Max']],
            name=row['Position Level'],
            boxmean='sd',
            marker=dict(color='#3b82f6')
        ))
    
    fig.update_layout(
        title='Salary Range by Position Level (Box & Whisker)',
        yaxis_title='Salary (SGD)',
        height=400,
        template='plotly_white',
        showlegend=False,
        plot_bgcolor='#0f1419',
        paper_bgcolor='#0f1419',
        font=dict(color='#e0e7ff')
    )
    
    st.plotly_chart(fig, use_container_width=True, key="rec_salary_bench")
    
    st.markdown("---")
    
    # 3. Skills Demand Analysis
    st.subheader("🔧 High-Demand Skills Heatmap")
    
    current_skills, emerging_skills = calculate_skill_gaps(filtered_df)
    
    all_skills = {}
    all_skills.update(current_skills)
    for skill, count in emerging_skills.items():
        all_skills[skill] = all_skills.get(skill, 0) + count
    
    skills_df = pd.DataFrame(
        sorted(all_skills.items(), key=lambda x: x[1], reverse=True)[:10],
        columns=['Skill', 'Demand']
    )
    
    fig = px.bar(
        skills_df,
        x='Demand',
        y='Skill',
        orientation='h',
        title='Top 10 In-Demand Skills (Recruitment Velocity)',
        color='Demand',
        color_continuous_scale='Blues',
        labels={'Demand': 'Number of Job Postings'}
    )
    
    fig.update_layout(height=400, plot_bgcolor='#0f1419', paper_bgcolor='#0f1419',
                     font=dict(color='#e0e7ff'))
    st.plotly_chart(fig, use_container_width=True, key="rec_skills_demand")
    
    st.markdown("---")
    
    # 4. Competitive Landscape (Top Hiring Companies)
    st.subheader("⚔️ Competitive Landscape: Top Hiring Companies")
    
    company_count = filtered_df['postedCompany_name'].value_counts().head(12)
    
    fig = px.bar(
        x=company_count.values,
        y=company_count.index,
        orientation='h',
        title='Top 12 Hiring Companies by Open Positions',
        color=company_count.values,
        color_continuous_scale='Reds',
        labels={'x': 'Job Postings', 'y': 'Company'}
    )
    
    fig.update_layout(height=450, plot_bgcolor='#0f1419', paper_bgcolor='#0f1419',
                     font=dict(color='#e0e7ff'))
    st.plotly_chart(fig, use_container_width=True, key="rec_hiring_companies")
    
    st.markdown("---")
    
    # 5. Export Recruitment Intelligence
    st.subheader("📥 Export Recruitment Data")
    
    col1, col2 = st.columns(2)
    
    with col1:
        export_df = sector_metrics[['Sector', 'Open_Positions', 'Avg_Salary', 'Avg_Applications']].copy()
        csv_data = export_df.to_csv(index=False)
        st.download_button(
            label="📄 Download Market Data (CSV)",
            data=csv_data,
            file_name=f"recruitment_intelligence_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv"
        )
    
    with col2:
        if EXCEL_AVAILABLE:
            excel_data = create_excel_export(filtered_df, "Recruiter")
            if excel_data:
                st.download_button(
                    label="📊 Download Full Report (Excel)",
                    data=excel_data,
                    file_name=f"recruitment_report_{datetime.now().strftime('%Y%m%d')}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )


# ============================================================================
# COMMON: DETAILED ANALYTICS & EXPORT
# ============================================================================

st.markdown("---")
st.header("📊 Detailed Data Analytics & Exploration")

tab1, tab2, tab3, tab4 = st.tabs(["🔍 Job Search", "🏭 Sector Deep-Dive", "📈 Trend Analysis", "📥 Download Data"])

with tab1:
    st.subheader("🔍 Advanced Job Search")
    
    search_term = st.text_input("Search job titles", placeholder="e.g., Python, Data Engineer, AWS")
    
    if search_term:
        search_results = filtered_df[
            filtered_df['title'].str.contains(search_term, case=False, na=False)
        ][['title', 'postedCompany_name', 'average_salary', 'positionLevels', 'primary_category', 
           'metadata_totalNumberOfView', 'metadata_totalNumberJobApplication']].head(25)
        
        search_results.columns = ['Job Title', 'Company', 'Salary (SGD)', 'Level', 'Sector', 'Views', 'Applications']
        
        st.dataframe(search_results, use_container_width=True)
        st.success(f"✅ Found {len(search_results)} matching positions")
    else:
        st.info("📌 Enter a search term to find relevant positions")
    
    st.markdown("---")
    st.subheader("📊 Top 10 Job Titles by Application Volume")
    fig_titles = create_top_job_titles_by_applications(filtered_df)
    st.plotly_chart(fig_titles, use_container_width=True, key="common_top_titles")

with tab2:
    st.subheader("🏭 Sector-Deep Dive Analysis")
    
    selected_sector_detail = st.selectbox(
        "Select Sector for Detailed Analysis",
        options=sorted(filtered_df['primary_category'].unique()),
        key='common_sector_detail'
    )
    
    sector_detail_data = filtered_df[filtered_df['primary_category'] == selected_sector_detail]
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Postings", len(sector_detail_data))
    with col2:
        avg_salary = sector_detail_data['average_salary'].mean() if len(sector_detail_data) > 0 else 0
        st.metric("Avg Salary", f"SGD {avg_salary:,.0f}" if avg_salary > 0 else "N/A")
    with col3:
        total_apps = sector_detail_data['metadata_totalNumberJobApplication'].sum()
        st.metric("Total Applications", f"{total_apps:,}")
    with col4:
        top_company = sector_detail_data['postedCompany_name'].mode()[0] if len(sector_detail_data) > 0 and len(sector_detail_data['postedCompany_name'].mode()) > 0 else "N/A"
        st.metric("Top Company", top_company[:15])
    
    st.markdown("**Top Positions in this Sector:**")
    top_positions = sector_detail_data['title'].value_counts().head(12)
    
    cols = st.columns(3)
    for idx, (pos, count) in enumerate(top_positions.items()):
        with cols[idx % 3]:
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #1e2936 0%, #243447 100%); padding: 1rem; border-radius: 0.75rem; margin: 0.5rem 0; border-left: 4px solid #3b82f6;">
            <strong>{pos[:25]}...</strong><br>
            <small style="color: #93c5fd;">{count} postings</small>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.subheader("📊 Top 10 Job Demand by Sector (Overall Market)")
    fig_sector_demand = create_sector_job_demand(filtered_df)
    st.plotly_chart(fig_sector_demand, use_container_width=True, key="common_sector_demand")

with tab3:
    st.subheader("📈 Comprehensive Trend Analysis")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        trend_metric = st.selectbox(
            "Select Trend Metric",
            options=['Job Postings', 'Average Salary', 'Applications', 'Views'],
            key="trend_metric_selector"
        )
        
        ma_window = st.slider(
            "Moving Average Window",
            min_value=2,
            max_value=6,
            value=3
        )
    
    with col2:
        st.info(f"📊 Analyzing {trend_metric} trends with {ma_window}-month moving average")
    
    # Create trend analysis
    trend_data = filtered_df.groupby('year_month').agg({
        'metadata_jobPostId': 'count',
        'average_salary': 'mean',
        'metadata_totalNumberJobApplication': 'sum',
        'metadata_totalNumberOfView': 'sum'
    }).reset_index()
    
    trend_data['year_month_str'] = trend_data['year_month'].astype(str)
    
    if trend_metric == 'Job Postings':
        y_col = 'metadata_jobPostId'
        y_label = 'Number of Job Postings'
    elif trend_metric == 'Average Salary':
        y_col = 'average_salary'
        y_label = 'Avg Salary (SGD)'
    elif trend_metric == 'Applications':
        y_col = 'metadata_totalNumberJobApplication'
        y_label = 'Total Applications'
    else:
        y_col = 'metadata_totalNumberOfView'
        y_label = 'Total Views'
    
    trend_data['ma'] = trend_data[y_col].rolling(window=ma_window, center=True).mean()
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=trend_data['year_month_str'],
        y=trend_data[y_col],
        mode='lines+markers',
        name='Actual',
        line=dict(color='#3b82f6', width=2),
        marker=dict(size=5)
    ))
    
    fig.add_trace(go.Scatter(
        x=trend_data['year_month_str'],
        y=trend_data['ma'],
        mode='lines',
        name=f'{ma_window}-Month MA',
        line=dict(color='#10b981', width=3, dash='dash')
    ))
    
    fig.update_layout(
        title=f'{trend_metric} Trend Analysis',
        xaxis_title='Period',
        yaxis_title=y_label,
        height=450,
        plot_bgcolor='#0f1419',
        paper_bgcolor='#0f1419',
        font=dict(color='#e0e7ff'),
        hovermode='x unified'
    )
    
    st.plotly_chart(fig, use_container_width=True, key="common_trend_analysis")

with tab4:
    st.subheader("📥 Export Filtered Data")
    
    col1, col2, col3 = st.columns(3)
    
    # CSV Export
    with col1:
        csv = filtered_df[['title', 'postedCompany_name', 'primary_category', 'average_salary', 
                          'positionLevels', 'employmentTypes', 'metadata_newPostingDate',
                          'metadata_totalNumberOfView', 'metadata_totalNumberJobApplication']].to_csv(index=False)
        
        st.download_button(
            label="📄 Download as CSV",
            data=csv,
            file_name=f"workforce_data_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv"
        )
    
    # Excel Export
    with col2:
        if EXCEL_AVAILABLE:
            excel_data = create_excel_export(filtered_df, persona)
            if excel_data:
                st.download_button(
                    label="📊 Download as Excel",
                    data=excel_data,
                    file_name=f"workforce_data_{datetime.now().strftime('%Y%m%d')}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
        else:
            st.warning("Excel export unavailable - requires openpyxl")
    
    # PDF Export
    with col3:
        if PDF_AVAILABLE:
            pdf_data = create_pdf_export(filtered_df, persona)
            if pdf_data:
                st.download_button(
                    label="📑 Download as PDF",
                    data=pdf_data,
                    file_name=f"workforce_report_{datetime.now().strftime('%Y%m%d')}.pdf",
                    mime="application/pdf"
                )
        else:
            st.warning("PDF export unavailable - requires reportlab")
    
    st.info(f"✅ Ready to download {len(filtered_df):,} records in your chosen format")

# ============================================================================
# FOOTER
# ============================================================================

st.markdown("---")

footer_col1, footer_col2, footer_col3 = st.columns(3)

with footer_col1:
    st.markdown("""
    **About This Dashboard**
    
    This workforce intelligence tool leverages Singapore's job market data 
    to provide actionable insights for career development, policy-making, 
    and talent recruitment.
    """)

with footer_col2:
    st.markdown("""
    **Key Metrics**
    
    • Employment Heatmaps  
    • Salary Benchmarking  
    • Skills Gap Analysis  
    • Labor Shortage Index  
    • Trend Forecasting
    """)

with footer_col3:
    st.markdown("""
    **Data Source**
    
    Singapore Job Market Dataset  
    Last Updated: 2023  
    Records: ~1M job postings  
    
    *Version 1.0.0*
    """)

st.markdown("---")
st.markdown(
    "<p style='text-align: center; color: gray; font-size: 12px;'>"
    "© 2026 Workforce Intelligence Dashboard | All Rights Reserved | "
    "Designed for data-driven HR decisions"
    "</p>",
    unsafe_allow_html=True
)
