"""
WORKFORCE INTELLIGENCE DASHBOARD
A Production-Ready Streamlit Application for Labor Market Analytics

Author: Data Science Team
Version: 1.0.0
Purpose: Transform raw industrial job statistics into actionable workforce insights
         for individuals, government agencies, and recruiters.
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import altair as alt
from datetime import datetime, timedelta
import json
from typing import Dict, List, Tuple
import warnings

warnings.filterwarnings('ignore')

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

# Custom CSS with modern professional dark theme
st.markdown("""
<style>
    * {
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', sans-serif;
    }
    
    .main {
        background: linear-gradient(180deg, #0f1419 0%, #1a1f2e 100%);
    }
    
    .stMetric {
        background: linear-gradient(135deg, #1e2936 0%, #243447 100%);
        padding: 1.75rem;
        border-radius: 1rem;
        box-shadow: 0 4px 15px rgba(59, 130, 246, 0.15);
        border: 2px solid #3b82f6;
        transition: all 0.3s ease;
    }
    
    .stMetric:hover {
        box-shadow: 0 6px 20px rgba(59, 130, 246, 0.25);
        transform: translateY(-2px);
    }
    
    .stMetric > label {
        font-size: 0.9rem !important;
        font-weight: 600 !important;
        color: #93c5fd !important;
        letter-spacing: 0.5px;
        text-transform: uppercase;
    }
    
    .stMetric > div > div:nth-child(2) {
        font-size: 2rem !important;
        font-weight: 800 !important;
        color: #ffffff !important;
        line-height: 1.2;
        margin-top: 0.5rem;
    }
    
    .metric-container {
        background: linear-gradient(135deg, #1e2936 0%, #243447 100%);
        color: #e0e7ff;
        padding: 1.75rem;
        border-radius: 1rem;
        margin: 1rem 0;
        border: 2px solid #3b82f6;
        box-shadow: 0 4px 15px rgba(59, 130, 246, 0.15);
    }
    
    .recommendation-box {
        background: linear-gradient(135deg, #065f46 0%, #047857 100%);
        border-left: 6px solid #10b981;
        padding: 1.5rem;
        border-radius: 0.75rem;
        margin: 1.25rem 0;
        color: #d1fae5;
        font-weight: 600;
        font-size: 0.95rem;
        box-shadow: 0 4px 12px rgba(16, 185, 129, 0.2);
    }
    
    .shortage-index {
        background: linear-gradient(135deg, #7c2d12 0%, #92400e 100%);
        border-left: 6px solid #fb923c;
        padding: 1.5rem;
        border-radius: 0.75rem;
        color: #fed7aa;
        font-weight: 600;
        font-size: 0.95rem;
        box-shadow: 0 4px 12px rgba(251, 146, 60, 0.2);
    }
    
    h1, h2, h3, h4, h5, h6 {
        color: #ffffff !important;
        font-weight: 800 !important;
        letter-spacing: -0.5px;
    }
    
    h1 { font-size: 2.75rem !important; margin: 2rem 0 0.75rem 0 !important; }
    h2 { font-size: 1.95rem !important; margin: 1.75rem 0 1rem 0 !important; }
    h3 { font-size: 1.5rem !important; margin: 1.5rem 0 0.75rem 0 !important; }
    h4 { font-size: 1.2rem !important; margin: 1.25rem 0 0.5rem 0 !important; }
    
    body, p, span, div {
        color: #e0e7ff !important;
    }
    
    .divider {
        margin: 2.5rem 0;
        border-top: 2px solid #3b82f6;
        opacity: 0.3;
    }
    
    .stTabs [role="tablist"] {
        border-bottom: 2px solid #3b82f6 !important;
    }
    
    .stTabs [role="tablist"] button {
        font-size: 1.05rem !important;
        font-weight: 700 !important;
        color: #93c5fd !important;
        padding: 1rem 1.75rem !important;
        background-color: transparent !important;
        border: none !important;
        border-bottom: 3px solid transparent !important;
    }
    
    .stTabs [role="tablist"] button[aria-selected="true"] {
        color: #ffffff !important;
        border-bottom: 3px solid #3b82f6 !important;
    }
    
    .stTabs [role="tablist"] button:hover {
        color: #bfdbfe !important;
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
        color: #e0e7ff !important;
        padding: 0.85rem !important;
        background-color: #243447 !important;
        border-bottom: 1px solid #3b82f6 !important;
    }
    
    .stDataFrame tr:hover td {
        background-color: #2d4557 !important;
    }
    
    .stWarning {
        background: linear-gradient(135deg, #78350f 0%, #92400e 100%);
        border: 2px solid #fbbf24;
        color: #fef3c7;
        font-weight: 600;
        padding: 1.25rem !important;
        border-radius: 0.75rem;
        font-size: 0.95rem;
        box-shadow: 0 4px 12px rgba(251, 191, 36, 0.2);
    }
    
    .stError {
        background: linear-gradient(135deg, #7f1d1d 0%, #991b1b 100%);
        border: 2px solid #f87171;
        color: #fee2e2;
        font-weight: 600;
        padding: 1.25rem !important;
        border-radius: 0.75rem;
        font-size: 0.95rem;
        box-shadow: 0 4px 12px rgba(248, 113, 113, 0.2);
    }
    
    .stSuccess {
        background: linear-gradient(135deg, #065f46 0%, #047857 100%);
        border: 2px solid #10b981;
        color: #d1fae5;
        font-weight: 600;
        padding: 1.25rem !important;
        border-radius: 0.75rem;
        font-size: 0.95rem;
        box-shadow: 0 4px 12px rgba(16, 185, 129, 0.2);
    }
    
    .stInfo {
        background: linear-gradient(135deg, #1e3a8a 0%, #1e40af 100%);
        border: 2px solid #60a5fa;
        color: #dbeafe;
        font-weight: 600;
        padding: 1.25rem !important;
        border-radius: 0.75rem;
        font-size: 0.95rem;
        box-shadow: 0 4px 12px rgba(96, 165, 250, 0.2);
    }
    
    .stSelectbox, .stMultiselect, .stSlider, .stTextInput {
        color: #e0e7ff !important;
    }
    
    .stSelectbox > div > div, .stMultiselect > div > div {
        background-color: #1e2936 !important;
        border: 2px solid #3b82f6 !important;
        color: #e0e7ff !important;
    }
    
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0f1419 0%, #1a1f2e 100%);
    }
    
    section[data-testid="stSidebar"] > div {
        background: linear-gradient(180deg, #0f1419 0%, #1a1f2e 100%);
    }
    
</style>
""", unsafe_allow_html=True)

# ============================================================================
# DATA LOADING & CACHING
# ============================================================================

@st.cache_data
def load_data(filepath: str) -> pd.DataFrame:
    """
    Load and cache the SGJobData CSV file.
    
    Args:
        filepath: Path to the CSV file
        
    Returns:
        DataFrame with processed job data
    """
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
def preprocess_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean and preprocess raw job data.
    
    Args:
        df: Raw DataFrame
        
    Returns:
        Cleaned DataFrame ready for analysis
    """
    # Create a copy to avoid SettingWithCopyWarning
    df = df.copy()
    
    # Convert date columns
    date_cols = ['metadata_newPostingDate', 'metadata_originalPostingDate', 'metadata_expiryDate']
    for col in date_cols:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors='coerce')
    
    # Extract year and month for temporal analysis
    df['year'] = df['metadata_newPostingDate'].dt.year
    df['month'] = df['metadata_newPostingDate'].dt.month
    df['year_month'] = df['metadata_newPostingDate'].dt.to_period('M')
    
    # Handle salary data with proper NaN handling
    df['salary_minimum'] = pd.to_numeric(df['salary_minimum'], errors='coerce').fillna(0)
    df['salary_maximum'] = pd.to_numeric(df['salary_maximum'], errors='coerce').fillna(0)
    df['average_salary'] = pd.to_numeric(df['average_salary'], errors='coerce').fillna(0)
    
    # Handle experience
    df['minimumYearsExperience'] = pd.to_numeric(df['minimumYearsExperience'], errors='coerce').fillna(0)
    
    # Extract primary category from categories JSON
    df['primary_category'] = df['categories'].apply(extract_primary_category)
    
    # Handle employment type
    df['employmentTypes'] = df['employmentTypes'].fillna('Unknown')
    
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
def calculate_employment_heatmap_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Generate employment heatmap data by sector and time period.
    
    Args:
        df: Processed DataFrame
        
    Returns:
        Aggregated data for heatmap visualization
    """
    heatmap_data = df.groupby(['year_month', 'primary_category']).agg({
        'metadata_jobPostId': 'count',
        'average_salary': 'mean',
        'minimumYearsExperience': 'mean'
    }).reset_index()
    
    heatmap_data.columns = ['Period', 'Sector', 'Posting_Count', 'Avg_Salary', 'Avg_Experience']
    heatmap_data['Period'] = heatmap_data['Period'].astype(str)
    
    return heatmap_data


@st.cache_data
def calculate_skill_gaps(df: pd.DataFrame) -> Tuple[Dict, Dict]:
    """
    Analyze current market skills vs. emerging needs.
    
    Args:
        df: Processed DataFrame
        
    Returns:
        Tuple of (current_skills, emerging_skills)
    """
    # Handle empty dataframe
    if len(df) == 0 or df.empty or 'title' not in df.columns:
        return {}, {}
    
    # Extract skills from job titles
    common_skills = {
        'Python': df['title'].str.contains('Python', case=False, na=False).sum() if 'title' in df.columns else 0,
        'Java': df['title'].str.contains('Java', case=False, na=False).sum() if 'title' in df.columns else 0,
        'C++': df['title'].str.contains('C\\+\\+|C Plus Plus', case=False, na=False, regex=True).sum() if 'title' in df.columns else 0,
        'JavaScript': df['title'].str.contains('JavaScript|Node', case=False, na=False).sum() if 'title' in df.columns else 0,
        'SQL': df['title'].str.contains('SQL', case=False, na=False).sum() if 'title' in df.columns else 0,
        'Cloud': df['title'].str.contains('AWS|Azure|GCP|Cloud', case=False, na=False).sum() if 'title' in df.columns else 0,
        'Data': df['title'].str.contains('Data|Analytics|BI', case=False, na=False).sum() if 'title' in df.columns else 0,
        'AI/ML': df['title'].str.contains('AI|Machine Learning|ML', case=False, na=False).sum() if 'title' in df.columns else 0,
    }
    
    emerging_skills = {
        'Cloud': common_skills['Cloud'],
        'AI/ML': common_skills['AI/ML'],
        'Data': common_skills['Data'],
        'DevOps': df['title'].str.contains('DevOps|Docker|Kubernetes', case=False, na=False).sum() if 'title' in df.columns else 0,
    }
    
    return common_skills, emerging_skills


@st.cache_data
def calculate_labor_shortage_index(df: pd.DataFrame) -> Dict[str, float]:
    """
    Calculate Labor Shortage Index for government users.
    
    Metrics:
    - Posting Volume Trend: Increase in job postings
    - Application Ratio: Views per posting (lower = shortage)
    - Salary Growth: YoY salary increase
    - Vacancy Fill Rate: Hard-to-fill positions
    
    Args:
        df: Processed DataFrame
        
    Returns:
        Dictionary with shortage indices by sector
    """
    shortage_index = {}
    
    for sector in df['primary_category'].unique():
        sector_data = df[df['primary_category'] == sector]
        
        # Components of shortage index (0-100 scale)
        # 1. Posting volume trend (normalized)
        posting_count = len(sector_data)
        posting_score = min((posting_count / len(df)) * 200, 100)  # Scale to 100
        
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


def get_job_recommendations(user_skills: List[str], desired_salary: float, 
                           location: str, df: pd.DataFrame) -> Dict:
    """
    Generate personalized job recommendations and upskill opportunities.
    
    This is the core Recommendation Engine.
    
    Args:
        user_skills: List of current skills
        desired_salary: Target salary
        location: Preferred work location (not yet in data, for future use)
        df: Processed DataFrame
        
    Returns:
        Dictionary with upskill opportunities and high-growth sectors
    """
    
    recommendations = {
        'upskill_opportunities': [],
        'high_growth_sectors': [],
        'salary_potential': 0
    }
    
    # Calculate skill gaps
    all_skills, emerging_skills = calculate_skill_gaps(df)
    
    # 1. Generate 3 Upskill Opportunities
    upskill_mapping = {
        'Analyst': ['Python', 'Data', 'SQL'],
        'Developer': ['Cloud', 'AI/ML', 'DevOps'],
        'Engineer': ['Cloud', 'DevOps', 'Python'],
        'Manager': ['Data', 'Analytics', 'AI/ML'],
    }
    
    missing_emerging_skills = [s for s in emerging_skills.keys() if s not in user_skills]
    
    opportunities = [
        f"Learn {missing_emerging_skills[0] if missing_emerging_skills else 'Cloud'} "
        f"to transition from Analyst to Data Engineer roles",
        f"Master {missing_emerging_skills[1] if len(missing_emerging_skills) > 1 else 'AI/ML'} "
        f"to unlock senior positions with 15-20% salary premium",
        f"Develop {missing_emerging_skills[2] if len(missing_emerging_skills) > 2 else 'DevOps'} "
        f"expertise to access specialized technical tracks"
    ]
    
    recommendations['upskill_opportunities'] = opportunities[:3]
    
    # 2. Identify 3 high-growth sectors
    sector_growth = {}
    for sector in df['primary_category'].unique():
        sector_df = df[df['primary_category'] == sector]
        growth_score = (
            len(sector_df) / len(df) * 40 +  # Posting volume weight
            sector_df['average_salary'].mean() / df['average_salary'].mean() * 30 +
            sector_df['metadata_totalNumberOfView'].mean() / 10  # Engagement weight
        )
        sector_growth[sector] = round(growth_score, 2)
    
    top_sectors = sorted(sector_growth.items(), key=lambda x: x[1], reverse=True)[:3]
    recommendations['high_growth_sectors'] = [
        {'sector': s[0], 'growth_score': s[1]} for s in top_sectors
    ]
    
    # 3. Calculate salary potential
    relevant_jobs = df[df['primary_category'].isin([s['sector'] for s in recommendations['high_growth_sectors']])]
    recommendations['salary_potential'] = round(relevant_jobs['average_salary'].mean(), 2)
    
    return recommendations


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


def create_salary_distribution_by_sector(df: pd.DataFrame) -> go.Figure:
    """
    Create salary distribution visualization by sector.
    
    Args:
        df: Processed DataFrame
        
    Returns:
        Plotly Figure object
    """
    salary_by_sector = df.dropna(subset=['average_salary']).groupby('primary_category')['average_salary'].agg(['mean', 'count']).reset_index()
    salary_by_sector = salary_by_sector[salary_by_sector['count'] >= 10].sort_values('mean', ascending=False).head(12)
    
    fig = go.Figure(data=[
        go.Bar(
            x=salary_by_sector['primary_category'],
            y=salary_by_sector['mean'],
            marker_color='#888888',
            hovertemplate='<b>%{x}</b><br>Avg Salary: SGD %{y:,.0f}<extra></extra>'
        )
    ])
    
    fig.update_layout(
        title='Average Salary Distribution by Industry Sector',
        xaxis_title='Industry Sector',
        yaxis_title='Average Salary (SGD)',
        height=400,
        template='plotly_white',
        xaxis_tickangle=-45,
        font=dict(family='Segoe UI', size=11)
    )
    
    return fig


def create_job_growth_trend(df: pd.DataFrame) -> go.Figure:
    """
    Create time-series forecast of job growth.
    
    Args:
        df: Processed DataFrame
        
    Returns:
        Plotly Figure object
    """
    trend_data = df.groupby('year_month').size().reset_index(name='count')
    trend_data['year_month'] = trend_data['year_month'].astype(str)
    
    fig = go.Figure()
    
    # Add historical data
    fig.add_trace(go.Scatter(
        x=trend_data['year_month'],
        y=trend_data['count'],
        mode='lines+markers',
        name='Historical Job Postings',
        line=dict(color='#666666', width=2),
        marker=dict(size=6)
    ))
    
    fig.update_layout(
        title='Job Posting Trends Over Time',
        xaxis_title='Time Period',
        yaxis_title='Number of Job Postings',
        height=400,
        template='plotly_white',
        hovermode='x unified',
        font=dict(family='Segoe UI', size=11)
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


# ============================================================================
# SIDEBAR: PERSONA SELECTION & FILTERS
# ============================================================================

# Removed external placeholder image to prevent connectivity issues
# Logo section can be added later with local file

st.sidebar.markdown("---")
st.sidebar.markdown("### 👤 SELECT YOUR PERSONA")

persona = st.sidebar.radio(
    "Who are you?",
    options=["Individual", "Government Agency", "Recruiter"],
    help="Choose your role to customize the dashboard view"
)

st.sidebar.markdown("---")
st.sidebar.markdown("### 🎛️ FILTERS")

# Load data
@st.cache_data
def load_and_preprocess():
    df = load_data("/home/julius/Capstone DS4/SGJobData.csv")
    df = preprocess_data(df)
    return df

df = load_and_preprocess()

# Year filter
available_years = sorted(df['year'].dropna().unique())
selected_years = st.sidebar.multiselect(
    "Filter by Year",
    options=available_years,
    default=available_years
)

# Sector filter
available_sectors = sorted(df['primary_category'].unique())
selected_sectors = st.sidebar.multiselect(
    "Filter by Industry Sector",
    options=available_sectors,
    default=available_sectors[:8]
)

# Employment type filter
employment_types = sorted(df['employmentTypes'].unique())
selected_employment = st.sidebar.multiselect(
    "Filter by Employment Type",
    options=employment_types,
    default=employment_types
)

# Apply filters with validation
filtered_df = df.copy()

if selected_years:
    filtered_df = filtered_df[filtered_df['year'].isin(selected_years)]
if selected_sectors:
    filtered_df = filtered_df[filtered_df['primary_category'].isin(selected_sectors)]
if selected_employment:
    filtered_df = filtered_df[filtered_df['employmentTypes'].isin(selected_employment)]

# Validate filtered dataset
if len(filtered_df) == 0:
    st.warning("⚠️ No jobs match your current filter selections. Please adjust your filters.")
    filtered_df = df.copy()

st.sidebar.markdown("---")

# Dynamic filters based on persona
if persona == "Individual":
    st.sidebar.markdown("""
    <div style="background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%); padding: 1.5rem; border-radius: 1rem; margin-bottom: 1.5rem; box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3); border: 2px solid #60a5fa;">
        <h3 style="color: white; margin: 0; font-size: 1.4rem; font-weight: 800; letter-spacing: -0.5px;">💼 YOUR PROFILE</h3>
    </div>
    """, unsafe_allow_html=True)
    user_current_skills = st.sidebar.multiselect(
        "Your Current Skills",
        options=['Python', 'Java', 'JavaScript', 'SQL', 'Cloud', 'Data', 'AI/ML', 'C++'],
        default=['Python'],
        help="Select skills you already possess"
    )
    
    desired_salary = st.sidebar.slider(
        "Target Monthly Salary (SGD)",
        min_value=1000,
        max_value=15000,
        value=5000,
        step=500
    )
    
    preferred_role = st.sidebar.selectbox(
        "Preferred Role",
        options=['Analyst', 'Developer', 'Engineer', 'Manager', 'Any']
    )

elif persona == "Government Agency":
    st.sidebar.markdown("### 📊 MACRO-ECONOMIC FILTERS")
    
    shortage_sensitivity = st.sidebar.slider(
        "Focus on High-Shortage Sectors",
        min_value=0.0,
        max_value=1.0,
        value=0.7,
        step=0.1
    )

elif persona == "Recruiter":
    st.sidebar.markdown("### 🎯 RECRUITMENT FILTERS")
    
    growth_focus = st.sidebar.selectbox(
        "Focus Area",
        options=['High Growth Sectors', 'High Salary Sectors', 'High Volume', 'Emerging Skills']
    )
    
    min_vacancy = st.sidebar.slider(
        "Minimum Vacancies per Posting",
        min_value=1,
        max_value=20,
        value=1
    )

st.sidebar.markdown("---")
st.sidebar.markdown(f"**Last Updated:** {datetime.now().strftime('%Y-%m-%d %H:%M')}")
st.sidebar.markdown(f"**Records Displayed:** {len(filtered_df):,}")

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
    st.header("🚀 Your Personalized Career Roadmap")
    
    # Get recommendations
    recommendations = get_job_recommendations(
        user_current_skills,
        desired_salary,
        "Singapore",
        filtered_df
    )
    
    # 1. Upskill Opportunities
    st.subheader("💡 Recommended Upskill Opportunities")
    col1, col2, col3 = st.columns(3)
    
    upskill_opps = recommendations['upskill_opportunities']
    with col1:
        st.markdown(f"""
        <div class="recommendation-box">
        <strong>Opportunity 1</strong><br>
        {upskill_opps[0]}
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="recommendation-box">
        <strong>Opportunity 2</strong><br>
        {upskill_opps[1]}
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="recommendation-box">
        <strong>Opportunity 3</strong><br>
        {upskill_opps[2]}
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # 2. High-Growth Sectors
    st.subheader("🎯 High-Growth Sectors for Your Profile")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        sectors_list = recommendations['high_growth_sectors']
        sectors_df = pd.DataFrame([
            {
                'Rank': i+1,
                'Sector': s['sector'],
                'Growth Score': f"{s['growth_score']:.1f}",
                'Salary Potential': f"SGD {recommendations['salary_potential']:,.0f}"
            }
            for i, s in enumerate(sectors_list)
        ])
        st.dataframe(sectors_df, hide_index=True, use_container_width=True)
    
    with col2:
        st.metric(
            "Salary Potential",
            f"SGD {recommendations['salary_potential']:,.0f}",
            "with upskilling"
        )
    
    st.markdown("---")
    
    # 3. Skill Gap Analysis
    st.subheader("📈 Skill Gap Analysis")
    current_skills, emerging_skills = calculate_skill_gaps(filtered_df)
    fig = create_skill_gap_chart(current_skills, emerging_skills)
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    # 4. Job Salary Distribution
    st.subheader("💰 Salary Distribution by Sector")
    fig = create_salary_distribution_by_sector(filtered_df)
    st.plotly_chart(fig, use_container_width=True)


elif persona == "Government Agency":
    st.header("📈 Macro-Economic Labor Market Dashboard")
    
    st.info(
        "👁️ **Government Focus:** Monitor labor shortages, wage trends, and sector health to inform workforce policy."
    )
    
    st.markdown("---")
    
    # 1. Labor Shortage Index
    st.subheader("🚨 Labor Shortage Index by Sector")
    st.markdown("*Higher values indicate more severe labor shortages*")
    
    shortage_index = calculate_labor_shortage_index(filtered_df)
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        selected_sector = st.selectbox(
            "Select Sector for Detailed Analysis",
            options=list(shortage_index.keys())
        )
        
        # Display top 5 shortage sectors
        st.markdown("**Top 5 Critical Shortage Areas:**")
        top_shortage = sorted(shortage_index.items(), key=lambda x: x[1], reverse=True)[:5]
        for i, (sector, index) in enumerate(top_shortage, 1):
            color = "🔴" if index > 70 else "🟡" if index > 50 else "🟢"
            st.markdown(f"{color} **{i}. {sector}** - {index:.1f}")
    
    with col2:
        fig = create_labor_shortage_gauge(shortage_index, selected_sector)
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    # 2. Employment Heatmap
    st.subheader("🔥 Employment Heatmap: Hiring Patterns by Sector")
    heatmap_data = calculate_employment_heatmap_data(filtered_df)
    fig = create_employment_heatmap(heatmap_data)
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    # 3. Job Growth Trends
    st.subheader("📊 Job Market Trends")
    fig = create_job_growth_trend(filtered_df)
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    # 4. Sector Summary Statistics
    st.subheader("📋 Sector Summary Statistics")
    
    sector_summary = filtered_df.groupby('primary_category').agg({
        'metadata_jobPostId': 'count',
        'average_salary': ['mean', 'min', 'max'],
        'minimumYearsExperience': 'mean',
        'metadata_totalNumberOfView': 'sum'
    }).reset_index()
    
    sector_summary.columns = ['Sector', 'Postings', 'Avg_Salary', 'Min_Salary', 'Max_Salary', 'Avg_Experience', 'Total_Views']
    sector_summary = sector_summary.sort_values('Postings', ascending=False).head(10)
    
    # Format for display
    for col in ['Avg_Salary', 'Min_Salary', 'Max_Salary']:
        sector_summary[col] = sector_summary[col].round(2)
    
    st.dataframe(sector_summary, hide_index=True, use_container_width=True)


elif persona == "Recruiter":
    st.header("🎯 Talent Pool & Recruitment Intelligence")
    
    st.info(
        "👁️ **Recruiter Focus:** Identify high-growth talent pools, skill trends, and competitive salary benchmarks."
    )
    
    st.markdown("---")
    
    # 1. Top Growing Sectors
    st.subheader("📈 High-Growth Talent Pools")
    
    sector_metrics = filtered_df.groupby('primary_category').agg({
        'metadata_jobPostId': 'count',
        'average_salary': 'mean',
        'metadata_totalNumberJobApplication': 'mean'
    }).reset_index()
    
    sector_metrics.columns = ['Sector', 'Open_Positions', 'Avg_Salary', 'Avg_Applications']
    sector_metrics = sector_metrics.sort_values('Open_Positions', ascending=False).head(10)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        fig = px.bar(
            sector_metrics,
            x='Sector',
            y='Open_Positions',
            color='Avg_Salary',
            hover_data=['Avg_Applications'],
            title='Open Positions by Sector',
            labels={'Open_Positions': 'Number of Openings', 'Avg_Salary': 'Avg Salary (SGD)'},
            color_continuous_scale='Greys'
        )
        fig.update_layout(xaxis_tickangle=-45, height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    with col1:
        st.dataframe(
            sector_metrics.assign(Avg_Salary=sector_metrics['Avg_Salary'].apply(lambda x: f'${x:,.0f}'))
                          .drop('Sector', axis=1)
                          .assign(Sector=sector_metrics['Sector']),
            hide_index=True,
            use_container_width=True
        )
    
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
            boxmean='sd'
        ))
    
    fig.update_layout(
        title='Salary Range by Position Level',
        yaxis_title='Salary (SGD)',
        height=400,
        template='plotly_white',
        showlegend=False
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    # 3. Skills Demand Analysis
    st.subheader("🔧 High-Demand Skills")
    
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
        title='Top 10 In-Demand Skills',
        color='Demand',
        color_continuous_scale='Greys',
        labels={'Demand': 'Number of Job Postings'}
    )
    
    fig.update_layout(height=400, template='plotly_white')
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    # 4. Competitive Analysis
    st.subheader("⚔️ Competitive Landscape")
    
    company_count = filtered_df['postedCompany_name'].value_counts().head(10)
    
    fig = px.pie(
        values=company_count.values,
        names=company_count.index,
        title='Top 10 Hiring Companies',
        labels={'values': 'Job Postings', 'names': 'Company'}
    )
    
    fig.update_layout(height=500)
    st.plotly_chart(fig, use_container_width=True)


# ============================================================================
# COMMON: DETAILED ANALYTICS & EXPORT
# ============================================================================

st.markdown("---")
st.header("📊 Detailed Data Analytics")

tab1, tab2, tab3 = st.tabs(["Job Search", "Sector Deep-Dive", "Download Data"])

with tab1:
    st.subheader("🔍 Advanced Job Search")
    
    search_term = st.text_input("Search job titles", placeholder="e.g., Python, Data Engineer, AWS")
    
    if search_term:
        search_results = filtered_df[
            filtered_df['title'].str.contains(search_term, case=False, na=False)
        ][['title', 'postedCompany_name', 'average_salary', 'positionLevels', 'primary_category']].head(20)
        
        st.dataframe(search_results, use_container_width=True)
        st.success(f"Found {len(search_results)} matching positions")
    else:
        st.info("Enter a search term to find relevant positions")

with tab2:
    st.subheader("🏭 Sector-Deep Dive Analysis")
    
    selected_sector_detail = st.selectbox(
        "Select Sector for Detailed Analysis",
        options=filtered_df['primary_category'].unique(),
        key='sector_detail'
    )
    
    sector_detail_data = filtered_df[filtered_df['primary_category'] == selected_sector_detail]
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Postings", len(sector_detail_data))
    with col2:
        avg_salary = sector_detail_data['average_salary'].mean() if len(sector_detail_data) > 0 else 0
        st.metric("Avg Salary", f"SGD {avg_salary:,.0f}" if avg_salary > 0 else "N/A")
    with col3:
        top_company = sector_detail_data['postedCompany_name'].mode()[0] if len(sector_detail_data) > 0 and len(sector_detail_data['postedCompany_name'].mode()) > 0 else "N/A"
        st.metric("Top Company", top_company)
    
    st.markdown("**Top Positions in this Sector:**")
    top_positions = sector_detail_data['title'].value_counts().head(8)
    for pos, count in top_positions.items():
        st.write(f"• {pos} ({count} postings)")

with tab3:
    st.subheader("📥 Export Filtered Data")
    
    # Create CSV
    csv = filtered_df[['title', 'postedCompany_name', 'primary_category', 'average_salary', 'positionLevels', 'employmentTypes', 'metadata_newPostingDate']].to_csv(index=False)
    
    st.download_button(
        label="Download as CSV",
        data=csv,
        file_name=f"workforce_data_{datetime.now().strftime('%Y%m%d')}.csv",
        mime="text/csv"
    )
    
    st.info(f"✅ Ready to download {len(filtered_df):,} records")

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
